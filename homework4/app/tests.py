import string
from datetime import date
from django.test import TestCase
from app import models
import random

# Create your tests here.
ratio = 200

import random
import string
from datetime import datetime

from app import models


def random_char(size):
    return ''.join(random.choice(string.ascii_letters) for x in range(size))


def random_int(size):
    return int((random.random() * size)) % size + 1


def FillUsers():
    for i in range(ratio + 1):
        models.User.objects.create_user(username=f'User #{i}', password=random_char(10))


def FillProfiles():
    users = models.User.objects.all()
    models.Profile.objects.bulk_create([
        models.Profile(
            user=users[i],
            nickname=random_char(20)
        ) for i in range(users.count())
    ])


def FillQuestions():
    profiles = models.Profile.objects.all()
    models.Question.objects.bulk_create([
        models.Question(
            profile=profiles[random_int(profiles.count())],
            title=random_char(10),
            text=random_char(random_int(200)),
            status=models.Question.STATUSES[i % 2],
            date=date.today(),
        ) for i in range(10 * profiles.count())
    ])


def FillAnswers():
    profiles = models.Profile.objects.all()
    questions = models.Question.objects.all()
    models.Answer.objects.bulk_create([
        models.Answer(
            profile=profiles[random_int(profiles.count())],
            question=questions[random_int(10 * profiles.count())],
            text=random_char(random_int(100)),
            correct=(i % 2)
        ) for i in range(100 * profiles.count())
    ])


def FillTags():
    users = models.User.objects.all()
    models.Tag.objects.bulk_create([
        models.Tag(
            name=random_char(random_int(10))
        ) for i in range(users.count())
    ])

    questions = models.Question.objects.all()

    for tag in models.Tag.objects.all():
        tag.question.set([
            questions[random_int(questions.count())] for i in range(10)
        ])


def FillDB():
    FillUsers()
    FillProfiles()
    FillQuestions()
    FillAnswers()
    FillTags()
