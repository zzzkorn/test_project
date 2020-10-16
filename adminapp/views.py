from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView

from adminapp.models import QuestionEditForm
from interviewapp.models import Interview, Question


@user_passes_test(lambda u: u.is_superuser)
def interviews(request):
    title = 'админка/опросы'
    interviews_list = Interview.objects.all()
    content = {
        'title': title,
        'interviews': interviews_list
    }
    return render(request, 'adminapp/interviews.html', content)


@user_passes_test(lambda u: u.is_superuser)
def interview_delete(request, interview_id):
    interview_item = get_object_or_404(Interview, pk=interview_id)
    interview_item.is_active = False
    interview_item.save()
    return HttpResponseRedirect(reverse('adminapp:interviews'))


class InterviewUpdateView(UpdateView):
    model = Interview
    template_name = 'adminapp/interviews_update.html'
    success_url = reverse_lazy('admin:interviews')
    fields = 'name expiration_date description is_active'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'опросы/редактирование'
        return context


class InterviewCreateView(CreateView):
    model = Interview
    template_name = 'adminapp/interviews_update.html'
    success_url = reverse_lazy('admin:interviews')
    fields = '__all__'


@user_passes_test(lambda u: u.is_superuser)
def questions(request, interview_id):
    title = 'админка/вопросы'
    interview_item = get_object_or_404(Interview, pk=interview_id)
    questions_list = Question.objects.all(inside_interview=interview_item)
    content = {
        'title': title,
        'interview': interview_item,
        'questions': questions_list
    }
    return render(request, 'adminapp/questions.html', content)


@user_passes_test(lambda u: u.is_superuser)
def question_create(request, interview_id):
    title = 'вопрос/создание'
    interview_item = get_object_or_404(Interview, pk=interview_id)

    if request.method == 'POST':
        question_form = QuestionEditForm(request.POST)
        if question_form.is_valid():
            question_form.save()
            return HttpResponseRedirect(reverse('adminapp:questions', args=[interview_id]))
    else:
        question_form = QuestionEditForm(initial={'inside_interview': interview_item})

    content = {
        'title': title,
        'update_form': question_form,
        'interview': interview_item
    }

    return render(request, 'adminapp/question_update.html', content)


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'adminapp/question_read.html'


@user_passes_test(lambda u: u.is_superuser)
def delete_question(request, question_id):
    question_item = get_object_or_404(Question, pk=question_id)
    question_item.is_active = False
    question_item.save()
    return HttpResponseRedirect(reverse('adminapp:questions'))


@user_passes_test(lambda u: u.is_superuser)
def update_question(request, question_id):
    title = 'вопрос/редактирование'
    edit_question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        edit_form = QuestionEditForm(request.POST, instance=edit_question)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('adminapp:questions'))
    else:
        edit_form = QuestionEditForm(instance=edit_question)

    content = {
        'title': title,
        'update_form': edit_form,
        'inside_interview': edit_question.inside_interview
    }

    return render(request, 'adminapp/question_update.html', content)
