from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    users = db.relationship('User', backref='department', lazy=True)
    bg_requests = db.relationship('BGRequest', backref='department', lazy=True)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    p_no = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    role = db.Column(db.String(20), default='Employee')  # Employee, HOD, Admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    bg_requests = db.relationship('BGRequest', backref='requester', lazy=True, foreign_keys='BGRequest.user_id')
    approvals = db.relationship('Approval', backref='hod', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

class BGRequest(db.Model):
    __tablename__ = 'bg_requests'
    id = db.Column(db.Integer, primary_key=True)
    
    # Field 1-6: Basic Info
    p_no = db.Column(db.String(20), nullable=False)
    employee_name = db.Column(db.String(100), nullable=False)
    email_id = db.Column(db.String(120), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date_of_request = db.Column(db.Date, nullable=False)
    
    # Field 7-9: Work Details
    work_order_no = db.Column(db.String(50), nullable=False)
    type_of_work = db.Column(db.String(100), nullable=False)
    job_value = db.Column(db.Float, nullable=False)
    
    # Field 10-11: Owners
    first_owner_name = db.Column(db.String(100), nullable=False)
    alternate_owner = db.Column(db.String(100))
    
    # Field 12-16: BG Details
    party_name = db.Column(db.String(100), nullable=False)
    nature_of_bg = db.Column(db.String(50), nullable=False)
    bg_amount = db.Column(db.Float, nullable=False)
    bg_expiry_date = db.Column(db.Date, nullable=False)
    bg_claim_period = db.Column(db.Integer, nullable=False)  # in days
    
    # Field 17-18: Extra
    remarks = db.Column(db.Text)
    status = db.Column(db.String(30), default='Pending')  # Pending, Under Review, Approved, Rejected, Completed
    
    # System fields
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    approval_type = db.Column(db.String(20))  # MD or Board (auto-set based on amount)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attachments = db.relationship('BGAttachment', backref='bg_request', lazy=True, cascade='all, delete-orphan')
    approvals = db.relationship('Approval', backref='bg_request', lazy=True, cascade='all, delete-orphan')
    
    def set_approval_type(self):
        if self.bg_amount <= 1500000:  # 15 Lakhs
            self.approval_type = 'MD'
        else:
            self.approval_type = 'Board'
    
    def get_status_badge_class(self):
        badges = {
            'Pending': 'badge-warning',
            'Under Review': 'badge-info',
            'Approved': 'badge-success',
            'Rejected': 'badge-danger',
            'Completed': 'badge-secondary',
            'Cancelled': 'badge-dark'
        }
        return badges.get(self.status, 'badge-secondary')

class BGAttachment(db.Model):
    __tablename__ = 'bg_attachments'
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('bg_requests.id'), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)  # bg_draft, md_approval, board_approval, other
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Approval(db.Model):
    __tablename__ = 'approvals'
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('bg_requests.id'), nullable=False)
    hod_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    decision = db.Column(db.String(20), nullable=False)  # Approved, Rejected
    remarks = db.Column(db.Text)
    approved_date = db.Column(db.DateTime, default=datetime.utcnow)

class AuditLog(db.Model):
    __tablename__ = 'audit_log'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(200), nullable=False)
    table_name = db.Column(db.String(50))
    record_id = db.Column(db.Integer)
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
