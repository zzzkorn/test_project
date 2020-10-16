from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from interviewapp.models import Interview, Question, Response


def interview(request, interview_id):
    title = 'описание опроса'
    interview_item = get_object_or_404(Interview, pk=interview_id)
    questions = Question.objects.filter(is_active=True, inside_interview=interview_item)
    content = {
        'title': title,
        'interview': interview_item,
        'questions': questions
    }
    return render(request, 'interviewapp/interview.html', content)


def question(request, question_id):
    title = 'вопрос'
    question_item = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        if request.user.is_authenticated:
            response_item = Response.object.filter(interviewee=request.user, question=question_item).first()
            if not response_item:
                response_item = Response(interviewee=request.user, question=question_item,
                                         response_data=request.POST.get('data'))
            else:
                response_item.response_data = request.POST.get('data')
        else:
            response_item = Response(interviewee=None, question=question_item,
                                     response_data=request.POST.get('data'))
        response_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        content = {
            'title': title,
            'question': question_item
        }
        return render(request, 'interviewapp/question.html', content)


def active(request, page=1):
    title = 'активные опросы'
    interviews = Interview.objects.fiter(is_active=True).order_by('-start_date')
    paginator = Paginator(interviews, 25)
    try:
        interviews_paginator = paginator.page(page)
    except PageNotAnInteger:
        interviews_paginator = paginator.page(1)
    except EmptyPage:
        interviews_paginator = paginator.page(paginator.num_pages)
    content = {
        'title': title,
        'interviews': interviews_paginator
    }
    return render(request, 'interviewapp/active.html', content)
