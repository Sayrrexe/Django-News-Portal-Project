from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title','text', 'post_category',]
        
    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("text")
        if description is not None and len(description) < 20:
            raise ValidationError({
				"text": "Описание не может быть менее 20 символов."
			})
        name = cleaned_data.get("title")
        if name == description:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data
    
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'title','text', 'post_category',]
        
    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("text")
        if description is not None and len(description) < 20:
            raise ValidationError({
				"description": "Описание не может быть менее 20 символов."
			})
        name = cleaned_data.get("title")
        if name == description:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data