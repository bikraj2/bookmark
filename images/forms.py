from django import forms
from django.conf import time
from django.utils.text import slugify
import requests
from .models import Image
from django.core.files.base import ContentFile
import hashlib
class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image

        fields = ['title','url','description']
        widgets  =  {
            'url':forms.HiddenInput
        }
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg','png','jpeg']
        extension = url.rsplit('.',1)[-1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError(
                "The given Url Doesnot match valid image extension"
            )
        return url
    def save(self, force_insert= False,force_update=False,commit=True):
        image = super().save(commit = False)
        image_url = self.cleaned_data['url']
        name = hashlib.sha1(str(time.time()).encode()).hexdigest()[:10]
        extension = image_url.split('.')[-1].lower()
        image_name = f'{name}:{extension}'
        print("here",image_name)
        response = requests.get(image_url)
        image.image.save(
            image_name,
            ContentFile(response.content),
            save =False
        )
        if commit:
            image.save()
        return image

