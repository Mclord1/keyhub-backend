from flask import Blueprint, request

from application.module.RolePermission import RolePermission
from application.utils.output import return_json, OutputObj
from . import *

roles_permission_blueprint = Blueprint('role-permission', __name__)


@roles_permission_blueprint.route('/roles', methods=['GET'])
@authenticate(PermissionEnum.VIEW_ROLES)
def get_all_roles():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    return return_json(
        OutputObj(code=200, message="Roles has been fetched", data=RolePermission.GetAllRoles(page, per_page)))


@roles_permission_blueprint.route('/permissions', methods=['GET'])
@authenticate(PermissionEnum.VIEW_PERMISSIONS)
def get_all_permissions():
    return return_json(OutputObj(code=200, message="Roles has been fetched", data=RolePermission.GetAllPermissions()))


@roles_permission_blueprint.route('/role/<int:id>', methods=['GET'])
@authenticate(PermissionEnum.VIEW_ROLES)
def get_role_detail(id):
    return return_json(OutputObj(code=200, message="Roles has been fetched", data=RolePermission.GetRoleDetails(id)))


@roles_permission_blueprint.route('/set-status/<int:id>', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_ROLE)
def set_role_status(id):
    return return_json(OutputObj(code=200, message="Role status has been changed",
                                 data=RolePermission.ToggleRoleActiveStatus(id)))


@roles_permission_blueprint.route('/role', methods=['POST'])
@authenticate(PermissionEnum.ADD_ROLES)
def add_role():
    args = request.json
    name = args.get('name')
    description = args.get('description')
    return return_json(OutputObj(code=200, message="A new role has been successfully added",
                                 data=RolePermission.AddRole(name, description)))


@roles_permission_blueprint.route('/role/<int:id>', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_ROLE)
def update_role(id):
    args = request.json
    name = args.get('name', None)
    description = args.get('description', None)
    return return_json(OutputObj(code=200, message="Role has been successfully updated",
                                 data=RolePermission.UpdateRole(id, name, description)))


@roles_permission_blueprint.route('/role/<int:id>', methods=['DELETE'])
@authenticate(PermissionEnum.DEACTIVATE_ROLE)
def delete_role(id):
    return return_json(
        OutputObj(code=200, message="Role has been successfully deleted", data=RolePermission.DeleteRole(id)))


@roles_permission_blueprint.route('/permission', methods=['PUT'])
@authenticate(PermissionEnum.MODIFY_ROLE)
def assign_permission_to_role():
    role_id = request.args.get('role_id')
    permission_id = request.args.get('permission_id')
    if not role_id or not permission_id or not role_id.isdigit() or not permission_id.isdigit():
        raise CustomException(message="Please pass a correct role id or permission id")
    return return_json(OutputObj(code=200, message="Permission has been successfully assigned to role",
                                 data=RolePermission.AssignPermissionToRole(role_id, permission_id)))


@roles_permission_blueprint.route('/permission', methods=['DELETE'])
@authenticate(PermissionEnum.DEACTIVATE_ROLE)
def remove_permission_from_role():
    role_id = request.args.get('role_id')
    permission_id = request.args.get('permission_id')
    if not role_id or not permission_id or not role_id.isdigit() or not permission_id.isdigit():
        raise CustomException(message="Please pass a correct role id or permission id")
    return return_json(OutputObj(code=200, message="Permission has been successfully removed from role",
                                 data=RolePermission.RemovePermissionFromRole(role_id, permission_id)))
