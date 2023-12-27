from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(blank=True, null=True, upload_to="media")

    def __str__(self):
        return self.user.username

class QuestionManager(models.Manager):
    def get_hot_questions(self):
        return self.filter(status__exact='h')

    def get_new_questions(self):
        return self.order_by('-date')

    def get_tagged_questions(self, tag):
        return self.filter(tag__exact=tag)

    def get_questions(self):
        return self.all()

    def find_by_id(self, id):
        try:
            vote = self.get(pk=id)
        except ObjectDoesNotExist:
            raise Http404
        return vote


class Question(models.Model):
    profile = models.ForeignKey(Profile, models.PROTECT)

    title = models.CharField(max_length=50)
    text = models.TextField()

    tags = None
    answers_count = 0
    like_number = 0

    HOT = 'h'
    NORMAL = 'n'
    STATUSES = [
        (HOT, 'hot'),
        (NORMAL, 'normal')
    ]
    status = models.CharField(max_length=1, choices=STATUSES)
    date = models.DateTimeField(blank=True, null=True)

    objects = QuestionManager()
    def __str__(self):
        return f'{self.title}'


class TagManager(models.Manager):

    def get_tags_by_question(self, question):
        return self.filter(question__exact=question)

    def find_by_id(self, id):
        try:
            vote = self.get(pk=id)
        except ObjectDoesNotExist:
            raise Http404
        return vote
    def get_tags(self):
        return self.all()


class Tag(models.Model):
    name = models.CharField(max_length=30)
    objects = TagManager()

    question = models.ManyToManyField(Question)

    def __str__(self):
        return f'{self.name}'


class AnswerManager(models.Manager):
    def get_answers(self, question):
        return self.filter(question__exact=question)

    def get_answers_count(self, question):
        return self.filter(question__exact=question).count()


class Answer(models.Model):
    profile = models.ForeignKey(Profile, models.PROTECT)
    question = models.ForeignKey(Question, models.CASCADE)

    text = models.TextField()
    correct = models.BooleanField(default=False)

    like_number = 0

    objects = AnswerManager()

    def __str__(self):
        return  self.text[:100]


class LikeQuestionManager(models.Manager):
    def get_questions_likes(self, question):
        return self.filter(question__exact=question).count()


class LikeQuestion(models.Model):
    profile = models.ForeignKey(Profile, models.CASCADE)
    question = models.ForeignKey(Question, models.CASCADE)

    objects = LikeQuestionManager()


class LikeAnswerManager(models.Manager):
    def get_answers_likes(self, answer):
        return self.filter(answer__exact=answer).count()


class LikeAnswer(models.Model):
    profile = models.ForeignKey(Profile, models.CASCADE)
    answer = models.ForeignKey(Answer, models.CASCADE)

    objects = LikeAnswerManager()


OPTIONS = {
    'username': 'Cat',
    'password': 'password',
    'nickname': 'Bird',
    'is_auth': True
}