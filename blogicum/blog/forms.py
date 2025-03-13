from django import forms
from django.contrib.auth.models import User

from .models import Comment, Post


class PostCreateForm(forms.ModelForm):
    """Форма для создания публикаций"""

    class Meta:
        model = Post
        exclude = ["is_published", "created_at", "author", "is_scheduled"]
        widgets = {
            "pub_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "image": forms.ClearableFileInput(attrs={"multiple": False}),
        }


class UserEditForm(forms.ModelForm):
    """Форма для редактирования информации о пользователе"""

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"
            self.fields[field].widget.attrs[
                "placeholder"
            ] = self.fields[field].label


class CommentForm(forms.ModelForm):
    """Форма для комментариев"""

    class Meta:
        model = Comment
        fields = ("text",)
