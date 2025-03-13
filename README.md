# 📚 EMS System - Education Management System

🚀 **EMS System** is a fully-featured education management system that provides an interactive environment for students, instructors, and assistants. It supports course management, assignments, and an internal chat system.

---

## 📌 Features  

### 🔹 User Management  
- **Admin:** Assigns instructors and assistants to courses.  
- **Instructor:** Manages course content and student activities.  
- **Assistant:** Supports instructors and supervises content.  
- **Student:** Can enroll in or leave courses freely.  

### 📚 Course Management  
- Create, update, and manage courses.  
- Students can enroll or leave courses freely.  
- Admin assigns instructors and assistants.  

### 📝 Assignments System  
- Instructors and assistants can add assignments.  
- Students can submit their solutions.  
- Instructors review and grade submissions.  

### 💬 Chat System  
- Real-time messaging between students.  
- Direct messages between students, assistants, and instructors.  

### 🔔 Notification System  
- Alerts for new assignments, course updates, and new messages.  

---

## 🛠️ Tech Stack  

- **Backend:** Django + Django REST Framework (DRF)  
- **Database:** PostgreSQL  
- **Authentication:** JWT / Token-Based Authentication  
- **Messaging:** WebSockets / Django Channels  
- **Frontend:** _(Planned for future development)_  

---

## 🚀 Setup & Installation  

### 1️⃣ Install Dependencies  
```sh
pip install -r requirements.txt
```

### 2️⃣ Apply Migrations  
```sh
python manage.py migrate
```

### 3️⃣ Run the Server  
```sh
python manage.py runserver
```

### 4️⃣ Create an Admin User  
```sh
python manage.py createsuperuser
```

---

## 📢 API Endpoints  

### 👤 Authentication  
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/register/` | Register a new user |
| `POST` | `/api/auth/login/` | Authenticate and obtain a token |
| `POST` | `/api/auth/logout/` | Log out the user |

### 📚 Courses  
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/courses/` | List all courses |
| `POST` | `/api/courses/` | Create a new course (Admin only) |
| `POST` | `/api/courses/enroll/` | Enroll a student in a course |
| `POST` | `/api/courses/leave/` | Withdraw a student from a course |

### 📝 Assignments  
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/assignments/` | List all assignments |
| `POST` | `/api/assignments/` | Create a new assignment (Instructor only) |
| `POST` | `/api/assignments/submit/` | Submit an assignment (Student only) |

---

## 👤 Contributors  
- **Ahmed Hashim** - Backend Developer  

---

## 📜 License  
This project is open-source under the **MIT License**.  
