from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest, Http404
from django.shortcuts import render
from . import models

base_context = {'base_tags': models.TAGS, 'options': models.OPTIONS}


def index(request):
    contact_list = models.QUESTIONS
    context = {'questions': models.QUESTIONS, 'page_obj': paginate(contact_list, request)}
    context.update(base_context)
    return render(request, 'index.html', context=context)


def hot_questions(request):
    contact_list = models.QUESTIONS
    context = {'questions': models.QUESTIONS, 'page_obj': paginate(contact_list, request)}
    context.update(base_context)
    return render(request, 'hot_questions.html', context=context)


def tag_question(request, tag: str):
    contact_list = models.QUESTIONS[int(tag[-1])-1::]
    context = {'tag': tag, 'questions': contact_list, 'page_obj': paginate(contact_list, request)}
    context.update(base_context)
    return render(request, 'tag_question.html', context=context)


def question(request, question_id: int):
    question_item = models.QUESTIONS[question_id-1]
    context = {'question': question_item}
    context.update(base_context)
    return render(request, 'question.html', context=context)


def ask(request):
    context = {}
    context.update(base_context)
    return render(request, 'ask.html', context=context)


def login(request):
    context = {}
    context.update(base_context)
    return render(request, 'login.html', context=context)


def signup(request):
    context = {}
    context.update(base_context)
    return render(request, 'signup.html', context=context)


def settings(request):
    context = {}
    context.update(base_context)
    return render(request, 'settings.html', context=context)


def paginate(object_list, request, per_page=3):
    paginator = Paginator(object_list, per_page)
    page_number = request.GET.get('page', 1)
    try:
        page = int(page_number)
        if page <= 0 or page > paginator.num_pages:
            raise Http404
    except ValueError:
        return HttpResponseBadRequest()

    return paginator.get_page(page_number)

