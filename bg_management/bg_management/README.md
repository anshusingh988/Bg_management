# 🏦 Bank Guarantee Management System
### Full-Stack Web Application | Python Flask + SQLAlchemy + Bootstrap 5

---

## 📋 Project Overview
Complete BG Management System with user authentication, 19-field BG request form,
HOD approval workflow, Excel report export, and audit trail.

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Open Browser
```
http://localhost:5000
```

---

## 🔐 Default Login Credentials

| Role     | Email                 | Password  |
|----------|-----------------------|-----------|
| Admin    | admin@bgms.com        | admin123  |
| HOD      | hod@bgms.com          | hod123    |
| Employee | employee@bgms.com     | emp123    |

> **Note:** These are created automatically on first run. Change passwords after login.

---

## 📁 Project Structure
```
bg_management_system/
├── app.py                  ← Main Flask app (run this)
├── config.py               ← Configuration settings
├── requirements.txt        ← Python packages
├── database/
│   ├── models.py           ← Database models (User, BGRequest, etc.)
│   └── __init__.py
├── routes/
│   ├── auth.py             ← Signup / Login / Logout
│   ├── dashboard.py        ← Dashboard stats
│   ├── bg_request.py       ← Create & view BG requests
│   ├── approval.py         ← HOD approval workflow
│   └── reports.py          ← Excel export
├── templates/
│   ├── base.html           ← Sidebar layout
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── create_request.html ← 19-field BG form
│   ├── my_requests.html
│   ├── request_detail.html
│   ├── approval.html       ← HOD queue
│   └── reports.html
├── utils/
│   ├── helpers.py          ← Utility functions
│   └── decorators.py       ← Role-based access
└── uploads/                ← File attachments (auto-created)
```

---

## ✅ Features Implemented

### Authentication
- [x] User Registration with P.No, Name, Email, Department, Role
- [x] Secure login with password hashing (Werkzeug)
- [x] Session management (Flask-Login)
- [x] Role-based access (Employee / HOD / Admin)

### BG Request Module (All 19 Fields)
- [x] P.No, Employee Name, Email, Department, Location, Date
- [x] Work Order No, Type of Work, Job Value
- [x] First Owner, Alternate Owner
- [x] Party Name, Nature of BG, BG Amount, Expiry Date, Claim Period
- [x] Remarks, Status (auto-set to Pending)
- [x] File Attachments (BG Draft, MD Approval, Board Approval + 2 more)

### Approval Workflow
- [x] **Amount ≤ ₹15 Lakhs** → MD Approval type
- [x] **Amount > ₹15 Lakhs** → Board Approval type
- [x] HOD can Approve / Reject with remarks
- [x] Status flow: Pending → Approved/Rejected
- [x] Quick approval modal on approval page

### Dashboard
- [x] My request statistics (Total, Pending, Approved, Rejected)
- [x] Recent requests table
- [x] Pending approvals widget (HOD only)
- [x] Quick actions panel
- [x] Recent activity log

### Reports & Export
- [x] BG Report → Excel (.xlsx) with filters (date, status)
- [x] Color-coded status cells in Excel
- [x] Frozen header row, professional formatting
- [x] Audit Trail → Excel (Admin only)
- [x] Quick export links by status

### Security
- [x] Password hashing (never stored plain text)
- [x] Role-based access control decorators
- [x] File upload validation (type & size)
- [x] SQL injection prevention (SQLAlchemy ORM)
- [x] Session-based authentication

---

## 🗄️ Database
Uses **SQLite** by default (no setup needed).
To switch to **MySQL**, update `config.py`:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/bg_management'
```

---

## 📊 Database Tables
| Table         | Purpose                    |
|---------------|----------------------------|
| users         | User accounts & roles      |
| departments   | Department master data     |
| bg_requests   | All BG requests (19 fields)|
| bg_attachments| Uploaded documents         |
| approvals     | HOD approval records       |
| audit_log     | System activity trail      |

---

## 🛠️ Tech Stack
- **Backend:** Python 3.8+ / Flask 2.3
- **Database:** SQLite (default) / MySQL compatible
- **ORM:** Flask-SQLAlchemy
- **Auth:** Flask-Login + Werkzeug security
- **Frontend:** Bootstrap 5 + Font Awesome 6
- **Excel Export:** OpenPyXL
- **File Uploads:** Werkzeug FileStorage

---

## 📞 Support
For issues, check the Flask logs in terminal when running `python app.py`
