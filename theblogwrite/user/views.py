from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm
from blog.models import Post

# Create your views here.
def register(request):
    # if request.user.is_authenticated:
    #     return redirect('Home')
    # else:
        
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('Home')
        else:
            messages.error(request, f'Account created for error!')  
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form, 'register':'active'})


def signin(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')    
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('Home')
    return render(request, "login.html", { 'form': form, 'signin':'active' })


def signout(request):
    logout(request)
    return redirect('Home')


@login_required(login_url='signin')
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                    request.FILES,
                                    instance = request.user.profile
                                    )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            # messages.success(request, f'Account  Successful updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)
        category = Post.objects.values('categories__title').filter(author = request.user).order_by('-date_posted')
    context = {
        'u_form' : u_form,
        'p_form' : p_form,
        'category' : category,
        'active' : 'active'
    }
    return render (request, 'profile.html', context)


