# BG Management System

A Flask-based Bank Guarantee (BG) Management System with HOD Approval workflow.

## Features
- Role-based access: Admin, HOD, Employee
- BG request creation and tracking
- HOD approval/rejection workflow
- Department-wise management
- Live pending approval count on dashboard

## Tech Stack
- Backend: Flask, Flask-Login, Flask-SQLAlchemy
- Database: MySQL (via PyMySQL)
- Frontend: Jinja2 templates
- Deployment: Render.com (Gunicorn)

## Default Credentials (for testing)
| Role | Email | Password |
|------|-------|----------|
| Admin | (contact for demo access) | - |

## Setup (Local)
```bash
pip install -r requirements.txt
python app.py
```

## Deployment
Deployed on Render.com
- Root Directory: `bg_management`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

