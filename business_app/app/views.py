from app import b_app
@b_app.route('/')
@b_app.route('/index')
def index():
	return "Hello, Software Engineering Group!"
