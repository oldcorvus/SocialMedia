from django import template
from ..models import Article, Category
from relations.models import Action
from django.contrib.contenttypes.models import ContentType
register = template.Library()

@register.simple_tag
def MainTitle(value="Moel"):
    return value


@register.inclusion_tag('blog/partials/user_followings.html')
def user_followings(user):
    
    following_ids = user.following.values_list('id',
                                                       flat=True)
    actions = Action.objects.exclude(user=user).filter(user_id__in=following_ids)

    ct_blog = ContentType.objects.get(app_label="blog", model="article")
    
    articles_actions=actions.filter(target_ct=ct_blog)

    return {
        'user_articles': articles_actions,
        'user':user,
    }
@register.inclusion_tag('blog/partials/sidebar_user_actions.html')
def followings_action_sidebar(username):
    
    following_ids = username.following.values_list('id',flat=True)

    actions = Action.objects.exclude(user=username).filter(user_id__in=following_ids)
    actions = actions.select_related('user',)\
                     .prefetch_related('target')[:3]
    return {'actions': actions}

@register.inclusion_tag('blog/partials/recent-side.html')
def recent_posts():
    articles = Article.objects.published()[:3]
    return {'recent_articles': articles}

@register.inclusion_tag('blog/partials/recent_articles.html')
def recent_articles():
    articles = Article.objects.published()[:8]
    return {'articles_recent': articles}
