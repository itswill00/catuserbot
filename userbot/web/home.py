from flask import Blueprint, redirect

web_bp = Blueprint("web", __name__)


@web_bp.route("/", methods=["GET"])
def home():
    return redirect("https://github.com/TgCatUB/catuserbot")
