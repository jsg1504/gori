from __future__ import unicode_literals
from django import forms
from content.models import Content


class ContentEditForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ('image_file',)
        exclude = ('description',)

