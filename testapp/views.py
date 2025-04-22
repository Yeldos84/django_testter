import os
import io
from datetime import datetime
import joblib
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, FileResponse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib import messages
from django.template.loader import get_template
from django.views import View
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics

from .forms import TestterUserCreationForm, TestterAuthenticationForm, PasswordResetForm, PhotoForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Test, Question, Answer, TestResult, ProfilePhoto
from django.db.models import Avg, Count

from xhtml2pdf import pisa
from io import BytesIO

from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from . serializers import QuestionsSerializer, TestSerializer, AnswerSerializer, UserSerializer

from rest_framework import generics
from .filters import QuestionFilter, AnswerFilter
from django_filters.rest_framework import DjangoFilterBackend

import numpy as np
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from .forms import ChatbotForm



model_path = os.path.join(settings.BASE_DIR, 'prediction_model.pkl')

if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = None  # Если модели нет, обработаем ошибку в коде



def base(request):
    return render(request, "testapp/base.html")


#
def index(request):
    return render(request, "testapp/index.html")


def profile(request):
    # photos = ProfilePhoto.objects.values('photo')[0].get('photo')
    # photos = '/media/' + photos

    photos = ProfilePhoto.objects.all()
    return render(request,'testapp/profile.html', {'photos': photos})

def upload_photo(request):
    profile, created = ProfilePhoto.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = PhotoForm(instance=profile)
    return render(request, 'testapp/upload_photo.html', {'form': form})

# Logs

def logs(request):
    f = open('g:/dlog/django.log')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")

# Excel

import pandas as pd

def results_to_excel_ok(request):
    results = TestResult.objects.filter(score__gte=3).select_related('test')
    data = results.values('test__title', 'user__username', 'score')
    df = pd.DataFrame(data)
    df.rename(columns={
        'test__title': 'Название Тестов',
        'user__username': 'пользователь',
        'score': 'Баллы'
    }, inplace=True)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="res_ok.xlsx"'
    df.to_excel(response, index=False)

    return response


def results_to_excel_no(request):
    results = TestResult.objects.filter(score__lt=3).select_related('test')
    data = results.values('test__title', 'user__username', 'score', 'prediction')
    df = pd.DataFrame(data)
    df.rename(columns={
        'test__title': 'Название Тестов',
        'user__username': 'пользователь',
        'score': 'Баллы',
        'prediction': 'Вероятность'
    }, inplace=True)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="res_no.xlsx"'
    df.to_excel(response, index=False)

    return response

#
#
# def login(request):
#     return render(request, "testapp/login.html")
#
# def register(request):
#     return render(request, "testapp/register.html")


def register(request):
    if request.method == 'POST':
        form = TestterUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация прошла успешно! Теперь вы можете войти.")
            return redirect('login')
    else:
        form = TestterUserCreationForm()
    return render(request, 'testapp/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = TestterAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('/')
    else:
        form = TestterAuthenticationForm()
    return render(request, 'testapp/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    messages.info(request, "Вы успешно вышли из системы.")
    return render(request, 'testapp/logout.html')


# def email(request):
#     u = User.objects.get(email="eldos.dos@gmail.com")
#     p = User.objects.all()
#     print(u)
#     for i in p:
#         print(i.email)
#
#     form = PasswordResetForm(request.POST, request.user)
#     username = request.user.username
#     useremail = request.user.email
#     print(username, useremail)
#     print(form.cleaned_data.get['email'])
#     subject = 'Thank you for registering to our site 2'
#     message = ' it  means a world to us '
#     email_from = settings.EMAIL_HOST_USER
#     # send_mail(subject, message, email_from, recipient_list)
#     return redirect('password_reset_done')


from django.shortcuts import render, get_object_or_404, redirect
from .models import Test, Question, Answer


@login_required(login_url='login')
def test_list(request):
    tests = Test.objects.all()
    return render(request, 'testapp/test_list.html', {'tests': tests})


def test_detail(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    questions = test.questions.all()
    for question in questions:
        print(question)
        for answer in question.answers.all():
            print(answer.text)
    return render(request, 'testapp/test_detail.html', {'test': test, 'questions': questions})


def submit_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    questions = test.questions.all()
    score = 0
    start_time = request.session.get(f"test_{test_id}_start", now())

    for question in questions:
        selected_answer = request.POST.get(f'question_{question.id}')
        if selected_answer:
            answer = Answer.objects.get(pk=selected_answer)
            if answer.is_correct:
                score += 1

    time_spent = (now() - start_time).total_seconds() / 60  # В минутах
    passed = score >= 3  # Считаем, сдал ли тест

    test_result, created = TestResult.objects.get_or_create(
        user=request.user,
        test=test,
        defaults={
            'score': score,
            'time_spent': time_spent,
            'attempts': 1,
            'passed': passed  # ✅ добавлено!
        }
    )

    if not created:
        test_result.attempts += 1
        test_result.score = score
        test_result.time_spent = time_spent
        test_result.passed = passed
        test_result.save()

    # Предсказание с проверкой, есть ли модель
    if model:
        features = np.array([[score, test_result.attempts, time_spent]])
        proba = model.predict_proba(features)

        if proba.shape[1] > 1:  # Проверяем, есть ли второй класс
            prediction = round(proba[0][1] * 100, 2)  # Вероятность успешной сдачи
        else:
            prediction = round(proba[0][0] * 100, 2)  # Если только 1 класс, берем его вероятность
    else:
        prediction = "Модель не загружена"

    test_result.prediction = prediction
    test_result.save()

    context = {
        'test': test,
        'score': score,
        'passed': "Да" if passed else "Нет",
        'prediction': round(prediction, 2) if isinstance(prediction, float) else prediction,
    }

    if passed:
        return render(request, 'testapp/test_result.html', context)
    return render(request, 'testapp/test_result_bad.html', context)


def test_statistics(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    results = TestResult.objects.filter(test=test)
    user_stats = results.values('user__username').annotate(
        count=Count('id'),
        avg_score=Avg('score')
    )
    overall_stats = results.aggregate(
        total_attempts=Count('id'),
        average_score=Avg('score')
    )

    return render(request, 'testapp/test_statistics.html', {
        'test': test,
        'user_stats': user_stats,
        'overall_stats': overall_stats
    })


# PDF

from django.templatetags.static import static
import shutil
import tempfile
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encoding='UTF-8', link_callback=None)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def generate_pdf(request):
    font_path = r'C:\Windows\Fonts\SEGOEUIL.ttf'

    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font file not found: {font_path}")

    temp_font_path = os.path.join(tempfile.gettempdir(), 'SEGOEUIL.ttf')
    shutil.copy(font_path, temp_font_path)
    context = {'path': temp_font_path}
    return render_to_pdf('testapp/pdf.html', context)



from reportlab.lib.units import inch
from reportlab.lib.colors import pink, green, brown, white


def some_view(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    c = User.objects.all()
    r = [q for q in c]
    pdfmetrics.registerFont(TTFont('MyFont', 'C:\Windows\Fonts\SEGOEUIL.ttf'))
    p.setFont('MyFont', 12)
    my_string = ",".join(str(element) for element in r)

    x = 0
    dx = 0.4 * inch
    for i in range(4):
        for color in (pink, green, brown):
            p.setFillColor(color)
    p.rect(x, 0, dx, 3 * inch, stroke=0, fill=1)
    x = x + dx
    p.setFillColor(white)
    p.setStrokeColor(white)

    p.drawCentredString(2.75 * inch, 1.3 * inch, my_string)
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="logs.pdf")


from reportlab.lib.pagesizes import letter
from reportlab.lib import colors, styles
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph

def create_certificate(request, test_id):
    test = get_object_or_404(Test, pk=test_id)

    # Создаем PDF-файл
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{request.user.first_name}_certificate.pdf"'



    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    pdfmetrics.registerFont(TTFont('MyFont', 'C:\Windows\Fonts\SEGOEUIL.ttf'))
    c.setFont('MyFont', 12)

    # Фон
    c.setFillColor(colors.lightblue)
    c.rect(0, 0, width, height, fill=1)

    # Заголовок
    c.setFont("MyFont", 36)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height - 100, "Сертификат о прохождении курса")

    # Имя
    c.setFont("MyFont", 24)
    c.drawCentredString(width / 2, height - 200, f"Этот сертификат подтверждает, что")

    c.setFont("MyFont", 30)
    c.drawCentredString(width / 2, height - 250, f'{request.user.last_name} {request.user.first_name}')

    # Название курса
    c.setFont("MyFont", 24)
    c.drawCentredString(width / 2, height - 300, f"успешно прошел курс")


    c.setFont("MyFont", 32)
    c.setFillColor(colors.red)
    c.drawCentredString(width / 2, height - 350, f'<<{test.title}>>')

    # Дата
    c.setFont("MyFont", 18)
    c.setFillColor(colors.black)
    now = datetime.now()
    f_date = now.strftime("%d %B %Y")
    months = {
        "January": "Января",
        "February": "Февраля",
        "March": "Марта",
        "April": "Апреля",
        "May": "Мая",
        "June": "Июня",
        "July": "Июля",
        "August": "Августа",
        "September": "Сентября",
        "October": "Октября",
        "November": "Ноября",
        "December": "Декабря",
    }
    for eng, rus in months.items():
        f_date = f_date.replace(eng, rus)
    c.drawCentredString(width / 2, height - 450, f"Дата: {f_date}")

    # Подпись
    c.setFont("MyFont", 18)
    c.drawCentredString(width / 2, height - 500, "____________________________")
    c.drawCentredString(width / 2, height - 520, "Подпись Директора")

    # Добавление ручной подписи
    sign_path = "testapp/static/img/sign4.png"
    sign_x = (width - 150) / 2
    sign_y = height - 520

    c.drawImage(sign_path, sign_x, sign_y, width=150, height=60, mask='auto')

    # Генерация QR-кода
    import qrcode
    qr_data = f"{request.user.first_name} - {test.title}"
    qr_img = qrcode.make(qr_data)
    qr_img_path = "temp_qr.png"
    qr_img.save(qr_img_path)

    # Добавление QR-кода в PDF
    c.drawImage(qr_img_path, (width - 80) / 2, height - 650, width=80, height=80)

    c.showPage()
    c.save()

    return response

# APIs ReadOnly
def render_api(request):
    return render(request, 'testapp/apis.html')

from django.conf import settings
import openai
import google.generativeai as genai

genai.configure(api_key=settings.GEMINI_API_KEY)
def questions(request):
    response_text = None

    if request.method == 'POST':
        form = ChatbotForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['message']

            try:
                model = genai.GenerativeModel("gemini-1.5-pro")
                response = model.generate_content(user_input)
                response_text = response.text
            except Exception as e:
                response_text = f"Ошибка: {str(e)}"
    else:
        form = ChatbotForm()

    # models = list(genai.list_models())
    # for model in models:
    #     print(model)

    return render(request, 'testapp/questions.html', {
        'form': form,
        'response_text': response_text
    })



# def face_detections(request):
#     return render(request, 'testapp/face_detections.html')


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
import cv2
import numpy as np
from deepface import DeepFace



@csrf_exempt  # Отключаем проверку CSRF для этого эндпоинта
def face_detections(request):
    if request.method != "POST":
        context = {
            "access": False,
            "message": "Неверный метод"
        }
        return render(request, 'testapp/face_detections.html', context)

    # Получаем изображение
    image_file = request.FILES.get('face_image')
    if not image_file:
        context = {
            "access": False,
            "message": "Файл не получен"
        }
        return render(request, 'testapp/face_detections.html', context)

    # Сохраняем изображение временно
    filename =f"{uuid.uuid4().hex}.jpg"
    file_path = default_storage.save(filename, ContentFile(image_file.read()))

    full_path = default_storage.path(file_path)

    try:
        # Анализируем изображение (пол, возраст)
        analysis = DeepFace.analyze(img_path=full_path, actions=['age', 'gender'], enforce_detection=False)[0]
        age = analysis.get("age", 0)
        gender = analysis.get("gender", "").lower()

        # Условие для доступа
        if gender == "man" and age >= 18:
            context = {
                "access": True,
                "message": "Доступ разрешён",
                "redirect_url": "/profile"
            }
        else:
            context = {
                "access": False,
                "message": f"Доступ запрещён: {gender}, {age} лет"
            }

        return render(request, 'testapp/face_detections.html', context)

    except Exception as e:
        print("[ERROR] Ошибка анализа лица:", e)
        context = {
            "access": False,
            "message": "Ошибка анализа лица"
        }
        return render(request, 'testapp/face_detections.html', context)


class ApiQuestionsViewset(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuestionFilter
class ApiTestViewset(ReadOnlyModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class ApiAnswerViewset(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnswerFilter

class ApiUserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


