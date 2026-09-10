from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from students.models import Student

class StudentRegistrationForm(UserCreationForm):
    # Additional fields for the Student model
    name = forms.CharField(max_length=255, required=True, help_text='Full Name')
    email = forms.EmailField(required=True, help_text='University Email Address')
    phone = forms.CharField(max_length=20, required=True, help_text='Contact Number')
    course = forms.CharField(max_length=100, required=True, help_text='E.g., BSc CSIT')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists() or Student.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    @transaction.atomic
    def save(self, commit=True):
        # 1. Save the User object first
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.is_staff = False  # Ensure they are registered as a Student, not an Admin
        
        if commit:
            user.save()
            # 2. Save the associated Student profile
            Student.objects.create(
                user=user,
                name=self.cleaned_data.get('name'),
                email=self.cleaned_data.get('email'),
                phone=self.cleaned_data.get('phone'),
                course=self.cleaned_data.get('course')
            )
        return user
