"""
URL configuration for instagram_copy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html"), name="home"),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('world/', include('world.urls')),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password/password_reset.html'), name="password_reset"),
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_form.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    ]

'''
    1. submit email form                        //PasswordResetView.as_view()
    2. Email sent success message               //PasswordResetDoneView.as_view()
    3. Link to password reset form in email     //PasswordResetConfirmView.as_view()
    4. Password successfully changed message    //PasswordResetCompleteView.as_view()
'''

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


