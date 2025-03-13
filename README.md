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
| `POST` | `/api/auth/register/` | Register a new user |
| `POST` | `/api/auth/login/` | Authenticate and obtain a token |
| `POST` | `/api/auth/logout/` | Log out the user |
| `POST` | `/api/auth/forgot-password/` | Request password reset |

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
| `POST` | `/api/assignments/grade/` | Grade an assignment (Instructor only) |

### 💬 Chat System  
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/chat/conversations/` | Get all conversations for a user |
| `POST` | `/api/chat/message/` | Send a message |
| `GET`  | `/api/chat/messages/{conversation_id}/` | Retrieve messages in a conversation |

---

## 👤 Contributors  
- **Ahmed Hashim** - Backend Developer  

---

## 📜 License  
This project is open-source under the **MIT License**.  
