from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton,MDFloatingActionButton
from kivy.lang import Builder
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
import numpy as np
import sounddevice as sd
import wavio
import os
from screen_graphics import screen_helper
from functions import spect_predict




class MainPageScreen(Screen):
    is_recording = False
    recording = None
    recorded_audios = []

    def start_recording(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, 'output_segments')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        if not self.is_recording:
            self.is_recording = True
            self.recording = sd.rec(int(10 * 16000), samplerate=16000, channels=1)
            Clock.schedule_once(self.stop_recording, 10)
            self.ids.start_button.disabled = True
            self.ids.stop_button.disabled = False
            

    def stop_recording(self, *args):
        if self.is_recording:
            self.is_recording = False
            sd.wait()
            if self.recording is not None and isinstance(self.recording, np.ndarray):
                script_dir = os.path.dirname(os.path.abspath(__file__))
                output_dir = os.path.join(script_dir, 'output_segments')
                audio_filename = os.path.join(output_dir, f'recording{len(self.recorded_audios) + 1}.wav')
                wavio.write(audio_filename, self.recording, 16000, sampwidth=2)
                self.recorded_audios.append(audio_filename)
                self.ids.start_button.disabled = False
                self.ids.stop_button.disabled = True
                # Call the spect_predict function with the saved audio filename

                # Check if the email checkbox is checked
                if self.ids.email_checkbox.active:
                    spect_predict(file_path =audio_filename, send_the_email = 'yes', send_the_sms = 'no')

                # # Check if the SMS checkbox is checked
                # if self.ids.sms_checkbox.active:
                #     spect_predict(file_path =audio_filename, send_the_email = 'no', send_the_sms = 'yes')

                

    def save_email_to_list(self):
        email = self.ids.email_textfield.text
        if email:
            with open('email_list.txt', 'a') as file:
                file.write(email + '\n')

    def save_phone_number_to_list(self):
        phone_number = self.ids.sms_textfield.text
        if phone_number:
            with open('phonebook.txt', 'a') as file:
                file.write(phone_number + '\n')

class DeforDetector(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Green'
        return Builder.load_string(screen_helper)

if __name__ == '__main__':
    DeforDetector().run()