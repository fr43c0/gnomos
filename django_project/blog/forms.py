from django import forms
from .models import Post
from .models import Document



class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('titulo','autor','document', )
