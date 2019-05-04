#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib import auth
from .models import User
from .models import ContactForm
from .models import Session
import datetime
import sqlite3
from datetime import timedelta



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
        return render(request,'guest_book/str1.html')  
  
def set_cookie(response, key, value, days_expire = 7):
    key = 'user_login'
    value = ''
 
    max_age = 365 * 24 * 60 * 60  
    period_life = datetime.timedelta(seconds=max_age) 
    current_time = datetime.datetime.utcnow()  
    end_time = current_time + period_life 
    
    expires = datetime.datetime.strftime(end_time, "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(
      key, value, 
      max_age=max_age, 
      expires=expires, 
      domain=settings.SESSION_COOKIE_DOMAIN, 
      secure=settings.SESSION_COOKIE_SECURE or None)

def login_view(request):
    error = ''

    if request.method == 'GET':
        return render(request, 'guest_book/login.html') 
                
    elif request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        
        error = None
        user_s = User.objects.filter(login=login).all()
        if len(user_s) == 0:
            return HttpResponse("Неверный логин/пароль")
            
        user = user_s[0]
        if user.password != password:
              return HttpResponse("Неверный логин/пароль")
          	
        if error != None: # есть ошибки
            return render(request, 'guest_book/login.html',
                                  {'error':error, 'login': login, 'password': password})                          
        else:
            response = render(request, 'guest_book/str1.html')
                                            
            key = 'user_login'                        
            value = login
            
            max_age = 365 * 24 * 60 * 60  
            period_life = datetime.timedelta(seconds=max_age) 
            current_time = datetime.datetime.utcnow()   			
            end_time = current_time + period_life  						           
            expires = datetime.datetime.strftime(end_time, "%a, %d-%b-%Y %H:%M:%S GMT") 
            response.set_cookie(key, value, max_age=max_age,
                                expires=expires)
            return response    
    else:
        return render(request,'guest_book/login.html')  
#---------------------------------------------------------------------------------------------

def login_verification(request):

    if request.method != 'GET': 
        return render(request, 'guest_book/log_verific.html') 
                   
    key = 'user_login'
    login = request.COOKIES.get(key, None)
    
    if login == None:
        return render(request, 'guest_book/log_verific.html')
    
    user_s = User.objects.filter(login=login).all()
    if len(user_s) == 0:
        return HttpResponse('пользователь ' + value + ' не найден в базе')
    
    user = user_s[0]
    html = 'добро пожаловать на сайт '  + user.login + '!, ' \
           '<br />т.к. кроме вас никто другой не может увидить данную страницу' \
           '<br /> вот вам ваш пароль: ' + user.password  
   
    return render(request, 'guest_book/contact.html',{'html':html})
    
    
def contact_view(request):
    errors = []
        
    if request.method == 'GET':
        return render(request,'guest_book/contact.html') 
 
    key = 'user_login'
    login = request.COOKIES.get(key, None)
    
    if login == None:
        return render(request, 'guest_book/log_verific.html')
    
    user_s = User.objects.filter(login=login).all()

    if len(user_s) == 0:
        return HttpResponse('пользователь ' + value + ' не найден в базе')

    elif request.method == 'POST':
        subject = request.POST.get('subject')   
        message = request.POST.get('message')
        now = datetime.datetime.now()
        html = "It is now %s." % now
        
    if errors == None:
        return render(request, 'guest_book/contact.html',
                          {'errors':errors, 'subject':subject, 'message':message})    
    else: 
        ContactForm(subject=subject, message=message).save() 
        
    cont = ContactForm.objects.all() 

    user = user_s[0]
    html = 'добро пожаловать на сайт '  + user.login + '!, ' \
           '<br />т.к. кроме вас никто другой не может увидить данную страницу' \
           '<br /> вот вам ваш пароль: ' + user.password 
                                     
   
    return render(request, 'guest_book/str1.html', context=
                                        {'cont':cont, 'html':html}) 
                             
                                                                                     
def regulat_view(request):
    return render(request, 'guest_book/regulations.html')
#------------------------------------------------------------------------------------             

         
        
   
        
        
        
        
        
        
        
         




















         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         


 





