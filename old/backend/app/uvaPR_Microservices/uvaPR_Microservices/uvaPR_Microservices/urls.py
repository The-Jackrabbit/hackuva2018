"""uvaPR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from mainApp import views
from rest_framework import routers


# View sets have default methods for handling GET/POST/etc, so this is explicitly overriding that
request_override_map = {
   'get': 'get',
	'post': 'post',
	'put': 'put',
}
user_list = views.UserViewSet.as_view(request_override_map)
season_list = views.SeasonViewSet.as_view(request_override_map)
tournament_list = views.TournamentViewSet.as_view(request_override_map)
set_list = views.SetViewSet.as_view(request_override_map)
game_list = views.GameViewSet.as_view(request_override_map)

upload_image = views.FileUploadViewSet.as_view({'post': 'perform_create'})

urlpatterns = [
	# API
	url(r'^api/image/upload/', views.upload_image, name='upload_image'),
	
	# VIEWS
	
   url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Needed to route static files
