from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime

from app import models


class LoginForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=30)
    password = forms.CharField(min_length=4, max_length=30, widget=forms.PasswordInput)


class SignUpForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=30)
    nickname = forms.CharField(min_length=4, max_length=30)
    password = forms.CharField(min_length=4, max_length=30, widget=forms.PasswordInput)
    second_password = forms.CharField(min_length=4, max_length=30, widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        second_password = self.cleaned_data['second_password']

        if password != second_password:
            raise ValidationError("Password don't match")

        if models.User.objects.filter(username=username):
            raise ValidationError("This username is already used")

        return self.cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        nickname = cleaned_data['nickname']
        cleaned_data.pop('nickname')
        cleaned_data.pop('second_password')
        user = models.User.objects.create_user(**cleaned_data)
        profile = models.Profile(user=user, nickname=nickname)
        profile.save()
        return profile


class SettingsForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=30)
    nickname = forms.CharField(min_length=4, max_length=30)
    # password = forms.CharField(min_length=4, max_length=30, widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)

    def clean(self):
        username = self.cleaned_data['username']

        if username != models.CurrentUser.profile.user.username and models.User.objects.filter(username=username):
            raise ValidationError("This username is already used")

        return self.cleaned_data


    def save(self):
        user = models.CurrentUser.profile.user
        user.username = self.cleaned_data['username']
        # user.set_password(self.cleaned_data['password'])
        # user.save(update_fields=["username", "password"])
        user.save(update_fields=["username"])
        profile = models.CurrentUser.profile
        profile.nickname = self.cleaned_data['nickname']
        profile.save(update_fields=["nickname"])

        models.CurrentUser.profile = profile

        return profile


class AskForm(forms.Form):
    title = forms.CharField(max_length=50)
    text = forms.CharField(min_length=4, widget=forms.Textarea)
    tags = forms.CharField()

    def ask(self):
        question = models.Question.objects.create(
            profile=models.CurrentUser.profile,
            title=self.cleaned_data['title'],
            text=self.cleaned_data['text'],
            status=models.Question.NORMAL,
            date=datetime.today()
        )

        tags = self.cleaned_data["tags"]
        for tag in tags.split('[, ]'):
            if models.Tag.objects.filter(name=tag):
                tag_model = models.Tag.objects.get(name=tag)
                tag_model.question.add(question)
                tag_model.save(update_fields=["question"])
            else:
                models.Tag.objects.create(name=tag).question.add(question)

        return question.id


class QuestionForm(forms.Form):
    answer = forms.CharField(min_length=4, widget=forms.Textarea)

    def respond(self, question_id):
        models.Answer.objects.create(
            profile=models.CurrentUser.profile,
            question=models.Question.objects.find_by_id(question_id),
            text=self.cleaned_data['answer'],
            correct=False
        )


