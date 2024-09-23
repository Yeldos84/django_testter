from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('questions', views.ApiQuestionsViewset)
router.register('tests', views.ApiTestViewset)

urlpatterns = [
    path("", views.index, name="index"),
    path('login', views.login, name='login'),
    path("base", views.index, name="base"),
    path("pdf", views.some_view, name="pdf"),
    path("pdf2", views.generate_pdf, name="pdf"),
    path('certificate/<int:test_id>', views.create_certificate, name='create_certificate'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('upload/', views.upload_photo, name='upload_photo'),
    path('logout', views.logout, name='logout'),
    path('password_reset', auth_views.PasswordResetView.as_view(template_name='testapp/password_reset.html'),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='testapp/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='testapp/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='testapp/password_reset_complete.html'), name='password_reset_complete'),
    path('test', views.test_list, name='test_list'),
    path('test/<int:test_id>/', views.test_detail, name='test_detail'),
    path('test/<int:test_id>/submit/', views.submit_test, name='submit_test'),
    path('test/<int:test_id>/statistics/', views.test_statistics, name='test_statistics'),
    path('apis/', views.render_api, name='apis'),
    path('api/', include(router.urls)),




]




