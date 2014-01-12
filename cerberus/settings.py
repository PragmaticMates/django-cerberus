from django.conf import settings

# Number of max failed login attempts
CERBERUS_MAX_ATTEMPTS = getattr(settings, 'CERBERUS_MAX_ATTEMPTS', 3)

# Number of seconds after the failed login attempts are forgotten in seconds
CERBERUS_LOCKOUT_TIME = getattr(settings, 'CERBERUS_LOCKOUT_TIME', 600)
