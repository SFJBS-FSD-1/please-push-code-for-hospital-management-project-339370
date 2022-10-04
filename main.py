import os
import functools

from datetime import datetime, date
from flask import Flask, render_template, redirect, url_for, request, flash, session, g
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy



def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY', default='dev')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    db = SQLAlchemy()

    class User(db.Model):
        __tablename__ = 'admin'
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        password = db.Column(db.String(200))
        created_at = db.Column(db.DateTime, server_default=db.func.now())
        updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    class Patients(db.Model):
        __tablename__ = 'patients'
        id = db.Column(db.Integer, primary_key=True)
        phone = db.Column(db.BigInteger, nullable=False)
        aadhar = db.Column(db.BigInteger, unique=True, nullable=False)
        name = db.Column(db.String(80), nullable=False)
        age = db.Column(db.Integer, nullable=False)
        admit_date = db.Column(db.DateTime, server_default=db.func.now())
        discharge_date = db.Column(db.DateTime, server_default=db.func.now())
        bed_type = db.Column(db.String(80), nullable=False)
        address = db.Column(db.String(250), nullable=False)
        city = db.Column(db.String(250), nullable=False)
        state = db.Column(db.String(250), nullable=False)
        status = db.Column(db.String(20), nullable=False)
        meds = db.relationship('Medicines', backref='patient', lazy=True)
        tests = db.relationship('Diagnostics', backref='patient', lazy=True)

    class Medicines(db.Model):
        __tablename__ = 'medicines'
        id = db.Column(db.Integer, primary_key=True)
        patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
        med_name = db.Column(db.String(80), nullable=False)
        med_id = db.Column(db.Integer, nullable=False)
        rate = db.Column(db.Integer, nullable=False)
        Dosage = db.Column(db.Text, nullable=False)
        created_at = db.Column(db.DateTime, server_default=db.func.now())
        updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    class Diagnostics(db.Model):
        __tablename__ = 'diagnostics'
        id = db.Column(db.Integer, primary_key=True)
        patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
        test_name = db.Column(db.String(80), nullable=False)
        test_id = db.Column(db.Integer, nullable=False)
        test_charge = db.Column(db.Integer, nullable=False)
        created_at = db.Column(db.DateTime, server_default=db.func.now())
        updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    db.init_app(app)
    migrate = Migrate(app, db)

    def require_login(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if not g.user:
                return redirect(url_for('log_in'))
            return view(**kwargs)
        return wrapped_view

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.before_request
    def load_user():
        user_id = session.get('user_id')
        if user_id:
            g.user = User.query.get(user_id)
        else:
            g.user = None

    @app.route('/sign_up', methods=('GET', 'POST'))
    def sign_up():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            error = None

            if not username:
                error = 'Username is required.'
            elif not password:
                error = 'Password is required.'
            elif User.query.filter_by(username=username).first():
                error = 'Username is already taken.'

            if error is None:
                user = User(username=username, password=generate_password_hash(password))
                db.session.add(user)
                db.session.commit()
                flash("Successfully signed up! Please log in.", 'success')
                return redirect(url_for('log_in'))

            flash(error, 'error')

        return render_template('staff_registration.html')

    @app.route('/log_in', methods=('GET', 'POST'))
    def log_in():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            error = None

            user = User.query.filter_by(username=username).first()

            if not user or not check_password_hash(user.password, password):
                error = 'Username or password are incorrect.'

            if error is None:
                session.clear()
                session['user_id'] = user.id
                return redirect(url_for('home'))

            flash(error, 'error')

        return render_template('login.html')

    @app.route('/log_out', methods=('GET', 'DELETE'))
    def log_out():
        session.clear()
        flash('Successfully logged out.', 'success')
        return redirect(url_for('log_in'))

    @app.route('/')
    def home():
        return render_template("home.html")

    @app.route('/create_patient', methods=['GET', 'POST'])
    @require_login
    def create_patient():
        if request.method == 'POST':
            phone = request.form['phone']
            aadhar = request.form['aadhar']
            name = request.form['pname']
            age = request.form['age']
            bed_type = request.form['tbed']
            address = request.form['address']
            state = request.form['state']
            city = request.form['city']
            status = request.form['status']

            pat = Patients.query.filter_by(aadhar=aadhar).first()

            if pat == None:
                patient = Patients(phone=phone,
                                   aadhar=aadhar,
                                   name=name,
                                   age=age,
                                   bed_type=bed_type,
                                   address=address,
                                   state=state,
                                   city=city, status=status)
                db.session.add(patient)
                db.session.commit()
                flash('Patient creation initiated successfully')
                return redirect(url_for('update_patient'))

            else:
                flash('Patient with this ID already exists')
                return redirect(url_for('create_patient'))

        else:
            return render_template('create_patient.html')

    @app.route('/update_patient')
    @require_login
    def update_patient():
        updatep = Patients.query.all()

        if not updatep:
            flash('No patients exists in database')
            return redirect(url_for('create_patient'))
        else:
            return render_template('update_patient.html', updatep=updatep)

    @app.route('/deletepat')
    @require_login
    def deletepat():
        updatep = Patients.query.all()

        if not updatep:
            flash('No patients exists in database')
            return redirect(url_for('create_patient'))
        else:
            print("inside else")
            return render_template('deletepat.html', updatep=updatep)

    @app.route('/search_patient', methods=['GET', 'POST'])
    @require_login
    def search_patient():
        if request.method == 'POST':
            phone = request.form['phone']

            if id != "":
                patient = Patients.query.filter_by(phone=phone).first()
                if patient == None:
                    flash('No Patients with  this phone exists')
                    return redirect(url_for('search_patient'))
                else:
                    flash('Patient Found')
                    return render_template('search_patient.html', patient=patient)

            if id == "":
                flash('Enter phone to search')
                return redirect(url_for('search_patient'))

        else:
            return render_template('search_patient.html')

    @app.route('/patientscreen')
    @require_login
    def patientscreen():
        pts = Patients.query.filter_by(status='Active')
        if not pts:
            flash('All Patients Discharged')
            return redirect(url_for('update_patient'))
        else:
            return render_template('patientscreen.html', pts=pts)

    @app.route('/editpatientdetail/<id>', methods=['GET', 'POST'])
    @require_login
    def editpatientdetail(id):
        editpat = Patients.query.filter_by(id=id)

        if request.method == 'POST':
            print("inside editpat post mtd")
            name = request.form['npname']
            age = request.form['nage']
            bed_type = request.form['tbed']
            address = request.form['naddress']
            status = request.form['status']
            state = request.form['nstate']
            city = request.form['ncity']
            discharge_date = datetime.today()
            row_update = Patients.query.filter_by(id=id).update(
                dict(name=name, age=age, bed_type=bed_type, address=address, state=state, city=city, status=status,
                     discharge_date=discharge_date))
            db.session.commit()
            print("Roww update", row_update)

            if row_update == None:
                flash('Something Went Wrong')
                return redirect(url_for('update_patient'))
            else:
                flash('Patient update initiated successfully')
                return redirect(url_for('update_patient'))

        return render_template('editpatientdetail.html', editpat=editpat)

    @app.route('/deletepatientdetail/<id>')
    @require_login
    def deletepatientdetail(id):
        delpat = Patients.query.filter_by(id=id).delete()
        db.session.commit()

        if delpat == None:
            flash('Something Went Wrong')
            return redirect(url_for('update_patient'))
        else:
            flash('Patient deletion initiated successfully')
            return redirect(url_for('update_patient'))

    return app

    if __name__ == "__main__":
        create_app().run(port=5001)


