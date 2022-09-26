from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from api.models import Question

# Create your views here.
# @login_required(login_url='/accounts/login/')
class QuestionListView(ListView):
    model = Question
    paginate_by = 25
    ordering = ['-date_create']

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        object_list = qs
        query = self.request.GET.get('title')
        if query:
            object_list = self.model.objects.filter(text__icontains=query)
        return object_list

