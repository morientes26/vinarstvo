from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from winelist.settings import LOGIN_URL

import logging

logger = logging.getLogger(__name__)

def login_view(request):
    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                logging.info('loggin user id=%s' , user.id)
                # Redirect to a success page.
                return redirect(redirect_by_role(user))
            else:
                # Return a 'disabled account' error message
                logging.info('disable account user id=%s', user)
    else:
        # Return an 'invalid login' error message.
        logging.error('invalid login %s', user)

    return redirect(LOGIN_URL)

def logout_view(request):
    print('logout')
    logout(request)
    return redirect(LOGIN_URL)

def redirect_by_role(user):
    if user.groups.count()>0:
        if user.groups.first().name=='waiter':
            return '/cart/' + get_token(user.username) 
    return 'list_products'

def get_token(username):
    #TODO: token service
    return "5df34dg"+username+"1f2s4d23"