from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(template_name='MyApp/logout.html'), name='logout'),
    path('register/', register, name='register'),
    path('student-register/', student_register, name='student-register'),
    path('warden-register/', warden_register, name='warden-register'),
    path('mentor-register/', mentor_register, name='mentor-register'),
    path('leave/new/', LeaveCreateView.as_view(), name='create'),
    path('leave/<int:pk>/update', LeaveUpdateView.as_view(), name='leave_update'),
    path('leave_list', LeaveListView.as_view(), name='leave_list'),
    path('api/', api_overview, name='endpoints'),
    path('api/list/', LeaveList.as_view(), name='endpoint-list'),
    path('api/create/', LeaveCreate.as_view(), name='endpoint-create'),
    path('api/update/<int:pk>/', LeaveUpdate.as_view(), name='endpoint-update'),
    path('', index, name='index')
]
