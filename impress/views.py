from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import uuid
import apiai
import time
import json
from django.views.decorators.csrf import csrf_exempt
from .models import UserPoints, UserData, UserPointHistory, \
UserQuestion, QuestionHistory, NextQuestionLink
from django.core import serializers
from datetime import datetime as dt
from dateutil import tz
import matplotlib as mpl
mpl.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
#BASE = '/Users/sumit/Desktop/instamojo/instasleuth'
BASE = '/var/www/'

def get_user_points_history(user_id):
    obj = UserPointHistory.objects.filter(user_id=user_id)
    final_list = []
    utcnow = dt.utcnow().replace(tzinfo=tz.tzutc())
    print utcnow

    for o in obj:
        u_points = o.user_points_taken
        timestamp = o.point_deviation_timestamp
        secs = (utcnow - timestamp).seconds
        print secs, "secs"
        d = {'user_points_taken': u_points, 'secs_ago': secs/60}
        final_list.append(d)
    return final_list

def get_mood_plot(user_id):
    data = get_user_points_history(user_id)
    x = []
    y = []
    for o in data:
        x.append(o['secs_ago'])
        y.append(o['user_points_taken'])
    x = x[::-1]
    y = y[::-1]

    plt.plot(x, y, "o-", color='blue')
    filename = str(user_id)+'_mood_chart.png'
    plt.xlabel('Mins Ago', fontsize=18)
    plt.ylabel('Mood Level', fontsize=16)

    plt.savefig('/var/www/IMPress/static/' + filename)
    # with open(filename, 'wb+') as destination:
    #     for chunk in file.chunks():
    #         destination.write(chunk)
    time.sleep(2)
    return 'http://54.89.58.71/static/'+filename



@csrf_exempt
def get_user_plot(request, user_id):
    image_url = get_mood_plot(user_id)
    return HttpResponse(image_url)


@csrf_exempt
def post_user_text(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        user_query = request.POST.get('user_query')
        question_id = request.POST.get('question_id', None)
        question_option_clicked = request.POST.get('option_number_clicked', None)
        
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
        print question_option_clicked
        if question_option_clicked:
            nxt_ques_obj = NextQuestionLink.objects.get(question_id=int(question_id), question_options=int(question_option_clicked))
            print nxt_ques_obj
            print nxt_ques_obj.question_id
            print nxt_ques_obj.question_options
            next_question_id = nxt_ques_obj.next_question_id
            print next_question_id, "next_question_id"

            q_obj = UserQuestion.objects.get(question_id=int(next_question_id))
            next_question_to_ask =  q_obj.question_text
            print next_question_to_ask
            next_question_id = q_obj.question_id
            options = q_obj.question_options
            scores = q_obj.question_scores

            res = {'question': next_question_to_ask,
                    'options': options, 'scores': scores,
                     'question_id': next_question_id,}
            return JsonResponse(res)
        return HttpResponse("Something")



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





