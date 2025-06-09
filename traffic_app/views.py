# traffic_app/views.py

from django.http import JsonResponse
from .status import status_data
from django.shortcuts import render

from django.http import StreamingHttpResponse
from .video_stream import gen_frames

from django.http import StreamingHttpResponse
from .video_stream import gen_frames  # Ensure this path is correct

from django.http import JsonResponse

def get_status(request):
    data = {
        "total": 15,
        "route_a": 8,
        "route_b": 7,
        "emergency": True,
        "emergency_type": "Ambulance",
        "light": "green",  # red | yellow | green
        "timer": 10,
        "accuracy": {
            "car": 89.5,
            "truck": 91.2,
            "bus": 88.3,
            "ambulance": 94.7
        }
    }
    return JsonResponse(data)


def video_feed(request):
    return StreamingHttpResponse(
        gen_frames(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


def video_feed(request):
    return StreamingHttpResponse(gen_frames(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def dashboard(request):
    return render(request, 'traffic_app/dashboard.html')

def get_status(request):
    return JsonResponse(status_data)
