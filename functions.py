import os  # to enable us navigate the system for files
import matplotlib.pyplot as plt  # to enable us visualize the waveforms
import tensorflow as tf
import tensorflow_io as tfio  # to make it easier for us to input and output in tf
import numpy as np  # for necessary Mathematical calculations with arrays
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from geopy.geocoders import Nominatim
import geocoder

# For sending SMS on phone
from jnius import autoclass
from plyer.facades import Sms




# Get the directory of the current Python script
script_dir = os.path.dirname(os.path.abspath(__file__))

model_path = 'chainsaw_detection.tflite'
recipients_list = 'email_list.txt'
phonebook = 'phonebook.txt'

# Constructs the file path relative to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
tf_model_path = os.path.join(script_dir, model_path)
recipients_list_path = os.path.join(script_dir, recipients_list)
phonebook_path = os.path.join(script_dir, phonebook)

# Define a function for creating the spectrogram

def spect_predict(file_path, send_the_email, send_the_sms):
    # load the wav file
    file_content = tf.io.read_file(file_path)

    # decode wav
    wav, sr = tf.audio.decode_wav(file_content, desired_channels=1)

    wav = tf.squeeze(wav, axis=-1)
    #sr = tf.cast(sr, dtype=tf.int64)

    # down sample from 44.1kHz to 16kHz
    #wav = tfio.audio.resample(wav, rate_in=sr, rate_out=16000)

    # grab the first 10s
    wav = wav[:160000]

    # pad zeros to the shorter clips
    #zero_pads = tf.zeros([160000] - tf.shape(wav), dtype=tf.float32)
    #wav = tf.concat([zero_pads, wav], 0)

    spectrogram = tf.signal.stft(wav, frame_length=320, frame_step=32)
    spectrogram = tf.abs(spectrogram)
    spectrogram = tf.expand_dims(spectrogram, axis=2)
    spectrogram = tf.expand_dims(spectrogram, axis=0)

    #load the lite interpreter
    interpreter = tf.lite.Interpreter(model_path)

    # Get input and output tensors
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    #set and predict
    # input_shape = input_details[0]['shape']
    interpreter.set_tensor(input_details[0]['index'], spectrogram)

    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])

    print("Output probability is ", output_data[0][0])

    # Making predictions

    if output_data[0][0] >= 0.75:
        if send_the_email == 'yes': 
            with open('password.txt', 'r') as file:
                password = file.read().strip()
            # print(password)
            subject = "Deforestation Detected"
            time, latitude, longitude = get_time_latitude_longitude()
            body = f'Deforestation has been detected at the following location:\n\nTime: {time}\nLocation: Latitude: {latitude}, Longitude: {longitude}\n'

            sender = "defordector@gmail.com"
            recipients = get_recipients_from_file(recipients_list_path)
            send_email(subject, body, sender, recipients, password) # Replace with the desired phone number
            # You can also pass the prediction value to the send_message function if needed
        
        # # For sending SMS to phone
        # if send_the_sms == 'yes': 
        #     # also send an sms
        #     sms_service.send(recipient = get_recipients_from_file(phonebook_path), message = body)

    else:
        pass  #

    

def get_recipients_from_file(filename):
    recipients = []
    try:
        with open(filename, 'r') as file:
            recipients = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{filename} file not found.")
    return recipients



def save_email_to_list(email):
    # Open the file in append mode and write the email
    with open('email_list.txt', 'a') as file:
        file.write(email + '\n')


def get_time_latitude_longitude():
    try:
        # Getting the current time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        # Getting the device location
        g = geocoder.ip('me')
        if g.latlng:
            latitude, longitude = g.latlng
            print('DAVE --------------------------\n\n\n\n\n\n\n',latitude, longitude, current_time)
            return current_time, latitude, longitude
        else:
            print("Unable to retrieve device location.")
            return current_time, None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        print("Message sent!")
        


# # Sending SMS on mobile

# # Define SmsManager using jnius
# SmsManager = autoclass('android.telephony.SmsManager')

# # Define AndroidSms class inheriting from plyer's Sms facade
# class AndroidSms(Sms):

#     def _send(self, **kwargs):
#         # Get the default SmsManager instance
#         sms = SmsManager.getDefault()
        
#         # Extract recipient and message from kwargs
#         recipient = kwargs.get('recipient')
#         message = kwargs.get('message')
        
#         # Send the SMS message
#         if sms:
#             sms.sendTextMessage(recipient, None, message, None, None)

# # Define instance function to return an instance of AndroidSms
# def instance():
#     return AndroidSms()

# # Example usage
# if __name__ == '__main__':
#     sms_service = instance()
#     sms_service.send(recipient='1234567890', message='Hello from Kivy!')






