# 📚 EMS System - Education Management System

🚀 **EMS System** is a fully-featured education management system that provides an interactive environment for students, instructors, and assistants. It supports course management, assignments, chat, and grading system.

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

## 🔮 Upcoming Features

- ✅ Attendance System (track student presence and generate reports)
- 🗓️ Timetable & Scheduling (with notifications and reminders)
- 🎥 Enhanced Course Materials (support for videos, PDFs, and slides)
- 📊 Student Dashboard & Analytics (progress tracking and insights)
- 🧪 Quizzes & Exams System (multiple question types with auto-grading)
- 📈 Gradebook & Transcripts (GPA calculation and exportable transcripts)
- 📁 Advanced Assignment Submission (multi-file, resubmission, feedback)
- 🌐 Multi-language Support (English/Arabic with i18n)
- 🔐 Role-Based Permissions (fine-grained access control)
- 🎓 Certificate Generator (auto-generated course completion certificates)
- 📬 Email & In-App Notifications (for assignments, messages, updates)
- 🔎 Search & Filter System (courses, messages, assignments)
- 🧑‍💼 Feedback & Rating System (students rate courses and instructors)
- 🤖 AI-Powered Features (recommendations and plagiarism detection)
---


## 🛠️ Tech Stack  

- **Backend:** Django + Django REST Framework (DRF)  
- **Database:** PostgreSQL  
- **Authentication:** JWT / Token-Based Authentication  
- **Messaging:** WebSockets / Django Channels  
- **Frontend:** _(Planned for future development)_  

---

## 🚀 Setup & Installation  


0️⃣ Clone the Repository  
```sh
mkdir project
cd project
git clone https://github.com/AhmedHashim04/EducationManagementSystem.git .
```

### 🟢 Windows Setup  
1️⃣ **Install Python and PostgreSQL**  
- Download and install [Python](https://www.python.org/downloads/)  
- Download and install [PostgreSQL](https://www.postgresql.org/download/)  

2️⃣ **Set Up Virtual Environment**  
```sh
python -m venv .
venv\Scripts\activate
```

3️⃣ **Install Dependencies**  
```sh
pip install --upgrade pip
pip install -r requirements.txt
```

4️⃣ **Configure PostgreSQL Database**  
- Open **pgAdmin** or connect via terminal.  
- Create a database (e.g., `ems_db`).  
- Update `DATABASES` settings in `settings.py`.  

5️⃣ **Apply Migrations & Create Superuser**  
```sh
python manage.py migrate
python manage.py createsuperuser
```

6️⃣ **Run the Server**  
```sh
python manage.py runserver
```

✅ Open **`http://127.0.0.1:8000/`** in your browser.  

### 🟢 Linux Setup  
```sh
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib -y
python3 -m venv .
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

🔹 **Configure PostgreSQL**  
```sh
sudo -i -u postgres
psql
CREATE DATABASE ems_db;
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ems_db TO your_username;
\q
exit
```

🔹 **Apply Migrations & Run Server**  
```sh
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 📢 API Endpoints  

### 👤 Authentication  

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/account/register/` | Register a new user |
| `POST` | `/api/account/token/` | Obtain a JWT token |
| `POST` | `/api/account/token/refresh/` | Refresh a JWT token |
| `POST` | `/api/account/token/verify/` | Verify a JWT token |
| `POST` | `/api/account/password-reset/` | Request a password reset |
| `POST` | `/api/account/password_change/` | Change the user's password |
| `GET`  | `/api/account/profile/` | Retrieve the user's profile |

### 📚 Courses  

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/courses/` | List all courses |
| `GET`  | `/api/courses/me/` | List courses the user is enrolled in |
| `GET`  | `/api/courses/me/{course_code}/` | Retrieve details of a specific course |
| `POST` | `/api/courses/me/{course_code}/permession/` | Assign assistant permissions (Admin only) |
| `GET`  | `/api/courses/me/{course_code}/materials/` | Retrieve course materials |

### 📝 Assignments  

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/courses/me/{course_code}/assignments/` | List all assignments for a course |
| `POST` | `/api/courses/me/{course_code}/assignments/` | Create a new assignment (Instructor only) |
| `GET`  | `/api/courses/me/{course_code}/assignments/{assignment_slug}/` | Retrieve details of a specific assignment |
| `POST` | `/api/courses/me/{course_code}/assignments/{assignment_slug}/solution/` | Submit a solution for an assignment (Student only) |
| `POST` | `/api/courses/me/{course_code}/assignments/{assignment_slug}/solution/{solution_id}/grade/` | Grade a submitted solution (Instructor only) |

### 💬 Chat System  

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/chat/` | List all chats for the user |
| `POST` | `/api/chat/` | Create a new chat |
| `GET`  | `/api/chat/{id}/` | Retrieve details of a specific chat |
| `GET`  | `/api/chat/{chat_id}/messages/` | List all messages in a chat |
| `POST` | `/api/chat/{chat_id}/messages/` | Send a message in a chat |

---

## 👤 Contributors  
- **Ahmed Hashim** - Backend Developer  

---

## 📜 License  
This project is open-source under the **MIT License**.
---

