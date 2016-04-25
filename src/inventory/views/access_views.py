from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from winelist.settings import LOGIN_URL
 
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            print('redirect to success page')
        else:
            # Return a 'disabled account' error message
            print('disable account')
    else:
        # Return an 'invalid login' error message.
        print('invalid login')

def logout_view(request):
    print('logout')
    logout(request)
    return redirect(LOGIN_URL)