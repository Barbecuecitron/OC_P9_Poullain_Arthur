from django import forms


class FollowForm(forms.Form):
    follow = forms.CharField(label='', max_length=100)
