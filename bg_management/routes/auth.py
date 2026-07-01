from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from database.models import db, User, Department
from utils.helpers import log_action

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    departments = Department.query.all()
    
    if request.method == 'POST':
        p_no = request.form.get('p_no', '').strip()
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        department_id = request.form.get('department_id')
        role = request.form.get('role', 'Employee')
        
        # Validations
        if not all([p_no, name, email, password, department_id]):
            flash('All required fields must be filled.', 'danger')
            return render_template('signup.html', departments=departments)
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('signup.html', departments=departments)
        
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('signup.html', departments=departments)
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('signup.html', departments=departments)
        
        if User.query.filter_by(p_no=p_no).first():
            flash('P.No already registered.', 'danger')
            return render_template('signup.html', departments=departments)
        
        user = User(
            p_no=p_no,
            name=name,
            email=email,
            department_id=int(department_id),
            role=role
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        log_action(f'User registered: {email}', 'users', user.id)
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('signup.html', departments=departments)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password) and user.is_active:
            login_user(user, remember=bool(remember))
            log_action(f'User logged in: {email}', 'users', user.id)
            flash(f'Welcome back, {user.name}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    log_action(f'User logged out: {current_user.email}', 'users', current_user.id)
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
