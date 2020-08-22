from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from blog.models import Post
import socket
# Create your views here.

def index(request):
    most_recent = Post.objects.order_by('-date_posted')[:3]
    context = { 'home': 'active',
                'most_recent' : most_recent
    }
    return render(request, 'index.html', context)


def about_us(request):
    return render(request, 'about_us.html')


def contact_us(request):
    if request.method == 'POST':
        c_name = request.POST['c-name']
        c_subject = request.POST['c-subject'] # Subject
        c_message = request.POST['c-message']  #Message
        c_email = request.POST['c-email']       # from email
        recipient_list = ['dv49886@gmail.com']  # To Email, Like team
        #send mail
        try:
            send_mail(c_subject, c_message, c_email, recipient_list )
            messages.success(request, f'ThankYou for Contact with us. {c_name}!')
            return render(request, 'contact_us.html', { 'contact_us': 'active'})
        except socket.gaierror:
            messages.error(request, f'Check your network connection...')
            return render(request, 'contact_us.html', { 'contact_us': 'active'})
    else: 
        return render(request, 'contact_us.html', { 'contact_us': 'active'})


