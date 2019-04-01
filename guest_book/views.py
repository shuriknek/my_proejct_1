#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from .models import User
from .models import ContactForm
from .models import Session
import datetime
import sqlite3
from datetime import timedelta



def index(request):
    return render(request, 'guest_book/base.html')

def reg_view(request):
    error = []
    
    if request.method == 'GET':
        return render(request,'guest_book/base_register.html')
    elif request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
    error = None
    if login == '':
        return HttpResponse("введите ваше имя")
    else:
        if password == '':
                return HttpResponse("введите ваш пароль")
    if error != None:
         return render(request,'guest_book/base_register.html',
                                    {'errors':errors,'login':login,'password':password})
    else: 
        User(login=login, password=password).save()
        return render(request,'guest_book/str1.html') 
       

def set_cookie(response, key, value, days_expire = 7):
    key = 'user_login'
    value = ''
    #           d    h    m    s
    max_age = 365 * 24 * 60 * 60  # one year
    period_life = datetime.timedelta(seconds=max_age) # время хранения куков
    current_time = datetime.datetime.utcnow()   # текущее явремя в секундах
    end_time = current_time + period_life  # дата удаления куков
    
    # переводим в текстовую строку
    expires = datetime.datetime.strftime(end_time, "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, 
                         expires=expires, httponly=True)
   
def login_view(request):
    error = ''
    
    if request.method == 'GET':
        return render(request, 'guest_book/login.html') 
    
    elif request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
       
        error = None
        # ишим такого пользователя
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
            response = render(request, 'guest_book/str1.html',  # ВАЖНО success_login.html
                                                  {'login': login}) 
            # response уже содержит html страницу
            
            # https://djbook.ru/rel1.9/ref/request-response.html#django.http.HttpResponse.set_cookie
            
            # прикрепляем к нашей html странице еще и куки - обычне переменные 
            key = 'user_login'  # ВАЖНО user_login
            value = login
            #           d    h    m    s
            max_age = 365 * 24 * 60 * 60  # пусть наша переменная 'user_login' хранится год (365 дней)
            period_life = datetime.timedelta(seconds=max_age) # время хранения куков
            current_time = datetime.datetime.utcnow()  # текущее явремя в секундах
            end_time = current_time + period_life  # дата удаления куков (браузер будет удолять сам)

            # переводим в текстовую строку
            expires = datetime.datetime.strftime(end_time, "%a, %d-%b-%Y %H:%M:%S GMT")  # "Wdy, DD-Mon-YY HH:MM:SS GMT"
            response.set_cookie(key, value, 
                                max_age=max_age,
                                expires=expires)
            # max_age количество секунд или None (по-умолчанию), если cookie должна существовать до закрытия браузера. 
            # expires должен быть строкой в формате "Wdy, DD-Mon-YY HH:MM:SS GMT" или объект datetime.datetime в UTC.
            
            # возвращаем html страницу пользователю
            return response

def stop_tracking(request):
    if request.COOKIES.get('user_login'):
        response = HttpResponse("Cookies Cleared")
        response.delete_cookie('user_login')
    else:
        response = HttpResponse("Мы не отслеживаем вас")
    return response

def track_user(request):
    response = render(request, 'guest_book/str1.html')
    if not request.COOKIES.get('user_login'):
        response.set_cookie('user_login', '1', 3600 * 24 * 365 * 2)
    else:
        user_login = int(request.COOKIES.get('user_login', '1')) + 1
        response.set_cookie('user_login', str(user_login), 3600 * 24 * 365 * 2)
    return response


         
def contact_view(request):
    errors = []
    
    if request.method == 'GET':
        return render(request,'guest_book/contact.html')
        
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
    return render(request, 'guest_book/str1.html', context=
                            {'cont':cont, 'html':html}) 
                             
                                                                  
def regulat_view(request):
    return render(request, 'guest_book/regulations.html')
#------------------------------------------------------------------------------------ 

   
   
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         


 





