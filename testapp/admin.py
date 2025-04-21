from django.contrib import admin
from .models import Test, Question, Answer, Result, TestResult, ProfilePhoto
from django.contrib import messages
from django.core.management import call_command
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['test', 'user', 'score', 'passed']
    # search_fields = ['name']
    # list_editable = ['digit_field']
    ordering = ['test']
    # list_per_page = 5
    # list_filter = ['name', 'birth_date']


# class TestAnswerAdmin(admin.ModelAdmin):
#     list_display = ['question', 'text', 'is_correct']
#     search_fields = ['question']
#     # list_editable = ['digit_field']
#     ordering = ['question']
#     # list_per_page = 5
#     # list_filter = ['name', 'birth_date']


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

@admin.action(description="🎲 Сгенерировать фейковые тесты и обучить ИИ")
def generate_fake_and_train(modeladmin, request, queryset):
    try:
        call_command('generate_all_fake')
        messages.success(request, "Генерация и обучение завершены!")
    except Exception as e:
        messages.error(request, f" Ошибка: {str(e)}")


class TestAdmin(admin.ModelAdmin):
    list_display = ('title',)
    actions = [generate_fake_and_train]




admin.site.register(Answer)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Result)
admin.site.register(ProfilePhoto)
admin.site.register(TestResult, TestResultAdmin)
