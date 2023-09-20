from django.core.management.base import BaseCommand, CommandError
import json
from course.models import Article

class Command(BaseCommand):
    help = 'Dumps articles to a JSON file.'
        
    def handle(self, *args, **options):
        # Start to dump articles.
        self.stdout.write("Starting to dump articles ...", ending="")
        
        # Get all articles.
        articles = Article.objects.all()

        # Dump articles to a JSON file, as well as to a markdown file if it exists.
        for article in articles:
            self.stdout.write(f"\tDumping article <{article.title}> ...", ending="\n")
            
            with open(f'article_{article.id}_{article.slug}.json', 'w', encoding='utf-8') as json_file:
                json.dump(
                    {
                        'title': article.title,
                        'publication_date': article.published_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'author': article.author.username,
                        'category': article.category.title,
                        'order_in_category': article.order_in_category,
                        'need_login': article.need_login,
                    }, 
                    json_file, 
                    indent=4,
                    ensure_ascii=False)
            
            with open(f'article_{article.id}_{article.slug}.md', 'w', encoding='utf-8') as md_file:
                md_file.write(article.body)

        # Finish dumping articles.
        self.stdout.write(self.style.SUCCESS('Successfully dumped articles to articles.json'))