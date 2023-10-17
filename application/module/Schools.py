from . import *
from ..Schema.school import UpdateSchoolSchema, SchoolSchema, ProjectSchema


class SchoolModel:

    @classmethod
    def toggle_status(cls, school_id, status):
        _school: School = School.GetSchool(school_id)

        _school.isDeactivated = status
        db.session.commit()
        return f"{_school.name} active status has been set to {status}"

    @classmethod
    def list_all_schools(cls, page, per_page):
        page = int(page)
        per_page = int(per_page)
        _school: School = School.query.order_by(desc(School.created_at)).paginate(page=page, per_page=per_page,
                                                                                  error_out=False)
        total_items = _school.total
        results = [item for item in _school.items]
        total_pages = (total_items - 1) // per_page + 1
        pagination_data = {
            "page": page,
            "size": per_page,
            "total_pages": total_pages,
            "total_items": total_items,
            "results": {
                "total_schools": len(results),
                "total_active_schools": len([x for x in results if not x.isDeactivated]),
                "total_deactivated_schools": len([x for x in results if x.isDeactivated]),
                "schools": [{
                    **school.to_dict(),
                    "num_of_teachers": len(school.teachers) if school.teachers else 0,
                    "num_of_students": len(school.students) if school.students else 0,
                    "num_of_parents": len(school.parents) if school.parents else 0,
                    "num_of_school_administrators": len(school.managers) if school.managers else 0,
                } for school in results],

            }
        }
        return PaginationSchema(**pagination_data).model_dump()

    @classmethod
    def view_school_info(cls, school_id):
        _school: School = School.GetSchool(school_id)

        return {
            "num_of_teachers": len(_school.teachers),
            "num_of_students": len(_school.students),
            "num_of_parents": len(_school.parents),
            "num_of_school_administrators": len(_school.managers),
            "student_by_gender": {
                "male": {
                    "count": len([x for x in _school.students if x.gender == "Male"]),
                    "percentage": (len([x for x in _school.students if x.gender == "Male"]) * 100) / len(
                        _school.students) if _school.students else 0
                },
                "female": {
                    "count": len([x for x in _school.students if x.gender == "Female"]),
                    "percentage": (len([x for x in _school.students if x.gender == "Female"]) * 100) / len(
                        _school.students) if _school.students else 0
                }
            },
            "teachers_by_gender": {
                "male": {
                    "count": len([x for x in _school.teachers if x.gender == "Male"]),
                    "percentage": (len([x for x in _school.teachers if x.gender == "Male"]) * 100) / len(
                        _school.teachers) if _school.teachers else 0
                },
                "female": {
                    "count": len([x for x in _school.teachers if x.gender == "Female"]),
                    "percentage": (len([x for x in _school.teachers if x.gender == "Female"]) * 100) / len(
                        _school.teachers) if _school.teachers else 0
                }
            },
            **_school.to_dict()
        }

    @classmethod
    def update_school(cls, school_id, data):
        req_school = validator.validate_data(UpdateSchoolSchema, data)

        school: School = School.query.filter_by(id=school_id).first()

        if not school:
            raise CustomException(message="School not found", status_code=403)

        _school: School = School.query.filter(
            (School.name == req_school.name) |
            (School.email == req_school.email) |
            (School.msisdn == req_school.msisdn) |
            (School.reg_number == req_school.reg_number)
        ).first()

        if _school:
            existing_values = []

            if _school.name == req_school.name:
                existing_values.append("name")
            if _school.email == req_school.email:
                existing_values.append("email")
            if _school.msisdn == req_school.msisdn:
                existing_values.append("msisdn")
            if _school.reg_number == req_school.reg_number:
                existing_values.append("reg_number")

            raise CustomException(message=f"School attributes already exist: {', '.join(existing_values)}",
                                  status_code=403)

        school.update_table(data)
        return f"School information has been updated successfully"

    @classmethod
    def add_school(cls, data):
        req_schema: SchoolSchema = validator.validate_data(SchoolSchema, data)

        name = req_schema.name
        email = req_schema.email
        msisdn = req_schema.msisdn
        reg_number = req_schema.reg_number
        country = req_schema.country
        state = req_schema.state
        address = req_schema.address
        primary_contact = req_schema.primary_contact

        _school: School = School.query.filter(
            (School.name == name) |
            (School.email == email) |
            (School.msisdn == msisdn) |
            (School.reg_number == reg_number)
        ).first()

        if _school:
            existing_values = []

            if _school.name == req_schema.name:
                existing_values.append("name")
            if _school.email == req_schema.email:
                existing_values.append("email")
            if _school.msisdn == req_schema.msisdn:
                existing_values.append("msisdn")
            if _school.reg_number == req_schema.reg_number:
                existing_values.append("reg_number")

            raise CustomException(message=f"School attributes already exist: {', '.join(existing_values)}",
                                  status_code=403)

        try:

            # Add school details to school model
            add_school = School(name=name, email=email, msisdn=msisdn, reg_number=reg_number, country=country,
                                state=state, address=address)
            add_school.save(refresh=True)

            Helper.User_Email_OR_Msisdn_Exist(primary_contact.email, primary_contact.msisdn)

            role = Role.GetRoleByName(BasicRoles.SCHOOL_ADMIN.value)

            # create the user account on User model
            user = User.CreateUser(primary_contact.email, primary_contact.msisdn, role)

            # create and add school admin
            add_school_admin = SchoolManager(
                school_id=add_school.id,
                name=primary_contact.name,
                gender=primary_contact.gender,
                residence=primary_contact.address,
                user_id=user.id
            )

            add_school_admin.save(refresh=True)

            return f"The school {add_school.name} has been added successfully"
        except Exception as e:
            db.session.rollback()
            print(e)
            raise e

    @classmethod
    def get_account_admins(cls, school_id):
        _school: School = School.GetSchool(school_id)
        return {
            "num_of_admins": len(_school.managers),
            "num_of_active_admins": len([x for x in _school.managers if not x.user.isDeactivated]),
            "num_of_deactivated_admins": len([x for x in _school.managers if x.user.isDeactivated]),
            "admins": [{
                "role": x.user.roles.name if x.user.roles else None,
                "email": x.user.email,
                "isDeactivated": x.user.isDeactivated,
                "msisdn": x.user.msisdn,
                **x.to_dict()
            } for x in _school.managers]
        }

    @classmethod
    def get_teachers(cls, school_id):
        _school: School = School.GetSchool(school_id)
        return {
            "num_of_teachers": len(_school.teachers),
            "num_of_active_teachers": len([x for x in _school.teachers if not x.user.isDeactivated]),
            "num_of_deactivated_teachers": len([x for x in _school.teachers if x.user.isDeactivated]),
            "teachers": [{
                "email": teacher.user.email,
                "isDeactivated": teacher.user.isDeactivated,
                "msisdn": teacher.user.msisdn,
                "num_of_projects": len([x for x in teacher.projects if x.school_id == school_id]),
                "num_of_students": len([x for x in teacher.students if x.school_id == school_id]),
                **teacher.to_dict()
            } for teacher in _school.teachers]
        }

    @classmethod
    def get_parents(cls, school_id):
        _school: School = School.GetSchool(school_id)
        return {
            "num_of_parents": len(_school.parents),
            "num_of_active_parents": len([x for x in _school.parents if not x.user.isDeactivated]),
            "num_of_deactivated_parents": len([x for x in _school.parents if x.user.isDeactivated]),
            "parents": [{
                "email": parent.user.email,
                "isDeactivated": parent.user.isDeactivated,
                "msisdn": parent.user.msisdn,
                "num_of_children": len([x for x in parent.students if x.school_id == school_id]),
                "num_of_active_children": len([student for student in parent.students if
                                               student.school_id == school_id and not student.user.isDeactivated]),
                "num_of_deactivated_children": len([student for student in parent.students if
                                                    student.school_id == school_id and student.user.isDeactivated]),
                **parent.to_dict()
            } for parent in _school.parents]
        }

    @classmethod
    def get_students(cls, school_id):
        _school: School = School.GetSchool(school_id)
        return {
            "num_of_students": len(_school.students),
            "num_of_active_students": len([x for x in _school.students if not x.user.isDeactivated]),
            "num_of_deactivated_students": len([x for x in _school.students if x.user.isDeactivated]),
            "students": [{
                "project": student.projects,
                "email": student.user.email,
                "isDeactivated": student.user.isDeactivated,
                "msisdn": student.user.msisdn,
                **student.to_dict()
            } for student in _school.students]
        }

    @classmethod
    def get_projects(cls, school_id):
        _school: School = School.GetSchool(school_id)
        return {
            "num_of_projects": len(_school.projects),
            "num_of_active_projects": len([x for x in _school.projects if not x.isDeactivated]),
            "num_of_deactivated_projects": len([x for x in _school.projects if x.isDeactivated]),
            "projects": [{
                "num_of_students": len([x for x in project.students]),
                "assigned_teachers": [x.to_dict() for x in project.teachers],
                "email": project.user.email,
                "isDeactivated": project.user.isDeactivated,
                "msisdn": project.user.msisdn,
                **project.to_dict()
            } for project in _school.projects]
        }

    @classmethod
    def search_projects(cls, args, school_id):

        query = Project.query.filter(Project.school_id == int(school_id)).filter(
            (Project.name.ilike(f'%{args}%') | Project.students.name.ilike(f'%{args}%') | Project.teachers.name.ilike(
                f'%{args}%'))
        )
        result = [x.to_dict() for x in query.all()]
        return result

    @classmethod
    def add_project(cls, data):
        req: ProjectSchema = validator.validate_data(ProjectSchema, data)

        project_exist = Project.query.filter_by(name=req.name).first()

        if project_exist:
            raise CustomException("Project with same name already exist", status_code=400)

        student = Student.GetStudent(req.student_id)
        teacher = Teacher.GetTeacher(req.teacher_id)
        school = School.GetSchool(req.school_id)

        try:
            add_project = Project(name=req.name, description=req.description, teachers=teacher, students=student,
                                  schools=school)
            add_project.save(refresh=True)
        except Exception:
            db.session.rollback()
            raise CustomException(ExceptionCode.DATABASE_ERROR)
        return f"The school project : {req.name} has been added successfully"

    @classmethod
    def update_project(cls, project_id, data):
        project = Project.GetProject(project_id)
        project.update_table(data)
        return project.to_dict()

    @classmethod
    def delete_project(cls, project_id):
        project = Project.GetProject(project_id)
        db.session.delete(project)
        db.session.commit()
        return "Project has been deleted"

    @classmethod
    def deactivate_project(cls, project_id, reason):
        project: Project = Project.GetProject(project_id)
        project.isDeactivated = True
        project.deactivate_reason = reason
        db.session.commit()
        return "Project has been deactivated"

    @classmethod
    def view_project_detail(cls, school_id, project_id):
        pass

    @classmethod
    def get_transactions(cls, school_id):
        pass

    @classmethod
    def get_subscriptions(cls, school_id):
        pass

    @classmethod
    def get_profile_settings(cls, school_id):
        pass
