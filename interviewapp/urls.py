from django.urls import path

import interviewapp.views as interview

app_name = 'interviewapp'

urlpatterns = [
    path('active', interview.active, name='active'),
    path('active/<int:page>', interview.active, name='active_page'),

    path('<int:interview_id>', interview.interview, name='interview'),

    path('question/<int question_id>', interview.question, name='question')
]