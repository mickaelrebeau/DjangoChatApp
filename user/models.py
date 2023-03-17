from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProfile(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'chat_users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='recipient')
    message = models.TextField()
    date = models.DateField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message
    
    class Meta:
        db_table = 'chat_messages'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ('-date',)


    def get_all_messages(id_1, id_2):
        messages = []
        message1 = Message.objects.filter(sender_id=id_1, recipient_id=id_2).order_by('-date')
        for x in range(len(message1)):
            messages.append(message1[x])
        message2 = Message.objects.filter(sender_id=id_2, recipient_id=id_1).order_by('-date')
        for x in range(len(message2)):
            messages.append(message2[x])

        for x in range(len(messages)):
            messages[x].is_read = True

        messages.sort(key=lambda x: x.date, reverse=False)
        
        return messages

    def get_message_list(u):
        all_msg = []
        all_users = []
        last_msg = []
        
        for message in Message.objects.all():
            for_you = message.recipient == u
            from_you = message.sender == u
            if for_you or from_you:
                all_msg.append(message)
                all_msg.sort(key=lambda x: x.sender.username)
                all_msg.sort(key=lambda x: x.date, reverse=True)
        
        for msg in all_msg:
            if msg.sender.username not in all_users or msg.recipient.username not in all_users:
                all_users.append(msg.sender.username)
                all_users.append(msg.recipient.username)
                last_msg.append(msg)

        return last_msg