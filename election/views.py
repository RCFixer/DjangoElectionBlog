from django.shortcuts import render, redirect, reverse
from django.views import generic
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator

from .forms import SurveyModelForm, OptionFormset
from .models import Survey, Option


class AccessByGroup(UserPassesTestMixin):

    def test_func(self):
        user = self.request.user
        if user.groups.filter(name='Moderator').count() or user.is_staff:
            return True
        return False


class SurveyResult(AccessByGroup, LoginRequiredMixin, View):

    def get(self, request, id):
        survey = Survey.objects.get(id=id)
        return render(request, 'election/result_survey.html', context={'survey': survey})


class SurveyList(AccessByGroup, LoginRequiredMixin, View):

    def get(self, request):
        surveys = Survey.objects.all()
        paginator = Paginator(surveys, 10)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()

        if page.has_previous():
            prev_url = '?page={}'.format(page.previous_page_number())
        else:
            prev_url = ''

        if page.has_next():
            next_url = '?page={}'.format(page.next_page_number())
        else:
            next_url = ''

        context = {
            'page_object': page,
            'is_paginated': is_paginated,
            'next_url': next_url,
            'prev_url': prev_url,
        }
        return render(request, 'election/index.html', context=context)


class SurveyDelete(AccessByGroup, LoginRequiredMixin, View):

    def get(self, request, id):
        survey = Survey.objects.get(id=id)
        survey.delete()
        return redirect('surveys_list_url')

class SurveyCreate(AccessByGroup, LoginRequiredMixin, View):
    template = 'election/create_survey.html'
    raise_exception = True

    def get(self, request):
        survey_form = SurveyModelForm
        formset = OptionFormset(queryset=Option.objects.none())
        return render(request, self.template, context = {
            'survey_form': survey_form,
            'formset': formset,
        })
    
    def post(self, request):
        survey_form = SurveyModelForm(request.POST)
        formset = OptionFormset(request.POST)
        if formset.is_valid() and survey_form.is_valid():
            survey = survey_form.save()
            for form in formset:
                option = form.save(commit=False)
                option.survey = survey
                option.save()
            return redirect('surveys_list_url')
        return render(request, self.template, {
            'survey_form': survey_form,
            'formset': formset,
        })


class SurveyAdd(AccessByGroup, LoginRequiredMixin, View):
    template = 'election/add_to_survey.html'
    raise_exception = True

    def get(self, request, id):
        survey = Survey.objects.get(id=id)
        formset = OptionFormset(queryset=Option.objects.none())
        return render(request, self.template, context = {
            'survey': survey,
            'formset': formset,
        })
    
    def post(self, request, id):
        survey = Survey.objects.get(id=id)
        formset = OptionFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                option = form.save(commit=False)
                option.survey = survey
                option.save()
            return redirect('surveys_list_url')
        return render(request, self.template, {
            'survey_form': survey_form,
            'formset': formset,
        })


class SurveyUpdate(AccessByGroup, LoginRequiredMixin, View):
    template = 'election/update_survey.html'
    raise_exception = True

    def get(self, request, id):
        survey = Survey.objects.get(id=id)
        survey_form = SurveyModelForm(instance=survey)
        return render(request, self.template, context = {
            'survey': survey,
            'survey_form': survey_form,
        })
    
    def post(self, request, id):
        if 'update' in request.POST:
            survey = Survey.objects.get(id=id)
            survey_form = SurveyModelForm(request.POST, instance=survey)
            if survey_form.is_valid():
                survey_form.save()
            options = survey.options.all()
            new_options = request.POST.getlist('option-title')
            counter = 0
            for option in options:
                option.title = new_options[counter]
                option.save()
                counter += 1
            return redirect('surveys_list_url')
        else:
            for key, value in request.POST.items():
                if value == '-':
                    option = Option.objects.get(id=int(key))
                    option.delete()
            return redirect(reverse('survey_update_url', kwargs={'id': id}))