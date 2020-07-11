from django.shortcuts import render
from .models import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse

# Create your views here.

#get question and display them

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    context  = {'latest_question_list':latest_question_list}
    return render(request,'polls/index.html', context)


#show specific question and choices

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    return render(request, 'polls/detail.html', {'question':question})

#get question and display result

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})

#vote for a question choice

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        #redisplay the question voting form
        return render(request, 'polls/detail.html',{
            'question':question,
            'error_message':"You didn't select a choice"})
    
    else:
        selected_choice.votes +=1
        selected_choice.save()

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def resultsData(request, obj):
    votedata = []

    question = Question.objects.get(id=obj)
    votes = question.choice_set.all()

    for i in votes:
        votedata.append({i.choice_text:i.votes})

    print(votedata)
    return JsonResponse(votedata, safe=False)

    