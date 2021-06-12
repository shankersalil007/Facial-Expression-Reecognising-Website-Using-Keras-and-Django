from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
import os
from .models import *
import cv2
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import numpy as np
from django.http.response import StreamingHttpResponse
from faceapp1.camera import VideoCamera


# Create your views here.


@login_required(login_url='login-h')
def home(request):
    return render(request, 'index.html')

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')


def loginpage(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
        except:
            messages.warning("Fill the details")
        if user is not None:
            login(request, user)

            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, 'Account was created for ' + username)

            return redirect('login-h')
    context = {'form': form}
    return render(request, 'register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login-h')


def photo(request):
    if request.method == 'POST':
        form = photo_forms(request.POST, request.FILES)
        print(os.getcwd())
        dir = 'C:/Users/reshm/Documents/pythonProject/face_aadhar/face/Images'
        for root, dirs, files in os.walk(dir):
            for file in files:
                path = os.path.join(dir, file)
                print(path)
                os.remove(path)
        if form.is_valid():
            form.save()
            new_model = tf.keras.models.load_model('data/iris_model2.h5')
            path = 'C:/Users/reshm/Documents/pythonProject/face_aadhar/face/Images'
            for root, dirs, files in os.walk(dir):
                for file in files:
                    path = os.path.join(dir, file)
                    print(path)
            img_width, img_height = 224, 224
            img = image.load_img(path, target_size=(img_width, img_height))
            out = np.expand_dims(img, axis=0)
            final_img = out / 255.0

            pred = new_model.predict(final_img)
            max_index = np.argmax(pred[0])
            print(max_index)
            values = (1,10,11,12,13,14,15,16,17,18,19,2,20,21,22,23,24,25,26,27,28
                      ,29,3,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,5,6,7,8,9)
            predicted = values[max_index]
            print(pred[0])
            print(predicted)
            var = person.objects.all()
            detail= None
            for i in var:
                if i.id == predicted:
                    detail = i
            return render(request, 'urls.html', {'msg': predicted,'detail':detail})
    else:
        form = photo_forms()
    return render(request, 'photo.html', {'form': form})