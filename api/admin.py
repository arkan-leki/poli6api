from django.contrib import admin

from api.models import Account, Answare, Question, Quize, Result

# Register your models here.
admin.site.register(Account)
admin.site.register(Quize)

class AnswaresInline(admin.TabularInline):
    model = Answare

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswaresInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answare)
admin.site.register(Result)
