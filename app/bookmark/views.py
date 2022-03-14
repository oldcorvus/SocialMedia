from django.shortcuts import render, redirect,  render,  get_object_or_404
from django.http import JsonResponse
from django.utils.text import slugify
from relations.utils import create_action
from django.contrib import messages
from .models import ImageBookmark
from .forms import ImageCreateForm
from comments.forms import CommentFrom
from django.views.generic import ListView, DeleteView, UpdateView, DetailView, CreateView, View
from blog.mixins import AuthorMixin, AjaxRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin


class BookmarkCreateView(LoginRequiredMixin, CreateView):
    model = ImageBookmark
    template_name = "bookmark/create.html"
    form_class = ImageCreateForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class(data=request.GET)})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "ایجاد بوکمارک "
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super(BookmarkCreateView, self).form_valid(form)
        create_action(self.request.user, 'bookmarked', self.object)
        messages.success(self.request, 'تصویر شما با موفقیت منتشر شد')
        return response


class BookmarkUpdateView(LoginRequiredMixin, AuthorMixin, UpdateView):
    model = ImageBookmark
    template_name = "bookmark/create.html"
    fields = ['title', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "ويرايش "
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(
            form.cleaned_data['title'][:30], allow_unicode=True)
        messages.success(self.request, "بوکمارک شما با موفقيت ويرايش يافت")

        return super(BookmarkUpdateView, self).form_valid(form)


class BookmarkDetailView(DetailView):

    model = ImageBookmark
    template_name = 'bookmark/details.html'
    context_object_name = 'bookmark'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_reply=False)
        context['form'] = CommentFrom()

        return context

    def get_object(self):
        bookmark = get_object_or_404(ImageBookmark, slug=self.kwargs.get('slug'),
                                     pk = self.kwargs.get('id'),
                                     created__year=self.kwargs.get('year'), created__month=self.kwargs.get('month'), created__day=self.kwargs.get('day'))
        return bookmark


class BookmarkDeleteView(LoginRequiredMixin, AuthorMixin, DeleteView):
    model = ImageBookmark

    def post(self, request, *args, **kwargs):
        bookmark = get_object_or_404(ImageBookmark, pk=self.kwargs.get('pk'))
        create_action(self.request.user, 'deleted bookmark', bookmark)
        bookmark.delete()
        messages.success(self.request, "بوکمارک شما با موفقيت حذف يافت")
        return redirect("blog:index")


class BookmarkLikeView(LoginRequiredMixin, AjaxRequiredMixin, View):

    def post(self, request):
        image_id = request.POST.get('id')
        action = request.POST.get('action')
        if image_id and action:
            try:
                image = ImageBookmark.objects.get(id=image_id)
                if action == 'like':
                    create_action(request.user, 'likes', image)
                    image.users_like.add(request.user)
                else:
                    image.users_like.remove(request.user)
                    create_action(request.user, 'dislikes', image)
                return JsonResponse({'status': 'ok'})
            except:
                pass
        return JsonResponse({'status': 'error'})


class BookmarkListView(ListView):
    paginate_by = 5
    model = ImageBookmark
    template_name = 'bookmark/list.html'
    context_object_name = 'images'

    def get_template_names(self):
        template_name = 'bookmark/list.html'
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            template_name = 'bookmark/list_ajax.html'
        return template_name
