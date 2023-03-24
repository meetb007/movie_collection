from django import forms

from collection.models import Collection


class CollectionForm(forms.ModelForm):
    title = forms.CharField(required=True)
    description = forms.CharField(required=True)
    movies = forms.JSONField(required=True)

    class Meta:
        model = Collection
        fields = ['title', 'description']


class CollectionUpdationForm(forms.Form):
    title = forms.CharField(required=False)
    description = forms.CharField(required=False)
    movies = forms.JSONField(required=False)

    class Meta:
        model = Collection
        fields = ['title', 'description']

    def clean(self):
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')
        movies = self.cleaned_data.get('movies')

        if not any([title, description, movies]):
            raise forms.ValidationError(f"Enter the fields for updation.")

        super(CollectionUpdationForm, self).clean()
