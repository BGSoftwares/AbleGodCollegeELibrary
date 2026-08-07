from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm


@login_required
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register_user.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('home')
