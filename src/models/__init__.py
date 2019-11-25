from flask_login import UserMixin
from src import db
from werkzeug.security import generate_password_hash,check_password_hash
# # DEFINE Blog model
# class Blog(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     title = db.Column(db.String(200), nullable = False)
#     body = db.Column(db.String, nullable = False)
#     author = db.Column(db.String(20), nullable = False)
#     created_date = db.Column(db.DateTime, server_default = db.func.now())
#     view_count = db.Column(db.Integer, default=0)

# DEFINE MODEL user
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255), nullable = False, unique = True)
    username = db.Column(db.String(255), nullable = False, unique = True)
    password = db.Column(db.String(255), nullable=False, unique = False)
    address = db.Column(db.String(255))
    events = db.relationship("Events", backref="event", lazy=True)
    orders = db.relationship("Orders", backref="user", lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

# DEFINE new events
class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    name_address = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    state = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, server_default = db.func.now())
    premire_date = db.Column(db.Date, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    tickets = db.relationship("Tickets", backref="ticket", lazy=True)
    
    def get_event(self, id):
        return Events.query.filter_by(user_id = id).all()
    
    def active_event(self, id):
        return Events.query.filter_by(user_id = id).filter_by(state = True).all()

# Model for type of tickets
class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_type = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"))
    ticket_item = db.relationship("Items", backref="ticket_item", lazy=True)

# Order class
class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    items = db.relationship("Items", backref="item_order", lazy=True)

# items
class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_type_id = db.Column(db.Integer, db.ForeignKey("tickets.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))


# # DEFINE MODEL comments
# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     body = db.Column(db.String, nullable = False)
#     post_id = db.Column(db.Integer, nullable = False)
#     author = db.Column(db.String, nullable = False)
#     created_at = db.Column(db.DateTime, server_default = db.func.now())

# likes = db.Table('likes',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     db.Column('post_id', db.Integer, db.ForeignKey('blog.id'), primary_key=True)
# )

db.create_all()