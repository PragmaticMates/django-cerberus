from django.shortcuts import render_to_response
from django.template import RequestContext

from models import Lockout
from settings import CERBERUS_MAX_ATTEMPTS, CERBERUS_LOCKOUT_TIME


def get_ip_address(request):
    # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
    ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
    return ip.split(', ')[0] if ip else request.META.get('REMOTE_ADDR', None)


def watch_logins(func):
    def new_func(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        ip = get_ip_address(request)

        # pass request.body as param
        #username = request.POST.get('username', None)
        lockout = get_lockout(ip)
        lockout = check_failed_login(request, response, lockout)

        if lockout.is_locked:
            response = get_locked_response(request, lockout)

        return response
    return new_func


def get_lockout(ip):
    """
    Returns the Lockout object for a given IP.
    """
    try:
        # get username to lookup
        lockout = Lockout.objects.filter(ip_address=ip, is_expired=False)[0]
    except IndexError:
        lockout = None

    if lockout:
        time_remaining = lockout.expiration_time
        if time_remaining is not None and time_remaining <= 0:
            # Unlock user
            lockout.is_expired = True
            lockout.save()
            return None

    return lockout


def check_failed_login(request, response, lockout):
    """
    If is a failed login, save the data in the database.
    It returns the Lockout instance.
    """
    ip = get_ip_address(request)
    user_agent = request.META.get('HTTP_USER_AGENT', None)
    username = request.POST.get('username', None)

    if not lockout:
        lockout = Lockout(ip_address=ip)

    if request.method == 'POST' and response.status_code != 302:
        # Failed login
        lockout.user_agent = user_agent
        lockout.username = username
        lockout.failed_attempts += 1
        lockout.params_get = request.GET
        lockout.params_post = request.POST

        if lockout.failed_attempts >= CERBERUS_MAX_ATTEMPTS:
            # Lock user
            lockout.is_locked = True
        lockout.save()
    elif request.method == 'POST' and response.status_code == 302 and lockout.id and not lockout.is_locked:
        # The user logged in successfully. Forgets about the failed login attempts
        lockout.is_expired = True
        lockout.save()

    return lockout


def get_locked_response(request, lockout):
    try:
        return render_to_response(
            'cerberus/lockout.html', {
                'lockout': lockout,
                'lockout_time': CERBERUS_LOCKOUT_TIME
            },
            context=RequestContext(request)
        )
    except TypeError:
        return render_to_response(
            'cerberus/lockout.html', {
                'lockout': lockout,
                'lockout_time': CERBERUS_LOCKOUT_TIME
            },
            context_instance=RequestContext(request)
        )
