from django.shortcuts import render
from django.db import connection
from .models import Note


def view_note(request, note_id):
    # FLAW 1: Broken Access Control
    note = Note.objects.get(id=note_id)
    return render(request, "note.html", {"note": note})

    # FIX:
    # note = Note.objects.get(id=note_id, owner=request.user)

def search_notes(request):
    query = request.GET.get("q", "")
    user_id = request.user.id

    #FLAW 2: SQL Injection
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
