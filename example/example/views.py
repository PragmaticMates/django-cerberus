from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView

from cerberus.decorators import watch_logins


class LoginView(FormView):
    template_name = 'example/login.html'
    form_class = AuthenticationForm

    @method_decorator(watch_logins)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        return reverse('logged_in')


class LoggedInView(TemplateView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoggedInView, self).dispatch(request, *args, **kwargs)
    template_name = 'example/logged_in.html'
