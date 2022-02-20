from django.urls import path

from user import views

urlpatterns=[

    path('reg',views.reg_view),
    path('login',views.login_view),
    path('logout',views.logut_view),

]