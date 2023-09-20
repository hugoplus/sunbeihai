import logging
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files import File
from django.utils.translation import gettext_lazy as _
from .models import Newsletter
from course.models import Course

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

def newsletter_detail(request, year, month, day, slug):
    """This is to show the details of the newsletter."""
    
    newsletter = get_object_or_404(
            Newsletter,
            status=Newsletter.Status.PUBLISHED, 
            slug=slug,
            published_at__year=year,
            published_at__month=month,
            published_at__day=day)
    
    courses = Course.published_objects.all()
    
    with open(newsletter.file.path, 'rb') as f:
        # Render the page.
        return render(
            request, 
            'newsletter/newsletter_detail.html', 
            {
                'newsletter': newsletter,
                'newsletter_content': f.read().decode('utf-8'),
                'courses': courses
            })

"""
"""

def newsletter_list(request):
    """This is to show the list of the newsletters."""
    
    # Get the published newsletters.
    newsletters = Newsletter.objects.filter(status=Newsletter.Status.PUBLISHED)
    
    # Get the courses.
    courses = Course.published_objects.all()
    
    # Get the paginator.
    paginator = Paginator(newsletters, 10)
    
    # Get the page number.
    page = request.GET.get('page')
    
    # Get the page of the paginator.
    try:
        paged_newsletters = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, deliver the first page.
        paged_newsletters = paginator.page(1)
    except EmptyPage:
        # If the page is out of range (e.g. 9999), deliver the last page of results.
        paged_newsletters = paginator.page(paginator.num_pages)
    
    # Render the page.
    return render(
        request, 
        'newsletter/newsletter_list.html', 
        {
            'newsletters': paged_newsletters,
            'courses': courses
        })