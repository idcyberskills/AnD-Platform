from flask import Blueprint, jsonify, request, send_file
from and_platform.api.helper import convert_model_to_dict
# from and_platform.api.v1.my.service import myservice_blueprint
from and_platform.core.config import get_config, get_app_config
from and_platform.core.security import validteam_only, current_team
from and_platform.models import ChallengeReleases, Solves, Servers, Teams
import os
import zipfile

myapi_blueprint = Blueprint("myapi", __name__, url_prefix="/my")
myapi_blueprint.before_request(validteam_only)
# myapi_blueprint.register_blueprint(myservice_blueprint)

@myapi_blueprint.get("/solves")
def get_my_solves():
    chall_release = ChallengeReleases.get_challenges_from_round(get_config("CURRENT_ROUND", 0))
    solves = Solves.query.with_entities(Solves.challenge_id).filter(
        Solves.team_id == current_team.id,
        Solves.challenge_id.in_(chall_release),
    ).all()
    solves = [elm[0] for elm in solves]

    return jsonify(status="success",data=solves)

@myapi_blueprint.post("/rollback")
def rollback_machine():
    from and_platform.core.server import do_rollback
    
    confirm_data: dict = request.get_json()
    if not confirm_data.get("confirm"):
        return jsonify(status="bad request", message="action not confirmed"), 400
    
    do_rollback.apply_async(args=(current_team.id, ), queue='contest')
    return jsonify(status="success",message="rollback request submitted.")

@myapi_blueprint.get("/manage")
def manage_machine():
    server = Servers.query.join(Teams, Teams.server_id == Servers.id).filter(Teams.id == current_team.id).scalar()
    return jsonify(status="success",data=convert_model_to_dict(server))

@myapi_blueprint.get("/vpn")
def get_vpn():
    num_member = get_config("NUM_MEMBER", 2)
    vpn_folder = os.path.join(get_app_config("DATA_DIR"), "vpn")
    vpnzip_path = os.path.join(vpn_folder, "zip", f"team{current_team.id}.zip")
    with zipfile.ZipFile(vpnzip_path, "w") as vpnzip:
        start_idx = num_member * (current_team.id - 1) + 1
        for i in range(start_idx, start_idx + num_member):
            vpnfile = os.path.join(vpn_folder, f"user{i}.client.conf")
            vpnzip.write(vpnfile)
    send_file(vpnzip_path)