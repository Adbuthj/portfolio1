from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import About, Project, Skill, Experience, ContactMessage
from .forms import AboutForm, ProjectForm, SkillForm, ExperienceForm

def portfolio_index(request):
    about = About.objects.first()
    projects = Project.objects.all()
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        # Forward to Gmail
        try:
            full_message = f"New message from: {name}\nEmail: {email}\n\nSubject: {subject}\n\nMessage:\n{message}"
            send_mail(
                f"Portfolio Contact: {subject}",
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email forwarding failed: {e}")

        messages.success(request, 'Your message has been sent successfully!')
        return redirect('portfolio_index')

    context = {
        'about': about,
        'projects': projects,
        'skills': skills,
        'experiences': experiences,
    }
    return render(request, 'portfolio/index.html', context)

@login_required
def dashboard(request):
    about = About.objects.first()
    projects = Project.objects.all()
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    messages_list = ContactMessage.objects.all().order_by('-created_at')

    about_form = AboutForm(instance=about) if about else AboutForm()
    project_form = ProjectForm()
    skill_form = SkillForm()
    experience_form = ExperienceForm()

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'about':
            form = AboutForm(request.POST, request.FILES, instance=about) if about else AboutForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'About information updated!')
                return redirect('dashboard')
        
        elif form_type == 'project':
            form = ProjectForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Project added successfully!')
                return redirect('dashboard')
        
        elif form_type == 'skill':
            form = SkillForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Skill added successfully!')
                return redirect('dashboard')
        
        elif form_type == 'experience':
            form = ExperienceForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Experience added successfully!')
                return redirect('dashboard')

    context = {
        'about': about,
        'projects': projects,
        'skills': skills,
        'experiences': experiences,
        'messages_list': messages_list,
        'about_form': about_form,
        'project_form': project_form,
        'skill_form': skill_form,
        'experience_form': experience_form,
    }
    return render(request, 'portfolio/dashboard.html', context)

@login_required
def delete_item(request, model_name, item_id):
    models_dict = {
        'project': Project,
        'skill': Skill,
        'experience': Experience,
    }
    
    if model_name in models_dict:
        model = models_dict[model_name]
        item = get_object_or_404(model, id=item_id)
        item.delete()
        messages.success(request, f'{model_name.capitalize()} deleted successfully!')
    
    return redirect('dashboard')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            
    return render(request, 'portfolio/login.html')

def logout_user(request):
    logout(request)
    return redirect('portfolio_index')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'portfolio/change_password.html', {
        'form': form
    })
