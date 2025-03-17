from datetime import datetime
import base64
import json

from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie

from .recognizer import compare_images2
from .models import Attendance, Attendee

@login_required(login_url='/login/')
def dashboard(request):
    user_id = request.user.id
    authorized_people = Attendee.objects.filter(owner=request.user)
    
    return render(request, 'user_dashboard.html', {
        'user_id': user_id,
        'username': request.user.email.split('@')[0],
        'authpeople': authorized_people,
        'imgs_exist': bool(authorized_people.count()),
        'attendance': Attendance.objects.filter(owner=request.user)
    })

def login_page(request:HttpRequest):
    if request.user.is_authenticated:
        return redirect(f'/dashboard/')
    
    if request.method.lower() == 'post':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request,
                            email=email,
                            password=password)
        
        if user is not None:
            login(request, user)
            print("djewdedwjd")
            return redirect(f'/dashboard/')
        else:
            return redirect("/signup/")

    return render(request, 'login.html', {})

def logout_view(request):
    logout(request)

    return redirect('/login/')

@login_required(login_url="/login/")
def create_attendance(request):
    name = request.POST["attendance-name"]
    time = datetime.now()
    Attendance.objects.create(attendance_name=name, owner=request.user, status="ongoing")

    return redirect("/dashboard/")

@login_required(login_url='/login/')
def attendance_profile_page(request, att_id):
    user = request.user
    try:
        attendance = Attendance.objects.get(att_id=att_id, owner=user)
    except Attendance.DoesNotExist:
        return HttpResponse(status=404)
    
    attendees = []
    for attendee in Attendee.objects.filter(owner=user):
        if attendance in attendee.attendances.all():
            attendees.append(attendee)

    return render(request, "attendance_profile.html",{
        "attendance": attendance.attendance_name,
        "attendees": attendees
    })

# @csrf_protect
def mark_attendance(request):
    body = json.loads(request.body)
    imageData = body["image"]
    att_id = body["attId"]
    # print(imageData)
    try:
        attendance = Attendance.objects.get(att_id=att_id)
        attendees = Attendee.objects.filter(owner=request.user)
        if not attendees:
            return JsonResponse({"status": "Face is unregistered. Contact the owner of this attendance", }, status=401)
        
        for attendee in attendees:
            is_match = compare_images2(imageData, bytes(attendee.image, "utf8"))
            if is_match:
                print("mat")
                attendee.attendances.add(attendance)
                return JsonResponse({'status': 'success', 'name': 
                attendee.name})
            print("no match")
            return JsonResponse({'status': 'unrecognized'})
    except Exception as error:
        print(error)
        return JsonResponse({"status": "error"}, status=500)
    

@ensure_csrf_cookie
def attendance_view(request, att_id:int, shortened_name:str):
    try:
        attendance = Attendance.objects.get(att_id=att_id)
    except Attendance.DoesNotExist:
        return HttpResponse(status=404)
    
    if attendance.attendance_name.replace(" ", "_")[:10] != shortened_name:
        return HttpResponse(status=404)
    
    return render(request, 'attendance.html', {
        'attendance_name': attendance.attendance_name,
        'att_id': att_id
        })

def signup_page(request):
    if request.method.lower() == 'post':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.create(username=email, email=email, password=password)
            login(request, user)
            return redirect('/dashboard/')
        except Exception as error:
            print(error, type(error))
            error_msg = "Email has already been registered. Try signing up"
            return render(request, 'signup.html', {'error': error_msg})

    return render(request, 'signup.html', {'error': None})

def verify_user_exists(user_id):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return False
    
    return user

def process_uploaded_data(request):
    if request.method == 'POST' and request.FILES.get('person-image'):
        image_file = request.FILES['person-image']
        if image_file.content_type == 'image/jpeg':
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            print(image_data)
            name = request.POST['name']
            # attendance = Attendance.objects.get(owner=request.user, status="ongoing")
            owner = request.user
            Attendee.objects.create(name=name, image=image_data, owner=owner)
            
            # return JsonResponse({'status': 'success'})
            return redirect("/dashboard/")
        else:
            # return JsonResponse({'status': 'failed', 'message': 'Invalid file type'}, status=400)
            return redirect("/dashboard/")
    # return JsonResponse({'status': 'failed', 'message': 'Invalid request'}, status=400)
    return redirect("/dashboard/")
