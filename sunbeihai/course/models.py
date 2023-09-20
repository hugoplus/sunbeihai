from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

"""
"""

User = get_user_model()

"""
Course model
"""

class PublishedCoursesManager(models.Manager):
    """This is the custom manager for Course model."""
    
    def get_queryset(self):
        return super().get_queryset().filter(status=Course.Status.PUBLISHED)
    
class HighlightedCoursesManager(models.Manager):
    """This is the custom manager for Course model."""
    
    def get_queryset(self):
        return super().get_queryset().filter(highlight_order__in=[1, 2, 3, 4, 5])

class Course(models.Model):
    """This is the course model."""
    
    # The fields for Course model.
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        
    title = models.CharField(max_length=125)
    slug = models.SlugField(
        max_length=125, 
        unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='courses')
    status = models.CharField(
        max_length=2, 
        choices=Status.choices, 
        default=Status.DRAFT)
    cover = models.ImageField(
        upload_to='courses/%Y/%m/%d/',
        blank=True)
    description = models.TextField()
    highlight_order = models.IntegerField(
        null=True, 
        blank=True)
    
    # The managers for Course model.
    objects = models.Manager() # The default manager.
    published_objects = PublishedCoursesManager() # The custom manager to retrieve published courses.
    highlighted_objects = HighlightedCoursesManager() # The custom manager to retrieve 5 highlighted courses.
    
    # The methods for Course model.
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self) -> str:
        return reverse(
            "course:course_detail", 
            kwargs={"slug": self.slug})
        
    def get_child_categories(self):
        """To retrieve the child categories of this course."""
        child_categories = []
        
        if self.contained_categories.count() > 0:
            child_categories.extend(list(self.contained_categories.filter(parent__isnull=True).order_by('order')))
        
        return child_categories
    
    def get_category_tree(self):
        """This method returns a category tree of this course."""
        category_tree = []
        
        if self.contained_categories.count() > 0:
            sub_categories = self.contained_categories.filter(parent__isnull=True).order_by('order')
            for sub_category in sub_categories:
                category_tree.append(sub_category.get_category_tree())
        
        return category_tree

    def get_content_tree(self):
        """This method returns a content tree of this course."""
        content_tree = []
        
        child_categories = self.get_child_categories()
        
        if len(child_categories) > 0:
            for child_category in child_categories:
                content_tree.append(child_category.get_content_tree())
        
        return content_tree

"""
Category model
"""

class Category(models.Model):
    """This is the category model."""
    
    # The fields for Category model.
    title = models.CharField(max_length=125)
    slug = models.SlugField(
        max_length=125, 
        unique=True)
    order = models.IntegerField(
        null=False,
        default=0)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='sub_categories',
        null=True,
        blank=True)
    course = models.ForeignKey(
        Course, 
        on_delete=models.PROTECT, 
        related_name='contained_categories',
        null=True,
        blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='categories')
    description = models.TextField(
        null=True,
        blank=True)
    
    # The methods for Category model.
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self) -> str:
        return reverse(
            "course:category_detail", 
            kwargs={"slug": self.slug})
        
    def get_category_tree(self):
        """This method returns a tree of all my sub categories."""
        my_category_tree = []
        my_category_tree.append(self) # Add myself as the first item in the tree.
        
        if self.sub_categories.count() > 0:
            sub_categories = self.sub_categories.all().order_by('order')
            for sub_category in sub_categories:
                my_category_tree.append(sub_category.get_category_tree())
        
        return my_category_tree
    
    def get_child_articles(self):
        """To retrieve all the child articles in this category."""
        
        articles = []
        if self.contained_articles.count() > 0:
            articles.extend(self.contained_articles.all().order_by('order_in_category')) # To generate a flatten list

        return articles
        
    def get_all_contained_articles(self):
        """To retrieve all my contained articles."""

        articles = []
        
        articles.extend(self.get_child_articles()) 
                
        if self.sub_categories.count() > 0:
            sub_categories = self.sub_categories.all().order_by('order')
            for category in sub_categories:
                articles.extend(category.get_all_contained_articles()) # To generate a flatten list

        return articles
    
    def get_content_tree(self):
        """To retrieve the content tree of this category."""
        
        # Define the quick sort function for the category tree.
        def content_tree_quick_sort(node_list):
            """To sort the give category tree."""

            if len(node_list) <= 1:
                return node_list

            return content_tree_quick_sort([x for x in node_list[1:] if x['order'] < node_list[0]['order']]) \
                    + node_list[0:1] \
                    + content_tree_quick_sort([x for x in node_list[1:] if x['order'] >= node_list[0]['order']])
                    
        # Define the root tree node.
        content_tree = {
            'id': self.id, 
            'text': self.title, 
            'order': self.order, 
            'href': self.get_absolute_url(), 
            'type': 'node', 
            'nodes': []}
        
        # Add all the child articles in this node.
        if self.contained_articles.count() > 0:
            articles = self.get_child_articles()
            for article in articles:
                content_tree['nodes'].append(
                    {
                        'id': article.id,
                        'text': article.title,
                        'href': article.get_absolute_url(),
                        'order': article.order_in_category,
                        'type': 'leaf'
                    })
        
        # Add all the sub categories and their articles in this node.
        if self.sub_categories.count() > 0:
            categories = self.sub_categories.all().order_by('order')
            for category in categories:
                content_tree['nodes'].append(
                    category.get_content_tree())
        
        # Sort the content tree.
        if not content_tree['nodes']:
            del content_tree['nodes']
        else:
            content_tree['nodes'] = content_tree_quick_sort(content_tree['nodes'])
        
        return content_tree

"""
Article model
"""

class PublishedArticlesManager(models.Manager):
    """This is the custom model manager for Article to retrieve published articles."""

    def get_queryset(self):
        return super().get_queryset().filter(status=Article.Status.PUBLISHED)

class Article(models.Model):
    """This is the data model for every article in the course."""

    # The fields for Article model.
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=255)
    slug = models.SlugField(
                    max_length=255, 
                    unique_for_date='published_at')
    author = models.ForeignKey(
                        User, 
                        on_delete=models.PROTECT,
                        related_name='my_articles')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(
                        max_length=2, 
                        choices=Status.choices, 
                        default=Status.DRAFT)
    category = models.ForeignKey(
                        Category, 
                        on_delete=models.PROTECT, 
                        related_name='contained_articles',
                        null=True,
                        blank=True)
    order_in_category = models.IntegerField(default=0)
    need_login = models.BooleanField(
                        null=False, 
                        default=False)

    # The managers for Article model.
    objects = models.Manager() # The default manager.
    published_objects = PublishedArticlesManager() # The custom manager to retrieve published articles.

    # The methods for Article model.
    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at'])]
    
    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse(
            'course:article_detail',
            kwargs={
                'year': self.published_at.year,
                'month': self.published_at.month,
                'day': self.published_at.day,
                'slug': self.slug
                })
        
    def get_parent_course(self):
        """To retrieve the parent course of this article."""
        
        if self.category:
            return self.category.course
        else:
            return None
    
    def get_active_comments(self):
        """To retrieve all the comments of this article."""
        
        # If this article has no comments, return an empty list.
        if self.comments.filter(is_active=True).count() == 0:
            return []
        
        # Find the active comments for this article.
        comments = list(self.comments.filter(is_active=True))[::-1]
        comment_list = []
        
        # Sort the comments by their parent.
        while len(comments):
            if comments[0].parent:
                comment_sub_list = [] # To hold the comments
                comment_index_list = [] # To hold the index of a comment
                
                comment_sub_list.append(comments[0])
                comment_index_list.append(0)
                
                # Add the comment chain to the comment_list
                comment = comments[0]
                while comment.parent:
                    comment = comment.parent
                    comment_sub_list.append(comment)
                    comment_index_list.append(comments.index(comment))
                    
                comment_list.append(comment_sub_list[::-1])
                
                comment_index_list = comment_index_list[::-1]
                
                # Remove the added comments from the comment list
                for i in comment_index_list:
                    comments.pop(i)

                comment_sub_list.clear()
                comment_index_list.clear()
            else:
                comment_list.append(comments[0])
                comments.pop(0)
        
        comment_list = comment_list[::-1]
        
        return comment_list
        
"""
Comment model
"""

class Comment(models.Model):
    """This is the data model for comments."""

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='sub_comments',
        null=True,
        blank=True)
    name = models.CharField(max_length=80)
    email = models.EmailField(null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.article}'
    
    def get_absolute_url(self) -> str:
        return reverse(
            'course:article_comment_detail',
            args=[
                self.article.id,
                self.id
                ])
    
"""
Subscriber
"""

class Subscriber(models.Model):
    """This is the data model for subscribers."""
    
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['email', 'created_at']),
            ]
    
    def __str__(self):
        return f"Subscriber: {self.email}"