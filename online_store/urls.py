# файл для настройки урлов
# например чтобы открыть страницу админа: http://localhost:8000/admin/
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls), # переводит на страницу админа
    path('', views.main_view, name='main'), # переводит на главную страницу
    path('login/', views.login_view, name='login'), # переводит на страницу входа в учетку
    path('logout/', views.logout_view, name='logout'), # выходит из учетки пользователя
    path('signup/', views.signup_view, name='signup'), # переводит на регистрацию
    path('add_to_cart/<product_id>/', views.add_to_cart_view, name='add_to_cart'), # добавление товара в корзину
    path('cart/', views.show_cart_view, name='cart'), # переводит в корзину
    path('about/', views.about_view, name='about'), # переводит на страницу информации
    path('contacts/', views.contacts_view, name='contacts'), # переводит на страницу информации
    path('news/', views.news_view, name='news'), # переводит на страницу с новостями
    path('call/', views.call_view, name='call'), # переводит на страницу с новостями
    path('calldo/', views.calldo_view, name='calldo'), # переводит на страницу с новостями
    path('<section>/', views.show_section_view, name='section'), # показ какого - либо раздела и пагинация раздела
    path('<section_slug>/<product_slug>/', views.show_product_view, name='product'), # показ информации и отзывы о товаре
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # подключаем статику
