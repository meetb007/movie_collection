from django import forms

from movie.models import Movie


class MovieForm(forms.ModelForm):
    title = forms.CharField(required=True)
    description = forms.CharField(required=True)
    uuid = forms.UUIDField(required=True)
    genres = forms.CharField(required=False)

    class Meta:
        model = Movie
        fields = ['title', 'description']
