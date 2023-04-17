from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect
from .forms import NewUserForm

# Create your views here.


def login(request):
    return render(request, 'login.html')


def register(request):
    return HttpResponse("Hello, world. You're at the register index.")


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request)
        print(form)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            messages.success(request, "Registration successful.")
            return render(request, 'login.html')
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})
