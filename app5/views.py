from django.shortcuts import render
from django.db.models import Avg, Max
# Create your views here.
from django.shortcuts import render,redirect
from.models import *
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

from django.utils.http import urlsafe_base64_encode
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, redirect
import random
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail


from django.conf import settings
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')



def contact(request):

    if request.method == "POST":

        name = request.POST['name']

        email = request.POST['email']

        subject = request.POST['subject']

        message = request.POST['message']

        send_mail(

            subject,

            f"""

Message from Quizify

Name : {name}

Email : {email}

--------------------------------

{message}

""",

            email,

            ['nikksnikhil07@gmail.com'],

            fail_silently=False

        )

        return render(request,
                      'contact_success.html')

    return render(request,'contact.html')


def user_home(request):

    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    current_user = user.objects.get(id=user_id)

    attempts = QuizAttempt.objects.filter(user=current_user)

    total_quizzes = attempts.count()

    if total_quizzes > 0:

        average_score = round(
            attempts.aggregate(
                Avg("percentage")
            )["percentage__avg"],
            1
        )

        best_score = attempts.aggregate(
            Max("score")
        )["score__max"]

    else:

        average_score = 0
        best_score = 0

    context = {

        "current_user": current_user,

        "total_quizzes": total_quizzes,

        "average_score": average_score,

        "best_score": best_score,

    }

    return render(
        request,
        "user_index.html",
        context
    )

def admin_home(request):

    total_users = user.objects.count()

    total_attempts = QuizAttempt.objects.count()

    total_categories = 5

    context = {

        "total_users": total_users,

        "total_attempts": total_attempts,

        "total_categories": total_categories,

    }

    return render(
        request,
        "admin_index.html",
        context
    )



def register(request):

    if request.method == "POST":

        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        phno = request.POST['phno']

        password = request.POST['password']
        confirm_password = request.POST['confirm_password']


        # ---------------------------------------
        # CHECK IF USERNAME ALREADY EXISTS
        # ---------------------------------------

        if user.objects.filter(username=username).exists() or username == 'admin':

            return render(request, 'register.html', {

                'msg': 'Username already exists. Please choose another username.'

            })


        # ---------------------------------------
        # CHECK IF EMAIL ALREADY EXISTS
        # ---------------------------------------

        if user.objects.filter(email=email).exists():

            return render(request, 'register.html', {

                'msg': 'An account with this email already exists.'

            })


        # ---------------------------------------
        # CHECK PASSWORDS
        # ---------------------------------------

        if password != confirm_password:

            return render(request, 'register.html', {

                'msg': 'Passwords do not match. Please try again.'

            })


        # ---------------------------------------
        # CREATE USER
        # ---------------------------------------

        obj = user(

            name=name,

            username=username,

            email=email,

            phno=phno,

            password=password

        )

        obj.save()


        # ---------------------------------------
        # SEND WELCOME EMAIL
        # ---------------------------------------

        send_mail(

            subject='Welcome to Quizify!',

            message=f'''
Hello {name},

Your Quizify account has been created successfully.

Username : {username}

Thank you for joining Quizify!

Challenge your mind.
Learn.
Play.
Progress.

Regards,
Quizify Team
''',

            from_email=None,

            recipient_list=[email],

            fail_silently=False,

        )


        # ---------------------------------------
        # REGISTRATION SUCCESS
        # ---------------------------------------

        return render(request, 'register_success.html')


    return render(request, 'register.html')

def login(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        # Admin Login
        if username == "admin" and password == "123@4":
            return redirect("admin_home")

        try:
            obj = user.objects.get(username=username, password=password)

            # Store logged-in user ID in session
            request.session["user_id"] = obj.id

            return redirect("user_home")

        except user.DoesNotExist:

            return render(
                request,
                "login.html",
                {"msg": "Invalid Username or Password"},
            )

    return render(request, "login.html")

def logout(request):

    request.session.flush()

    return redirect("home")

def forgot_password(request):

    if request.method == "POST":

        email = request.POST['email']

        try:

            obj = user.objects.get(email=email)

            otp = random.randint(100000, 999999)

            request.session['otp'] = str(otp)
            request.session['email'] = email

            send_mail(

                "Quizify Password Reset OTP",

                f"""
Hello {obj.name},

You requested to reset your Quizify password.

Your OTP is:

{otp}

Do not share this OTP with anyone.

Regards,

Quizify Team
""",

                settings.EMAIL_HOST_USER,

                [email],

                fail_silently=False

            )

            # Redirect to OTP page
            return redirect('verify_otp')

        except user.DoesNotExist:

            return render(
                request,
                'forgot_password.html',
                {'msg': 'Wrong Email Address'}
            )

    return render(request, 'forgot_password.html')

from django.utils.http import urlsafe_base64_decode

def reset_password(request):

    email = request.session.get('email')

    if not email:
        return redirect('forgot_password')

    if request.method == "POST":

        password = request.POST['password']
        confirm = request.POST['confirm_password']

        if password != confirm:

            return render(
                request,
                'reset_password.html',
                {'msg': 'Passwords do not match'}
            )

        obj = user.objects.get(email=email)

        obj.password = password

        obj.save()

        request.session.flush()

        return redirect('login')

    return render(request, 'reset_password.html')

def verify_otp(request):

    if request.method == "POST":

        entered_otp = request.POST['otp']

        saved_otp = request.session.get('otp')

        if entered_otp == saved_otp:

            return redirect('reset_password')

        else:

            return render(request,
                          'verify_otp.html',
                          {'msg': 'Invalid OTP'})

    return render(request, 'verify_otp.html')

from django.shortcuts import render

def profile(request):

    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    current_user = user.objects.get(id=user_id)

    attempts = QuizAttempt.objects.filter(
        user=current_user
    ).order_by("-completed_at")

    total_quizzes = attempts.count()

    if total_quizzes > 0:

        average_score = round(
            attempts.aggregate(
                Avg("score")
            )["score__avg"],
            1
        )

        best_score = attempts.aggregate(
            Max("score")
        )["score__max"]

        average_percentage = round(
            attempts.aggregate(
                Avg("percentage")
            )["percentage__avg"],
            1
        )

    else:

        average_score = 0
        best_score = 0
        average_percentage = 0

    context = {

        "current_user": current_user,

        "attempts": attempts,

        "total_quizzes": total_quizzes,

        "average_score": average_score,

        "best_score": best_score,

        "average_percentage": average_percentage,

    }

    return render(
        request,
        "profile.html",
        context
    )

def category(request):

    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    current_user = user.objects.get(id=user_id)

    context = {
        "current_user": current_user,
    }

    return render(request, "category.html", context)

def quiz(request, category):

    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    current_user = user.objects.get(id=user_id)

    category_map = {

        "science": {
            "model": ScienceQuestion,
            "name": "Science",
        },

        "mathematics": {
            "model": MathematicsQuestion,
            "name": "Mathematics",
        },

        "general knowledge": {
            "model": GeneralKnowledgeQuestion,
            "name": "General Knowledge",
        },

        "computer science": {
            "model": ComputerScienceQuestion,
            "name": "Computer Science",
        },

        "history": {
            "model": HistoryQuestion,
            "name": "History",
        },

    }

    data = category_map.get(category.lower())

    if data is None:
        return redirect("category")

    Model = data["model"]

    category_name = data["name"]

    # Get current version of this category
    setting, created = QuizSettings.objects.get_or_create(
        category=category_name,
        defaults={"active_version": 1}
    )

    # Check if user already attempted this version
    already_attempted = QuizAttempt.objects.filter(

        user=current_user,
        category=category_name,
        version=setting.active_version

    ).exists()

    if already_attempted:
        messages.warning(

            request,

            f"You have already completed the {category_name} quiz. "
            "You can attempt it again only after the admin updates the questions or try another category!"

        )

        return redirect("category")

    # Load questions
    questions = Model.objects.exclude(
        question=""
    ).order_by("id")

    # -------------------------
    # SUBMIT QUIZ
    # -------------------------

    if request.method == "POST":

        score = 0
        correct = 0
        wrong = 0
        attempted = 0

        # Create attempt first
        attempt = QuizAttempt.objects.create(

            user=current_user,

            category=category_name,

            version=setting.active_version,

            score=0,

            total_marks=30,

            attempted_questions=0,

            correct_answers=0,

            wrong_answers=0,

            percentage=0

        )

        for q in questions:

            answer = request.POST.get(f"question{q.id}")

            if answer:

                attempted += 1

            is_correct = answer == q.correct_answer

            if is_correct:

                score += q.marks

                correct += 1

            else:

                wrong += 1

            UserAnswer.objects.create(

                attempt=attempt,

                question_id=q.id,

                question=q.question,

                option_a=q.option_a,

                option_b=q.option_b,

                option_c=q.option_c,

                option_d=q.option_d,

                selected_answer=answer if answer else "",

                correct_answer=q.correct_answer,

                marks_awarded=q.marks if is_correct else 0,

                is_correct=is_correct

            )

        attempt.score = score

        attempt.correct_answers = correct

        attempt.wrong_answers = wrong

        attempt.attempted_questions = attempted

        attempt.percentage = round((score / 30) * 100, 2)

        attempt.save()

        return redirect("result", attempt.id)

    context = {

        "current_user": current_user,

        "category": category,

        "questions": questions,

    }

    return render(
        request,
        "science_quiz.html",
        context
    )
def instruction(request, category):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    current_user = user.objects.get(id=user_id)

    return render(request, "instruction.html", {
        "current_user": current_user,
        "category": category,
    })

from django.shortcuts import render





from django.contrib import messages



def question_categories(request):
    return render(request, "question_categories.html")

def manage_questions(request):
    return render(request, "manage_questions.html")

def manage_category(request, category):
    category_map = {

        "science": {
            "model": ScienceQuestion,
            "name": "Science",
        },

        "mathematics": {
            "model": MathematicsQuestion,
            "name": "Mathematics",
        },

        "general knowledge": {
            "model": GeneralKnowledgeQuestion,
            "name": "General Knowledge",
        },

        "computer science": {
            "model": ComputerScienceQuestion,
            "name": "Computer Science",
        },

        "history": {
            "model": HistoryQuestion,
            "name": "History",
        },

    }

    data = category_map.get(category.lower())

    if data is None:
        return redirect("category")

    Model = data["model"]

    category_name = data["name"]

    if Model is None:
        return redirect("manage_questions")

    # ------------------------------------------
    # Create 15 empty questions on first visit
    # ------------------------------------------

    if Model.objects.count() == 0:

        for i in range(1, 16):

            if i <= 5:
                difficulty = "Easy"
            elif i <= 10:
                difficulty = "Medium"
            else:
                difficulty = "Hard"

            Model.objects.create(
                difficulty=difficulty,
                question="",
                option_a="",
                option_b="",
                option_c="",
                option_d="",
                correct_answer="A",
            )

    # Always get the questions in order
    questions = Model.objects.all().order_by("id")

    # ------------------------------------------
    # Save / Update
    # ------------------------------------------

    if request.method == "POST":

        updated = False

        for i, q in enumerate(questions, start=1):

            question = request.POST.get(f"question{i}", "").strip()
            option_a = request.POST.get(f"a{i}", "").strip()
            option_b = request.POST.get(f"b{i}", "").strip()
            option_c = request.POST.get(f"c{i}", "").strip()
            option_d = request.POST.get(f"d{i}", "").strip()
            correct_answer = request.POST.get(f"answer{i}", "A")

            if (
                    q.question != question or
                    q.option_a != option_a or
                    q.option_b != option_b or
                    q.option_c != option_c or
                    q.option_d != option_d or
                    q.correct_answer != correct_answer
            ):
                updated = True

            q.question = question
            q.option_a = option_a
            q.option_b = option_b
            q.option_c = option_c
            q.option_d = option_d
            q.correct_answer = correct_answer

            q.save()

        # Increase version only if something actually changed
        if updated:
            increase_quiz_version(category_name)

        return redirect("manage_category", category=category)

    context = {

        "category": category,

        "questions": questions,

        "first_time": False,

    }

    return render(
        request,
        "manage_category.html",
        context,
    )

from django.shortcuts import render, get_object_or_404

def result(request, attempt_id):

    attempt = get_object_or_404(
        QuizAttempt,
        id=attempt_id
    )

    answers = UserAnswer.objects.filter(
        attempt=attempt
    )

    context = {

        "attempt": attempt,

        "answers": answers

    }

    return render(
        request,
        "result.html",
        context
    )

def increase_quiz_version(category_name):

    setting, created = QuizSettings.objects.get_or_create(
        category=category_name,
        defaults={"active_version": 1}
    )

    setting.active_version += 1
    setting.save()

def manage_users(request):

    users = user.objects.all().order_by("name")

    total_users = users.count()

    total_attempts = QuizAttempt.objects.count()

    context = {

        "users": users,

        "total_users": total_users,

        "total_attempts": total_attempts,

    }

    return render(
        request,
        "manage_users.html",
        context,
    )
def view_user(request, user_id):

    selected_user = get_object_or_404(
        user,
        id=user_id
    )

    attempts = QuizAttempt.objects.filter(
        user=selected_user
    ).order_by("-completed_at")

    total_quizzes = attempts.count()

    if total_quizzes:

        best_score = attempts.aggregate(
            Max("score")
        )["score__max"]

        average_score = round(
            attempts.aggregate(
                Avg("score")
            )["score__avg"],
            1
        )

        average_percentage = round(
            attempts.aggregate(
                Avg("percentage")
            )["percentage__avg"],
            1
        )

    else:

        best_score = 0
        average_score = 0
        average_percentage = 0

    context = {

        "selected_user": selected_user,

        "attempts": attempts,

        "total_quizzes": total_quizzes,

        "best_score": best_score,

        "average_score": average_score,

        "average_percentage": average_percentage,

    }

    return render(
        request,
        "view_user.html",
        context
    )


def delete_user(request, user_id):

    selected_user = get_object_or_404(
        user,
        id=user_id
    )

    if request.method == "POST":

        # Save details before deleting
        name = selected_user.name
        email = selected_user.email

        # Send email
        send_mail(
            subject="Your Quizify Account Has Been Removed",
            message=f"""
Hello {name},

This email is to inform you that your Quizify account has been removed by the administrator.

As a result, your account and all associated data, including:

• Quiz attempts
• Quiz history
• Scores
• Saved answers

have been permanently deleted from our system.

If you believe this was done in error or have any questions, please contact the Quizify administrator.

Thank you for being a part of Quizify.

Regards,

Quizify Team
""",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        # Delete the user
        selected_user.delete()

        messages.success(
            request,
            "User deleted successfully."
        )

        return redirect("manage_users")

    return render(
        request,
        "delete_user.html",
        {
            "selected_user": selected_user,
        }
    )
def statistics(request):
    return render(request, "statistics.html")
def quiz_attempts(request):

    attempts = QuizAttempt.objects.all().order_by("-completed_at")

    total_attempts = attempts.count()

    total_users = attempts.values("user").distinct().count()

    highest_score = attempts.aggregate(
        Max("score")
    )["score__max"] or 0

    average_percentage = attempts.aggregate(
        Avg("percentage")
    )["percentage__avg"] or 0

    context = {

        "attempts": attempts,

        "total_attempts": total_attempts,

        "total_users": total_users,

        "highest_score": highest_score,

        "average_percentage": round(average_percentage,1),

    }

    return render(
        request,
        "quiz_attempts.html",
        context
    )
def get_category_stats(category_name):

    attempts = QuizAttempt.objects.filter(category=category_name)

    total_attempts = attempts.count()

    average = round(
        attempts.aggregate(Avg("percentage"))["percentage__avg"] or 0,
        1
    )

    top_attempt = attempts.order_by("-score", "completed_at").first()

    if top_attempt:

        best_score = top_attempt.score
        topper = top_attempt.user.name
        date = top_attempt.completed_at.strftime("%d %b %Y")

    else:

        best_score = 0
        topper = "No Attempts"
        date = "-"

    return {

        "average": average,

        "attempts": total_attempts,

        "best_score": best_score,

        "topper": topper,

        "date": date,

    }

def category_details(request):

    science = get_category_stats("Science")

    maths = get_category_stats("Mathematics")

    gk = get_category_stats("General Knowledge")

    cs = get_category_stats("Computer Science")

    history = get_category_stats("History")

    categories = [

        ("Science", science),

        ("Mathematics", maths),

        ("General Knowledge", gk),

        ("Computer Science", cs),

        ("History", history),

    ]

    hardest = min(categories, key=lambda x: x[1]["average"])

    easiest = max(categories, key=lambda x: x[1]["average"])

    most = max(categories, key=lambda x: x[1]["attempts"])

    context = {

        "science": science,

        "maths": maths,

        "gk": gk,

        "cs": cs,

        "history": history,

        "hardest_category": hardest[0],

        "hardest_average": hardest[1]["average"],

        "easiest_category": easiest[0],

        "easiest_average": easiest[1]["average"],

        "most_attempted": most[0],

        "most_attempts": most[1]["attempts"],

    }

    return render(

        request,

        "category_details.html",

        context

    )