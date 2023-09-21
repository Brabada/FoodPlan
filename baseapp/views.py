from django.shortcuts import render
from .forms import CustomUserCreationForm


def index(request):


    return render(request, 'index.html')


def register(request):

    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print('im here!!!!!')
        if form.is_valid():
            form.save()

    context = {
        'form': form,
    }
    return render(request, 'register.html', context)