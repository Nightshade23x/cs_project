LINK: https://github.com/Nightshade23x/cs_project

Installation instructions:

The application is a Django web application. After cloning the repository, dependencies can be installed using pip install -r requirements.txt. The server can then be started locally using python manage.py runserver in the Terminal.

**FLAW 1: Broken Access Control**

Source link:
https://github.com/Nightshade23x/cs_project/blob/main/notes/views.py#L9-L14

**Description of the flaw:**
This vulnerability occurs in the view_note function, where a note is retrieved solely based on its ID using Note.objects.get(id=note_id). The code does not verify whether the currently authenticated user is the owner of the requested note. As a result, any logged in user can access notes belonging to other users simply by changing the note ID in the URL. This violates the principle of access control by failing to enforce authorization checks at the object level.
The issue is demonstrated in the screenshot flaw-1-before-1, where user1 is able to view a note owned by user2 by directly navigating to /notes/note/2/. This confirms that sensitive user data is exposed without proper permission checks.

**Impact:**
Broken access control allows unauthorized data access and can lead to privacy violations. In real-world applications, this could expose confidential or personal information and undermine trust in the system.

**How to fix it:**
The fix enforces ownership validation by filtering the note using both the note ID and the currently authenticated user. This ensures that users can only access their own notes. The corrected code restricts database access at the query level, preventing unauthorized access entirely.

FIX:
  ```python
note = Note.objects.get(id=note_id, owner=request.user)
```
With this fix applied, attempts to access another user’s note result in a “DoesNotExist” error, as shown in the flaw-1-after-1 screenshot, confirming that access control is correctly enforced.



