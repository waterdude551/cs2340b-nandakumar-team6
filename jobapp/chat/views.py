from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import User
from .models import Conversation, Message

@login_required
def list_convos(request):
    """Show all conversations for the current user"""
    user = request.user
    conversations = Conversation.objects.filter(
        Q(recruiter=user) | Q(seeker=user)
    )
    context = {'conversations': conversations}
    return render(request, 'chat/list_convos.html', context)


@login_required
def show_convo(request, conversation_id):
    """Show messages with one specific person"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    if request.user not in [conversation.recruiter, conversation.seeker]:
        return redirect('chat.list_convos')
    
    messages = conversation.messages.all()
    messages.filter(read=False).exclude(sender=request.user).update(read=True)
    
    if request.method == 'POST':
        text = request.POST.get('message')
        if text:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                text=text
            )
            return redirect('chat.show_convo', conversation_id=conversation_id)
    
    other_person = conversation.seeker if request.user == conversation.recruiter else conversation.recruiter
    
    context = {
        'conversation': conversation,
        'messages': messages,
        'other_person': other_person
    }
    return render(request, 'chat/show_convo.html', context)


@login_required
def start_convo(request):
    """Show form to select seeker and write first message (recruiters only)"""
    
    if request.user.role != 'recruiter':
        return redirect('chat.list_convos')
    
    # Get seekers that this recruiter hasn't already started a conversation with
    existing_convos = Conversation.objects.filter(recruiter=request.user)
    existing_seeker_ids = existing_convos.values_list('seeker_id', flat=True)
    
    available_seekers = User.objects.filter(
        role='seeker'
    ).exclude(
        id__in=existing_seeker_ids
    )
    
    context = {'available_seekers': available_seekers}
    return render(request, 'chat/start_convo.html', context)


@login_required
def create_convo(request):
    """Actually create the conversation and first message"""
    
    if request.user.role != 'recruiter':
        return redirect('chat.list_convos')
    
    if request.method == 'POST':
        seeker_id = request.POST.get('seeker_id')
        text = request.POST.get('message')
        
        if seeker_id and text:
            seeker = get_object_or_404(User, id=seeker_id)
            
            # Check if conversation already exists
            existing_convo = Conversation.objects.filter(
                recruiter=request.user,
                seeker=seeker
            ).first()
            
            if existing_convo:
                return redirect('chat.show_convo', conversation_id=existing_convo.id)
            
            # Create conversation
            conversation = Conversation.objects.create(
                recruiter=request.user,
                seeker=seeker
            )
            
            # Create first message
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                text=text
            )
            
            return redirect('chat.show_convo', conversation_id=conversation.id)
    
    return redirect('chat.start_convo')