from django import forms

from main.models import Films


class FilmForm(forms.ModelForm):
    class Meta:
        model = Films
        fields = ['title', 'description', 'year', 'country', 'time', 'producer', 'genre', 'image', 'video']


