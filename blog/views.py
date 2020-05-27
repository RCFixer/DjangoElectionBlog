from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .models import Post
from .forms import PostForm, SurveyForm
from election.models import Survey, Option
from election.views import AccessByGroup


def posts_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
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
    return render(request, 'blog/index.html', context=context)


class PostResult(View):

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        if post.surveys.all():
            return render(request, 'blog/post_result.html', context={'post': post})
        return redirect(reverse('posts_list_url'))

class PostDetail(View):
    template = 'blog/post_detail.html'

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        return render(request, self.template, context={'post': post})

    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        surveys = post.surveys.all()
        for survey in surveys:
            option_id = int(request.POST.get(survey.title))
            option = Option.objects.get(id=option_id)
            option.count += 1
            option.save()
        return redirect(reverse('post_result_url', kwargs={'id': id}))


class PostCreate(AccessByGroup, LoginRequiredMixin, View):
    template = 'blog/post_create_form.html'

    def get(self, request):
        form = PostForm
        survey_form = SurveyForm()
        return render(request, self.template, context={'form': form, 'survey_form': survey_form})

    def post(self, request):
        bound_form = PostForm(request.POST)
        if bound_form.is_valid():
            new_post = bound_form.save()
            survey_form = request.POST.getlist('surveys')
            for survey_id in survey_form:
                new_post.surveys.add(Survey.objects.get(id=int(survey_id)))
            return redirect(new_post)
        return render(request, self.template, context={'form': bound_form})


class PostUpdate(AccessByGroup, LoginRequiredMixin, View):
    template = 'blog/post_update_form.html'

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        bound_form = PostForm(instance=post)
        survey_form = SurveyForm(initial={'surveys':post.surveys.all})
        context={'form': bound_form, 'post': post, 'survey_form': survey_form}
        return render(request, self.template, context=context)

    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        bound_form = PostForm(request.POST, instance=post)
        survey_form = request.POST.getlist('surveys')
        post.surveys.clear()
        for survey_id in survey_form:
            post.surveys.add(Survey.objects.get(id=int(survey_id)))
        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect(new_post)
        return render(request, self.template, context={'form': bound_form, 'post': post})


class PostDelete(AccessByGroup, LoginRequiredMixin, View):
    template = 'blog/post_delete_form.html'

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        return render(request, self.template, context={'post': post})

    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        post.delete()
        return redirect(reverse('posts_list_url'))