from django.core import validators
from django.db import models
from django.contrib.auth.models import User


class Test(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        ordering = ['id']
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return self.title

class Question(models.Model):
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=500)

    class Meta:
        ordering = ['id']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def user_can_answer(self, user):
        user_choices = user.choice_set.all()
        done = user_choices.filter(question=self)
        print(done)
        if done.exists():
            return False
        return True



    def __str__(self):
        return f'{self.test.title} - {self.text}'

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return f'{self.question.test} - {self.text} - {self.is_correct}'


class Result(models.Model):
    quiz = models.ForeignKey(Test, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    correct = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.quiz.title} - {self.user} - correct answer:{self.correct}'


class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='test')
    score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'test')
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'


    def __str__(self):
        return f'{self.test} - {self.user} - Правильные ответы: {self.score}'


class ProfilePhoto(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='files/%Y/%m/%d', validators=[validators.FileExtensionValidator
                                                        (allowed_extensions=('jpg', 'gif', 'png'))],
                           error_messages={'invalid_extension': 'This file do not supported!'})

    def __str__(self):
        return f'{self.photo}'