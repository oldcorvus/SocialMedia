from django import template
from relations.models import Action
from django.contrib.contenttypes.models import ContentType
register = template.Library()


@register.inclusion_tag('blog/partials/user_followings.html')
def user_followings(user):

    following_ids = user.following.values_list('id',
                                               flat=True)
    actions = Action.objects.exclude(
        user=user).filter(user_id__in=following_ids)

    ct_blog = ContentType.objects.get(app_label="blog", model="article")

    ct_bookmark = ContentType.objects.get(
        app_label="bookmark", model="imagebookmark")

    articles_actions = actions.filter(target_ct=ct_blog)
    user_bookmarks = actions.filter(target_ct=ct_bookmark)

    return {
        'user_articles': articles_actions,
        'user_bookmarks': user_bookmarks,
        'user': user,
    }


@register.inclusion_tag('blog/partials/sidebar_user_actions.html')
def followings_action_sidebar(username):

    following_ids = username.following.values_list('id', flat=True)

    actions = Action.objects.exclude(
        user=username).filter(user_id__in=following_ids)
    actions = actions.select_related('user',)\
                     .prefetch_related('target')[:3]
    return {'actions': actions}
