"""
URL configuration for facebook project.

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
from django.conf import settings
from django.conf.urls.static import static
from mainApp import views
from .views import *

urlpatterns = [
    path('api/facebook-leads/', FacebookLeadsView.as_view(), name='facebook-leads-api'),
    path('api/create-monday-leads/', FacebookLeadMondayView.as_view(), name='facebook-monday-api'),
    path('api/monday-data/', MondayDataView.as_view(), name='monday-data-api'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
