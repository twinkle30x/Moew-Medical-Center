from . import db
from flask_login import UserMixin
import enum

class ActivityType(enum.Enum):
    vaccine = "Vaccine"
    consultation = "Consultation"
    grooming = "Grooming"
    spa = "Spa"
    dentalcare = "Dental Care"
    surgicalprocedure = "Surgical procedure"
    nutrition = "Nutrition Advice"
    spaying = "Spay (female)"
    neuter = "Neuter (male)"
    xray = "X-Ray"
    bathing = "Complete Bathing"
    brushing = "Brushing and Coat Care"
    trimming = "Sanitary Trimming"
    nailClipping = "Nail Clipping"
    earCleaning = "Ear Cleaning"
    haircut = "Stylish Haircut"
    spaTreatment = "Specialty Spa Treatment"

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    activity = db.Column(db.Enum(ActivityType))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    appointments = db.relationship('Appointment')
    reservations = db.relationship('Reservation')

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkin = db.Column(db.Date)
    checkout = db.Column(db.Date)
    name = db.Column(db.String(100))
    breed = db.Column(db.String(100))
    age = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))