from django import template
from blog.models import Article
from bookmark.models import ImageBookmark
from django.contrib.contenttypes.models import ContentType
register = template.Library()


@register.simple_tag
def MainTitle(value="Moel"):
    return value


@register.inclusion_tag('blog/partials/recent-side.html')
def recent_posts():
    bookmarks = ImageBookmark.objects.all()[:6]
    articles = Article.objects.published()[:3]
    return {'recent_articles': articles, 'recent_bookmarks': bookmarks}
