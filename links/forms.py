from models import UserProfile
from models import Link
from models import Vote
from django import forms

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=("user",)

class LinkCreateForm(forms.ModelForm):
    class Meta:
        model=Link
        exclude=('submitter','rank_scores',)

class VoteForm(forms.ModelForm):
    class Meta:
        model=Vote
        exclude= ()