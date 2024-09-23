from django.contrib import admin
from .models import Test, Question, Answer, Result, TestResult, ProfilePhoto

class TestResultAdmin(admin.ModelAdmin):
    list_display = ['test', 'user', 'score']
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


admin.site.register(Answer)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Test)
admin.site.register(Result)
admin.site.register(ProfilePhoto)
admin.site.register(TestResult, TestResultAdmin)
