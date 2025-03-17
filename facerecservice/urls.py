from django.contrib import admin
from django.urls import path, resolve

from django.conf import settings
from django.conf.urls.static import static

import mainapp.views as views

urlpatterns = [
    path("login/", views.login_page),
    path("logout/", views.logout_view),
    path("signup/", views.signup_page),
    path("dashboard/", views.dashboard),
    path("upload/", views.process_uploaded_data),
    path("", views.dashboard),
    path("attendance/", views.mark_attendance),
    path("create-attendance/", views.create_attendance),
    path("attendance/<int:att_id>/<str:shortened_name>/", views.attendance_view),
    path("attendance-profile/<int:att_id>/", views.attendance_profile_page)
]

if settings.DEBUG:  # Only in development mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)