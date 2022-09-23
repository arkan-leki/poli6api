from django.contrib import admin

from api.models import Account, Question, Answare, Quize, Result

# Register your models here.
admin.site.register(Account)

class QuizeAdmin(admin.ModelAdmin):
    model = Quize
    list_display = ['category', 'imageURL', 'questions']

admin.site.register(Quize,QuizeAdmin)

class AnswaresInline(admin.TabularInline):
    model = Answare

class QuestionAdmin(admin.ModelAdmin):
    model = Question
    list_display = ('text', 'quize', 'correct_answare')
    list_filter = ['quize']
    inlines = [AnswaresInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answare)
admin.site.register(Result)
