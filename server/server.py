from flask import Flask, request, jsonify, render_template
import paho.mqtt.client as mqtt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time, os, base64
from dotenv import load_dotenv

app = Flask(__name__)

if not load_dotenv():
    print("Error loading .env file")
    exit(1)

# MQTT Broker details TODO: put into .env later on
mqtt_broker = os.getenv("MQTT_BROKER")
mqtt_port = 1883
mqtt_topic = os.getenv("MQTT_TOPIC")
user = os.getenv("MQTT_USER")
password = os.getenv("MQTT_PASS")

email_user = os.getenv("EMAIL_USER")
email_recipient = os.getenv("EMAIL_RECIPIENT")
email_app_pass = os.getenv("EMAIL_APP-PASS")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK Returned code=", rc)
        client.subscribe(mqtt_topic)
    else:
        print("Bad connection Returned code=", rc)


def on_message(client, userdata, msg):
    print(f"Received message from topic {msg.topic}: {type(msg.payload)}")
    # photo = base64.b64decode(msg.payload)
    photo = msg.payload
    send_email(photo)


def send_email(photo):
    msg = MIMEMultipart()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    msg["Subject"] = f"Doorbell Notification - {current_time}"
    msg["From"] = email_user
    msg["To"] = email_recipient

    body = "Someone is at your door"
    msg.attach(MIMEText(body))

    payload = MIMEBase("application", "octet-stream")
    payload.set_payload(photo)
    encoders.encode_base64(payload)
    payload.add_header("Content-Disposition", f"attachment; filename=photo.jpg")
    msg.attach(payload)

    try:
        # Connect to the google's SMTP server
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(email_user, email_app_pass)
        s.sendmail(email_user, [email_recipient], msg.as_string())
        s.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    photo = request.files["photo"].read()
    print(f"Size of photo: {len(photo)} bytes")

    client.publish(mqtt_topic, photo)
    return jsonify({"message": "Photo uploaded successfully"})


if __name__ == "__main__":
    # Initialize the MQTT client
    client = mqtt.Client()
    client.username_pw_set(user, password)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_start()
    app.run(host="0.0.0.0", port=5000, debug=True)
