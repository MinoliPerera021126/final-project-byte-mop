from django import forms
from django.forms import inlineformset_factory
from .models import Zone, Building, Division, Task, Subtask
from django.contrib.auth import get_user_model

User = get_user_model()

class ZoneForm(forms.ModelForm):
    class Meta:
        model = Zone
        fields = ['name', 'description']

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['zone', 'name', 'floors', 'description']

class DivisionForm(forms.ModelForm):
    # allow choosing an assistant from existing users (staff or everyone; filter in view if needed)
    assistant = forms.ModelChoiceField(queryset=User.objects.all(), required=False, help_text="Assign assistant (optional)")

    class Meta:
        model = Division
        fields = ['building', 'name', 'description', 'assistant']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['division', 'title', 'description']

class SubtaskForm(forms.ModelForm):
    class Meta:
        model = Subtask
        fields = ['title', 'notes', 'is_done']

# Inline formset: edit/add multiple Subtasks when creating or editing a Task
SubtaskFormSet = inlineformset_factory(
    Task, Subtask,
    form=SubtaskForm,
    extra=1, can_delete=True
)
