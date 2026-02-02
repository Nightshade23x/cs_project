LINK: https://github.com/Nightshade23x/cs_project

**Installation instructions:**

The application is a Django web application. After cloning the repository, dependencies can be installed using pip install -r requirements.txt. The server can then be started locally using python manage.py runserver in the Terminal.

---

**FLAW 1: Broken Access Control**

Source link:
https://github.com/Nightshade23x/cs_project/blob/main/notes/views.py#L10-L16

**Description of the flaw:**

This vulnerability occurs in the view_note function, where a note is retrieved solely based on its ID using Note.objects.get(id=note_id). The code does not verify whether the currently authenticated user is the owner of the requested note. As a result, any logged in user can access notes belonging to other users simply by changing the note ID in the URL. This violates the principle of access control by failing to enforce authorization checks at the object level.
The issue is demonstrated in the screenshot flaw-1-before-1, where user1 is able to view a note owned by user2 by directly navigating to /notes/note/2/. This shows that sensitive user data is exposed without proper permission checks.

**Impact:**

Broken access control allows unauthorized data access and can lead to privacy violations. In real world applications, this could expose confidential or personal information and undermine trust in the system.

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

This vulnerability occurs in the search_notes function, where raw SQL is dynamically constructed using Python string interpolation. The user provided input query is directly embedded into the SQL statement without any parameterization. As a result, an attacker can manipulate the SQL query by injecting malicious SQL code through the search parameter.
Because the application executes this SQL statement directly against the database, it becomes vulnerable to SQL injection attacks. An attacker could potentially bypass query restrictions, access data belonging to other users, or modify the database contents. 

**Impact:**

SQL injection is a critical vulnerability that can lead to unauthorized data disclosure, data modification, or complete database compromise. In real world applications, successful exploitation could expose sensitive user information and damage the integrity and availability of the system.

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

Insecure design flaws can expose sensitive system functionality and user data. In this case, unauthorized access to administrative information could facilitate further attacks such as user enumeration. Over time, such design weaknesses significantly increase the attack surface of the application.

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

---

**FLAW 5: Security Misconfiguration**

Source link:

https://github.com/Nightshade23x/cs_project/blob/main/notes/views.py#L83-L108

**Description of the flaw:**

This vulnerability is present in the debug_info function, which exposes sensitive configuration details to any user who accesses the endpoint. The view renders internal application settings such as the DEBUG flag, database engine, database name, and the application’s SECRET_KEY. No access control checks are performed before displaying this information.
Exposing such configuration data represents a security misconfiguration, as internal system details that should remain confidential are made publicly accessible. In particular, revealing the SECRET_KEY poses a severe risk, as it is used by Django to secure sessions and cryptographic operations.

**Impact:**

Security misconfiguration can significantly weaken an application’s security posture. Disclosure of sensitive configuration details can aid attackers in crafting more effective attacks, compromising authentication mechanisms, or exploiting other vulnerabilities. In real-world systems, exposure of secrets may lead to session hijacking or complete application compromise.

**How to fix it:**

The issue can be fixed by restricting access to debugging information and limiting the data that is exposed. Only authorized administrative users should be allowed to view debugging details, and sensitive values such as the secret key should never be displayed.

**FIX:**

```python
if not request.user.is_staff:
    return render(request, "error.html", {
        "error": "Access denied."
    })

debug_data = {
    "DEBUG": settings.DEBUG,
}

return render(request, "debug.html", {
    "debug_data": debug_data
})
```

With this fix applied, sensitive configuration details are no longer exposed to regular users. Access is restricted to authorized administrators, and only minimal, non-sensitive debugging information is displayed, reducing the risk of information leakage.

---

**FLAW 6: Cryptographic Failures**

Source link:
https://github.com/Nightshade23x/cs_project/blob/main/notes/views.py#L111-L125

**Description of the flaw:**

This vulnerability is related to how user credentials are handled during registration in the insecure_register function. If passwords were stored directly without proper hashing, this would represent a cryptographic failure, as sensitive data would be stored in plaintext or using insecure mechanisms. Improper handling of credentials violates fundamental security principles for protecting user data.
Storing passwords insecurely significantly increases risk, especially if the database is compromised. Passwords must always be processed using strong, one way cryptographic hashing functions designed for password storage.

**Impact:**

Cryptographic failures involving password handling can lead to severe security consequences. If attackers gain access to the database, plaintext or weakly protected passwords can be immediately abused. This may result in account takeover, credential reuse attacks on other platforms, and widespread compromise of user accounts.

**How to fix it:**

The issue is mitigated by using Django’s built-in create_user method, which automatically applies secure password hashing before storing credentials in the database. This ensures that passwords are never stored in plaintext and are protected using industry-standard cryptographic practices.

**FIX:**

```python
user = User.objects.create_user(
    username=username,
    password=password
)
```

With this fix applied, user passwords are securely hashed before being stored. Even if the database is compromised, attackers cannot directly recover original passwords, significantly reducing the risk of further exploitation.

---

**Conclusion**

This project demonstrated several common web application security weaknesses based on the OWASP Top 10 (2021) list, which were implemented deliberately in a Django application. Each flaw highlighted how insecure design decisions, improper input handling, and missing authorization checks can lead to serious security risks. For every vulnerability, a corresponding fix was documented to illustrate secure coding practices and effective mitigation strategies.



