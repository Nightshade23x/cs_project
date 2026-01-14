from django.shortcuts import render
from .models import Note


def view_note(request, note_id):
    # FLAW 1: Broken Access Control
    note = Note.objects.get(id=note_id)
    return render(request, "note.html", {"note": note})

    # FIX:
    # note = Note.objects.get(id=note_id, owner=request.user)
  