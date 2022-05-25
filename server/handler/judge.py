from flask import Blueprint

judge_bp = Blueprint('judge', __name__)


@judge_bp.route('/', methods=['GET'])
def index() -> str:
    return 'This is Judge App'
