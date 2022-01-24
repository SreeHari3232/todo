from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login

class CustomLogin(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasklist')


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        return context
    

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/taskdetail.html'



class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'base/taskform.html'
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasklist')
    
     
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'base/taskform.html'
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasklist')
    
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'base/taskdelete.html'
    context_object_name = 'tasks'
    fields = '__all__'
    success_url = reverse_lazy('tasklist')
    


    
