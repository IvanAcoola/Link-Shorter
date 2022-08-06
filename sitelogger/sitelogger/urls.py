from django.contrib import admin
from django.urls import path
from loggerapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view),
    path('profile/', profile_view),
    path('<str:last>/', index),
    path('', none_page)
]
