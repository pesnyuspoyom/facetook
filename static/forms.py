from django import forms

class VideoForm(forms.Form):
    video_link = forms.URLField()