from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import MenuCategory, MealType, Allergy


class MultiMealTypeField(forms.MultipleChoiceField):
    def validate(self, value):
        if not any(map(int, value)):
            raise ValidationError('Выберите хотя бы один тип приема пищи!')


class CustomAuthentication(AuthenticationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
            })
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите e-mail'
            }
        )
    )
    name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя (не обязательно)',
                'autofocus': True,
            }
        )
    )
    password1 = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите пароль',
            }
        )
    )
    password2 = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Повторите пароль',
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')


class PersonalInfoProfileForm(forms.ModelForm):

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'readonly': True,
                'class': 'form-control',
            }
        )
    )

    password1 = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                'readonly': True,
                'class': 'form-control',
                'placeholder': '',
            }
        )
    )

    password2 = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                'readonly': True,
                'class': 'form-control',
                'placeholder': 'Повторите пароль',
            }
        )
    )

    avatar = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'link-dark text-decoration-none align-middle',
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ('name', 'email', 'password1', 'password2', 'avatar')


class OrderForm(forms.Form):
    promocode = forms.CharField(
        required=False,
    )
    month_count = forms.IntegerField(
        required=True,
    )
    portion_quantity = forms.IntegerField(
        required=True,
    )
    menu_category = forms.ModelChoiceField(
        queryset=MenuCategory.objects.all(),
        widget=forms.RadioSelect(
            attrs={
                'class': 'foodplan_selected d-none',
            }
        ),
    )
    meal_types_choices = MealType.objects.all().order_by('name').values_list('id', 'name')
    meal_types = MultiMealTypeField(
        choices=meal_types_choices,
    )
    allergies = forms.ModelMultipleChoiceField(
        queryset=Allergy.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )
