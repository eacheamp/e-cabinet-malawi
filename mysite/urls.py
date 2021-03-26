"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler400, handler403, handler404, handler500


from mysite.e_cab import views

urlpatterns = [
    path('home/', views.Home.as_view(), name='home'),
    path('', views.new_home.as_view(), name='newhome'),

    path('about/', views.About.as_view(), name='about'),

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    #path('motion/upload/', views.upload_motion, name='upload_motion'),

    path('cabinetdebrief/', views.cabinet_results, name='cabinet_results'),
    #path('cabinetroom/', views.motion_list, name='motion_list'),
    path('<int:pk>/vote', views.VoteMotionView.as_view(), name='vote_motion'),

    path('After_vote/', views.After_vote.as_view(), name='After_vote'),

    path('chair_list/', views.chair_list, name='chair_list'),

    path('<int:pk>/chair_desc', views.Chair_Desc.as_view(), name='chair_desc'),

    path('<int:pk>/motion_pass', views.Motion_pass.as_view(), name='motion_pass'),
    path('<int:pk>/motion_fail', views.Motion_fail.as_view(), name='motion_fail'),

    path('chairdecision/', views.final_ruling, name='final_ruling'),

    path('e-cabinet/', views.e_cabinet, name='e-cabinet'),

    path('admin/', admin.site.urls),
]

handler400 = 'mysite.e_cab.views.error_400_view'
handler403 = 'mysite.e_cab.views.error_403_view'
handler404 = 'mysite.e_cab.views.error_404_view'
handler500 = 'mysite.e_cab.views.error_500_view'

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # strictly for development, should not be used in production
