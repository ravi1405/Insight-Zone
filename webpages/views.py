from collections import UserDict
from django.contrib.auth.models import User
from django import forms
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import render, redirect , get_object_or_404
from django.contrib import messages
from .forms import RegisterForm , RatingForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db import models
from .models import Note, UserProfile, College , Semester ,Rating 
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
import magic

@login_required(login_url="/login/")
def deleteNote(request):
    if request.method == "POST":
        note_id = request.POST.get('note-id','')
        print("++++++")
        print(note_id)
        if note_id:
            note = Note.objects.filter(id=note_id)
            print(note)
            note[0].delete()
    response = redirect('/notes')
    return response


def get_mimetype(file):
    """
    Get MIME by reading the header of the file
    """
    initial_pos = file.tell()
    file.seek(0)
    mime_type = magic.from_buffer(file.read(2048), mime=True)
    file.seek(initial_pos)
    return mime_type

@login_required(login_url="/login/")
def downloadnote(request):
    print('hello')
    # file_path = 'media/'
    noteID = request.GET.get('id')
    if not noteID:
        return
    note =  Note.objects.filter(id=int(noteID)).first()
    with open(note.pdf.path, 'rb') as file:
        response = FileResponse(file.read(), content_type=get_mimetype(file))
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(note.pdf.name)
        return response


@login_required(login_url="/login/")
def saveNote(request):
    error_message = None

    if request.method == "POST" and 'savenote' in request.FILES:
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        pdf = request.FILES['savenote']
        note_id = request.POST.get('note-id')

        if not title or not desc or not pdf:
            error_message = "Please fill in all the fields."
            note = None
            if note_id:
                note = Note.objects.filter(id=note_id).first()

            return render(request, 'notes.html', context={'note': note, 'error_message': error_message})

        if note_id:
            note = Note.objects.filter(id=note_id).first()
            if note:
                note.title = title
                note.desc = desc
                note.pdf = pdf
                note.save()

                if request.FILES['savenote']:
                    upload = request.FILES['savenote']
                    fss = FileSystemStorage()
                    fss.save(upload.name, upload)

                return redirect('/notes')

        note = Note.objects.create(
            user=request.user,
            title=title,
            desc=desc,
            pdf=pdf
        )

        return redirect('/notes')

    

    if request.method == "GET" and request.GET.get('id', ''):
        note = Note.objects.filter(id=request.GET.get('id')).first()
        if note:
            return render(request, 'notes.html', context={'note': note})

    # Get the current file name
    current_file_name = request.POST.get('savenote', 'No file chosen')

    return render(request, 'notes.html', context={'error_message': error_message, 'current_file_name': current_file_name})



def register(request):
    if request.method == 'GET':
        form  = RegisterForm()
        context = {'form': form}
        return render(request, 'register.html', context)

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            userRec = form.save()
            UserProfile(user=userRec, usertype=form.data.get('usertype')).save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('webpages:index')
        else:
            print('Form is not valid')
            messages.error(request, 'Error Processing Your Request')
            context = {'form': form}
            response = render(request, 'register.html', context)
            return response

    return render(request, 'register.html', {})


@login_required(login_url="/login/")
def contact(request):
    return render(request,'contact.html')

@login_required(login_url="/login/")
def products(request):
    return render(request,'products.html')

@login_required(login_url="/login/")
def single_product(request):
    return render(request,'single-product.html')




# def profile(request):
#     usertype = request.user.profile.usertype if request.user.is_authenticated else None
#     if request.method == 'POST':
#         if usertype == 'Student':
#             college_id = request.POST.get('college')
#             semester_id = request.POST.get('semester')
#             try:
#                 if college_id:
#                     request.user.profile.College_id = int(college_id)
#                 if semester_id:                                
#                     request.user.profile.Semester_id = int(semester_id)
#                 request.user.profile.save()
#             except:
#                 pass
#             return render(request,'profile.html', context={'colleges': College.objects.all(), 'usertype':usertype , 'semesters': Semester.objects.all()})
#         elif usertype == 'Professor':
#             college_id = request.POST.get('college')
#             try:
#                 if college_id:
#                     request.user.profile.College_id = int(college_id)
#                 request.user.profile.save() 
#             except:
#                 pass   
#     return render(request,'profile.html', context={'colleges': College.objects.all(), 'usertype':usertype, 'semesters': Semester.objects.all()})

@login_required(login_url="/login/")
def profile(request):
    if request.method == 'POST':
        college_id = request.POST.get('college')
        semester_id = request.POST.get('semester')
        try:
            if college_id:
                request.user.profile.College_id = int(college_id)
            if semester_id:                                
                request.user.profile.Semester_id = int(semester_id)
            request.user.profile.save()
        except ValueError as e:
            pass
    return render(request,'profile.html', context={'colleges': College.objects.all() , 'semesters': Semester.objects.all()})

@login_required(login_url="/login/")
def notes(request):
    query = request.GET.get('list','my')
    # notes = Note.objects.filter(user=request.user)
    search_term = ''

    if 'search' in request.POST:
        search_term = request.POST['search']
        notes = Note.objects.all().filter(Q(pdf__contains=search_term) | Q(title__contains=search_term) | Q(desc__contains=search_term))
    else:
        notes = Note.objects.all()
    if query == "cr":
        return render(request, 'notes.html')
    elif query == "my":
        notes = notes.filter(user=request.user)
    elif query == "st":
        notes = notes.filter(user__profile__usertype__contains='Student').exclude(user=request.user)
    elif query == "pf":
        notes = notes.filter(user__profile__usertype__contains='Professor').exclude(user=request.user)
    return render(request,'notes-list.html',  context={'notes': notes, 'search_term': search_term, 'query':query})

@login_required(login_url="/login/")
def about(request):
    return render(request,'about.html')

@login_required(login_url="/login/")
def future(request):
    return render(request,'future.html')

@login_required(login_url="/login/")
def index(request):
    students = User.objects.filter(profile__usertype__contains='Student')
    professors = User.objects.filter(profile__usertype__contains='Professor')
    colleges = User.objects.all()
    return render(request,'index.html', context={"students": students , "professors": professors})

@login_required(login_url="/login/")
def colleges(request):
    query = request.GET.get('list')
    colleges = College.objects.filter()
    search_term = ''

    if 'search' in request.POST:
        search_term = request.POST['search']
        colleges = College.objects.all().filter(Q(name__contains=search_term) | Q(address__contains=search_term))
    return render(request,'colleges.html', context={'colleges': colleges, 'search_term': search_term, 'query': query})

@login_required(login_url="/login/")
def logout(request):
    request.session.delete()
    return redirect('/login')


@login_required(login_url="/login/")
def student(request, student_id):
    student_id = request.GET['student_id']
    user =  User.objects.get(id=student_id)
    notes = Note.objects.filter(user=user.id)
    return render(request,'student.html', context={"user": user, "notes": notes})

# @login_required(login_url="/login/")
# def professor(request, professor_id):
#     try:
#         user = User.objects.get(id=professor_id)
#     except User.DoesNotExist:
#         messages.error(request, 'Invalid professor ID')
#         return redirect('some_page')

#     notes = Note.objects.filter(user=user.id)
#     ratings = Rating.objects.filter(rated_user=user)

#     total_ratings = ratings.count()
#     if total_ratings > 0:
#         average_rating = sum([rating.rating for rating in ratings]) / total_ratings
#     else:
#         average_rating = None

#     if request.method == "POST":
#         form = RatingForm(request.POST)
#         if form.is_valid():
#             rating = form.cleaned_data['rating']
#             Rating.objects.create(rated_user=user, rated_by=request.user, rating=rating)
#             messages.success(request, 'Thank you for rating!')
#             return redirect('professor', professor_id=professor_id)  # Redirect to the same professor page
#     else:
#         form = RatingForm()

#     return render(request, 'professor.html', context={"user": user, "notes": notes, "average_rating": average_rating, "form": form})

# @login_required(login_url="/login/")
# def professor(request, professor_id):
#     professor_id = request.GET['professor_id']
#     user =  User.objects.get(id=professor_id)
#     notes = Note.objects.filter(user=user.id)
#     return render(request,'student.html', context={"user": user, "notes": notes})

@login_required(login_url="/login/", redirect_field_name=None)
def professor(request, professor_id):
    try:        
        professor_id = request.GET['professor_id']
        user =  User.objects.get(id=professor_id)
        notes = Note.objects.filter(user=user.id)
    except User.DoesNotExist:
        return redirect('webpages:index')

    notes = Note.objects.filter(user=user.id)
    ratings = Rating.objects.filter(rated_user=user)

    total_ratings = ratings.count()
    if total_ratings > 0:
        average_rating = sum([rating.rating for rating in ratings]) / total_ratings
    else:
        average_rating = None

    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            Rating.objects.create(rated_user=user, rated_by=request.user, rating=rating)
            return redirect('webpages:professor', professor_id=professor_id)  # Redirect to the same professor page
    else:
        form = RatingForm()

    return render(request, 'professor.html', context={"user": user, "notes": notes, "average_rating": average_rating, "form": form})


# @login_required(login_url="/login/")
# def professor(request, professor_id):
#     professor_id = request.GET['professor_id']
#     user =  User.objects.get(id=professor_id)
#     notes = Note.objects.filter(user=user.id)    
#     try:
#         user = User.objects.get(id=professor_id)
#     except User.DoesNotExist:
#         messages.error(request, 'Invalid professor ID')
#         return redirect('some_page')

#     notes = Note.objects.filter(user=user.id)
#     ratings = Rating.objects.filter(rated_user=user)

#     total_ratings = ratings.count()
#     if total_ratings > 0:
#         average_rating = sum([rating.rating for rating in ratings]) / total_ratings
#     else:
#         average_rating = None

#     if request.method == "POST":
#         form = RatingForm(request.POST)
#         if form.is_valid():
#             rating = form.cleaned_data['rating']
#             Rating.objects.create(rated_user=user, rated_by=request.user, rating=rating)
#             messages.success(request, 'Thank you for rating!')
#             return redirect('professor', professor_id=professor_id)  # Redirect to the same professor page
#     else:
#         form = RatingForm()

#     return render(request, 'professor.html', context={"user": user, "notes": notes, "average_rating": average_rating, "form": form})

# def college(request, College_id):
#     College_id = request.GET['College_id']
#     user =  User.objects.get(id=College_id)
#     notes = Note.objects.filter(user=user.id)
#     return render(request,'college.html', context={"user": user, "notes": notes})