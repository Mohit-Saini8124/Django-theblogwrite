from django import forms
from tinymce import TinyMCE
from .models import Comment, Post

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Post
        fields = ('title', 'categories', 'thumbnail', 'content')


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'name' : "Add Comment"
    }))
    class Meta:
        model = Comment
        fields = ('content', )