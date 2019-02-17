#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from .models import User
from .models import ContactForm
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
    max_age = 365 * 24 * 60 * 60  # one year
    period_life = datetime.timedelta(seconds=max_age) # время хранения куков
    current_time = datetime.datetime.utcnow()   # текущее явремя в секундах
    end_time = current_time + period_life  # дата удаления куков

    # переводим в текстовую строку    
    expires = datetime.datetime.strftime(end_time, "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, 
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
        # ишим такого пользователя
        user_s = User.objects.filter(login=login).all()
        if len(user_s) == 0:
             return render(request, 'guest_book/log.html')                  	
        user = user_s[0]        
        if user.password != password:
            return render(request, 'guest_book/log.html')
                            
        if error != None: # есть ошибки
            return render(request, 
                          'guest_book/login.html', # ВАЖНО login.html
                          {'error':error, 'login': login, 'password': password})            
        else:
            return render(request, 'guest_book/str1.html',
                                    {'login': login}) 
                                               
             # прикрепляем к нашей html странице еще и куки - обычне переменные 
            key = 'user_login'  # ВАЖНО user_login
            value = login
            
            max_age = 365 * 24 * 60 * 60  # пусть наша переменная 'user_login' хранится год (365 дней)
            period_life = datetime.timedelta(seconds=max_age) # время хранения куков
            current_time = datetime.datetime.utcnow()   			# текущее явремя в секундах
            end_time = current_time + period_life 
            
            expires = datetime.datetime.strftime(end_time, "%a, %d-%b-%Y %H:%M:%S GMT")  # "Wdy, DD-Mon-YY HH:MM:SS GMT"
            response.set_cookie(key, value, max_age=max_age,
                                            expires=expires) # дата удаления куков (браузер будет удолять сам) 
                                        
            return response
    else:
        raise KeyError('Критическая ошибка! - Мы от браузера ждем только GET или POST Запросы! ')                      						
        

def contact_view(request):
    errors = []
    
    if request.method == 'GET':
        return render(request,'guest_book/contact.html')
        
    elif request.method == 'POST':
        subject = request.POST.get('subject')   
        message = request.POST.get('message')
        now = datetime.datetime.now()
        html = "It is now %s." % now
        
        key = 'user_login'  # ВАЖНО user_login
        user_login = request.COOKIES.get(key, None)
        max_age = 365 * 24 * 60 * 60  # one year
        period_life = datetime.timedelta(seconds=max_age) # время хранения куков
        current_time = datetime.datetime.utcnow()   # текущее явремя в секундах
        end_time = current_time + period_life  # дата удаления куков

       # переводим в текстовую строку    
        expires = datetime.datetime.strftime(end_time, "%a, %d-%b-%Y %H:%M:%S GMT")
        response.set_cookie(key, value, max_age=max_age, 
                            expires=expires, 
                            domain=settings.SESSION_COOKIE_DOMAIN, 
                            secure=settings.SESSION_COOKIE_SECURE or None)
        
    if user_login == None:
        return HttpResponse('у вас нет куки user_login! - надо логинится :)')
    user = User.objects.filter(login=request.POST['login']) 
    if len(user_s) == 0:
        return HttpResponse('пользователь ' + value + ' не найден в базе')   
    else: 
        ContactForm(subject=subject, message=message).save() 
        
    cont = ContactForm.objects.all()   
        
    user = user[0]
    html = 'добро пожаловать на сайт '  + user.login + '!, ' \
           '<br />т.к. кроме вас никто другой не может увидить данную страницу' \
           '<br /> вот вам ваш пароль: ' + user.password  
    # ну например мы пользоватю показываем его профиль с паролем
    return HttpResponse(html)
  

                                         
def regulat_view(request):
    return render(request, 'guest_book/regulations.html')
 

def cookie_detect_view(request): 
    response = HttpResponse('вижу вот такие куки из браузера:' + str(dict(request.COOKIES))
    ) 
    return response








