from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.

def index(request):
    """The home page for learning log. """
    return render(request,'learning_logs/index.html')
    
@login_required #python now knows to run the code in login_required() before topics()
def topics(request): #fx needs request object Django received from the server.
    """Show all topics. """
    topics = Topic.objects.filter(owner = request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show the details of one particular topic"""
    topic = get_object_or_404(Topic, id = topic_id)#instance of Topic class and below is instance of Entry class FK to this topic.
    # Make sure topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404
    
    entries = topic.entry_set.order_by('-date_added') #to get data through ForeignKey rel. you use the lowercase name of 
    context = {'topic':topic,'entries':entries} # related model followed by an underscore and word set.
    return render(request,'learning_logs/topic.html',context)

@login_required
def new_topic(request):
    """ Add a new topic. """
    if request.method != 'POST':
        #No data submitted; create a blank form.
        form = TopicForm()
    else:
        #POST data submitted; process the data. which means add it to db
        form = TopicForm(data = request.POST)
        if form.is_valid():
            check_owner(request,form)
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request,'learning_logs/new_topic.html', context) # we import the form we just wrote, TopicForm

@login_required    
def new_entry(request, topic_id): #topic_id this fx receives from URL
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id = topic_id)
    if request.method != 'POST':
        # No data submitted; create a blank form
        form = EntryForm()
    else:
        # POST data submitted; process the data and add it to DB
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit = False)
            new_entry.topic = topic
            new_entry.save()     
            return HttpResponseRedirect(reverse('learning_logs:topic',
                args = [topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        #Initial request; pre fill form with the current entry
        form = EntryForm(instance = entry)
    else:
        #POST data submitted; process data
        form = EntryForm(instance = entry, data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args = [topic.id]))

    context = {'entry':entry, 'topic': topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)

def check_owner(request,form):
    """Check if topic associated with this user or not"""
    new_entry =  form.save(commit = False)
    new_entry.owner = request.user
    new_entry.save() 
