from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('hot/', views.hot_questions, name='hot'),
    path('tag/<str:tag_name>/', views.tag_question, name='tag_question'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('settings/', views.settings, name='settings'),

    path('questions/get/<int:start>/<int:end>/<str:status>', views.questions_get),
    path('answers/get/<int:question_id>/', views.answers_get),
    path('profile/get/<int:profile_id>/', views.profile_get)
]
