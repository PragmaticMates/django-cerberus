from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from views import LoggedInView, LoginView


admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Examples:
    url(r'^log-out/', 'django.contrib.auth.views.logout', {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^logged-in/', LoggedInView.as_view(), name='logged_in'),
    url(r'^$', LoginView.as_view(), name='login'),
)
