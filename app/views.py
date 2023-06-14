# все функции, для основной логики сайта

import urllib

from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from app.forms import RegistrationForm, LoginForm, ReviewForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Article, Section, Product, Order, OrderProductRelation, Review, ReviewProductRelation


def main_view(request): # функция для главной страницы
    template = 'app/index.html' # шаблон для главной страницы
    articles_data = Article.objects.all().order_by('-date_created').prefetch_related('products') # берем все обьекты таблицы Article (статей) и сортируем по дате создания
    articles = []
    for article in articles_data: # проходимся по всем статьям (Не знаете что одеть летом?, Добро пожаловать на сайт просто магазина)
        products = []
        for product in article.products.all(): # проходим по товаром из статьи (iPhone 7 Pixel 2 Nexus 5x Фуфайка)
            products.append({'id': product.id, 'name': product.name, 'image': product.image, 'category': product.section.slug, 'slug': product.slug}) # делаем список из всех товаров у статьи
        articles.append({'name': article.name, 'text': article.text, 'products': products}) # список статей, где у каждой статьи товары со всей информацией
    context = { # передаем список статей, где у каждой статьи товары со всей информацией
        'articles': articles,
    }
    return render(request, template, context)


def signup_view(request): # функция регистрации
    template = 'app/signup.html' # шаблон для регистрации
    msg = None
    if request.method == 'POST': # если послываем данные на сервер
        form = RegistrationForm(request.POST) # используем форму для регистрации
        if form.is_valid(): # проверяет данные формы и возвращает True, если данные корректны
            first_name = form.cleaned_data['first_name'] # правильно обрабатывает введенные в поле данные
            email = form.cleaned_data['username']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            User.objects.create_user(first_name=first_name, username=username, email=email, password=password) # создать пользователя и добавить в таблицу
            user = authenticate(username=username, password=password) # проверить наборв учетных данных
            login(request, user) # залогиниить пользователя
            return redirect('main') # вернуть на главную страницу
        else: # если форма не валидна
            form = RegistrationForm() # возвращает пустую форму
            msg = 'Пользователь с таким Email уже зарегистрирован либо ваши пароли не совпадают. Повторите попытку' # возвращается сообщение, которое выведтся рядом с формой
    else: # если метод не POST
        form = RegistrationForm() # возвращает пустую форму
    context = {
        'form': form, # возвращает форму
        'msg': msg # возвращает сообщение
    }
    return render(request, template, context) # страница просто перезагружается и возвращает сообщение


def login_view(request): # функция авторизации
    template = 'app/login.html' # шаблон для входа в учетку
    msg = None
    if request.method == 'POST': # если послываем данные на сервер
        form = LoginForm(request.POST) # используем форму для авторизации
        if form.is_valid(): # проверяет данные формы и возвращает True, если данные корректны
            username = form.cleaned_data['username'] # правильно обрабатывает введенные в поле данные
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password) # проверить набор учетных данных
            if user is not None and user.is_active: # если данные пользователя верны и user.is_active = True
                auth.login(request, user) # залогиниить пользователя
                return redirect('main') # вернуться на главную страницу
            else: # если данные пользователя не верны
                form = LoginForm() # возвращается пустая форма
                msg = 'Данные для входа введены неправильно' # возвращается сообщение, которое выведтся рядом с формой
    else: # если метод не POST
        form = LoginForm() # то возвращается пустая форма

    context = {
        'form': form, # возвращает форму
        'msg': msg # возвращает сообщение
    }
    return render(request, template, context) # страница просто перезагружается и возвращает сообщение


def logout_view(request): # функция выхода пользователя из учетки
    auth.logout(request) # отмена авторизации пользователя
    return redirect('main') # переводит на главную страницу, main из urls.py, атрибут name


def show_section_view(request, section): # показ какого либо раздела и пагинация
    template = 'app/section.html' # шаблон для страницы телефонов
    page_num = int(request.GET.get('page', 1)) # пагинатор
    prev_page_url = None # пагинатор
    next_page_url = None # пагинатор
    pages = [] # пагинатор

    try:
        section = Section.objects.get(slug=section) # получить раздел
        products = list(Product.objects.filter(section=section)) # получить товары у раздела
        if len(products) > 0: # если товары в разделе есть
            is_empty = False
            count = 6
            paginator = Paginator(products, count) # пагинатор
            for p in list(paginator.page_range): # пагинатор
                pages.append({'link': '?' + urllib.parse.urlencode({'page': p}), 'number': p}) # пагинатор
            page_num = int(request.GET.get('page', 3)) # пагинатор
            page = paginator.get_page(page_num) # пагинатор
            product_list = page.object_list # пагинатор
            if page.has_next(): # если есть следующая страница
                params = urllib.parse.urlencode({'page': page_num + 1}) # пагинатор
                next_page_url = '?' + params # пагинатор
            else: # если есть нет следующей страницы
                next_page_url = None
            if page.has_previous(): # если есть предыдущая страница страница
                params = urllib.parse.urlencode({'page': page_num - 1})
                prev_page_url = '?' + params
            else: # если нет предыдущей страницы
                prev_page_url = None
        else: # если товаров в разделе нет
            product_list = None
            is_empty = True
    except ObjectDoesNotExist: # если обьектов нет
        product_list = None
        is_empty = False

    context = {
        'section': section, # раздел
        'product_list': product_list,
        'is_empty': is_empty, # пустая?
        'current_page': page_num,
        'prev_page_url': prev_page_url, # предыдущая страница
        'next_page_url': next_page_url, # следующая страница
        'pages': pages # страницы
    }
    return render(request, template, context)


def show_product_view(request, section_slug, product_slug): # показ информации и отзывы о товаре
    template = 'app/product.html' # шаблон информации о товаре
    try:
        section = Section.objects.get(slug=section_slug) # получение раздела
        product_data = Product.objects.prefetch_related('reviews').get(section=section, slug=product_slug) # получение товаров раздела

        if request.method == 'POST': # если метод POST
            form = ReviewForm(request.POST) # берем форму отзывов у конкретного товара
            if form.is_valid(): # проверяет данные формы и возвращает True, если данные корректны
                text = form.cleaned_data['description'] # правильно обрабатывает введенные в поле данные
                rating = form.cleaned_data['mark']
                author = form.cleaned_data['name']
                new_review = Review.objects.create(text=text, rating=rating, author=author, product=product_data) # создать новый отзыв
                ReviewProductRelation.objects.create(product=product_data, review=new_review)
                form = ReviewForm({'name': request.user.first_name}) # поле Имя в форме автоматически заполняется как имя пользователя
        else: # если метод не POST
            form = ReviewForm({'name': request.user.first_name}) # поле Имя в форме автоматически заполняется как имя пользователя
        reviews = product_data.reviews.all().order_by('-id') # получить отзывы о товаре сортируя по id
        context = {
            'product_data': product_data,
            'reviews': reviews,
            'form': form
        }
    except ObjectDoesNotExist: # если обьектов нет
        context = {}

    return render(request, template, context)


def add_to_cart_view(request, product_id): # функция добавления в корзину
    if request.user.is_authenticated: # если пользователь идентифицирован
        this_user = request.user # присвоить пользателя
        try:
            actual_order = Order.objects.get(customer=this_user, complete=False) # получает заказ где "customer = действующий пользователь", а "complete = False"
        except ObjectDoesNotExist: # если не один обьект не был найден
            actual_order = Order.objects.create(customer=this_user, total=0, complete=False) # создать обьект-заказ где "customer = действующий пользователь", "complete = False", "total = 0"
        product = Product.objects.get(id=product_id) # получает товар где id = product_id
        try:
            product_order_relation = OrderProductRelation.objects.get(order=actual_order, product=product) # из промежуточной таблицы заказ - товар, получить заказ где "order=actual_order" и "product=product"
        except ObjectDoesNotExist: # если не один обьект не был найден
            product_order_relation = OrderProductRelation.objects.create(order=actual_order, product=product, amount=0, total=0) # создать обьект где "order=actual_order", "product=product", "amount=0", "total=0"
        product_order_relation.amount += 1 # добавить количество
        product_order_relation.total += product.price * product_order_relation.amount # добавить сумму (цена*кол-во)
        product_order_relation.save() # сохранить обьект
        actual_order.total += product.price # к старому заказу добавляет сумму этого товара
        actual_order.save() # сохранить обьект

    return redirect('cart') # возвращает на страницу корзины


def show_cart_view(request): # функция показа корзины
    template = 'app/cart.html' # шаблон корзины

    if request.user.is_authenticated: # залогинился ли пользователь
        this_user = request.user # получаем пользователя
        try: # попробовать получить обьекты корзины
            actual_order = Order.objects.prefetch_related('products').only('products__name', 'products__description', 'products__price').get(customer=this_user, complete=False) # обьяснения ниже
        except ObjectDoesNotExist: # если не один обьект не был найден
            actual_order = Order.objects.prefetch_related('products').only('products__name', 'products__description', 'products__price').create(customer=this_user, total=0, complete=False) # обьяснения ниже

        if request.method == 'POST': # если метод POST
            actual_order.complete = True # присвоить полю "complete = True"
            actual_order.save() # сохранить обьект
            Order.objects.prefetch_related('products').only('products__name', 'products__description', 'products__price').create(customer=this_user, total=0, complete=False) # обьяснения ниже
            context = {
                'msg': 'Ваш заказ оформлен! В ближайшее время с вами свяжется наш консультант.'
            }

        else: # если метод не POST
            product_order_relation = OrderProductRelation.objects.filter(order=actual_order).select_related('product') # получить заказ, где order = actual_order
            number_of_items = len(product_order_relation) # получить кол-во товаров в заказе
            items = []
            for item in product_order_relation: # проходимся по товарам из заказа
                items.append({'product': item.product, 'amount': item.amount, 'total': item.total}) # добавить в список: Имя продукта, кол-во, стоимость каждого товара
            context = {
                'number_of_items': number_of_items, # кол-во товаров
                'items': items, # товар
                'total': actual_order.total, # стоимость
                'order_id': actual_order.id # id заказа
            }
    else: # если пользователь не залогинился, то ничего
        context = {}
    return render(request, template, context)


def about_view(request): # функция для главной страницы
    template = 'app/about.html' # шаблон для главной страницы
    context = {}
    return render(request, template, context)


def contacts_view(request): # функция для главной страницы
    template = 'app/contacts.html' # шаблон для главной страницы
    context = {}
    return render(request, template, context)


def news_view(request): # функция для главной страницы
    template = 'app/news.html' # шаблон для главной страницы
    context = {}
    return render(request, template, context)


def call_view(request): # функция для главной страницы
    template = 'app/call.html' # шаблон для главной страницы
    context = {}
    return render(request, template, context)

def calldo_view(request): # функция для главной страницы
    template = 'app/calldo.html' # шаблон для главной страницы
    context = {}
    return render(request, template, context)
# prefetch_related() - если используется связь М-М, возвращает QuerySet, который получает данные “за один подход”, избежать нарастающего количества запросов при обращении к связанным объектам
# only() - только поля которой должны выбираться из базы данных
# create() - создать обьект где "customer = действующий пользователь", "complete = False", "total = 0"