from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic # base the form on Topic class
        fields = ['text'] # base the form's size on text field of Topic
        labels = {'text': ''} # not to generate a label for text field

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry # base the form on Entry class
        fields = ['text'] # base the form's size on text field of Entry
        labels = {'text': ''} # not to generate a label for text field.
        widgets = {'text': forms.Textarea(attrs = {'cols': 80})}
