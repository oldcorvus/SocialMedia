from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserChangeForm, UserCreationForm, VerifyCodeForm, UserLoginForm
from django.contrib.auth import get_user_model
from .models import OtpCode, CustomUser
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

User = get_user_model()


class UserRegisterView(View):
    form_class = UserCreationForm
    template_name = 'account/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            CustomUser.objects.create_user(username=cd['username'], phone_number=cd['phone_number'], email=cd['email'],
                                           password=cd['password1'])
            messages.success(request, 'you registered.', 'success')
            return redirect('/')

        return render(request, self.template_name, {'form': form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'account/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(
            phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                User.objects.create_user(user_session['phone_number'], user_session['email'],
                                         user_session['full_name'], user_session['password'])

                code_instance.delete()
                messages.success(request, 'you registered.', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'this code is wrong', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'با موفقیت خارج از سایت شدید', 'success')
        return redirect('blog:index')


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, email=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'با موفقیت وارد سایت شدید', 'info')
                return redirect('/')
            messages.error(request, 'ایمیل یا رمز عبور نادرست است', 'warning')
        return render(request, self.template_name, {'form': form})


class UserDetailView(DetailView):

    model = CustomUser
    template_name = 'account/profile.html'
    context_object_name = 'user'
    slug_url_kwarg = "user"
    slug_field = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser, username=self.kwargs['user'])
        if self.request.user == user:
            context['self_profile'] = True
        return context

    def get_queryset(self):
        return super().get_queryset()


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    template_name = "account/edit-profile.html"
    form_class = UserChangeForm
    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "ویرایش "
        return context

    def test_func(self):
        user = self.get_object()
        if self.request.user == user:
            return True
        return False

    def form_valid(self, form):
        messages.success(self.request, " با موفقيت ويرايش يافت")

        return super(UserUpdateView, self).form_valid(form)
