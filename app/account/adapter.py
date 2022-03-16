from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse
class AccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        url = super(AccountAdapter, self).get_login_redirect_url(request)
    
        return reverse("useraccounts:user_login")