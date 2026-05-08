from django import forms
from django.contrib.auth.models import User
from .models import Profile, Post, PostComment

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Prénom", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Nom", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    niveau = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Licence 3, Master 1'}))
    centres_interet = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ex: Football, Lecture, Informatique...'})
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Parlez-nous un peu de vous...'})
    )
    
    class Meta:
        model = Profile
        fields = ['photo', 'filiere', 'niveau', 'bio', 'centres_interet']
        widgets = {
            'filiere': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control border-0 shadow-none', 'rows': 2, 'placeholder': 'Quoi de neuf sur le campus ?'}),
            'image': forms.FileInput(attrs={'class': 'form-control form-control-sm'}),
        }

class PostCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control rounded-pill', 'placeholder': 'Écrire un commentaire...'})
        }