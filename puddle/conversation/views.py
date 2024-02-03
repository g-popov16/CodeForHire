from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from item.models import Item
from .models import Conversation
from .forms import ConversationMessageForm

from django.db.models import Q


@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if request.method == 'POST':
        selected_members = request.POST.getlist('members')

        # Ensure current user is part of the conversation
        if request.user.id not in map(int, selected_members):
            selected_members.append(request.user.id)

        # Sort the member IDs for consistent comparison
        selected_member_ids = sorted(map(int, selected_members))

        # Find an existing conversation with the exact same members
        existing_conversation = None
        for conversation in Conversation.objects.filter(item=item):
            member_ids = sorted(member.id for member in conversation.members.all())
            if member_ids == selected_member_ids:
                existing_conversation = conversation
                break

        # Redirect to the existing conversation if found
        if existing_conversation:
            return redirect('conversation:detail', pk=existing_conversation.pk)

        # Create a new conversation if none exists
        conversation = Conversation.objects.create(item=item)
        conversation.members.set(User.objects.filter(id__in=selected_members))
        conversation.save()

        return redirect('conversation:detail', pk=conversation.pk)

    else:
        users = User.objects.all()
        return render(request, 'conversation/select_members.html', {'users': users})


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations
    })

@login_required

def detail(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', 
                  {'conversation': conversation,
                   'form': form
                      })
