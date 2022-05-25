from flask import Blueprint

user_bp: Blueprint = Blueprint('user', __name__)


@user_bp.route('/', methods=['GET'])
def index() -> str:
    return 'This is User App'


@user_bp.route('/register', methods=['POST'])
def register():
    return 'This is User Register interface'


@user_bp.route('/login', methods=['POST'])
def login():
    return 'This is User Login interface'
