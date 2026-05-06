from django.db import models

class About(models.Model):
    full_name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profile/')
    email = models.EmailField()
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "About Me"

    def __str__(self):
        return self.full_name

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    link = models.URLField(blank=True, null=True)
    technologies = models.CharField(max_length=500, help_text="Comma separated list of technologies")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Tools', 'Tools'),
        ('Other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    proficiency = models.IntegerField(help_text="Value between 1 and 100")

    def __str__(self):
        return f"{self.name} ({self.category})"

class Experience(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    period = models.CharField(max_length=100, help_text="e.g. Jan 2020 - Present")
    description = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['-order', '-id']

    def __str__(self):
        return f"{self.title} at {self.company}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
