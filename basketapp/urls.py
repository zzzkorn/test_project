from django.urls import path

import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.basket, name='index'),
    path('/<int:page>', basketapp.basket, name='index_page'),

    path('interview_completed/<int:interview_id>', basketapp.interview_completed, name='interview_completed'),

    path('add/<int:interview_id>', basketapp.add, name='add'),
]