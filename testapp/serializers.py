from rest_framework import serializers
from . models import Question, Test

class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'test', 'text')


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('id', 'title')