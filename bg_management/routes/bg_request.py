from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory, abort
from flask_login import login_required, current_user
from database.models import db, BGRequest, BGAttachment, Department
from utils.helpers import log_action, save_uploaded_file
import os
from datetime import datetime

bg_request = Blueprint('bg_request', __name__)

@bg_request.route('/create-request', methods=['GET', 'POST'])
@login_required
def create():
    departments = Department.query.all()
    
    if request.method == 'POST':
        try:
            # Parse date fields
            date_of_request = datetime.strptime(request.form['date_of_request'], '%Y-%m-%d').date()
            bg_expiry_date = datetime.strptime(request.form['bg_expiry_date'], '%Y-%m-%d').date()
            
            new_req = BGRequest(
                p_no=request.form['p_no'].strip(),
                employee_name=request.form['employee_name'].strip(),
                email_id=request.form['email_id'].strip().lower(),
                department_id=int(request.form['department_id']),
                location=request.form['location'].strip(),
                date_of_request=date_of_request,
                work_order_no=request.form['work_order_no'].strip(),
                type_of_work=request.form['type_of_work'].strip(),
                job_value=float(request.form['job_value']),
                first_owner_name=request.form['first_owner_name'].strip(),
                alternate_owner=request.form.get('alternate_owner', '').strip() or None,
                party_name=request.form['party_name'].strip(),
                nature_of_bg=request.form['nature_of_bg'],
                bg_amount=float(request.form['bg_amount']),
                bg_expiry_date=bg_expiry_date,
                bg_claim_period=int(request.form['bg_claim_period']),
                remarks=request.form.get('remarks', '').strip() or None,
                status='Pending',
                user_id=current_user.id
            )
            new_req.set_approval_type()
            
            db.session.add(new_req)
            db.session.flush()  # Get ID before commit
            
            # Handle file uploads
            upload_folder = current_app.config['UPLOAD_FOLDER']
            file_fields = {
                'bg_draft': 'bg_drafts',
                'md_approval': 'md_approvals',
                'board_approval': 'board_approvals',
                'attachment_4': 'others',
                'attachment_5': 'others'
            }
            
            for field_name, subfolder in file_fields.items():
                file = request.files.get(field_name)
                if file and file.filename:
                    file_path, orig_name = save_uploaded_file(file, subfolder, upload_folder)
                    if file_path:
                        attachment = BGAttachment(
                            request_id=new_req.id,
                            file_type=field_name,
                            file_name=orig_name,
                            file_path=file_path
                        )
                        db.session.add(attachment)
            
            db.session.commit()
            log_action(f'BG Request created #{new_req.id}', 'bg_requests', new_req.id)
            flash(f'BG Request #{new_req.id} submitted successfully! Status: Pending', 'success')
            return redirect(url_for('bg_request.my_requests'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting request: {str(e)}', 'danger')
    
    return render_template('create_request.html', 
        departments=departments, 
        user=current_user,
        today=datetime.now().strftime('%Y-%m-%d'))

@bg_request.route('/my-requests')
@login_required
def my_requests():
    status_filter = request.args.get('status', '')
    query = BGRequest.query.filter_by(user_id=current_user.id)
    if status_filter:
        query = query.filter_by(status=status_filter)
    requests_list = query.order_by(BGRequest.created_at.desc()).all()
    return render_template('my_requests.html', requests=requests_list, status_filter=status_filter)

@bg_request.route('/request/<int:req_id>')
@login_required
def view_request(req_id):
    req = BGRequest.query.get_or_404(req_id)
    # Only owner, HOD, or Admin can view
    if req.user_id != current_user.id and current_user.role not in ['HOD', 'Admin']:
        abort(403)
    return render_template('request_detail.html', req=req)

@bg_request.route('/uploads/<path:filename>')
@login_required
def uploaded_file(filename):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    directory = os.path.join(upload_folder, os.path.dirname(filename))
    return send_from_directory(directory, os.path.basename(filename))
