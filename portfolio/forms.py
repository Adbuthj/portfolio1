from django import forms
from .models import About, Project, Skill, Experience

class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = '__all__'
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-input'}),
            'full_name': forms.TextInput(attrs={'class': 'form-input'}),
            'role': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-input'}),
            'github': forms.URLInput(attrs={'class': 'form-input'}),
            'twitter': forms.URLInput(attrs={'class': 'form-input'}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-input'}),
            'link': forms.URLInput(attrs={'class': 'form-input'}),
            'technologies': forms.TextInput(attrs={'class': 'form-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-input'}),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'proficiency': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 100}),
        }

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'company': forms.TextInput(attrs={'class': 'form-input'}),
            'period': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-input'}),
        }
