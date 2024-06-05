from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from enquete.models import Question

def index(request):
    questions = Question.objects.order_by('question_text')
    context = {'questions': questions}
    return render(request, 'enquete/index.html', context)

def results(request, question_id):
    question = Question(pk=question_id)
    context = {'question': question}
    return render(request, 'enquete/results.html', context)

def vote(request, question_id):
   question = get_object_or_404(Question, pk=question_id)
   try:
       selected_option = question.option_set.get(pk=request.POST['option'])
   except KeyError:
      return render(request, 'enquete/vote.html', {
          'question': question,
          'error_message': "Selecione uma opção",
      })
   else:
       selected_option.votes += 1
       selected_option.save()
       return HttpResponseRedirect(reverse('enquete:results', args=(question_id, )))