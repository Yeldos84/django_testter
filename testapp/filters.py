import django_filters
from .models import Question, Answer

class QuestionFilter(django_filters.FilterSet):
    class Meta:
        model = Question
        fields = {
            'test': ['exact'],  # Фильтрация по полю test
            'text': ['icontains'],  # Фильтрация по тексту с использованием регистронезависимого поиска
        }



class AnswerFilter(django_filters.FilterSet):
    class Meta:
        model = Answer
        fields = {
            'question': ['exact'],  # Фильтрация по полю question
            'text': ['icontains'],  # Фильтрация по тексту с использованием регистронезависимого поиска
        }
