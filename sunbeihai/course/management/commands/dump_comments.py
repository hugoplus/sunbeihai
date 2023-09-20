from django.core.management.base import BaseCommand, CommandError
import json
from course.models import Article, Comment

class Command(BaseCommand):
    help = 'Dumps comments to a JSON file.'
        
    def handle(self, *args, **options):
        # Start to dump comments.
        self.stdout.write("Starting to dump comments ...", ending="\n")
        
        # Get all articles.
        articles = Article.objects.all()

        # Dump comments of every article to a JSON file.
        for article in articles:
            if article.comments.filter(is_active=True).count() == 0:
                continue
            
            self.stdout.write(f"\tDumping comments of article <{article.title}> ...", ending="\n")
            
            comments = list(article.comments.filter(is_active=True))
            
            comment_list = []
            
            for comment in comments:
                comment_list.append(
                    {
                        'id': comment.id,
                        'name': comment.name,
                        'email': comment.email,
                        'body': comment.body,
                        'parent_id': comment.parent_id,
                        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    }
                )
            
            with open(f'article_{article.id}_{article.slug}_comments.json', 'w', encoding='utf-8') as json_file:
                json.dump(
                    comment_list, 
                    json_file, 
                    indent=4,
                    ensure_ascii=False)

        # Finish dumping comments.
        self.stdout.write(self.style.SUCCESS('Successfully dumped comments to comments.json'))