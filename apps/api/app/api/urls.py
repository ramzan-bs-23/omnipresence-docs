"""
API URL configuration for Omnipresence.
"""
from django.urls import path
from .views import auth

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', auth.login_view, name='login'),
    path('auth/logout/', auth.logout_view, name='logout'),
    path('auth/me/', auth.me_view, name='me'),

    # Other API endpoint modules will be included here:
    # path('participants/', include('app.api.participants.urls')),
    # path('groups/', include('app.api.groups.urls')),
    # path('sessions/', include('app.api.sessions.urls')),
    # path('presence/', include('app.api.presence.urls')),
    # path('reports/', include('app.api.reports.urls')),
    # path('admin/', include('app.api.admin.urls')),
    # path('notifications/', include('app.api.notifications.urls')),
]
