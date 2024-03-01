from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "webpages"

urlpatterns=[
    path('',views.index, name='index'),
    path('register/',views.register, name='register'),
    path('index',views.index,name="index"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='sign_in'),
    path('logout/',  views.logout, name='logout'),

    path('about', views.about, name="about"),
    path('contact', views.contact, name="contact"),
    path('products', views.products, name="products"),
    path('future', views.future, name="future"),
    path('single-product', views.single_product, name="single-product"),
    path('student',  views.student, name='student', kwargs={"student_id": ''}),
    path('professor',  views.professor, name='professor', kwargs={"professor_id": ''}),
    # path('college',  views.college, name='college', kwargs={"college_id": ''}),
    #path('footer', views.footer, name="footer"),
    #path('ex', views.ex, name="ex"),

    path('profile', views.profile, name="profile"),
    path('notes', views.notes, name='notes'),
    path('colleges', views.colleges, name='colleges'),
    path('save-note', views.saveNote, name='savenotes'),
    path('downloadnote', views.downloadnote, name='downloadnote'),
    path('delete-note', views.deleteNote, name='deletenotes')
]