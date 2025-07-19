from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import tensorflow as tf
import numpy as np
import cv2
import os
import datetime
from tqdm import tqdm
import zipfile
import time

from werkzeug.utils import secure_filename

app = Flask(__name__)
mysql = MySQL(app)

app.secret_key = 'tube'

app.config['MYSQL_HOST'] = 'localhost'  
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tube'
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = 'static/uploads'

loaded_model = tf.keras.models.load_model('pneumonia_model_alex.h5')

@app.route('/')
def index():
    msg = request.args.get('msg')
    if msg:
        return render_template('index.html', msg=msg)
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form and 'mobile' in request.form:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        data = cursor.fetchone()
        if data:
            msg = 'User Already Exists, Please Try to Use Another Email Id.'
            return redirect(url_for('index', msg=msg))
        else:
            cursor.execute('INSERT INTO users VALUES (NULL,%s, %s, %s, %s)', (name, email, password, mobile))
            mysql.connection.commit()
            msg = 'You have been registered successfully!'
            return redirect(url_for('index', msg=msg))

    return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        data = cursor.fetchone()
        if data:
            session['email'] = email
            session['id'] = data['id']
            session['loggedin'] = True
            return redirect(url_for('dashboard'))
        else:
            msg = 'Invalid login details. Please type valid input details.'
            return redirect(url_for('index',msg=msg))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('id',None)
    session.pop('email',None)
    session.pop('loggedin',None)
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/prevention')
def prevention():
    return render_template('prevention.html')

@app.route('/pneumonia_prevention')
def pneumonia_prevention():
    return render_template('pneumonia_prevention.html')

@app.route('/report')
def report():
    return render_template('report.html')

def predict_class(path):
    img = cv2.imread(path)
    RGBImg = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    RGBImg= cv2.resize(RGBImg,(224,224))
    image = np.array(RGBImg) / 255.0
    new_model = tf.keras.models.load_model("64x3-CNN.model")
    predict=new_model.predict(np.array([image]))
    per=np.argmax(predict,axis=1)

    confidence_score = np.max(predict) * 100
    print(confidence_score)
    if per == 1:
        return f'The result from uploaded X-Ray image is "Tuberculosis found"\n Accuracy:{confidence_score}'
    else:
        return f'The result from uploaded X-Ray image is "No Tuberculosis found"\nAccuracy:{confidence_score}'

@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        if f and f.filename.endswith('.png'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            f.save(file_path)
            predict = predict_class(file_path)
            current_datetime = datetime.datetime.now()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO user_history VALUES (NULL,%s, %s, %s, %s)', (session['id'], file_path, predict, current_datetime))
            mysql.connection.commit()
            return render_template('upload-file.html', file_path=file_path, file_result=predict)
    return render_template('upload-file.html')

@app.route('/history', methods=['GET','POST'])
def history():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM user_history WHERE user_id = %s", (session['id'],))
    all_data = cursor.fetchall()
    return render_template('view-history.html',all_data=all_data)

def get_image_address(image_path):
    image_path = image_path.replace("\\", "/")
    return image_path
app.jinja_env.globals.update(get_image_address=get_image_address)

def preprocess_image(image_path, img_height=224, img_width=224):
    img = tf.io.read_file(image_path)
    img = tf.image.decode_image(img, channels=3, expand_animations=False)
    img = tf.image.resize(img, [img_height, img_width])
    img /= 255.0  # Normalize to [0,1] range
    img = tf.expand_dims(img, 0)  # Add batch dimension
    return img

def predict_image_class(loaded_model, image_path):
    class_names = ['NORMAL', 'PNEUMONIA']
    img = preprocess_image(image_path)
    predictions = loaded_model.predict(img)
    predicted_class = np.argmax(predictions, axis=1)[0]  # Get the index of the max probability
    confidence = np.max(tf.nn.softmax(predictions, axis=1)[0])  # Get the max probability as confidence
    print(confidence)
    return class_names[predicted_class], confidence

@app.route('/uploadpn', methods=['GET', 'POST'])
def uploadpn():
    if request.method == 'POST':
        f = request.files['file']
        if f and (f.filename.endswith(('.png', '.jpg', '.jpeg'))):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            f.save(file_path)
            predicted_class, confidence = predict_image_class(loaded_model, file_path)
            current_datetime = datetime.datetime.now()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO user_history VALUES (NULL, %s, %s, %s, %s)', (session['id'], file_path, predicted_class, current_datetime))
            mysql.connection.commit()
            return render_template('upload-pn.html', file_path=file_path, file_result=f"{predicted_class} Accuracy:{confidence}")
    return render_template('upload-pn.html')


UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/train', methods=['GET', 'POST'])
def train():
    if request.method == 'POST':
        # Get the uploaded dataset folder (as a zip file)
        dataset_file = request.files['dataset']
        if dataset_file:
            filename = secure_filename(dataset_file.filename)
            dataset_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            dataset_file.save(dataset_path)

            # Unzip the folder
            with zipfile.ZipFile(dataset_path, 'r') as zip_ref:
                zip_ref.extractall(app.config['UPLOAD_FOLDER'])

            # Start training in a separate function
            accuracy = start_training()  # Simulate training function

            # Send back the accuracy and completion message
            return jsonify({'accuracy': accuracy, 'message': 'Training Complete!'})
    
    return render_template('train.html')

# Mock function for training the model (Simulate it with a sleep call)
def start_training():
    # Simulating training process with a loop and sleep (can be replaced with actual model training)
    accuracy = 0.85  # Example accuracy
    for i in tqdm(range(100)):
        time.sleep(0.1)  # Simulate processing time
    return accuracy

# Route to check progress (dummy example)
@app.route('/progress')
def progress():
    # You can store progress in a global variable or session
    # For now, this just returns dummy progress percentage
    return jsonify({'progress': 50})