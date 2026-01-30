LINK: https://github.com/Nightshade23x/cs_project

**Installation instructions:**

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

---
**FLAW 2: Injection**

Source link:
https://github.com/Nightshade23x/cs_project/blob/main/notes/views.py#L18-L30

**Description of the flaw:**

This vulnerability occurs in the search_notes function, where raw SQL is dynamically constructed using Python string interpolation. The user-provided input query is directly embedded into the SQL statement without any sanitization or parameterization. As a result, an attacker can manipulate the SQL query by injecting malicious SQL code through the search parameter.
Because the application executes this SQL statement directly against the database, it becomes vulnerable to SQL injection attacks. An attacker could potentially bypass query restrictions, access data belonging to other users, or modify the database contents. 

Impact:
SQL injection is a critical vulnerability that can lead to unauthorized data disclosure, data modification, or complete database compromise. In real-world applications, successful exploitation could expose sensitive user information and damage the integrity and availability of the system.

How to fix it:
The vulnerability can be fixed by avoiding raw SQL queries and using Django’s ORM instead. The ORM automatically parameterizes queries and safely handles user input, preventing SQL injection. By filtering notes using Django’s query methods, user input is never directly executed as SQL.

FIX:
 ```python
notes = Note.objects.filter(owner=request.user, title__icontains=query)
```
With this fix applied, user input is safely handled by the ORM, and SQL injection attacks are prevented by design. The query logic remains functionally equivalent while significantly improving the security of the application.



