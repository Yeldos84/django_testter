from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from testapp.models import Test, Question, Answer, TestResult
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
import joblib
import os
from faker import Faker
from random import randint, choice, shuffle, uniform

fake = Faker()

class Command(BaseCommand):
    help = "Генерирует тесты, вопросы, ответы, пользователей и результаты + обучает модель"

    def handle(self, *args, **kwargs):
        self.stdout.write("Начинаем генерацию данных...\n")

        # 1. Тесты, Вопросы, Ответы
        for i in range(3):
            test = Test.objects.create(title=f"Фейковый тест {i+1}")

            for j in range(5):
                question = Question.objects.create(
                    test=test,
                    text=fake.sentence(nb_words=6)
                )

                correct_index = randint(0, 3)
                for k in range(4):
                    Answer.objects.create(
                        question=question,
                        text=fake.word(),
                        is_correct=(k == correct_index)
                    )

        self.stdout.write("Тесты, вопросы и ответы созданы.")

        # 2. Пользователи и TestResult
        for i in range(5):
            username = f"user_{i}"
            user, _ = User.objects.get_or_create(username=username)

            for test in Test.objects.all():
                score = randint(0, 5)
                attempts = randint(1, 3)
                time_spent = round(uniform(1, 15), 2)
                passed = score >= 3

                TestResult.objects.update_or_create(
                    user=user,
                    test=test,
                    defaults={
                        'score': score,
                        'attempts': attempts,
                        'time_spent': time_spent,
                        'passed': passed
                    }
                )

        self.stdout.write("Пользователи и результаты сгенерированы.")

        # 3. Обучение модели
        df = pd.DataFrame(TestResult.objects.all().values('score', 'attempts', 'time_spent', 'passed'))

        if df['passed'].nunique() < 2:
            self.stdout.write(self.style.ERROR("Недостаточно классов для обучения модели (нужны и True, и False)"))
            return

        X = df[['score', 'attempts', 'time_spent']]
        y = df['passed'].astype(int)

        model = LogisticRegression()
        model.fit(X, y)

        joblib.dump(model, "prediction_model.pkl")
        self.stdout.write(self.style.SUCCESS("Модель обучена и сохранена как prediction_model.pkl"))

        self.stdout.write(self.style.SUCCESS("Генерация и обучение завершены!"))
