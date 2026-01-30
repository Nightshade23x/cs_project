LINK: https://github.com/Nightshade23x/cs_project

**Installation instructions:**

The application is a Django web application. After cloning the repository, dependencies can be installed using pip install -r requirements.txt. The server can then be started locally using python manage.py runserver in the Terminal.

**FLAW 1: Broken Access Control**

Source link:
https://github.com/Nightshade23x/cs_project/blob/main/notes/views.py#L10-L16

**Description of the flaw:**
This vulnerability occurs in the view_note function, where a note is retrieved solely based on its ID using Note.objects.get(id=note_id). The code does not verify whether the currently authenticated user is the owner of the requested note. As a result, any logged in user can access notes belonging to other users simply by changing the note ID in the URL. This violates the principle of access control by failing to enforce authorization checks at the object level.
The issue is demonstrated in the screenshot flaw-1-before-1, where user1 is able to view a note owned by user2 by directly navigating to /notes/note/2/. This confirms that sensitive user data is exposed without proper permission checks.

**Impact:**
Broken access control allows unauthorized data access and can lead to privacy violations. In real-world applications, this could expose confidential or personal information and undermine trust in the system.

**How to fix it:**
The fix enforces ownership validation by filtering the note using both the note ID and the currently authenticated user. This ensures that users can only access their own notes. The corrected code restricts database access at the query level, preventing unauthorized access entirely.

**FIX:**
  ```python
note = Note.objects.get(id=note_id, owner=request.user)
```
With this fix applied, attempts to access another user’s note result in a “DoesNotExist” error, as shown in the flaw-1-after-1 screenshot, confirming that access control is correctly enforced.

---
**FLAW 2: Injection**

Source link:
https://github.com/Nightshade23x/cs_project/blob/main/notes/views.py#L18-L34

**Description of the flaw:**

This vulnerability occurs in the search_notes function, where raw SQL is dynamically constructed using Python string interpolation. The user-provided input query is directly embedded into the SQL statement without any sanitization or parameterization. As a result, an attacker can manipulate the SQL query by injecting malicious SQL code through the search parameter.
Because the application executes this SQL statement directly against the database, it becomes vulnerable to SQL injection attacks. An attacker could potentially bypass query restrictions, access data belonging to other users, or modify the database contents. 

**Impact:**

SQL injection is a critical vulnerability that can lead to unauthorized data disclosure, data modification, or complete database compromise. In real-world applications, successful exploitation could expose sensitive user information and damage the integrity and availability of the system.

**How to fix it:**

The vulnerability can be fixed by avoiding raw SQL queries and using Django’s ORM instead. The ORM automatically parameterizes queries and safely handles user input, preventing SQL injection. By filtering notes using Django’s query methods, user input is never directly executed as SQL.

**FIX:**
 ```python
notes = Note.objects.filter(owner=request.user, title__icontains=query)
```
With this fix applied, user input is safely handled by the ORM, and SQL injection attacks are prevented by design. The query logic remains functionally equivalent while significantly improving the security of the application.

---

**FLAW 3: Identification and Authentication Failures**

Source link:
https://github.com/Nightshade23x/cs_project/blob/main/notes/views.py#L36-L62

**Description of the flaw:**

This vulnerability occurs in the insecure_login function, where user authentication is handled incorrectly. Instead of verifying both the username and password, the application retrieves a user object based solely on the provided username using User.objects.filter(username=username).first(). If a user with that username exists, the application logs the user in without validating the password.
This means that anyone can authenticate as any existing user by simply knowing their username, completely bypassing password verification. This represents a serious identification and authentication failure, as the system does not properly confirm a user’s identity before granting access.

**Impact:**

Authentication failures of this kind allow attackers to impersonate legitimate users and gain full access to their accounts. In real-world systems, this could lead to account takeover, unauthorized actions, data breaches, and loss of trust in the application’s security.

**How to fix it:**

The issue can be fixed by using Django’s built-in authenticate function, which securely verifies both the username and password before logging a user in. This ensures that authentication only succeeds when valid credentials are provided, restoring proper identity verification.

**FIX:**
```python
user = authenticate(request, username=username, password=password)
if user:
    login(request, user)
    return redirect("search_notes")
return render(request, "login.html", {
    "error": "Invalid username or password. Please try again."
})
```

With this fix applied, users can only log in with valid credentials. Invalid login attempts no longer result in unauthorized access, ensuring that authentication is correctly enforced according to security best practices.

---

**FLAW 4: Insecure Design**

Source link:
https://github.com/Nightshade23x/cs_project/blob/main/notes/views.py#L64-L80

**Description of the flaw:**

This vulnerability appears in the admin_panel function, which displays a list of all registered users in the system. The code does not perform any authorization checks to verify whether the requesting user has administrative privileges. As a result, any authenticated user can access the admin panel endpoint and view sensitive information about all users which should only be available for the admin to see.
This represents an insecure design flaw, as the application lacks proper access control logic for a high privilege feature. 

**Impact:**

Insecure design flaws can expose sensitive system functionality and user data. In this case, unauthorized access to administrative information could facilitate further attacks such as user enumeration, social engineering, or privilege escalation. Over time, such design weaknesses significantly increase the attack surface of the application.

**How to fix it:**

The issue can be fixed by explicitly restricting access to administrative functionality. By checking whether the requesting user has staff or administrator privileges before rendering the admin panel, the application ensures that only authorized users can access this sensitive feature.

**FIX:**
```python
if not request.user.is_staff:
    return render(request, "error.html", {
        "error": "Access denied: You are not an administrator."
    })

users = User.objects.all()
return render(request, "admin.html", {
    "users": users
})
```

With this fix applied, non admin users are denied access to the admin panel, while authorized users can continue to use the feature as intended. This aligns the application’s design with the principle of least privilege and improves overall system security.


