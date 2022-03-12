
from .models import Comment
from django.forms import ModelForm
from ckeditor.widgets import CKEditorWidget


class CommentFrom(ModelForm):
    class Meta:
        model = Comment
        fields = ['body', ]
        Widgets = {
            'body': CKEditorWidget()
        }
