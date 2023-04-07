from . import app, db
from . import views


app.add_url_rule('/', view_func=views.index)
app.add_url_rule('/positions', view_func=views.position_list)
app.add_url_rule('/employees', view_func=views.employee_list)

app.add_url_rule('/position/create', view_func=views.position_create, methods=["POST", "GET"])
app.add_url_rule('/position/<int:position_id>/update', view_func=views.position_update, methods=["POST", "GET"])
app.add_url_rule('/position/<int:position_id>/delete', view_func=views.position_delete, methods=["POST", "GET"])

app.add_url_rule('/employee/create', view_func=views.employee_create, methods=["POST", "GET"])
app.add_url_rule('/employee/<int:employee_id>', view_func=views.employee_detail)
app.add_url_rule('/employee/<int:employee_id>/update', view_func=views.employee_update, methods=["POST", "GET"])
app.add_url_rule('/employee/<int:employee_id>/delete', view_func=views.employee_delete, methods=["POST", "GET"])

app.add_url_rule('/account/register', view_func=views.user_register, methods=['POST', 'GET'])
app.add_url_rule('/account/login', view_func=views.user_login, methods=['POST', 'GET'])
app.add_url_rule('/account/logout', view_func=views.user_logout)