import re     
from .models import EmergencyRequest                                                                                                  
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import UserRegistration, EmergencyRequest
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

def rank_donors(donors, request_blood, request_district):

    ranked = []

    for donor in donors:

        score = 0

        if donor.blood_group == request_blood:
            score += 50

        if donor.district.lower() == request_district.lower():
            score += 30

        if score >= 80:
            stars = "⭐⭐⭐⭐⭐ Best Match"
        elif score >= 50:
            stars = "⭐⭐⭐⭐"
        else:
            stars = "⭐⭐⭐"

        ranked.append({
            "donor": donor,
            "score": score,
            "stars": stars
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)

    return ranked

def get_compatible_donors(blood_group):

    compatibility = {
        "A+": ["A+", "A-", "O+", "O-"],
        "A-": ["A-", "O-"],
        "B+": ["B+", "B-", "O+", "O-"],
        "B-": ["B-", "O-"],
        "AB+": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
        "AB-": ["A-", "B-", "AB-", "O-"],
        "O+": ["O+", "O-"],
        "O-": ["O-"],
    }

    return compatibility.get(blood_group, [])

def get_priority(message):

    message = message.lower()

    high_keywords = [
        "urgent",
        "critical",
        "accident",
        "operation",
        "icu",
        "1 hour",
        "2 hour",
        "immediately",
        "emergency",
    ]

    medium_keywords = [
        "today",
        "tonight",
        "tomorrow",
    ]

    for word in high_keywords:
        if word in message:
            return "🔴 HIGH PRIORITY"

    for word in medium_keywords:
        if word in message:
            return "🟡 MEDIUM PRIORITY"

    return "🟢 LOW PRIORITY"


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

        # Fake Phone Detection

        if not re.match(r'^01[3-9]\d{8}$', mobile):

            messages.error(request, "Invalid Bangladeshi Phone Number")

            return redirect('register')

        # Duplicate Email Check

        if UserRegistration.objects.filter(email=email).exists():

            messages.error(request, "Email Already Exists")

            return redirect('register')

        # Duplicate Student ID

        if UserRegistration.objects.filter(student_id=student_id).exists():

            messages.error(request, "Student ID Already Exists")

            return redirect('register')

        # Duplicate Phone

        if UserRegistration.objects.filter(mobile=mobile).exists():

            messages.error(request, "Phone Number Already Exists")

            return redirect('register')
        # AI Fraud Score System

        fraud_score = 0

        # Suspicious patterns

        if "test" in full_name.lower():
            fraud_score += 2

        if mobile.endswith("000"):
          fraud_score += 2

        if len(password) < 8:
           fraud_score += 2

        if district.lower() == "unknown":
           fraud_score += 3

# Block suspicious account

        if fraud_score >= 5:

          messages.error(
            request,
            "Suspicious Activity Detected"
            )
          

          return redirect('register')
        
        # Password Strength Validation

        if len(password) < 8:

           messages.error(request, "Password Must Be At Least 8 Characters")

           return redirect('register')


        if password.isdigit():

           messages.error(request, "Password Cannot Be Only Numbers")

           return redirect('register')
        # Suspicious Name Detection

        if len(full_name) < 3:

           messages.error(request, "Invalid Full Name")

           return redirect('register')


        if full_name.isdigit():

           messages.error(request, "Name Cannot Be Numbers")

           return redirect('register')

        # Repeated Digit Detection

        if mobile == mobile[0] * len(mobile):

            messages.error(request, "Fake Phone Number Detected")

            return redirect('register')

        # Password Validation

        if len(password) < 8:

            messages.error(request, "Password Must Be At Least 8 Characters")

            return redirect('register')

        # Hash Password

        hashed_password = make_password(password)

        # Create User

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
def donor_search(request):

    donors = UserRegistration.objects.all()

    blood_group = request.GET.get('blood_group')

    district = request.GET.get('district')

    if blood_group:
        donors = donors.filter(
            blood_group=blood_group
        )

    if district:
        donors = donors.filter(
            district__icontains=district
        )

    return render(request, 'donor_search.html', {
        'donors': donors
    })
def home(request):

    return redirect('login')
def emergency_request(request):

    priority = None
    compatible_donors = []
    recommended_donors = []

    if request.method == "POST":

        patient_name = request.POST.get("patient_name")
        blood_group = request.POST.get("blood_group")
        district = request.POST.get("district")
        hospital = request.POST.get("hospital")
        contact_number = request.POST.get("contact_number")
        message = request.POST.get("message")

        EmergencyRequest.objects.create(
            patient_name=patient_name,
            blood_group=blood_group,
            district=district,
            hospital=hospital,
            contact_number=contact_number,
            message=message,
        )

        compatible_donors = get_compatible_donors(blood_group)
        donors = UserRegistration.objects.filter(
            blood_group__in=compatible_donors
        )

        recommended_donors = rank_donors(
            donors,
            blood_group,
            district
        )

        priority = get_priority(message)

        requests = EmergencyRequest.objects.all().order_by("-id")

        return render(
            request,
            "emergency_request.html",
            {
                "requests": requests,
                "compatible_donors": compatible_donors,
                "recommended_donors": recommended_donors,
                "priority": priority,
            },
        )

    requests = EmergencyRequest.objects.all().order_by("-id")

    return render(
        request,
        "emergency_request.html",
        {
            "requests": requests,
            "compatible_donors": compatible_donors,
            "recommended_donors": recommended_donors,
            "priority": priority,
        },
    )
def health_tips(request):
    return render(
        request,
        'health_tips.html'
    )
