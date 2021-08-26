from django.forms import ModelForm
from .models import Project

# Create a form HTML based on a Model
class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'featured_image', 'demo_link', 'source_link', 'tags']