import os

from flask import send_from_directory

from application import app, jwt, socketio
from application.api import *
from application.models import User

EXEC_ENV = os.environ.get('EXEC_ENV')

# BLUEPRINT REGISTRATION
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(roles_permission_blueprint, url_prefix='/role-permission')
app.register_blueprint(school_blueprint, url_prefix='/school')
app.register_blueprint(teacher_blueprint, url_prefix='/teacher')
app.register_blueprint(student_blueprint, url_prefix='/student')
app.register_blueprint(parent_blueprint, url_prefix='/parent')
app.register_blueprint(helper_blueprint, url_prefix='/helper')
app.register_blueprint(subcription_blueprint, url_prefix='/subscription')
app.register_blueprint(transaction_blueprint, url_prefix='/transaction')
app.register_blueprint(audit_blueprint, url_prefix='/audit')
app.register_blueprint(sme_bp, url_prefix='/sme')
app.register_blueprint(keywords_bp, url_prefix='/keywords')
app.register_blueprint(curriculum_bp, url_prefix='/curriculums')
app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')
app.register_blueprint(report_blueprint, url_prefix='/reports')
app.register_blueprint(notification_blueprint, url_prefix='/notification')
app.register_blueprint(checklists_bp, url_prefix='/checklist')
app.register_blueprint(message_blueprint, url_prefix='/message')


@jwt.user_lookup_loader
def _user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data['sub']
    # Retrieve the user object based on the identity (user ID)
    user = User.query.filter_by(id=identity).first()
    return user


if __name__ == '__main__':
    # socketio.run(app, host='0.0.0.0', port=2000, debug=True)
    app.run(host='0.0.0.0', port=5001, debug=True)
    # app.run(port=5000, debug=True)
