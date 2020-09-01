from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
	path('index/', views.index, name='index'),
    path('index/predaja/', views.thesis_submission, name='submission'),
    path('index/<int:thesis_id>/predaja/', views.thesis_update, name='update'),
    path('obavijesti/', views.notifications, name='notifications'),
    path('obavijesti/označi/sve/kao/pročitane/', views.notifications_mark_read, name='notifications_mark_read'),
    path('profil/<int:user_id>/', views.profile, name='profile'),
    path('prikaz/<int:thesis_id>/', views.thesis_display, name='thesis_display'),
    path('provjera/izvornosti/', views.generate_verification, name='generate_verification'),
    path('mentor/promjena/statusa/', views.mentor_status_change, name='mentor_status_change'),
    path('student/promjena/statusa/', views.student_status_change, name='student_status_change'),
    path('student/zamjena/datoteke/', views.student_document_change, name='student_document_change'),
    path('predsjednik/promjena/statusa/', views.president_status_change, name='president_status_change'),
    path('dodavanje/clanova/odbora/', views.add_comitee, name='add_comitee'),
    path('dodavanje/ocjene/rada/i/obrane/', views.add_grade, name='add_grade'),
    path('dodavanje/konacne/ocjene/', views.add_final_grade, name='add_final_grade'),

]
