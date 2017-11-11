from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import uuid
import apiai
import time
import json
from django.views.decorators.csrf import csrf_exempt
from .models import UserPoints, UserData, UserPointHistory, UserQuestion, QuestionHistory
from django.core import serializers
from shutil import copyfile

#BASE = '/Users/sumit/Desktop/instamojo/instasleuth'
BASE = '/var/www/'

@csrf_exempt
def post_user_text(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user_query = request.POST.get('user_query')
        question_id = request.POST.get('question_id', None)
        
    ai = apiai.ApiAI(settings.CLIENT_ACCESS_TOKEN)

    session_id = uuid.uuid4().hex

    entries = [
        apiai.UserEntityEntry('Firefox', ['Firefox']),
        apiai.UserEntityEntry('XCode', ['XCode']),
        apiai.UserEntityEntry('Sublime Text', ['Sublime Text'])
    ]

    user_entities_request = ai.user_entities_request(
        [
            apiai.UserEntity("Application", entries, session_id)
        ]
    )

    user_entities_response = user_entities_request.getresponse()

    print 'Upload user entities response: ', (user_entities_response.read())

    request = ai.text_request()

    request.session_id = session_id
    request.query = user_query

    response = request.getresponse()
    a = json.loads(response.read())
    intent_name = a['result']['metadata']['intentName']

    if intent_name == 'Welcome Intent':
        obj = UserQuestion.objects.all()[0]
        next_question_to_ask =  obj.question_text
        next_question_id = obj.question_id
        print next_question_to_ask, "next_question_to_ask"
        res = {'question': next_question_to_ask,
                'options': None, 'question_id': next_question_id}
        return JsonResponse(res)

    if question_id:
        obj = QuestionHistory(user_id=user_id,
                        question_id=question_id,
                        question_answer=user_query)
        obj.save()
        print type(question_id), question_id, "ok"
        q_obj = UserQuestion.objects.get(question_id=int(question_id)+1)
        print q_obj.question_text,"question_id"
        # for o in q_obj:
        #     print q_obj.o
        next_question_to_ask =  q_obj.question_text
        print next_question_to_ask
        next_question_id = q_obj.question_id
        options = q_obj.question_options
        scores = q_obj.question_scores

        res = {'question': next_question_to_ask,
                'options': options, 'scores': scores,
                 'question_id': next_question_id,}
        return JsonResponse(res)



@csrf_exempt
def user_points(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        latest_user_points = request.POST.get('user_points')
        print user_id, latest_user_points
        obj = UserPointHistory(user_id=user_id, user_points_taken=latest_user_points)
        obj.save()
        obj = UserPoints.objects.get(user_id=user_id)
        # objs = UserPoints.objects.all()
        # de_objs = [{'user_id':o.user_id, 'user_points': o.user_points} for o in objs]
        # print de_objs
        print obj.user_points, "is it null"
        obj.user_points += int(latest_user_points)
        obj.save()
        return JsonResponse({'user_points': obj.user_points})

    if request.method == "GET":
        user_id = request.GET.get('user_id')
        obj = UserPoints.objects.get(user_id=user_id)
        print obj.user_id, "popo", obj.user_points
        return JsonResponse({'user_points': obj.user_points})





