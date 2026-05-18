from django.shortcuts import render, redirect
from .models import UserRegistration
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password


def register(request):

    if request.method == "POST":

        full_name = request.POST.get('full_name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        blood_group = request.POST.get('blood_group')
        university = request.POST.get('university')
        student_id = request.POST.get('student_id')
        district = request.POST.get('district')
        thana = request.POST.get('thana')
        union = request.POST.get('union')
        village = request.POST.get('village')
        password = request.POST.get('password')

        hashed_password = make_password(password)

        UserRegistration.objects.create(
            full_name=full_name,
            mobile=mobile,
            email=email,
            blood_group=blood_group,
            university=university,
            student_id=student_id,
            district=district,
            thana=thana,
            union=union,
            village=village,
            password=hashed_password
        )

        messages.success(request, "Account Created Successfully!")

        return redirect('login')

    return render(request, 'register.html')


def login_view(request):

    if request.method == "POST":

        student_id = request.POST.get('student_id')
        password = request.POST.get('password')

        try:
            user = UserRegistration.objects.get(
                student_id=student_id
            )

            if check_password(password, user.password):

                request.session['user_id'] = user.id

                return redirect('dashboard')

            else:
                messages.error(request, "Wrong Password")

        except UserRegistration.DoesNotExist:

            messages.error(request, "Student ID Not Found")

    return render(request, 'login.html')


def dashboard(request):

    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    user = UserRegistration.objects.get(id=user_id)

    return render(request, 'dashboard.html', {
        'user': user
    })


def logout_view(request):

    request.session.flush()

    return redirect('login')