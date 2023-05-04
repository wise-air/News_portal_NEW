from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=10)

    class Meta:
        model = Post
        fields = ['author',
                  'postCategory',
                  'headline',
                  'text',
                  'postRating',
                  ]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("headline")
        text = cleaned_data.get("text")
        rating = cleaned_data.get('postRating')

        if name == text:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )
        elif rating < 0:
            raise ValidationError(
                'Рейтинг не может быть меньше нуля'
            )

        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data["headline"]
        if name[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы"
            )
        return name