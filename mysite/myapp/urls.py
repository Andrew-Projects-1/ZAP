from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page>/', views.index, name='index'),
    path('questions/', views.questions, name='questions'), # Name is not really required
    path('login/', auth_views.LoginView.as_view()),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout_user'),
    path('question_json/', views.question_json, name='question_json'),
    path('answer/<int:quest_id>/', views.answer_form, name='answer_form'),
    path('rants/', views.rants, name='rants'),
    path('rants_json/', views.rants_json, name='rants_json'),
    path('rants_answer/<int:quest_id>/', views.rants_answer_form, name='rants_answer_form'),
    path('community/', views.community, name='community'),
    path('chatroom/', views.ind, name='ind'),
    path("chat/<str:room_name>/", views.room, name="room"),

    path('questions_delete/<int:quest_id>/', views.questions_delete, name="questions_delete"),
    path('rants_delete/<int:quest_id>/', views.rants_delete, name="rants_delete"),

    path('questions_answers_delete/<int:quest_id>/', views.questions_answers_delete, name="questions_answers_delete"),
    path('rants_answers_delete/<int:quest_id>/', views.rants_answers_delete, name="rants_answers_delete"),

    path('profile/', views.profile, name='profile_update'),
    path('SHA/', views.SHA, name='SHA_Page'),

    path("password_change", views.password_change, name="password_change"),
    path("confirm_password", views.confirm_password, name="confirm_password"),

    path('inbox/', views.ListThreads.as_view(), name='inbox'),
    path('inbox/create-thread/', views.CreateThread.as_view(), name='create-thread'),
    path('inbox/<int:pk>/', views.ThreadView.as_view(), name='thread'),
    path('inbox/<int:pk>/create-message/', views.CreateMessage.as_view(), name='create-message'),

    path('notification/<int:notification_pk>/thread/<int:object_pk>', views.ThreadNotification.as_view(), name='thread-notification'),
    path('notification/delete/<int:notification_pk>', views.RemoveNotification.as_view(), name='notification-delete'),

    #path('messaging/', views.messaging, name='messaging'),
]