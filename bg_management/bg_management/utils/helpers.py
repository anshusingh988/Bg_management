import os
from datetime import datetime
from database.models import AuditLog, db
from flask import request as flask_request
from flask_login import current_user

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, subfolder, upload_folder):
    """Save uploaded file and return path"""
    if file and allowed_file(file.filename):
        from werkzeug.utils import secure_filename
        import uuid
        ext = file.filename.rsplit('.', 1)[1].lower()
        unique_name = f"{uuid.uuid4().hex}.{ext}"
        folder_path = os.path.join(upload_folder, subfolder)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, unique_name)
        file.save(file_path)
        return os.path.join(subfolder, unique_name), file.filename
    return None, None

def log_action(action, table_name=None, record_id=None, details=None):
    """Log user action to audit trail"""
    try:
        user_id = current_user.id if current_user.is_authenticated else None
        ip = flask_request.remote_addr
        log = AuditLog(
            user_id=user_id,
            action=action,
            table_name=table_name,
            record_id=record_id,
            details=details,
            ip_address=ip
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        pass  # Don't fail main operation due to logging error

def format_currency(amount):
    """Format amount in Indian currency"""
    if amount >= 10000000:
        return f"₹{amount/10000000:.2f} Cr"
    elif amount >= 100000:
        return f"₹{amount/100000:.2f} L"
    else:
        return f"₹{amount:,.2f}"

def format_date(date_obj):
    if date_obj:
        return date_obj.strftime('%d-%m-%Y')
    return '-'
