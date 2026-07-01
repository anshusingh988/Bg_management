from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from database.models import db, BGRequest, Approval
from utils.helpers import log_action
from utils.decorators import hod_required
from datetime import datetime

approval = Blueprint('approval', __name__)

@approval.route('/approvals')
@login_required
@hod_required
def approvals_list():
    status_filter = request.args.get('status', 'Pending')
    query = BGRequest.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    requests = query.order_by(BGRequest.created_at.desc()).all()
    return render_template('approval.html', requests=requests, status_filter=status_filter)

@approval.route('/approve/<int:req_id>', methods=['POST'])
@login_required
@hod_required
def approve_request(req_id):
    req = BGRequest.query.get_or_404(req_id)
    decision = request.form.get('decision')
    remarks = request.form.get('remarks', '').strip()
    
    if decision not in ['Approved', 'Rejected']:
        flash('Invalid decision.', 'danger')
        return redirect(url_for('approval.approvals_list'))
    
    # Update request status
    req.status = decision
    req.updated_at = datetime.utcnow()
    
    # Store approval record
    appr = Approval(
        request_id=req.id,
        hod_id=current_user.id,
        decision=decision,
        remarks=remarks
    )
    db.session.add(appr)
    db.session.commit()
    
    log_action(f'BG Request #{req.id} {decision} by HOD', 'bg_requests', req.id, f'Remarks: {remarks}')
    flash(f'Request #{req.id} has been {decision}.', 'success' if decision == 'Approved' else 'warning')
    return redirect(url_for('approval.approvals_list'))
