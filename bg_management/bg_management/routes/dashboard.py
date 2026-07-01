from flask import Blueprint, render_template
from flask_login import login_required, current_user
from database.models import BGRequest, Approval, AuditLog, User
from sqlalchemy import func

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@dashboard.route('/dashboard')
@login_required
def index():
    # Stats for current user
    my_requests = BGRequest.query.filter_by(user_id=current_user.id).all()
    my_pending = sum(1 for r in my_requests if r.status == 'Pending')
    my_approved = sum(1 for r in my_requests if r.status == 'Approved')
    my_rejected = sum(1 for r in my_requests if r.status == 'Rejected')
    
    # Recent requests
    recent_requests = BGRequest.query.filter_by(user_id=current_user.id)\
        .order_by(BGRequest.created_at.desc()).limit(5).all()
    
    # HOD stats
    pending_approvals = []
    if current_user.role in ['HOD', 'Admin']:
        pending_approvals = BGRequest.query.filter_by(status='Pending').order_by(BGRequest.created_at.desc()).all()
    
    # Recent audit logs
    recent_activity = AuditLog.query.filter_by(user_id=current_user.id)\
        .order_by(AuditLog.timestamp.desc()).limit(8).all()
    
    # Total system stats (admin)
    total_requests = BGRequest.query.count()
    total_amount = BGRequest.query.filter_by(status='Approved').with_entities(func.sum(BGRequest.bg_amount)).scalar() or 0
    
    return render_template('dashboard.html',
        my_requests=my_requests,
        my_pending=my_pending,
        my_approved=my_approved,
        my_rejected=my_rejected,
        recent_requests=recent_requests,
        pending_approvals=pending_approvals,
        recent_activity=recent_activity,
        total_requests=total_requests,
        total_amount=total_amount
    )
