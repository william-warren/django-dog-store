from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator


class NewDogTagForm(forms.Form):
    owner_name = forms.CharField()
    dog_name = forms.CharField()
    dog_birthday = forms.DateField(input_formats=["%Y-%m-%d"])


class NewReviewForm(forms.Form):
    author = forms.CharField()
    content = forms.CharField()
    rating = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
