from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .models import Appointment, ActivityType, Reservation
from . import db
from datetime import datetime
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/medicalservices')
def medicalservices():
    return render_template("medicalservices.html", user=current_user)

@views.route('/accessories')
@login_required
def accessories():
    return render_template("accessories.html", user=current_user)

@views.route('/meowtel', methods=['GET', 'POST'])
@login_required
def meowtel():
    if request.method == 'POST':
        checkin = datetime.strptime(request.form.get('checkin'), '%Y-%m-%d').date() 
        checkout = datetime.strptime(request.form.get('checkout'), '%Y-%m-%d').date() 
        name = request.form.get('name')
        breed = request.form.get('breed')
        age = request.form.get('age')
        new_reservation = Reservation(checkin=checkin, checkout=checkout, name=name, breed=breed, age=age, user_id=current_user.id)
        db.session.add(new_reservation)
        db.session.commit()
        flash('Reservation saved!', category='success')
    return render_template("meowtel.html", user=current_user)

@views.route('/cancel-reservation', methods=['POST'])
def cancel_reservation():
    data = request.json
    reservation_id = data['reservationId']
    reservation = Reservation.query.get(reservation_id)
    if reservation and reservation.user_id == current_user.id:
        db.session.delete(reservation)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 400

@views.route('/grooming')
@login_required
def grooming():
    return render_template("grooming.html", user=current_user)

@views.route('/account')
@login_required
def account():
    return render_template("account.html", user=current_user)

@views.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    if request.method == 'POST':
        try:
            date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date() if request.form.get('date') else None
            time = datetime.strptime(request.form.get('time'), '%H:%M').time() if request.form.get('time') else None
        except ValueError:
            flash('Invalid date or time format', category='error')
            return render_template("contact.html", user=current_user)
        try:
            activity_enum = ActivityType[request.form.get('activity')] if request.form.get('activity') else None
        except KeyError:
            flash('Invalid activity selected', category='error')
            return render_template("contact.html", user=current_user)
        new_appointment = Appointment(date=date, time=time, activity=activity_enum, user_id=current_user.id)
        db.session.add(new_appointment)
        db.session.commit()
        flash('Appointment saved!', category='success')
    return render_template("contact.html", user=current_user)

@views.route('/cancel-appointment', methods=['POST'])
def cancel_appointment():
    data = request.json
    appointment_id = data['appointmentId']
    appointment = Appointment.query.get(appointment_id)
    if appointment and appointment.user_id == current_user.id:
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 400
