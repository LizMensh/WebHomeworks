from django.contrib import auth
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse, path
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes

from . import models
from . import forms
from .modelSerializers import QuestionSerializer, ProfileSerializer, AnswerSerializer
from .tests import FillDB

base_context = {'base_tags': models.Tag.objects.get_tags(),
                'current_user': models.CurrentUser}


# Sites

def index(request):
    # FillDB()
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


def tag_question(request, tag_name: str):
    tag = models.Tag.objects.find_by_name(tag_name)
    contact_list = models.Question.objects.get_questions_by_tag(tag)

    for question in contact_list:
        question.answers_count = models.Answer.objects.get_answers_count(question)
        question.tags = models.Tag.objects.get_tags_by_question(question)
        question.like_number = models.LikeQuestion.objects.get_questions_likes(question)

    context = {'tag': tag.name,
               'questions': contact_list,
               'page_obj': paginate(contact_list, request)}
    context.update(base_context)

    return render(request, 'tag_questions.html', context=context)


def question(request, question_id: int):
    context = {}

    if request.method == "POST":
        if not models.CurrentUser.is_auth:
            return redirect(reverse("login"))

        form = forms.QuestionForm(request.POST)
        if form.is_valid():
            form.respond(question_id)
            print("respond")
            return redirect(reverse('question', kwargs={'question_id': question_id}))
        context.update({'Invalid': True, 'Exception': form.errors})
        print(form.errors)

    question_item = models.Question.objects.find_by_id(question_id)
    question_item.tags = models.Tag.objects.get_tags_by_question(question_id)

    answers = models.Answer.objects.get_answers(question_id)
    for answer in answers:
        answer.like_number = models.LikeAnswer.objects.get_answers_likes(answer)

    context.update({'question': question_item, 'answers': answers})
    context.update(base_context)

    return render(request, 'question.html', context=context)


def ask(request):
    if not models.CurrentUser.is_auth:
        return redirect(reverse("login"))

    context = {}

    if request.method == "GET":
        form = forms.LoginForm()

    if request.method == "POST":
        form = forms.AskForm(request.POST)
        if form.is_valid():
            id = form.ask()
            return redirect(reverse('question', kwargs={'question_id': id}))
        context.update({'Invalid': True, 'Exception': form.errors})

    context.update(base_context)
    return render(request, 'ask.html', context=context)


def login(request):
    context = {}

    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                models.CurrentUser.profile = models.Profile.objects.find_by_user(user)
                models.CurrentUser.is_auth = True
                return redirect(reverse("index"))
            else:
                form.add_error(None, 'Invalid username or password!')
        context.update({'Invalid': True, 'Exception': form.errors})
        print(form.errors)

    context.update(base_context)
    return render(request, 'login.html', context=context)


def logout(request):
    models.CurrentUser.profile = None
    models.CurrentUser.is_auth = False

    return redirect(reverse("index"))


def signup(request):
    context = {}

    if request.method == "GET":
        form = forms.SignUpForm()

    if request.method == "POST":
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            profile = form.save()
            if profile:
                models.CurrentUser.profile = profile
                models.CurrentUser.is_auth = True
                return redirect(reverse("index"))
            else:
                form.add_error(None, 'Invalid saving error!')
        context.update({'Invalid': True, 'Exception': form.errors})
        print(form.errors)

    context.update(base_context)
    return render(request, 'signup.html', context=context)


def settings(request):
    if not models.CurrentUser.is_auth:
        return redirect(reverse("login"))

    context = {}

    if request.method == "POST":
        form = forms.SettingsForm(request.POST)
        if form.is_valid():
            profile = form.save()
            if profile:
                models.CurrentUser.profile = profile
            else:
                form.add_error(None, 'Invalid saving error!')
        context.update({'Invalid': True, 'Exception': form.errors})
        print(form.errors)

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


@api_view(['GET'])
def questions_get(request, start: int, end: int, status: str):
    if request.method == 'GET':
        questions = models.Question.objects.filter(status__exact=status)[max(start - 1, 0):min(end, models.Question.objects.count())]
        serializer = QuestionSerializer(questions, many=True)
        return Response({"data": serializer.data}, status=200)


@api_view(['GET'])
def answers_get(request, question_id: int):
    if request.method == 'GET':
        answers = models.Answer.objects.get_answers(question_id)
        serializer = AnswerSerializer(answers, many=True)
        return Response({"data": serializer.data}, status=200)


@api_view(['GET'])
def profile_get(request, profile_id: int):
    if request.method == 'GET':
        profile = models.Profile.objects.find_by_id(profile_id)
        serializer = ProfileSerializer(profile)
        data = dict(serializer.data)
        data["user"] = {"username": profile.user.username}
        return Response({"data": data}, status=200)
