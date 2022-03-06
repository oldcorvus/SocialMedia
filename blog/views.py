from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DeleteView, DetailView
from blog.mixins import AuthorMixin, AjaxRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Article , Category
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from relations.utils import create_action
from django.contrib import messages
from django.utils.text import slugify
from comments.forms import CommentFrom
from bookmark.models import ImageBookmark


class IndexPage(ListView):
    paginate_by = 4
    template_name = 'blog/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        articles = Article.objects.published()
        return articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_categories = Category.objects.filter(status=True)
        context['category_data'] = all_categories
        context['slidebar'] = Article.objects.filter(
            status='P', promote=True)[:3]
        context['recent_bookmarks'] = ImageBookmark.objects.all()[:6]

        return context


class ArticleListView(ListView):
    paginate_by = 12
    template_name = 'blog/categories-grid.html'
    context_object_name = 'articles'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category-title'] = category
        return context


class ArticleDetailView(DetailView):

    model = Article
    template_name = 'blog/details-post-default.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_reply=False)
        context['form'] = CommentFrom()

        return context

    def get_object(self):
        article = get_object_or_404(Article, slug=self.kwargs.get('slug'),
                                    status='P', publish__year=self.kwargs.get('year'), publish__month=self.kwargs.get('month'), publish__day=self.kwargs.get('day'))
        return article


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "blog/create-article.html"
    fields = ['title', 'cover', 'content', 'category', 'status']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "ایجاد مقاله "
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['content'].widget = CKEditorUploadingWidget()
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(
            form.cleaned_data['title'][:30], allow_unicode=True)
        response = super(ArticleCreateView, self).form_valid(form)
        create_action(self.request.user, 'posted  article', self.object)
        messages.success(self.request, 'پست شما با موفقیت منتشر شد ')
        return response


class ArticleUpdateView(LoginRequiredMixin, AuthorMixin, UpdateView):
    model = Article
    template_name = "blog/create-article.html"
    fields = ['title', 'content', 'cover', 'category', 'status']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "ويرايش "
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['content'].widget = CKEditorUploadingWidget()
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(
            form.cleaned_data['title'][:30], allow_unicode=True)
        messages.success(self.request, "مقاله شما با موفقيت ويرايش يافت")

        return super(ArticleUpdateView, self).form_valid(form)


class ArticleDeleteView(LoginRequiredMixin, AuthorMixin, DeleteView):
    model = Article

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        create_action(self.request.user, 'deleted article', article)
        article.delete()
        messages.success(self.request, "مقاله شما با موفقيت حذف يافت")
        return redirect("blog:index")


class UserArticlesListView(LoginRequiredMixin, ListView):
    model = Article
    paginate_by = 5
    template_name = "blog/user_articles.html"
    context_object_name = 'articles'

    def get_queryset(self):
        username = self.kwargs.get('username')
        return Article.objects.filter(author__username=username)


class ArticleUpdateView(LoginRequiredMixin, AuthorMixin, UpdateView):
    model = Article
    template_name = "blog/create-article.html"
    fields = ['title', 'content', 'cover', 'category', 'status']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "ويرايش "
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['content'].widget = CKEditorUploadingWidget()
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(
            form.cleaned_data['title'][:30], allow_unicode=True)
        messages.success(self.request, "مقاله شما با موفقيت ويرايش يافت")

        return super(ArticleUpdateView, self).form_valid(form)


class ArticleLikeView(LoginRequiredMixin, AjaxRequiredMixin, View):

    def post(self, request):
        article_id = request.POST.get('id')
        action = request.POST.get('action')
        if article_id and action:
            try:
                article = Article.objects.get(id=article_id)
                if action == 'like':
                    create_action(request.user, 'likes', article)
                    article.users_like.add(request.user)
                else:
                    create_action(request.user, 'dislikes', article)
                    article.users_like.remove(request.user)
                return JsonResponse({'status': 'ok'})
            except:
                pass
        return JsonResponse({'status': 'error'})
