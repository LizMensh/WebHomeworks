from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render
from django.views.decorators.http import require_GET
from . import models


base_context = {'base_tags': models.Tag.objects.get_tags(),
                'options': models.OPTIONS}


# Sites


def index(request):
    contact_list = models.Question.objects.get_new_questions()
    for question in contact_list:
        question.answers_count = models.Answer.objects.get_answers_count(question)
        question.tags = models.Tag.objects.get_tags_by_question(question)
        question.like_number = models.LikeQuestion.objects.get_questions_likes(question)

    context = {'page_obj': paginate(contact_list, request)}
    context.update(base_context)
    return render(request, 'index.html', context=context)


def hot_questions(request):
    contact_list = models.Question.objects.get_hot_questions()
    for question in contact_list:
        question.answers_count = models.Answer.objects.get_answers_count(question)
        question.tags = models.Tag.objects.get_tags_by_question(question)
        question.like_number = models.LikeQuestion.objects.get_questions_likes(question)

    context = {'questions': contact_list,
               'page_obj': paginate(contact_list, request)}
    context.update(base_context)

    return render(request, 'hot_questions.html', context=context)


def tag_question(request, tag_id: int):
    contact_list = models.Question.objects.get_tagged_questions(tag_id)
    for question in contact_list:
        question.answers_count = models.Answer.objects.get_answers_count(question)
        question.tags = models.Tag.objects.get_tags_by_question(question)
        question.like_number = models.LikeQuestion.objects.get_questions_likes(question)

    context = {'tag': models.Tag.objects.find_by_id(tag_id),
               'questions': contact_list,
               'page_obj': paginate(contact_list, request)}
    context.update(base_context)

    return render(request, 'tag_questions.html', context=context)


def question(request, question_id: int):
    question_item = models.Question.objects.find_by_id(question_id)
    question_item.tags = models.Tag.objects.get_tags_by_question(question_id)

    answers = models.Answer.objects.get_answers(question_id)
    for answer in answers:
        answer.like_number = models.LikeAnswer.objects.get_answers_likes(answer)

    context = {'question': question_item,
               'answers': answers}
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