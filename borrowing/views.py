from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import BorrowingForm


@login_required
def add_borrowing(request):
    if request.method == 'POST':
        form = BorrowingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-home')
    else:
        form = BorrowingForm()
    return render(request, 'borrowing/add_borrowing.html', {'form': form})
