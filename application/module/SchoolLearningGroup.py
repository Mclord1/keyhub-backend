from . import *
from ..Schema.school import LearningGroupSchema


class SchoolLearningGroupsModel:

    @classmethod
    def list_all_groups(cls, school_id, page, per_page):
        page = int(page)
        per_page = int(per_page)
        _group = LearningGroup.query.filter(LearningGroup.school_id == school_id).order_by(
            desc(LearningGroup.created_at)).paginate(page=page, per_page=per_page, error_out=False)
        total_items = _group.total
        results = [item for item in _group.items]
        total_pages = (total_items - 1) // per_page + 1

        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": {
                "total_active": len([x for x in results if not x.isDeactivated]),
                "total_inactive": len([x for x in results if x.isDeactivated]),
                "groups": [{
                    **res.to_dict(add_filter=False),
                    "created_by": res.user.email if res.user else None,
                    "creator_name": f'{res.user.admins.first_name} {res.user.admins.last_name}' if res.user and res.user.admins else None,
                    'students': [x.to_dict() for x in res.students],
                    'teachers': [x.to_dict() for x in res.teachers],
                    'projects': [x.to_dict(add_filter=False) for x in res.projects],
                }
                    for res in results]
            }
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def get_group_detail(cls, school_id, group_id):
        _group: LearningGroup = LearningGroup.GetLearningGroupID(school_id, group_id)
        result = {
            'name': _group.name,
            'created_on': _group.created_at,
            'created_by': _group.user.email if _group.user else None,
            'creator_name': f'{_group.user.admins.first_name} {_group.user.admins.last_name}' if _group.user and _group.user.admins else None,
            'country': _group.user.admins.country if _group.user and _group.user.admins else None,
            'description': _group.description,
            'isDeactivated': _group.isDeactivated,
            'students': [x.to_dict() for x in _group.students],
            'teachers': [x.to_dict() for x in _group.teachers],
            'projects': [x.to_dict(add_filter=False) for x in _group.projects],
        }
        return result

    @classmethod
    def search_learning_group(cls, args, school_id):
        query = LearningGroup.query.filter(LearningGroup.school_id == int(school_id)).filter(
            (LearningGroup.name.ilike(f'%{args}%'))
        )

        result = [
            {
                'id': _group.id,
                'name': _group.name,
                'created_on': _group.created_at,
                'created_by': _group.user.email if _group.user else None,
                'creator_name': f'{_group.user.admins.first_name} {_group.user.admins.last_name}' if _group.user and _group.user.admins else None,
                'country': _group.user.admins.country if _group.user and _group.user.admins else None,
                'description': _group.description,
                'isDeactivated': _group.isDeactivated,
                'students': [x.to_dict() for x in _group.students],
                'teachers': [x.to_dict() for x in _group.teachers],
                'projects': [x.to_dict(add_filter=False) for x in _group.projects],
            }

            for _group in query.all()]
        return result

    @classmethod
    def create_learning_group(cls, data, school_id):
        _school = School.GetSchool(school_id)
        req: LearningGroupSchema = validator.validate_data(LearningGroupSchema, data)

        try:
            new_group = LearningGroup(name=req.name, created_by=current_user.id, description=req.description, schools=_school)
            new_group.save(refresh=True)
            Audit.add_audit('Added School Learning group', current_user, new_group.to_dict(add_filter=False))
            return new_group.to_dict(add_filter=False)
        except IntegrityError:
            db.session.rollback()
            raise CustomException(message="A Learning group with the name already exist")

    @classmethod
    def toggle_school_learning_group_status(cls, school_id, group_id):
        _group: LearningGroup = LearningGroup.GetLearningGroupID(school_id, group_id)

        try:
            _group.isDeactivated = not _group.isDeactivated
            db.session.commit()
            Audit.add_audit("Deactivated learning group" if _group.isDeactivated else "Activate learning group ", current_user, _group.to_dict(add_filter=False))
            return f"The Group has been deactivated" if _group.isDeactivated else "The Group has been activated"
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def delete_group(cls, school_id, group_id):
        _group: LearningGroup = LearningGroup.GetLearningGroupID(school_id, group_id)

        if _group.students or _group.teachers or _group.projects:
            raise CustomException(message="There are users associated to this school group", status_code=500)

        try:

            db.session.commit()
            db.session.delete(_group)
            Audit.add_audit('Deleted Learning group', current_user, _group.to_dict(add_filter=False))
            db.session.commit()
            return "The group has been deleted"
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def update_group(cls, school_id, group_id, name, description):
        try:
            _group: LearningGroup = LearningGroup.GetLearningGroupID(school_id, group_id)
            if name:
                _group.name = name
            if description:
                _group.description = description
            db.session.commit()
            Audit.add_audit('Updated Learning group information', current_user, _group.to_dict(add_filter=False))

            subscribed_users = [x.user_id for x in _group.subscribed_groups]
            Notification.send_push_notification(subscribed_users, f"{_group.name} information has been updated", LearningGroup.__name__, {"id": _group.id})
            return _group.to_dict(add_filter=False)
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)

    @classmethod
    def add_comment(cls, school_id, group_id, comment, file, file_name):

        group: LearningGroup = LearningGroup.GetLearningGroupID(school_id, group_id)

        stored_file_name, profile_url, file_path, content_type = None, None, None, None

        comment = comment if comment else None

        if file:
            file_path, stored_file_name = FileFolder.learning_group_file(group.schools.name, group.name, file_name)
            profile_url, content_type = FileHandler.upload_file(file, file_path)

        new_comment = LearningGroupComment(
            learning_group_id=group.id,
            user_id=current_user.id,
            comment=comment,
            file_name=stored_file_name,
            file_url=profile_url,
            file_path=file_path,
            content_type=content_type
        )

        new_comment.save(refresh=True)

        subscribed_users = [x.user_id for x in group.subscribed_groups]
        Notification.send_push_notification(subscribed_users, new_comment.comment, LearningGroup.__name__, {"id": new_comment.id})
        return "Comment has been added successfully"

    @classmethod
    def get_comments(cls, school_id, group_id):
        group: LearningGroup = LearningGroup.GetLearningGroupID(school_id, group_id)
        return [
            {
                **x.to_dict(add_filter=False),
                "commented_by": {
                    **User.GetUserObject(x.user.id)
                },
            }
            for x in group.learning_group_comments]

    @classmethod
    def edit_comments(cls, group_id, comment_id, new_comment, new_file, new_file_name):
        comments: LearningGroupComment = LearningGroupComment.query.filter_by(learning_group_id=group_id, id=comment_id).first()

        if not comments:
            raise CustomException(message="Comment not found", status_code=404)

        if not current_user.managers or current_user.id != comments.user_id:
            if not current_user.admins:
                raise CustomException(message="Only comment author or admin can delete this comment", status_code=400)

        group: LearningGroup = LearningGroup.query.filter_by(id=group_id).first()

        if new_file:
            new_file_name = new_file_name if new_file_name else comments.file_name
            file_path, stored_file_name = FileFolder.learning_group_file(group.schools.name, group.name, new_file_name)
            profile_url, content_type = FileHandler.update_file(new_file, file_path)
            comments.content_type = content_type
            comments.file_path = file_path
            comments.file_name = stored_file_name
            comments.file_url = profile_url

        if new_comment:
            comments.comment = new_comment

        db.session.commit()
        return "Comment has been updated successfully"

    @classmethod
    def remove_comment(cls, group_id, comment_id):
        comments: LearningGroupComment = LearningGroupComment.query.filter_by(learning_group_id=group_id, id=comment_id).first()
        if not comments:
            raise CustomException(message="Comment not found", status_code=404)

        if (not current_user.managers) or (current_user.id != comments.user_id):
            if not current_user.admins:
                raise CustomException(message="Only comment author or admin can delete this comment", status_code=400)

        FileHandler.delete_file(comments.file_name)
        comments.delete()

        group: LearningGroup = LearningGroup.query.filter_by(id=group_id).first()

        subscribed_users = [x.user_id for x in group.subscribed_groups]
        Notification.send_push_notification(subscribed_users, f"{current_user.email} has removed a comment", LearningGroup.__name__)
        return "Comment has been deleted successfully"

    @classmethod
    def add_file(cls, school_id, group_id, file, file_name):
        group: LearningGroup = LearningGroup.GetLearningGroupID(school_id, group_id)

        file_path, stored_file_name = FileFolder.learning_group_file(group.schools.name, group.name, file_name)

        profile_url, content_type = FileHandler.upload_file(file, file_path)

        new_file = LearningGroupFile(learning_group_id=group.id, file_name=stored_file_name, file_url=profile_url, file_path=file_path, user_id=current_user.id, content_type=content_type)
        new_file.save(refresh=True)

        subscribed_users = [x.user_id for x in group.subscribed_groups]
        Notification.send_push_notification(subscribed_users, f"{current_user.email} added a new file", LearningGroup.__name__)
        return "File has been added successfully"

    @classmethod
    def get_files(cls, school_id, group_id):
        group: LearningGroup = LearningGroup.GetLearningGroupID(school_id, group_id)
        return [
            {
                **x.to_dict(add_filter=False),
                "uploaded_by": x.user.to_dict() | User.GetUserObject(x.user.id),
                "file_url": FileHandler.get_file_url(x.file_path)
            }
            for x in group.learning_group_files]

    @classmethod
    def remove_file(cls, group_id, file_id):
        _files: LearningGroupFile = LearningGroupFile.query.filter_by(learning_group_id=group_id, id=file_id).first()
        if not _files:
            raise CustomException(message="File not found", status_code=404)

        if not current_user.managers or current_user.id != _files.user_id:
            if not current_user.admins:
                raise CustomException(message="Only File author or admin can delete this File", status_code=400)

        FileHandler.delete_file(_files.file_path)
        _files.delete()

        group: LearningGroup = LearningGroup.query.filter_by(id=group_id).first()

        subscribed_users = [x.user_id for x in group.subscribed_groups]
        Notification.send_push_notification(subscribed_users, f"{current_user.email} removed a file", LearningGroup.__name__)
        return "File has been deleted successfully"

    @classmethod
    def subscribe(cls, group_id, school_id):
        group: LearningGroup = LearningGroup.GetLearningGroupID(school_id, group_id)

        try:
            subscribe = LearningGroupSubscription(learning_group_id=group.id, user_id=current_user.id)
            subscribe.save()
            return f"You have successfully subscribed to {group.name}"
        except IntegrityError:
            db.session.rollback()
            raise CustomException(message="You are already subscribed to this group.", status_code=400)
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def unsubscribe(cls, group_id):
        group: LearningGroupSubscription = LearningGroupSubscription.query.filter_by(learning_group_id=group_id, user_id=current_user.id).first()

        if not group:
            raise CustomException(message="Learning Group not found", status_code=404)

        group.delete()
        return "You have been removed from the learning group."


class ChildComment:

    @classmethod
    def add_comment(cls, comment_id, comment):
        group_comment: LearningGroupComment = LearningGroupComment.query.filter_by(id=int(comment_id)).first()

        if not group_comment:
            raise CustomException(message="Comment not found", status_code=404)

        new_comment = LearningGroupChildComment(learning_group_comment_id=group_comment.id, user_id=current_user.id, comment=comment)
        new_comment.save(refresh=True)

        subscribed_users = [x.user_id for x in group_comment.learning_groups.subscribed_groups]
        Notification.send_push_notification(subscribed_users, new_comment.comment, LearningGroup.__name__, {"id": new_comment.id})
        return "Comment has been added successfully"

    @classmethod
    def get_comments(cls, comment_id):
        group_comment: [LearningGroupChildComment] = LearningGroupChildComment.query.filter_by(learning_group_comment_id=comment_id).all()
        return [
            {
                **x.to_dict(add_filter=False),
                "commented_by": {
                    **User.GetUserObject(x.user.id)
                },
            }
            for x in group_comment]

    @classmethod
    def edit_comments(cls, comment_id, new_comment):

        group_comment: LearningGroupChildComment = LearningGroupChildComment.query.filter_by(id=int(comment_id)).first()

        if not group_comment:
            raise CustomException(message="Comment not found", status_code=404)

        if not current_user.managers and (int(current_user.id) != int(group_comment.user_id)):
            if not current_user.admins:
                raise CustomException(message="Only comment author or admin can edit this comment", status_code=400)

        group_comment.comment = new_comment
        db.session.commit()
        return "Comment has been updated successfully"

    @classmethod
    def remove_comment(cls, comment_id):
        group_comment: LearningGroupChildComment = LearningGroupChildComment.query.filter_by(id=comment_id).first()
        if not group_comment:
            raise CustomException(message="Comment not found", status_code=404)

        if not current_user.managers and current_user.id != group_comment.user_id:
            if not current_user.admins:
                raise CustomException(message="Only comment author or admin can delete this comment", status_code=400)

        db.session.delete(group_comment)
        subscribed_users = [x.user_id for x in group_comment.learning_group_comment.learning_groups.subscribed_groups]
        Notification.send_push_notification(subscribed_users, f"{current_user.email} has removed a comment", LearningGroup.__name__)
        db.session.commit()
        return "Comment has been deleted successfully"
