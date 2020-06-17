from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, UpdateView, ListView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from .serializers import *
from .models import Leave
from .forms import *


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return HttpResponse('Check Your Login Creds...')
    return render(request, 'MyApp/login.html')


@login_required(login_url='login/')
def index(request):
    return render(request, 'MyApp/home.html')


class LeaveCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Leave
    fields = ['start_date', 'end_date', 'start_time', 'end_time', 'why_leave']

    def form_valid(self, form):
        student = Student.objects.get(user=self.request.user)
        form.instance.student = student
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_student:
            return True
        return False


class LeaveUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Leave
    fields = ['is_accepted', 'comment', 'is_rejected']

    def test_func(self):
        if self.request.user.is_mentor:
            return True
        return False


class LeaveListView(LoginRequiredMixin, ListView):
    model = Leave
    template_name = 'MyApp/leave_list.html'
    context_object_name = 'leaves'
    queryset = Leave.objects.all().order_by('id')


def register(request):
    return render(request, "MyApp/signup.html")


def student_register(request):
    form = StudentRegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.set_password(user.password)
        user.is_student = True
        user.save()
        return redirect('index')
    return render(request, "MyApp/student-signup.html", {'form': form})


def mentor_register(request):
    form = MentorRegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.set_password(user.password)
        user.is_mentor = True
        user.save()
        return redirect('index')
    return render(request, "MyApp/mentor-signup.html", {'form': form})


def warden_register(request, *args, **kwargs):
    form = WardenRegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.set_password(user.password)
        user.is_warden = True
        user.save()
        return redirect('index')
    return render(request, "MyApp/warden-signup.html", {'form': form})


# Endpoints

@login_required(login_url='login/')
@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'All Leave Applications': 'http://127.0.0.1:8000/api/list/',
        'Create Leave Application': 'http://127.0.0.1:8000/api/create/',
        'Authorize LEave Application': 'http://127.0.0.1:8000/api/update/<int:pk>/',
    }

    return Response(api_urls)


class LeaveList(LoginRequiredMixin, generics.ListAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveListSerializer


class LeaveCreate(LoginRequiredMixin, UserPassesTestMixin, generics.ListCreateAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveCreateSerializer

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)

    def test_func(self):
        if self.request.user.is_student:
            return True
        return False


class LeaveUpdate(LoginRequiredMixin, UserPassesTestMixin, generics.UpdateAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)

    def test_func(self):
        if self.request.user.is_mentor:
            return True
        return False
