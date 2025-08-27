from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from .models import User, Comment
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


def home(request):
    return render(request, "home.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid credentials"})

        if password == user.password:
            # if check_password(password, user.password):
            request.session["user_id"] = user.id
            request.session["username"] = user.username
            request.session["role"] = user.role
            return redirect("dashboard")
        else:
            return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            User.objects.create(
                username=username,
                password=password,
                # password=make_password(password),
                role="user",
            )
            return redirect("login")
        except Exception as e:
            return render(request, "register.html", {"error": "Registration failed"})

    return render(request, "register.html")


def dashboard(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")

    search_query = request.GET.get("search", "")
    if search_query:
        cursor = connection.cursor()
        query = f"SELECT * FROM main_comment WHERE text LIKE '%{search_query}%'"
        cursor.execute(query)
        comments_data = cursor.fetchall()
        comments = [
            Comment(id=row[0], author=row[1], text=row[2], user_id=row[3])
            for row in comments_data
        ]

        # comments = Comment.objects.filter(text__icontains=search_query)
    else:
        comments = Comment.objects.all()

    return render(
        request,
        "dashboard.html",
        {
            "comments": comments,
            "username": request.session.get("username"),
            "role": request.session.get("role"),
            "search_query": search_query,
        },
    )


def add_comment(request):
    if request.method == "POST":
        if not request.session.get("user_id"):
            return redirect("login")

        author = request.POST.get("author")
        text = request.POST.get("text")
        user_id = request.session.get("user_id")

        if author and text:
            Comment.objects.create(author=author, text=text, user_id=user_id)

    return redirect("dashboard")


def delete_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return redirect("dashboard")
    except Comment.DoesNotExist:
        return HttpResponse("Comment not found")

    # if "user_id" not in request.session:
    #     return HttpResponse("Unauthorized", status=401)
    #
    # comment = get_object_or_404(Comment, id=comment_id)
    # user_id = request.session["user_id"]
    # role = request.session.get("role", "user")
    #
    # if role == "admin" or comment.user_id == user_id:
    #     comment.delete()
    #     return redirect("dashboard")
    # else:
    #     return HttpResponse("Forbidden", status=403)


def logout(request):
    if "user_id" in request.session:
        del request.session["user_id"]
    # request.session.flush()

    return redirect("home")


def admin_dashboard(request):
    if request.session.get("role") != "admin":
        return HttpResponse("Access denied. Admin role required.", status=403)

    users = User.objects.all()
    comments = Comment.objects.all()

    return render(
        request,
        "admin_dashboard.html",
        {
            "users": users,
            "comments": comments,
            "admin_username": request.session.get("username"),
        },
    )


def setup_users(request):
    User.objects.all().delete()
    Comment.objects.all().delete()

    User.objects.create(username="admin", password="admin123", role="admin")
    User.objects.create(username="user", password="password", role="user")
    User.objects.create(username="user2", password="password", role="user")

    # User.objects.create(username="admin", password=make_password("admin123"), role="admin")
    # User.objects.create(username="user", password=make_password("password"), role="user")
    # User.objects.create(username="user2", password=make_password("password"), role="user")

    return HttpResponse(
        "Test users created! <br>"
        "Admin: admin/admin123 <br>"
        "User: user/password <br>"
        "User2: user2/password <br>"
        "<a href='/'>Go back</a>"
    )
