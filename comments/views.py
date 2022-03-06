from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.views import View
from blog.models import Article
from comments.forms import CommentFrom
from .models import Comment
from django.urls import reverse
from ckeditor.widgets import CKEditorWidget
from django.contrib.contenttypes.models import ContentType


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentFrom

    def form_valid(self, form):
        if self.kwargs.get('type') == 'article':
            target = get_object_or_404(Article, pk=self.kwargs.get('id'))
        else:
            pass

        form.instance.author = self.request.user
        form.instance.content_object = target

        if self.kwargs.get('reply'):
            form.instance.is_reply = True
            form.instance.reply = get_object_or_404(
                Comment, pk=self.kwargs['reply'])
        return super(CommentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog:index')


class ApproveComment(LoginRequiredMixin, View):
    def get(self, request, id):
        comment = get_object_or_404(Comment, id=id)
        comment.approve = True
        comment.save()
        return redirect(to='blog:index')
