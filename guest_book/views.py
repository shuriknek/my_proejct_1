#!/usr/bin/env python3

#-*- coding:utf-8; -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from .models import User
from .models import ContactForm
import datetime
import sqlite3
from datetime import timedelta

def serv(request):
    return render(request, "/")

def index(request):
    return render(request, 'guest_book/base.html')

def reg_view(request):
    errors = []
    
    if request.method == 'GET':
        return render(request,'guest_book/base_register.html')
    elif request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
    if login == '':
        return HttpResponse("введите ваше имя")
    else:
        if password == '':
                return HttpResponse("введите ваш пароль")
    if errors == None:
         return render(request,'guest_book/base_register.html',
                                    {'errors':errors,'login':login,'password':password})
    else: 
        User(login=login, password=password).save()        
        return render(request,'guest_book/success_login.html') 
    

def login_view(request):

    if request.method == 'GET':
        return render(request, 'guest_book/login.html')         
    elif request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        if login == '':
            return render(request, 'guest_book/log.html')
        user = User.objects.get(login=request.POST['login'])
        if user.password == request.POST['password']:
            request.session['user_id'] = user.id
            return render(request, 'guest_book/success_login.html')
        else:
             return render(request,'guest_book/log.html') 
    
def if_user_autorized(request):
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            return HttpResponse('Да есть куки')
        else:
            return HttpResponse('Please enable cookies and try again.') 
    request.session.set_test_cookie()
    return render(request, 'guest_book/login.html')
         

def contact_view(request):
    errors = []
    
    if request.method == 'GET':
        return render(request,'guest_book/contact.html')
        
    elif request.method == 'POST':
        subject = request.POST.get('subject')   
        message = request.POST.get('message')
       
    if errors == None:
        return render(request, 'guest_book/contact.html',
                          {'errors':errors, 'subject':subject, 'message':message})                       
    else:  
        ContactForm(subject=subject, message=message).save()
        return render(request,'guest_book/success_login.html', {'subject':subject, 'message':message})
                
def cont_view(request): 
    errors = []
    
    if request.method == 'POST':
        subject = request.POST.get('subject')   
        message = request.POST.get('message')
        
    if errors == None:
        return render(request, 'guest_book/contact.html',
                          {'errors':errors, 'subject':subject, 'message':message}) 
    else:  
        cont = ContactForm.objects.values_list('id', 'message', 'subject')
        return render(request, 'guest_book/str1.html', {'cont':cont})  
        
def regulat_view(request):
    return render(request, 'guest_book/regulations.html')
        
        
        
        
        



