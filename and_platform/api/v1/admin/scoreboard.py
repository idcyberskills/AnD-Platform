from and_platform.models import Teams
from and_platform.core.score import get_overall_team_score
from flask import Blueprint, jsonify
from datetime import datetime

scoreboard_blueprint = Blueprint("admin_scoreboard", __name__, url_prefix="/scoreboard")


@scoreboard_blueprint.get("/")
def get_admin_scoreboard():
    teams = Teams.query.all()
    scoreboard = []
    for team in teams:
        team_score = get_overall_team_score(team.id)

        tmp_chall = {}
        for chall in team_score["challenges"]:
            chall_id = chall["challenge_id"]
            chall.pop("challenge_id")
            tmp_chall[chall_id] = chall

        team_score.pop("team_id")
        team_score.update({
            "id": team.id,
            "name": team.name,
            "challenges": tmp_chall
        })

        scoreboard.append(team_score)

    scoreboard_sort = sorted(scoreboard, key=lambda x: x["total_score"], reverse=True)
    for i in range(len(scoreboard_sort)):
        scoreboard_sort[i]["rank"] = i+1
    return jsonify(status="success", data=scoreboard_sort)
