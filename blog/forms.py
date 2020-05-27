from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Post
from election.models import Survey

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body']
        labels = {
            'title': _('Заголовок'),
            'body': _('Текст'),
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }


class SurveyForm(forms.Form):
    surveys = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
                                            queryset=Survey.objects.all(),
                                            label='Голосования',
                                            required=False,)

    #class Meta:
    #    widgets = {
    #        'surveys': forms.SelectMultiple(attrs={'class': 'form-control'}),
    #    }