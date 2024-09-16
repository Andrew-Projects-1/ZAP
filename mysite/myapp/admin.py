from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.QuestionModel)
admin.site.register(models.AnswerModel)
admin.site.register(models.RantsQuestionModel)
admin.site.register(models.RantsAnswerModel)
admin.site.register(models.Profile)
admin.site.register(models.Room)
admin.site.register(models.Message)
admin.site.register(models.ThreadModel)
admin.site.register(models.MessageModel)
admin.site.register(models.Notification)