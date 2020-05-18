from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from .models import Post, Comment


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }
        
    

class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        



