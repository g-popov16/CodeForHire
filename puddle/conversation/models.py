from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Thread(models.Model):
    title = models.CharField(max_length=255)
    # Other fields...

    def get_absolute_url(self):
        return reverse('conversation:thread_detail', kwargs={'pk': self.pk})

class Post(models.Model):
    thread = models.ForeignKey(Thread, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()

class Conversation(models.Model):
    item = models.ForeignKey('item.Item', related_name='conversations', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('-modified_at',)

class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_messages', on_delete=models.CASCADE)
