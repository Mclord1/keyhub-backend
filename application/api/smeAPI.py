from flask import Blueprint, request, jsonify
from pydantic import BaseModel

from application import db
from application.Enums.Permission import PermissionEnum
from application.Schema import validator
from application.models import School
from application.models.smeModel import SME
from application.utils.authenticator import authenticate, has_school_privilege

sme_bp = Blueprint("sme", __name__)


class SMESchema(BaseModel):
    name: str
    surname: str
    email: str
    contact_telephone: str
    website: str
    company_name: str
    registered_address: str
    area_of_expertise: str
    nin_certificate: bool


class KeywordSchema(BaseModel):
    name: str


# Create an SME
@sme_bp.route("/<int:school_id>", methods=["POST"])
@authenticate(PermissionEnum.MODIFY_SCHOOL)
@has_school_privilege
def create_sme(school_id):
    sme_data = request.get_json()

    sme: SMESchema = validator.validate_data(SMESchema, sme_data)

    _school = School.GetSchool(school_id)

    sme_model = SME(
        name=sme.name,
        surname=sme.surname,
        email=sme.email,
        contact_telephone=sme.contact_telephone,
        website=sme.website,
        company_name=sme.company_name,
        registered_address=sme.registered_address,
        area_of_expertise=sme.area_of_expertise,
        nin_certificate=sme.nin_certificate,
        schools=_school
    )
    db.session.add(sme_model)
    db.session.commit()
    return jsonify({"message": "SME created successfully"}), 201


@sme_bp.route("/<int:school_id>", methods=["GET"])
@authenticate(PermissionEnum.MODIFY_SCHOOL)
@has_school_privilege
def get_sme(school_id):
    sme = SME.query.filter_by(school_id = school_id).first()
    if not sme:
        return jsonify({"error": "SME not found"}), 404
    return jsonify(sme.to_dict(add_filter=False))


# Update an SME by ID
@sme_bp.route("/<int:school_id>", methods=["PUT"])
@authenticate(PermissionEnum.MODIFY_SCHOOL)
@has_school_privilege
def update_sme(school_id):
    _sme : SME = SME.query.filter_by(school_id = school_id).first()
    if not _sme:
        return jsonify({"error": "SME not found"}), 404

    data = request.get_json()
    print(data)
    _sme.update_table(data)
    db.session.commit()
    return jsonify({"message": "SME updated successfully"})


# Delete an SME by ID
@sme_bp.route("/<int:school_id>", methods=["DELETE"])
@authenticate(PermissionEnum.MODIFY_SCHOOL)
@has_school_privilege
def delete_sme(school_id):
    sme = SME.query.filter_by(school_id = school_id).first()
    if not sme:
        return jsonify({"error": "SME not found"}), 404

    db.session.delete(sme)
    db.session.commit()
    return jsonify({"message": "SME deleted successfully"})
