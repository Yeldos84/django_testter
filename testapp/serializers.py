from rest_framework import serializers
from . models import Question, Test, Answer, User

class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'test', 'text')


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ('id', 'title')


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('question', 'text', 'is_correct')



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')