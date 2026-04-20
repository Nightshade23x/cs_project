from django.shortcuts import render
from django.db import connection
from .models import Note
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.conf import settings


def view_note(request, note_id):
    # FLAW 1: Broken Access Control
    note = Note.objects.get(id=note_id)
    return render(request, "note.html", {"note": note})

    # FIX:
    # note = Note.objects.get(id=note_id, owner=request.user)


def search_notes(request):
    # FLAW 2: Injection
    query = request.GET.get("q", "")
    user_id = request.user.id

    sql = f"""
        SELECT * FROM notes_note
        WHERE owner_id = {user_id}
        AND title LIKE '%{query}%'
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
    return render(request, "search_results.html", {"rows": rows, "query": query})

    # FIX:
    # notes = Note.objects.filter(owner=request.user, title__icontains=query)


def insecure_login(request):
    # FLAW 3: Identification and Authentication Failures

    if request.method == "GET":
        return render(request, "login.html")

    username = request.POST.get("username")
    password = request.POST.get("password")

    user = User.objects.filter(username=username).first()

    if user:
        login(request, user)
        return redirect("search_notes")

    return render(request, "login.html", {
        "error": "Invalid username or password. Please try again."
    })

    # FIX:
    # user = authenticate(request, username=username, password=password)
    # if user:
    #     login(request, user)
    #     return redirect("search_notes")
    # return render(request, "login.html", {
    #     "error": "Invalid username or password. Please try again."
    # })


def debug_info(request):
    # FLAW 4: Security Misconfiguration
    debug_data = {
        "DEBUG": settings.DEBUG,
        "DATABASE_ENGINE": settings.DATABASES["default"]["ENGINE"],
        "DATABASE_NAME": settings.DATABASES["default"]["NAME"],
        "SECRET_KEY": settings.SECRET_KEY,
    }

    return render(request, "debug.html", {
        "debug_data": debug_data
    })

    # FIX:
    # if not request.user.is_staff:
    #     return render(request, "error.html", {
    #         "error": "Access denied."
    #     })
    #
    # debug_data = {
    #     "DEBUG": settings.DEBUG,
    # }
    #
    # return render(request, "debug.html", {
    #     "debug_data": debug_data
    # })


def insecure_register(request):
    # FLAW 5: Cryptographic Failures
    if request.method == "GET":
        return render(request, "register.html")

    username = request.POST.get("username")
    password = request.POST.get("password")

    user = User(
        username=username,
        password=password
    )
    user.save()

    return redirect("login")

    # FIX:
    # user = User.objects.create_user(
    #     username=username,
    #     password=password
    # )
    # return redirect("login")