from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, ListView, DetailView

from .forms import CustomUserCreationForm
from .models import Message, UserProfile

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'home.html'


class SignupView(CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = '/login'


class ChatListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'chat.html'
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = UserProfile.objects.get(pk=self.request.user.pk)
        messages = Message.get_message_list(user)

        other_users = []

        for msg in range(len(messages)):
            if messages[msg].sender != user:
                other_users.append(messages[msg].sender)
            else:
                other_users.append(messages[msg].recipient)

        context['messages'] = messages
        context['other_users'] = other_users
        context['you'] = user
        return context
        
class InboxView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'inbox.html'
    login_url = '/login'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)
    
    def get_object(self):
        UserName = self.kwargs.get("username")
        return get_object_or_404(UserProfile, username=UserName)
    

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            user = UserProfile.objects.get(pk=self.request.user.pk)
            other_user = UserProfile.objects.get(username=self.kwargs.get('username'))
            messages = Message.get_message_list(user)

            other_users = []

            for msg in range(len(messages)):
                if messages[msg].sender != user:
                    other_users.append(messages[msg].sender)
                else:
                    other_users.append(messages[msg].recipient)

            sender = other_user
            recipient = user

            context['messages'] = Message.get_all_messages(sender, recipient)
            context['messages_list'] = messages
            context['other_person'] = other_user
            context['other_users'] = other_users
            context['you'] = user

            return context


    def post(self, request, *args, **kwargs):
        sender = UserProfile.objects.get(pk=request.POST.get('you'))
        recipient = UserProfile.objects.get(pk=request.POST.get('recipient'))
        message = request.POST.get('message')

        if request.user.is_authenticated:
            if request.method == 'POST':
                if message:
                    Message.objects.create(sender=sender, recipient=recipient, message=message)
            return redirect('chat:inbox', username=recipient.username)
        else:
            return render(request, 'registration/login.html')
    

class UserListView(LoginRequiredMixin ,ListView):
    model = UserProfile
    template_name = 'users_list.html'
    context_object_name = 'users'
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = UserProfile.objects.get(pk=self.request.user.pk)
        context['users'] = UserProfile.objects.exclude(pk=user.pk)
        return context
