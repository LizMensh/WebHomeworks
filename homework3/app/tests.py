import string
from datetime import datetime
from django.test import TestCase
from app import models
import random

# Create your tests here.
# ratio = 10000
#
#
# import random
# import string
# from datetime import datetime
#
# from app import models
#
# def random_char(size):
#     return ''.join(random.choice(string.ascii_letters) for x in range(size))
#
# def random_int(size):
#     return (random.random() * size + 1) % size
# def FillUsers():
#     models.User.objects.bulk_create([
#         models.User(
#             username=f'User #{i}',
#             password=random_char(10)
#         ) for i in range(ratio)
#     ])
#
# def FillProfiles():
#     models.Profile.objects.bulk_create([
#         models.Profile(
#             user=models.User.objects.get(i)
#         ) for i in range(ratio)
#     ])
#
# def FillQuestions():
#     models.Question.objects.bulk_create([
#         models.Question(
#             profile=models.Profile.objects.get(random_int(ratio)),
#             title=random_char(10),
#             text=random_char(random.random() * 100),
#             status=models.Question.STATUSES[i % 2],
#             date=datetime.date(random_int(3000), random_int(13), random_int(29)),
#         ) for i in range(10 * ratio)
#     ])
#
# def FillAnswers():
#     models.Answer.objects.bulk_create([
#         models.Answer(
#             profile=models.Profile.objects.get(random_int(ratio)),
#             question=models.Question.objects.get(random_int(10 * ratio)),
#             text=random_char(random.random() * 100),
#             correct=(i % 2)
#         ) for i in range(100 * ratio)
#     ])
#
#
# def FillTags():
#     models.Tag.objects.bulk_create([
#         models.Tag(
#             name=random_char(random_int(10)),
#             question=models.Question.objects.get(random_int(10 * ratio)),
#         ) for i in range(100 * ratio)
#     ])
#
# def FillDB():
#     FillUsers()
#     FillProfiles()
#     FillQuestions()
#     FillAnswers()
#     FillTags()
