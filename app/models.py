# для создания моделей (таблиц) БД и связи между ними

from django.db import models
from django.contrib.auth.models import User # импортируем авторизацию


class Section(models.Model): # таблица Разделов
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.CharField(null=True, blank=True, max_length=80, verbose_name='Название на английском (для ссылки)')

    class Meta: # как будут отображаться в админке
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self): # для красивого вывода
        return self.name


class Product(models.Model): # таблица Товаров
    name = models.CharField(max_length=50, verbose_name='Название')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.PositiveIntegerField(verbose_name='Стоимость')
    slug = models.CharField(max_length=80, verbose_name='Алиас')

    section = models.ForeignKey('Section', on_delete=models.CASCADE, verbose_name='Раздел') # связь один ко многим с таблицой разделов
    reviews = models.ManyToManyField('Review', related_name='Product', verbose_name='Отзывы', through='ReviewProductRelation') # связь многие ко многим с таблицой Отзывов

    class Meta: # как будут отображаться в админке
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self): # для красивого вывода
        return self.name


class Article(models.Model): # таблица Статей
    name = models.CharField(max_length=50, verbose_name='Заголовок')
    text = models.TextField(max_length=250, default='', verbose_name='Текст')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    products = models.ManyToManyField('Product', related_name='Article', verbose_name='Товары') # связь многие ко многим с таблицой Товаров

    class Meta: # как будут отображаться в админке
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self): # для красивого вывода
        return str(self.name)


class Review(models.Model): # таблица Отзывов
    text = models.TextField(verbose_name='Текст')
    rating = models.PositiveIntegerField(verbose_name='Оценка')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар') # связь один ко многим с таблицой Товаров
    author = models.CharField(max_length=50, null=True, blank=True, verbose_name='Автор')

    class Meta: # как будут отображаться в админке
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self): # для красивого вывода
        return str(self.author) + '(' + str(self.product.name) + ')' + ': ' + self.text[:50]


class ReviewProductRelation(models.Model): # промежуточная таблица отзыв - товар
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар') # связь один ко многим с таблицой Товаров
    review = models.ForeignKey('Review', on_delete=models.CASCADE, verbose_name='Отзыв') # связь один ко многим с таблицой Отзывов

    class Meta: # как будут отображаться в админке
        verbose_name = 'Отзыв-Товар'
        verbose_name_plural = 'Отзывы-Товары'

    def __str__(self): # для красивого вывода
        return self.review


class Order(models.Model): # таблица Заказов
    customer = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='Автор') # связь один ко многим с Пользователем
    products = models.ManyToManyField('Product', related_name='Order', verbose_name='Товары', through='OrderProductRelation') # связь многие ко многим с таблицой Товаров
    total = models.PositiveIntegerField(verbose_name='Общая стоимость заказа')
    complete = models.BooleanField(default=False, verbose_name='Завершен')

    class Meta: # как будут отображаться в админке
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderProductRelation(models.Model): # промежуточная таблица заказ - товар
    order = models.ForeignKey('Order', on_delete=models.CASCADE, verbose_name='Заказ') # связь один ко многим с таблицой Заказов
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар') # связь один ко многим с таблицой Товаров
    amount = models.PositiveIntegerField(verbose_name='Количество')
    total = models.PositiveIntegerField(verbose_name='Сумма')

    class Meta: # как будут отображаться в админке
        verbose_name = 'Заказ-Товар'
        verbose_name_plural = 'Заказ-Товар'

    def __str__(self): # для красивого вывода
        return str(self.order) + ' ' + str(self.product.name)
