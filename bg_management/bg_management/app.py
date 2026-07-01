from flask import Flask, redirect, url_for
from flask_login import LoginManager
from config import Config
from database.models import db, User, Department
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Init extensions
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please login to access this page.'
    login_manager.login_message_category = 'warning'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_pending_bg_count():
        """Makes the live count of pending BG requests available to every
        template (used for the 'Approvals' badge in the sidebar for HOD/Admin)."""
        from flask_login import current_user as _cu
        from database.models import BGRequest
        if _cu.is_authenticated and _cu.role in ['HOD', 'Admin']:
            count = BGRequest.query.filter_by(status='Pending').count()
            return dict(pending_bg_count=count)
        return dict(pending_bg_count=0)
    
    # Register blueprints
    from routes.auth import auth
    from routes.dashboard import dashboard
    from routes.bg_request import bg_request
    from routes.approval import approval
    from routes.reports import reports
    
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(bg_request)
    app.register_blueprint(approval)
    app.register_blueprint(reports)
    
    @app.route('/')
    def index():
        return redirect(url_for('dashboard.index'))
    
    # Create tables and seed data
    with app.app_context():
        db.create_all()
        seed_data()
    
    return app

def seed_data():
    """Seed initial departments and admin user"""
    if Department.query.count() == 0:
        departments = [
            Department(name='Civil Engineering', location='Jamshedpur'),
            Department(name='Mechanical Engineering', location='Jamshedpur'),
            Department(name='Electrical Engineering', location='Jamshedpur'),
            Department(name='IT Department', location='Jamshedpur'),
            Department(name='Finance', location='Jamshedpur'),
            Department(name='HR Department', location='Jamshedpur'),
            Department(name='Operations', location='Bokaro'),
            Department(name='Procurement', location='Ranchi'),
        ]
        for dept in departments:
            db.session.add(dept)
        db.session.commit()
        print("✅ Departments seeded")
    
    if User.query.count() == 0:
        admin = User(
            p_no='ADMIN001',
            name='System Admin',
            email='admin@bgms.com',
            department_id=1,
            role='Admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        hod = User(
            p_no='HOD001',
            name='HOD Manager',
            email='hod@bgms.com',
            department_id=1,
            role='HOD'
        )
        hod.set_password('hod123')
        db.session.add(hod)
        
        emp = User(
            p_no='EMP001',
            name='Test Employee',
            email='employee@bgms.com',
            department_id=2,
            role='Employee'
        )
        emp.set_password('emp123')
        db.session.add(emp)
        
        db.session.commit()
        print("✅ Default users seeded:")
        print("   Admin: admin@bgms.com / admin123")
        print("   HOD:   hod@bgms.com / hod123")
        print("   Emp:   employee@bgms.com / emp123")

if __name__ == '__main__':
    # app = create_app()
    # app.run(debug=True, port=5000)

    app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
