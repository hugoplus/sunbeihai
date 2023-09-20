import logging
import re
import redis
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from django.views.decorators.http import require_POST, require_GET
from django.core.exceptions import SuspiciousOperation
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .models import Course, Category, Article, Comment, Subscriber
from .forms import CommentForm
from django.http import Http404

"""
"""

logging.basicConfig(
    filename='course.log', 
    level=logging.DEBUG, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

"""
"""

User = get_user_model() # Load the custom user model

"""
"""

DEFAULT_MAX_COMMENTS_TO_SHOW = 10

"""
"""

r = redis.Redis(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT, 
    db=settings.REDIS_DB)

"""
"""

def article_list(request):
    """To list the published articles, which is the default homepage of course."""
    
    # Retrieve all the published articles.
    try:
        published_article = Article.published_objects.all()
        highlighted_courses = Course.highlighted_objects.all()
    except Exception as e:
        logger.exception("An error occurred: %s", e)
        published_article = []
        highlighted_courses = []

    # Set paginator.
    paginator = Paginator(published_article, 5)
    page_number = request.GET.get('page', 1)
    
    try:
        articles = paginator.page(page_number)
    except PageNotAnInteger:
        logger.exception("An PageNotAnInteger error occurred.")
        articles = paginator.page(1)
        page_number = 1
    except EmptyPage:
        logger.exception("An EmptyPage error occurred.")
        articles = paginator.page(paginator.num_pages)
        page_number = paginator.num_pages
        
    page_list = paginator.get_elided_page_range(page_number, on_each_side=2, on_ends=2)
    page_list = [page for page in page_list]
    page_list = [[i, v] for i, v in enumerate(page_list)]

    return render(
        request,
        'course/article_list.html',
        {
            'articles': articles,
            'courses': highlighted_courses,
            'pages': page_list
        }
    )

"""
"""

def get_comment_form(request):
    """To get the comment form."""
    
    # Create the form for users to submit comments
    current_user = request.user
    
    if current_user.is_authenticated:
        form = CommentForm(
            initial={
                'name': current_user.username,
                'email': current_user.email,})
    else:
        form = CommentForm()
    
    return form

"""
"""

def article_detail(request, year, month, day, slug):
    """This is to show the details of the article."""
    
    article = get_object_or_404(
            Article,
            status=Article.Status.PUBLISHED, 
            slug=slug,
            published_at__year=year,
            published_at__month=month,
            published_at__day=day)
    
    article_title = {'title': article.title}
    
    # Get the course that this article belongs to.
    course = article.get_parent_course()
    
    # Retrieve the content tree of this course.
    content_tree = course.get_content_tree() if course else []
    
    # Find the previous page and the next page.
    def article_traversal(article_tree, id=-1, previous_url='', next_url='', located=False, stoppable=False):
        previous_article_url = previous_url
        next_article_url = next_url
        has_found = located
        should_stop = stoppable

        for node in article_tree:
            if should_stop:
                break

            if node['type'] == 'leaf':
                if node['id'] == id:
                    has_found = True
                else:
                    if not has_found:
                        previous_article_url = node['href']
                    else:
                        next_article_url = node['href']
                        should_stop = True
            else:
                if 'nodes' in node:
                    previous_article_url, next_article_url, has_found, should_stop = article_traversal(
                        node['nodes'],
                        id,
                        previous_url=previous_article_url,
                        next_url=next_article_url,
                        located=has_found,
                        stoppable=should_stop)

        return previous_article_url, next_article_url, has_found, should_stop

    previous_article_url, next_article_url, *junk = article_traversal(content_tree, id=article.id)
    
    # Find the active comments for this article.
    comment_list = article.get_active_comments()
    
    # Check if the comment list needs to be truncated.
    comment_more = False
    
    if article.comments.count() > DEFAULT_MAX_COMMENTS_TO_SHOW:
        count = 0
        amount = len(comment_list[0])
        while amount <= DEFAULT_MAX_COMMENTS_TO_SHOW:
            count += 1
            amount += len(comment_list[count])
            
        comment_list = comment_list[:count+1]
        comment_more = True
    
    # Create the form for users to submit comments
    form = get_comment_form(request)
    
    # Increment total views by 1
    total_views = r.incr(f"article:{article.id}:views")
    
    return render(
        request, 
        'course/article_detail.html',
        {
            'course_id': course.id,
            'article': article, 
            'article_title': article_title,
            'content_tree': content_tree,
            'previous_article_url': previous_article_url,
            'next_article_url': next_article_url,
            'comments': comment_list,
            'comment_more': comment_more,
            'form': form,
            'total_views': total_views
        }
    )

"""
"""

def article_comment(request, article_id):
    """To add a comment to one article."""
    
    # If the request is a GET request, then it is not a valid request.
    if request.method == 'GET':
        raise Http404

    # Find the article.
    article = get_object_or_404(Article, id=article_id, status=Article.Status.PUBLISHED)
    
    comment = None
    
    # A comment was submitted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        try:
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
        except Exception as e:
            logger.exception("An error occurred: %s", e)
            raise SuspiciousOperation("Some suspicious operation on database occurred.")
        
    return redirect(article.get_absolute_url())

"""
"""

def article_comment_append(request, article_id, parent_comment_id):
    """To add a new comment and attach it to its parent comment."""
    
    # If the request is a GET request, then it is not a valid request.
    if request.method == 'GET':
        raise Http404

    # Find the article and the comment chain.
    article = get_object_or_404(Article, id=article_id, status=Article.Status.PUBLISHED)
    parent_comment = get_object_or_404(Comment, id=parent_comment_id)
    
    comment = None
    
    # A comment was submitted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        try:
            comment = form.save(commit=False)
            comment.article = article
            comment.parent = parent_comment
            comment.save()
        except Exception as e:
            logger.exception("An error occurred: %s", e)
            raise SuspiciousOperation("Some suspicious operation on database occurred.")
        
    return redirect(article.get_absolute_url())

"""
"""

def article_comment_detail(request, article_id, comment_id):
    """To manage the comment list attached to one article."""
    
    # Find the article.
    article = get_object_or_404(Article, id=article_id, status=Article.Status.PUBLISHED)
    # Find the comments for this specific article.
    comment = get_object_or_404(Comment, id=comment_id, is_active=True)
    
    # Find the comment chain for this specific comment.
    comments = [comment]
    
    while comment.parent:
        comment = comment.parent
        comments.append(comment)
    
    comments = list(comments)[::-1]
    
    # Create the form for users to submit comments
    form = get_comment_form(request)
    
    return render(
        request,
        'course/comment_detail.html',
        {
            'article': article,
            'comments': comments,
            'first_comment': comments[0],
            'last_comment': comments[-1],
            'form': form
        }
    )

"""
"""

def article_comment_list(request, article_id):
    """To retrieve the comment list attached to one article."""
    
    article = get_object_or_404(Article, id=article_id, status=Article.Status.PUBLISHED)
    
    # Find the active comments for this article.
    comment_list = article.get_active_comments()
    
    # Create the form for users to submit comments
    form = get_comment_form(request)
    
    return render(
        request,
        'course/article_comment_list.html',
        {
            'article': article,
            'comments': comment_list,
            'form': form
        }
    )

"""
"""

@require_GET
def article_search(request):
    """To handle the query here."""

    # If there is no query, redirect to the course page.
    if 'query' not in request.GET:
        return redirect('/course/')
    
    # If there is a query, search the articles.
    try:
        query = request.GET.get('query')
        search_vector = SearchVector('title', 'body')
        search_query = SearchQuery(query)
        results = Article.published_objects.annotate(
            search=search_vector,
            rank=SearchRank(search_vector, search_query)
            ).filter(
                Q(title__icontains=query) | Q(body__icontains=query) | Q(search=search_query)
            ).order_by('-rank')
    except Exception as e:
        logger.exception("An error occurred: %s", e)
        raise SuspiciousOperation("Some suspicious operation on database occurred.")

    return render(
        request,
        'course/search.html',
        {
            'query': query,
            'results': results
        }
    )

"""
"""

def validate_email_format(email: str) -> bool:
    """To validate the email format here."""

    # Regular expression pattern for a basic email format validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

"""
"""

@require_POST
def course_subscribe(request):
    """To save the subscribers here."""

    if 'subscriber' not in request.POST:
        return redirect('/course/')
    
    email = request.POST.get('subscriber')
    
    # If the email is not valid, send the error message.
    if not validate_email_format(email):
        data = {
            'status': 'error', 
            'title': _('订阅失败'),
            'message': _('很遗憾，由于您的电子邮箱地址无效，您未能订阅成功《孙北海的Python武器库》周报。')}
        json_params = {'ensure_ascii': False}
        
        return JsonResponse(data, json_dumps_params=json_params)
    
    # If the email is valid, save the subscriber here.
    try:
        subscriber = Subscriber(email=email)
        
        subscriber.save()
        
        data = {
            'status': 'success', 
            'title': _('订阅成功'),
            'message': _('恭喜您成功订阅《孙北海的Python武器库》周报！')}
        json_params = {'ensure_ascii': False}
        
        return JsonResponse(data, json_dumps_params=json_params)
    except Exception as e:
        logger.exception("An error occurred: %s", e)
    
    # If the subscriber is not saved, send the error message.
    data = {
        'status': 'error', 
        'title': _('订阅失败'),
        'message': _('很遗憾，您未能订阅成功《孙北海的Python武器库》周报。')}
    json_params = {'ensure_ascii': False}
        
    return JsonResponse(data, json_dumps_params=json_params)
    
"""
"""

def course_detail(request, slug):
    """To retrieve the course detail here."""

    course = get_object_or_404(Course, slug=slug, status=Course.Status.PUBLISHED)
    
    # Locate the first article of this course.
    child_categories = course.get_child_categories()
    first_category = child_categories[0] if len(child_categories) > 0 else None
    child_articles = first_category.get_child_articles() if first_category else []
    first_article = child_articles[0] if len(child_articles) > 0 else None
    
    # If there is no article, redirect to the course page.
    return redirect(first_article.get_absolute_url()) \
        if first_article \
        else redirect('/course/')

"""
"""

def category_detail(request, slug):
    """To retrieve the category detail here."""

    category = get_object_or_404(Category, slug=slug)
    
    # Locate the first article of this category.
    child_articles = category.get_child_articles()
    first_article = child_articles[0] if len(child_articles) > 0 else None
    
    # If there is no article, redirect to the course page.
    return redirect(first_article.get_absolute_url()) \
        if first_article \
        else redirect('/course/')
