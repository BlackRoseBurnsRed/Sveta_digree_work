from django.template import Context
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from timetable import models
from django.views.decorators.csrf import csrf_protect,  csrf_exempt, requires_csrf_token
from timetable import models
from django.forms.models import model_to_dict

# Create your views here.

last_created_schedule = dict()


#Return true if there is this subject at the day
def check_subject_at_day(day, subject_id):
    try:
        day.index(subject_id)
        return False
    except ValueError:
        if len(day) == 4:
            return False
        return True

def make_dicts_for_schedule(schedule):
    res = []
    day_index = 0
    for weekday in schedule:
        index = 0
        day = []
        while index < len(weekday):
            lesson = dict()
            lesson['lesson'] = index + 1
            lesson['subject'] = models.Subject.objects.get(id=weekday[index]).name
            lesson['subject_id'] = weekday[index]
            index = index + 1
            day.append(lesson)
        res.append({'lessons': day, 'day_index': day_index})
        day_index = day_index + 1
    return res

def cfsHandler(class_number):
    curriculum = []
    for i in list(models.StudyPlan.objects.filter(class_number=int(class_number))):
        curriculum.append(model_to_dict(i))
    schedule_by_week = [[], [], [], [], []]

    for item in curriculum:
        if models.Subject.objects.get(id=item['subject_id']).need_spec_audience != 0:
            continue
        hours = 0
        while hours < int(item['hours']):
            for weekday in schedule_by_week:
                if hours == int(item['hours']):
                    break
                if check_subject_at_day(weekday, item['subject_id']):
                    hours = hours + 1
                    weekday.append(item['subject_id'])
                    continue
            break

    return schedule_by_week


def index(request):
    args = dict()
    args['user'] = auth.get_user(request)
    return render_to_response('timetable_template1.html', args)


@csrf_exempt
def create_special_schedule(request):
    args = dict()
    args['user'] = auth.get_user(request)
    if request.method == "POST" and request.POST:
        class_number = request.POST.get('class_number', '')
        class_liter = request.POST.get('class_number', 'liter')
        args['class_number'] = class_number
        args['class_liter'] = class_liter
        return render_to_response('created_scheduele.html', args)
    else:
        return render_to_response('create_special_scheduele.html', args)


@csrf_exempt
def create_fixed_schedule(request):
    args = dict()
    args['user'] = auth.get_user(request)
    if request.method == "POST" and request.POST:
        class_number = request.POST.get('class_number', '')
        class_liter = request.POST.get('class_liter', '')
        args['class_number'] = class_number
        args['class_liter'] = class_liter
        last_created_schedule['lessons'] = make_dicts_for_schedule(cfsHandler(int(class_number)))
        last_created_schedule['class_number'] = class_number
        last_created_schedule['class_liter'] = class_liter
        last_created_schedule['teacher'] = models.Class.objects.get(number=class_number, liter=class_liter).teacher_id
        args['schedule'] = last_created_schedule['lessons']
        print(args['schedule'])
        return render_to_response('created_scheduele.html', args)
    else:
        return render_to_response('create_fixed_scheduele.html', args)

@csrf_exempt
def save_schedule(request):
    args = dict()
    args['user'] = auth.get_user(request)
    class_number = last_created_schedule['class_number']
    class_liter = last_created_schedule['class_liter']
    teacher_id = last_created_schedule['teacher']
    day_index = 0
    for day in last_created_schedule['lessons']:
        for lesson in day['lessons']:
            subject_id = lesson['subject_id']
            lesson_number = lesson['lesson']
            one_lesson  = models.Scheduele(
                class_number = class_number,
                class_liter = class_liter,
                weekday = day_index,
                lesson_number = lesson_number,
                subject_id = subject_id,
                teacher_id = teacher_id
            )
            one_lesson.save()
        day_index = day_index + 1

    return render_to_response('succes_saved.html', args)


@csrf_exempt
def edit_schedule(request):
    args = dict()
    args['user'] = auth.get_user(request)
    if request.method == "POST" and request.POST:
        return render_to_response('succes_saved.html', args)

    args['schedule'] = last_created_schedule['lessons']
    return render_to_response('edit_scheduele.html', args)