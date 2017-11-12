from django.contrib import admin
from .models import UserPoints, UserData, UserPointHistory, UserQuestion, QuestionHistory, NextQuestionLink

class UserPointsAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name', 'user_age',
    				'user_sex', 'user_rs', 'user_location',
    				'user_points')
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('user_id_fk', 'user_likes', 'user_dislikes')
class UserPointHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_points_taken', 'point_deviation_timestamp')
class UserQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'question_text', 'question_options', 'question_scores')
class QuestionHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'question_id', 'question_answer')
class NextQuestionLinkAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'question_options', 'next_question_id')

admin.site.register(UserPoints, UserPointsAdmin)
admin.site.register(UserData, UserDataAdmin)
admin.site.register(UserPointHistory, UserPointHistoryAdmin)
admin.site.register(UserQuestion, UserQuestionAdmin)
admin.site.register(QuestionHistory, QuestionHistoryAdmin)
admin.site.register(NextQuestionLink, NextQuestionLinkAdmin)