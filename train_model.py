import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from django.conf import settings
from testapp.models import TestResult  # Убедись, что имя приложения правильное

# Загружаем данные из базы
results = TestResult.objects.all().values('score', 'attempts', 'time_spent', 'passed')
df = pd.DataFrame(results)

# Проверяем, есть ли данные
if df.empty:
    print("No data for train.")
    exit()

# Разделение данных
X = df[['score', 'attempts', 'time_spent']]  # Признаки
y = df['passed'].astype(int)  # Целевая переменная (0 - не сдал, 1 - сдал)

# Проверяем баланс классов
print("Balance class (passed):")
print(df['passed'].value_counts())

# Если только один класс - обучение не имеет смысла
if df['passed'].nunique() == 1:
    print("⚠ Invalid data: one class!")
    exit()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создаем и обучаем модель
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Путь для сохранения модели
model_path = os.path.join(settings.BASE_DIR, 'prediction_model.pkl')
joblib.dump(model, model_path)

print("Balance class (passed):")
print(df['passed'].value_counts(normalize=True) * 100)

print(f"Model trained! {model_path}")
