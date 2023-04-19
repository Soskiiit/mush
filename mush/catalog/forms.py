from django import forms


class EditProjectForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'})
    )
    public = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input pointer', 'role': 'switch'}
        )
    )
    images = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'multiple': 'multiple',
                'accept': 'images/*',
            }
        )
    )
    model = forms.FileField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
                'accept': '.glb,.gltf',
            }
        )
    )
