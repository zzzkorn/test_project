from django.urls import path

import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('interviews/create/', adminapp.InterviewCreateView.as_view(), name='interview_create'),
    path('interviews/read/', adminapp.interviews, name='interviews'),
    path('interviews/update/<int:pk>/', adminapp.InterviewUpdateView.as_view(), name='interview_update'),
    path('interviews/delete/<int:interview_id>/', adminapp.interview_delete, name='interview_delete'),

    path('questions/read/interview/<int:interview_id>/', adminapp.questions, name='questions'),
    path('questions/create/interview/<int:interview_id>/', adminapp.question_create, name='create_question'),

    path('question/read/<int:pk>/', adminapp.QuestionDetailView.as_view(), name='read_question'),
    path('question/update/<int:question_id>/', adminapp.update_question, name='update_question'),
    path('question/delete/<int:question_id>/', adminapp.delete_question, name='delete_question'),

]