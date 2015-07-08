from django.db import models
from django.utils.translation import ugettext_lazy as _

try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone

from settings import CERBERUS_LOCKOUT_TIME


class Lockout(models.Model):
    username = models.CharField(max_length=255, verbose_name=_(u'username'), db_index=True,
        blank=True, null=True, default=None)
    failed_attempts = models.PositiveIntegerField(verbose_name=_(u'failed attempts'), default=0)
    ip_address = models.GenericIPAddressField(verbose_name=_(u'IP address'),
        blank=True, null=True, default=None)
    user_agent = models.CharField(max_length=1024, verbose_name=_(u'user agent'),
        blank=True, null=True, default=None)
    params_get = models.TextField(verbose_name=_(u'GET params'))
    params_post = models.TextField(verbose_name=_(u'POST params'))
    is_locked = models.BooleanField(verbose_name=_(u'locked'), default=False, db_index=True)
    is_expired = models.BooleanField(verbose_name=_(u'expired'), default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cerberus_lockouts'
        verbose_name = _(u'lockout')
        verbose_name_plural = _(u'lockouts')
        ordering = ('-created', )

    def __unicode__(self):
        return u'%s: %s' % (self.username, self.ip_address)

    @property
    def expiration_time(self):
        """
        Returns the time until this access attempt is forgotten.
        """
        if CERBERUS_LOCKOUT_TIME <= 0:
            return None

        now = timezone.now()
        delta = now - self.modified
        time_remaining = CERBERUS_LOCKOUT_TIME - delta.seconds
        return time_remaining

    def get_expiration_time_text(self):
        """
        Returns the text for the admin based on the time to forget
        """
        time_remaining = self.expiration_time

        if not self.is_locked:
            return _(u'Not locked yet')
        elif time_remaining is None:
            return _(u'Infinite')
        elif time_remaining <= 0:
            return _(u'Forgotten')
        else:
            return _(u'%(time_remaining)s seconds' % {'time_remaining': time_remaining})
    get_expiration_time_text.short_description = _(u'Expiration time')
