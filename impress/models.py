from django.db import models

class UserPoints(models.Model):
	user_id = models.AutoField(primary_key=True)
	user_name = models.CharField(max_length=100)
	user_age = models.CharField(max_length=100)
	user_sex = models.CharField(max_length=100)
	user_rs = models.CharField(max_length=100)
	user_location = models.CharField(max_length=100)
	user_points = models.IntegerField(max_length=100)


class UserData(models.Model):
	user_id_fk = models.ForeignKey(UserPoints, db_column="user_id")
	user_likes = models.CharField(max_length=2000)
	user_dislikes = models.CharField(max_length=2000)

class UserPointHistory(models.Model):
	user_id = models.IntegerField(max_length=100)
	user_points_taken = models.IntegerField(max_length=2000)
	point_deviation_timestamp = models.DateTimeField(auto_now_add=True, blank=True)

class UserQuestion(models.Model):
	# user_id_fk = models.ForeignKey(UserPoints, db_column="user_id")
	question_id = models.IntegerField(max_length=2000, primary_key=True)
	question_text = models.CharField(max_length=2000)
	question_options = models.CharField(max_length=2000, blank=True)
	question_scores = models.CharField(max_length=2000, blank=True)


class QuestionHistory(models.Model):
	user_id = models.IntegerField(max_length=100)
	question_id = models.IntegerField(max_length=100)
	question_answer = models.CharField(max_length=1000)







