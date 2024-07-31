# Medicine Recommendation System
This is a Flask-based web application that provides personalized medicine recommendations based on user input. The system allows users to register, log in, and receive medicine recommendations by entering a disease name. The application also includes a contact page for users to send inquiries via email.

## Features
- #### User Authentication:
  Register and log in with an email and password.
- #### Medicine Recommendation:
  Enter a disease name to get a list of the 10 most relevant medicines.
- #### Contact Form:
  Users can send messages via the contact page using SMTP.
- #### Personalized Dashboard:
  Display the first letter of the user's email in a circle on the recommendation page.
## Project Structure
__________________________________________________________________________________________
```
Medicine_Recommendations/
│
├── app.py
├── medicine_recommendations.ipynb
├── data/
│   └── medicines.csv
├── static/
│   ├── css/
│   │   ├── style.css
|   |   ├── ss.css
|   |   ├── style.css.map
│   │   └── style_recommend.css
│   ├── fonts/
│   │   └── material-icon/
│   │       └── css/
│   │           └── material-design-iconic-font.min.css
│   ├── images/
│   │   ├── signin.png
│   │   └── signup.png
│   ├── js/
│   │   └── main.js
│   └── vendor/
│       └── jquery/
|           ├── jquery-ui.min.js
│           └── jquery.min.js
├── templates/
├── index.html
├── login_custom.html
├── register_custom.html
├── recommendation.html
│── contact.html
└── requirements.txt
```
## Installation
#### 1. Clone the repository:
```
git clone https://github.com/moussalasfar/Medicine_Recommendations.git
cd Medicine_Recommendations
```
#### 2. Install the required dependencies:
```pip install -r requirements.txt```
#### 3. Set up the database:
Ensure you have a MySQL database running. Update the database URI in ```app.py``` with your credentials.
#### 4. Run the application:
```python app.py```
#### 5. Access the application:
Open your browser and go to ```http://127.0.0.1:5000/```.
## Usage
- #### Register/Login:
  Create a new account or log in with your credentials.
- #### Get Recommendations:
  Enter the name of a disease to get medicine recommendations.
- #### Contact:
  Use the contact form to send inquiries.
## contact
For any questions or informations:
- **linkedin**:<a href="www.linkedin.com/in/moussa-lasfar-423793196" target="_blank">Moussa Lasfar</a><br>
- **Email**:`moussalasfar2000@gmail.com`
