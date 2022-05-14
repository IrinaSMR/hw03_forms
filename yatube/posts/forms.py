from .models import Post
from django.forms import ModelForm


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {'group': 'Группа', 'text': 'Текст'}
        help_texts = {'text': ('Обязательное поле для заполнения')}
