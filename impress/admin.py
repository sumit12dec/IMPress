from django.contrib import admin
from .models import UserPoints, UserData, UserPointHistory, UserQuestion, QuestionHistory, NextQuestionLink

class UserPointsAdmin(admin.ModelAdmin):
    pass
class UserDataAdmin(admin.ModelAdmin):
    pass
class UserPointHistoryAdmin(admin.ModelAdmin):
	pass
class UserQuestionAdmin(admin.ModelAdmin):
	pass
class QuestionHistoryAdmin(admin.ModelAdmin):
	pass
class NextQuestionLinkAdmin(admin.ModelAdmin):
	pass
admin.site.register(UserPoints, UserPointsAdmin)
admin.site.register(UserData, UserDataAdmin)
admin.site.register(UserPointHistory, UserPointHistoryAdmin)
admin.site.register(UserQuestion, UserQuestionAdmin)
admin.site.register(QuestionHistory, QuestionHistoryAdmin)
admin.site.register(NextQuestionLink, NextQuestionLinkAdmin)