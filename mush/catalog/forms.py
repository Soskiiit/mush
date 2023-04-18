from django import forms


class UpdateModelForm(forms.Form):
    name = forms.CharField(max_length=100)
    public = forms.BooleanField()
    images = forms.FileField()  # multiple images
    model = forms.FileField()
