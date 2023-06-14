# для настройки отображения админки

from django.contrib import admin
from .models import Section, Product, Article, Review, ReviewProductRelation, Order, OrderProductRelation


# @admin.register(ReviewProductRelation) # добавляем в админку промежуточную таблицу отзыв - товар
# class ReviewProductRelationAdmin(admin.ModelAdmin):
#     pass


class ReviewProductRelationInline(admin.TabularInline): # обьяснение ниже
    model = ReviewProductRelation
    extra = 0


@admin.register(Section) # добавляем в админку Разделы
class SectionAdmin(admin.ModelAdmin):
    pass


@admin.register(Product) # добавляем в админку Товары
class ProductAdmin(admin.ModelAdmin):
    inlines = [ReviewProductRelationInline]


@admin.register(Article) # добавляем в админку Статьи
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(Review) # добавляем в админку Отзывы
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderProductRelation) # добавляем в админку промежуточную таблицу заказ - товар
class OrderProductRelationAdmin(admin.ModelAdmin):
    pass


class OrderProductRelationInline(admin.TabularInline): # обьяснение ниже
    model = OrderProductRelation
    extra = 0


@admin.register(Order) # обьяснение ниже
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductRelationInline]


# Интерфейс администратора позволяет редактировать связанные объекты на одной странице с родительским объектом. Это называется “inlines”. Например, у нас есть две модели:
#
# class Author(models.Model):
#    name = models.CharField(max_length=100)
#
# class Book(models.Model):
#    author = models.ForeignKey(Author)
#    title = models.CharField(max_length=100)

# Вы можете редактировать книги автора на странице редактирования автора. Вы добавляете “inlines” к модели добавив их в ModelAdmin.inlines:
#
# class BookInline(admin.TabularInline):
#     model = Book
#
# class AuthorAdmin(admin.ModelAdmin):
#     inlines = [
#         BookInline,
#     ]