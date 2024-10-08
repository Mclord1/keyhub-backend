import datetime
import random
import string

from flask import request

from application import db
from application.models import ConfirmationCode, User, Parent, SchoolParent, Teacher, SchoolTeacher, Student
from application.module import current_user
from application.utils.emailHandler import EmailHandler
from exceptions.custom_exception import CustomException, ExceptionCode


class Helper:

    @classmethod
    def generate_token(cls):
        return ''.join(random.choices(string.digits, k=4))

    @classmethod
    def send_otp(cls, user):
        token = request.headers.get('Authorization').split()[1] if request.headers.get('Authorization') else ''
        otp_code = cls.generate_token()
        expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=2)
        add_to_confirmation = ConfirmationCode(email=user.email, user_id=user.id, code=otp_code, expiration=expiration_time)
        add_to_confirmation.save(refresh=True)
        EmailHandler.send_otp(user.email, otp_code, token)
        return f"OTP code has been sent to {user.email}"

    @classmethod
    def look_up_account(cls, Model, User, args):
        #
        # if not current_user.admins and not current_user.managers:
        #     raise CustomException(message="Only school manager or admin has the privilege")

        query = Model.query.join(User).filter(
            (Model.first_name.ilike(f'%{args}%') | Model.last_name.ilike(f'%{args}%'))
            | User.email.ilike(f'%{args}%')
        )

        if not current_user.admins and current_user.managers:
            if Model == Parent:
                query.filter(SchoolParent.school_id == current_user.managers.school_id)
            elif Model == Teacher:
                query.filter(SchoolTeacher.school_id == current_user.managers.school_id)
            else:
                query.filter(Model.school_id == current_user.managers.school_id)

        result = []
        for u in query.all():
            result_dict = {
                **u.to_dict(),
                'email': u.user.email,
                'user_id': u.user.id,
                'msisdn': u.user.msisdn,
                'isDeactivated': u.user.isDeactivated,
                'deactivate_reason': u.user.deactivate_reason,
            }
            result.append(result_dict)

        return result

    @classmethod
    def disable_account(cls, user, reason):
        try:
            user.isDeactivated = not user.isDeactivated
            user.deactivate_reason = reason
            db.session.commit()
            return f"{user.email} account has been deactivated" if user.isDeactivated else f"{user.email} account has been activated"

        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def User_Email_OR_Msisdn_Exist(cls, email, msisdn):
        user: User = db.session.query(User).filter(
            (User.email == email) or (User.msisdn == msisdn)
        ).first()

        if user:
            raise CustomException(
                message="The Email or Phone number already registered with other user.",
                status_code=400
            )

        return True

    @classmethod
    def get_user(cls, Model, user_id):

        # if not current_user.admins and not current_user.managers:
        #     raise CustomException(message="Only school manager or admin has the privilege", status_code=400)

        _user = Model.query.filter_by(id=user_id).first()

        if not _user:
            raise CustomException(message=f"{Model.__name__} does not exist", status_code=404)

        if Model == Teacher or Model == Parent:
            if not current_user.admins and (current_user.managers and current_user.managers.school_id not in [x.id for x in _user.schools]):
                raise CustomException(message="You do not have privilege to access this user", status_code=400)
        else:
            if not current_user.admins and (current_user.managers and current_user.managers.school_id != _user.school_id):
                raise CustomException(message="You do not have privilege to access this user", status_code=400)

        return _user
