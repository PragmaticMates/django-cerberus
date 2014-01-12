django-cerberus
===============

Django app that locks out users after too many failed login attempts until release time expires.

Tested on Django 1.4.5.


Requirements
------------
- Django


Installation
------------

1. Install python library using pip: pip install django-cerberus

2. Add ``cerberus`` to ``INSTALLED_APPS`` in your Django settings file

3. Sync your database


Usage
-----

Add ``cerberus.decorators.watch_logins`` decorator to your login view. Example::


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


Settings
''''''''

CERBERUS_MAX_ATTEMPTS
    Number of max failed login attempt. Default: ``5``.

CERBERUS_LOCKOUT_TIME
    Number of seconds after the failed login attempts are forgotten in seconds. Default: ``600``.


Model
'''''
Each lockout model instance contains username, number of failed login attempts, IP address, user agent details,
GET and POST parameters, information if lockout is locked (user tried to log in with wrong credentials at least
``CERBERUS_MAX_ATTEMPTS`` times) and if lockout is expired (based on ``CERBERUS_LOCKOUT_TIME``).


Template
''''''''
You can override ``cerberus/lockout.html`` template if you wish. There is ``lockout`` instance and ``lockout_time`` variable
(CERBERUS_LOCKOUT_TIME) available in template context.


Authors
-------

Library is by `Erik Telepovsky` from `Pragmatic Mates`_. See `our other libraries`_.

.. _Pragmatic Mates: http://www.pragmaticmates.com/
.. _our other libraries: https://github.com/PragmaticMates