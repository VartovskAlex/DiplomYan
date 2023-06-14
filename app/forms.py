# для создания форм у авторизации, регистрации и отзывах

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext, ugettext_lazy as _


class RegistrationForm(UserCreationForm): # форма для регистрации
    error_messages = { # выводит уведомление что пароли при регистрации совпадают
        'password_mismatch': _("Пароли не совпадают."),
    }
    first_name = forms.CharField(max_length=100, # поле Имя, максимальная длина поля 100
                                 label=_("Имя пользователя:"), # не обязательно
                                 widget=forms.TextInput( # виджеты формы, обрабатывает отрисовку HTML, чтобы каждое поле формы различалось от других
                                     attrs={'id': 'inputUsername',
                                            'class': 'form-control first-field', # как выглядит форма
                                            'placeholder': 'Имя', # отображается на страничке
                                            'value': '', # значение по умолчание
                                            'required': '',
                                            'autofocus': '',
                                            'data-cip-id': 'inputUsername'})
                                 )
    username = forms.EmailField(max_length=254, # поле Email
                                label=_("E-mail пользователя:"), # не обязательно
                                widget=forms.EmailInput( # виджеты формы, обрабатывает отрисовку HTML, чтобы каждое поле формы различалось от других
                                    attrs={'class': 'form-control', # как выглядит форма
                                           'placeholder': 'Email', # отображается на страничке
                                           'value': '', # значение по умолчание
                                           'required': '',
                                           'data-cip-id': 'inputEmail'})
                                )
    password1 = forms.CharField(label=_("Придумайте пароль:"), # поле пароля
                                widget=forms.PasswordInput( # виджеты формы, обрабатывает отрисовку HTML, чтобы каждое поле формы различалось от других
                                    attrs={'class': 'form-control', # как выглядит форма
                                           'placeholder': 'Пароль', # отображается на страничке
                                           'required': '',
                                           'data-cip-id': 'inputPassword1'})
                                )
    password2 = forms.CharField(label=_("Подтвердите пароль:"), # поле подтверждения пароля, label не обязательно
                                widget=forms.PasswordInput( # виджеты формы, обрабатывает отрисовку HTML, чтобы каждое поле формы различалось от других
                                    attrs={'class': 'form-control last-field', # как выглядит форма
                                           'placeholder': 'Повторите пароль', # отображается на страничке
                                           'required': '',
                                           'data-cip-id': 'repeatPassword2'}),
                                help_text=_("Введите тот же пароль, что и ранее.")) # описание для поля
    field_order = ['first_name', 'username', 'password1', 'password2']


class LoginForm(forms.Form): # форма для авторизации
    username = forms.EmailField(max_length=254, # поле Email
                                label=_("E-mail пользователя:"), # не обязательно
                                widget=forms.EmailInput( # виджеты формы, обрабатывает отрисовку HTML, чтобы каждое поле формы различалось от других
                                    attrs={'class': 'form-control first-field', # как выглядит форма
                                           'placeholder': 'Email', # отображается на страничке
                                           'value': '', # значение по умолчание
                                           'required': '',
                                           'autofocus': '',
                                           'data-cip-id': 'inputEmail'})
                                )
    password = forms.CharField(label=_("Пароль:"), # поле пароля
                               widget=forms.PasswordInput( # виджеты формы, обрабатывает отрисовку HTML, чтобы каждое поле формы различалось от других
                                   attrs={'class': 'form-control last-field', # как выглядит форма
                                          'placeholder': 'Пароль', # отображается на страничке
                                          'required': '',
                                          'data-cip-id': 'inputPassword1'})
                               )
    field_order = ['username', 'password']


CHOICES=[('1', '★'), # строковое поле, предназначенное для выбора конкретного варианта из списка доступных вариантов.
         ('2', '★★'),
         ('3', '★★★'),
         ('4', '★★★★'),
         ('5', '★★★★★')]


class ReviewForm(forms.Form): # форма отзывов у конкретного товара
    name = forms.CharField(label=_("Имя:"), # поле Имя автора
                           widget=forms.TextInput( # виджеты формы, обрабатывает отрисовку HTML, чтобы каждое поле формы различалось от других
                               attrs={'class': 'form-control', # как выглядит форма
                                      'aria-describedby': 'nameHelp',
                                      'placeholder': 'Представьтесь', # отображается на страничке
                                      'required': '',
                                      'data-cip-id': 'name'}),
                           )
    description = forms.CharField(label=_("Содержание"), # поле Содержание
                                  widget=forms.Textarea( # виджеты формы, обрабатывает отрисовку HTML, чтобы каждое поле формы различалось от других
                                      attrs={'class': 'form-control', # как выглядит форма
                                             'placeholder': 'Содержание', # отображается на страничке
                                             'required': '',
                                             'rows': '',
                                             'cols': ''}),
                                  )
    mark = forms.ChoiceField(choices=CHOICES, # поле Оценка, надо выбирать вариант из CHOICES
                             widget=forms.RadioSelect( # виджеты формы, обрабатывает отрисовку HTML, чтобы каждое поле формы различалось от других
                                 attrs={'class': 'form-check-input'}) # как выглядит форма
                             )
