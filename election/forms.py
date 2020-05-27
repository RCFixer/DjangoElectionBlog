from django import forms
from django.forms import formset_factory, modelformset_factory

from .models import Survey, Option

class SurveyForm(forms.Form):
    title = forms.CharField(
        label='Название голосования',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название голосования'
        })
    )

class SurveyModelForm(forms.ModelForm):

    class Meta:
        model = Survey
        fields = ('title', 'posts')
        labels = {
            'title': 'Название голосования'
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок голосования'
                }
            ),
            'posts': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


SurveyFormset = formset_factory(SurveyForm)
SurveyModelFormset = modelformset_factory(
    Survey,
    fields=('title', 'posts'),
    extra=1,
    widgets={
        'title': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите заголовок голосования'
            }
        ),
        'posts': forms.SelectMultiple(attrs={'class': 'form-control'}),
    }
)

OptionFormset = modelformset_factory(
    Option,
    fields=('title', ),
    extra=1,
    widgets={'title': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите вариант ответа',
            'required': 'True',
        })
    }
)