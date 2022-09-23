from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from api.models import Question

# Create your views here.
# @login_required(login_url='/accounts/login/')
class QuestionListView(ListView):
    model = Question
