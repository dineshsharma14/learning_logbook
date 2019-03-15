"""Defines url patterns for learning_logs """

from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns = [
    # Homepage
    path('', views.index, name = 'index'),

    # Show all topics
    path('topics',views.topics, name = 'topics'),

    # Show individual topic in detail
    path('topics/<int:topic_id>', views.topic, name = 'topic'), # here looks like we are calling topic fx w/o () and args

    # Page for adding a new topic
    path('new_topic', views.new_topic, name = 'new_topic'),

    # Page for adding a new entry
    path('new_entry/<int:topic_id>', views.new_entry, name = 'new_entry'),

    # Page for editing an entry
    path('edit_entry/<int:entry_id>', views.edit_entry, name = 'edit_entry'),
    ]
