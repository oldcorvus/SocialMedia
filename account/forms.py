
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import CustomUser, OtpCode


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'username')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user = CustomUser.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError('شماره تماس از قبل موجود است')
        OtpCode.objects.filter(phone_number=phone).delete()
        return phone

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise forms.ValidationError('رمز ها یکسان نیستند')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    def clean_password2(self):
        if 'email' in self.cleaned_data:
            email = self.cleaned_data['email']
            user = CustomUser.objects.filter(email=email)
            if user.exists():
                raise forms.ValidationError(
                    "با ایمیل وارد شده قبلا ثبت نام صورت گرفته شده لطفا ایمیل دیگری را انتخاب کنید")


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="you can change password using <a href=\"../password/\">this form</a>.")

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'first_name',
                  'last_name', 'about_me', 'profile_image')


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class UserLoginForm(forms.Form):
    """user login form"""
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
