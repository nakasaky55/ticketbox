from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests
from src import login_manager,db,app
from src.models import Events,User,Tickets,Orders,Items
event_blueprint = Blueprint('eventbp', __name__, template_folder='../../templates')

@event_blueprint.route("/create", methods=["POST","GET"])
@login_required
def create_new_event():
    if request.method == "POST":
        new_event = Events(
            name = request.form['name'],
            name_address = request.form['name_address'],
            address = request.form['address']
        )
        current_user.events.append(new_event)
        db.session.commit()
        flash("Add event success", "info")
    return render_template("events/create_event.html")

@event_blueprint.route("/manage", methods=["GET", "POST"])
@login_required
def manage_events():
    events = Events.query.filter_by(user_id = current_user.id).all()
    return render_template("events/manage_events.html", events=events)


@event_blueprint.route("/all_events", methods=["GET", "POST"])
@login_required
def all_events():
    events = Events.query.filter_by(state = True).all()
    return render_template("events/events.html", events = events)

@event_blueprint.route("/event_detail/<id>", methods=["GET","POST"])
@login_required
def event_detail(id):
    event = Events.query.get(id)
    if request.method == "POST":
        action = request.args.get('action')
        if action == "publish_event":
            
            print("asd", request.form['premire_date'])
            if request.form['premire_date']:
                event.premire_date = request.form['premire_date']
            if request.form['active'] == "on":
                event.state = True
            else:
                event.state = False
            db.session.commit()
            return redirect(url_for("eventbp.event_detail", id = id))
            pass
        elif action =="add_ticket":
            ticket = Tickets()
            ticket.ticket_type = request.form['ticket_type']
            ticket.price = request.form['ticket_price']
            ticket.quantity = request.form['ticket_quantities']
            event.tickets.append(ticket)
            db.session.commit()
            return redirect(url_for("eventbp.manage_events"))
        pass
    return render_template("events/event_detail.html", event = event)

@event_blueprint.route("/event_detail/<id>/purchase", methods=["GET", "POST"])
@login_required
def event_purchase(id):
    event = Events.query.get(id)
    action = request.args.get('action')
    orders_array = []
    if request.method == "POST":
        if action == "purchase":
            order = Orders(user_id=current_user.id)
            db.session.add(order)
            db.session.commit()
            for ticket in event.tickets:
                a = request.form['ticket_{0}'.format(ticket.id)]
                for _ in range(int(a)):
                    item = Items(order_id = order.id, ticket_type_id = ticket.id)
                    orders_array.append(item)
            db.session.add_all(orders_array)
            db.session.commit()
            
    return render_template("events/event_purchase.html", event = event)