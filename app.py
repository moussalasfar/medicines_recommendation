from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_cle_secrete'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/db2'
db = SQLAlchemy(app)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class Historique(db.Model):
    idH = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    input = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Load the medicines dataset
medicines_df = pd.read_csv('data/medicines.csv')

def get_user_email(user_id):
    user = db.session.get(Client, user_id)  # Updated to use Session.get()
    return user.email if user else None

@app.context_processor
def utility_processor():
    def get_user_email(user_id):
        user = db.session.get(Client, user_id)  # Updated to use Session.get()
        return user.email if user else None
    return dict(get_user_email=get_user_email)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        password = request.form['pass']
        existing_user = Client.query.filter_by(email=email).first()
        if existing_user is None:
            client = Client(username=username, email=email, password=password)
            db.session.add(client)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email address already registered.', 'danger')
    return render_template('register_custom.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        client = Client.query.filter_by(email=email, password=password).first()
        if client:
            session['user_id'] = client.id
            flash('Login successful!', 'success')
            return redirect(url_for('recommend'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login_custom.html')

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    medicines = []
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    if request.method == 'POST':
        disease = request.form['disease']
        # Filter the medicines that are used for the given disease
        filtered_medicines = medicines_df[medicines_df['Uses'].str.contains(disease, case=False, na=False)]
        # Get the top 10 medicines
        medicines = filtered_medicines.head(10).to_dict('records')
        
        # Enregistrer la recherche dans l'historique
        new_search = Historique(client_id=user_id, input=disease)
        db.session.add(new_search)
        db.session.commit()

    # Récupérer l'historique des recherches de l'utilisateur
    search_history = Historique.query.filter_by(client_id=user_id).order_by(Historique.date.desc()).all()

    return render_template('recommend.html', medicines=medicines, search_history=search_history)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Envoyer l'e-mail
        send_email(email, name, message)
        flash('Message sent successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('contact.html')

def send_email(sender_email, name, message):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'zaynab.zizi.67@gmail.com'  # Votre adresse e-mail pour l'authentification
    smtp_password = 'wcpl arcy pqsx flcq'  # Mot de passe ou mot de passe d'application

    receiver_email = 'zaynabfarina@gmail.com'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = 'from medicine recommendation'

    body = 'Name: {}\nEmail: {}\nMessage: {}'.format(name, sender_email, message)
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        print('Email sent successfully!')
    except smtplib.SMTPAuthenticationError as e:
        print(f'Authentication error occurred: {e}')
    except smtplib.SMTPConnectError as e:
        print(f'Connection error occurred: {e}')
    except smtplib.SMTPException as e:
        print(f'SMTP error occurred: {e}')
    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    app.run(debug=True)
