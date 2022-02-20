from django.urls import path

from note import views

urlpatterns=[

    path('all',views.list_view),
    path('add',views.add_note),
    path('updated/<int:note_id>',views.updated_note),
    path('deleted',views.delete_note),

]