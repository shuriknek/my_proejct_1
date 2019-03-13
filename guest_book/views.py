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
            return HttpResponse("пользователь не найден")
            
        user = user_s[0]
        if user.password != password:
              return HttpResponse("пароль не найден")
          	
        if error != None: # есть ошибки
            return render(request, 'guest_book/login.html', # ВАЖНО login.html
                                  {'error':error, 'login': login, 'password': password})           
        else: 
            response = render(request, 'guest_book/str1.html',
                                           {'login': login}) 
            # response уже содержит html страницу
            key = 'user_login'  # ВАЖНО user_login
            value = login
            #           d    h    m    s
            max_age = 365 * 24 * 60 * 60  # пусть наша переменная 'user_login' хранится год (365 дней)
            period_life = datetime.timedelta(seconds=max_age) # время хранения куков
            current_time = datetime.datetime.utcnow()   			# текущее явремя в секундах
            end_time = current_time + period_life  						# дата удаления куков (браузер будет удолять сам)

            # переводим в текстовую строку
            expires = datetime.datetime.strftime(end_time, "%a, %d-%b-%Y %H:%M:%S GMT")  # "Wdy, DD-Mon-YY HH:MM:SS GMT"
            response.set_cookie(key, value, 
                                max_age=max_age,
                                expires=expires)
            # max_age количество секунд или None (по-умолчанию), если cookie должна существовать до закрытия браузера. 
            # expires должен быть строкой в формате "Wdy, DD-Mon-YY HH:MM:SS GMT" или объект datetime.datetime в UTC.
            
            # возвращаем html страницу пользователю
            return response
    else:
        return render(request,'guest_book/login.html')  
           

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
                            expires=expires, HttpOnly = True,
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
 
def set_cookie(response, key, value, days_expire = 7): 
    if days_expire is None: 
        max_age = 365 * 24 * 60 * 60 #one year 
    else: 
        max_age = days_expire = 24 * 60 * 60
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT") 
        response.set_cookie(key, value, max_age=max_age,
                               expires=expires)
                              

def cookie_set_view (request): 
    response = HttpResponse("hello") 
    response.set_cookie('my_cookie_var','123')
    response.set_cookie('website_text', 'zdes bil site na django')   
    return response

def cookie_detect_view(request): 
    response = HttpResponse('вижу вот такие куки из браузера:' + str(dict(request.COOKIES))
    ) 
    return response



 

