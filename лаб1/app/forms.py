# -*- coding: utf-8 -*-
"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Comment, Blog  # Добавлен импорт модели Comment


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class AnketaForm(forms.Form):
    name = forms.CharField(
        label='Ваше имя',
        min_length=2,
        max_length=100
    )
    city = forms.CharField(
        label='Ваш город',
        min_length=2,
        max_length=100
    )
    job = forms.CharField(
        label='Ваш род занятий',
        min_length=2,
        max_length=100
    )
    gender = forms.ChoiceField(
        label='Ваш пол',
        choices=[('1', 'Мужской'), ('2', 'Женский')],
        widget=forms.RadioSelect,
        initial='1'
    )
    internet = forms.ChoiceField(
        label='Вы пользуетесь интернетом?',
        choices=[
            ('1', 'Каждый день'),
            ('2', 'Несколько раз в день'),
            ('3', 'Несколько раз в неделю'),
            ('4', 'Несколько раз в месяц')
        ],
        initial='1'
    )
    notice = forms.BooleanField(
        label='Получать новости сайта на e-mail?',
        required=False
    )
    email = forms.EmailField(
        label='Ваш e-mail',
        min_length=7
    )
    message = forms.CharField(
        label='Коротко о себе',
        widget=forms.Textarea(attrs={'rows': 12, 'cols': 20})
    )

class CustomRegisterForm(UserCreationForm):
    """Форма регистрации пользователя с дополнительными настройками"""
    username = forms.CharField(
        label="Имя пользователя",
        max_length=150,
        validators=[
            RegexValidator(
                regex='^[\w.@+-]+$',
                message='Только буквы, цифры и символы @/./+/-/_'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_"
    )
    
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="""
        <ul class="text-muted" style="padding-left: 15px; margin-top: 5px;">
            <li>Ваш пароль не должен совпадать с вашим именем или другой персональной информацией</li>
            <li>Ваш пароль должен содержать как минимум 6 символов</li>
            <li>Ваш пароль не может быть одним из широко распространённых паролей</li>
            <li>Ваш пароль не может состоять только из цифр</li>
        </ul>
        """
    )
    
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Для подтверждения введите, пожалуйста, пароль ещё раз"
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется")
        return email

class CommentForm(forms.ModelForm):
    """Форма для добавления комментариев"""
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': 'Комментарий'}
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Оставьте ваш комментарий здесь...'
            })
        }

class BlogForm(forms.ModelForm):
    """Форма для создания/редактирования статей блога"""
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image')
        labels = {
            'title': 'Заголовок статьи',
            'description': 'Краткое содержание',
            'content': 'Полный текст статьи',
            'image': 'Изображение'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок статьи'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Краткое описание статьи (до 300 символов)'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 12,
                'placeholder': 'Полное содержание статьи'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            })
        }
        help_texts = {
            'image': 'Рекомендуемый размер изображения: 1200x800px',
        }