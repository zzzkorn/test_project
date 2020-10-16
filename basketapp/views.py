from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from basketapp.models import Basket
from interviewapp.models import Interview, Response


@login_required
def basket(request, page=1):
    title = 'пройденые опросы'
    baskets = Basket.objects.filter(user=request.user)
    paginator = Paginator(baskets, 25)
    try:
        baskets_paginator = paginator.page(page)
    except PageNotAnInteger:
        baskets_paginator = paginator.page(1)
    except EmptyPage:
        baskets_paginator = paginator.page(paginator.num_pages)
    content = {
        'title': title,
        'baskets': baskets_paginator,
    }
    return render(request, 'basketapp/basket.html', content)


@login_required
def add(request, interview_id):
    interview_item = get_object_or_404(Interview, pk=interview_id)
    basket_item = Basket.objects.filter(user=request.user, interview=interview_item).first()
    if not basket_item:
        basket_item = Basket(user=request.user, interview=interview_item)
    basket_item.save()
    return HttpResponseRedirect(reverse('main:index'))


@login_required
def interview_completed(request, interview_id):
    title = 'пройденый опрос'
    interview_item = get_object_or_404(Interview, pk=interview_id)
    responses = Response.objects.filter(inside_interview__question__inside_interview=interview_item,
                                        interviewee=request.user).order_by('-response_time')
    content = {
        'title': title,
        'interview': interview_item,
        'responses': responses,
    }
    return render(request, 'basketapp/interview.html', content)
