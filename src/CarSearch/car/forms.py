from django import forms

# Regular form
class FileUploadForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ["dbf"]:
            raise forms.ValidationError("Only dbf files are allowed.")
        # return cleaned data is very important.
        return file