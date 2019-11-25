from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, current_user, login_required
from flask_admin import Admin
from flask_moment import Moment



app = Flask(__name__)
app.config.from_object('config.Config')
moment = Moment(app)
moment.init_app(app)

db = SQLAlchemy(app)


from src.models import User
## more models incoming
migrate = Migrate(app, db)

## set up login_manager
login_manager= LoginManager(app)
login_manager.login_view = "userbp.login"

@login_manager.user_loader
def load_user(id):
  return User.query.get(id)


from src.components.events import event_blueprint
app.register_blueprint(event_blueprint, url_prefix='/event')

from src.components.user import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')


# from src.models.admin import MyAdmin
# admin = Admin(app, name='KHOA', template_mode='bootstrap3')
# admin.add_view(MyAdmin(User, db.session))



@app.route('/')
@login_required
def root():
  # user = User.query.get(3)
  # login_user(user)
  return render_template("base/index.html")