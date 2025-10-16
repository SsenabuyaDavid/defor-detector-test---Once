screen_helper = """
MainPageScreen:
    BoxLayout:
        orientation: 'vertical'
        
        # AnchorLayout for the "Defor Detector" label
        AnchorLayout:
            size_hint_y: None
            height: dp(56)
            anchor_x: 'center'
            anchor_y: 'top'
            padding: dp(10)
            canvas.before:
                Color:
                    rgba: app.theme_cls.primary_color
                Rectangle:
                    size: self.size
                    pos: self.pos

            MDLabel:
                text: "Defor Detector"
                halign: 'center'
                color: 1, 1, 1, 1
                font_size: '20sp'
                bold: True
        
        # ScrollView for the rest of the content
        ScrollView:

            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(10)
                padding: dp(10)
                adaptive_height: True

                MDRectangleFlatButton:
                    id: start_button
                    text: 'Start Recording'
                    on_press: root.start_recording()
                    size_hint_y: None
                    height: dp(48)

                MDRectangleFlatButton:
                    id: stop_button
                    text: 'Stop Recording'
                    on_press: root.stop_recording()
                    size_hint_y: None
                    height: dp(48)
                    disabled: True  # Initially disabled until recording starts

                MDTextField:
                    id: email_textfield
                    hint_text: "Type an email"
                    mode: "rectangle"
                    size_hint_y: None
                    height: dp(48)
                    size_hint_x: 1  # Ensure it stretches to fill the width

                MDRectangleFlatButton:
                    text: 'Save Email to List'
                    on_release: root.save_email_to_list()
                    size_hint_y: None
                    height: dp(48)

                Widget:
                    size_hint_y: None
                    height: dp(50)  # Spacer to push the buttons to the top of the screen
                
                MDTextField:
                    id: sms_textfield
                    hint_text: "Type phone number"
                    mode: "rectangle"
                    size_hint_y: None
                    height: dp(48)
                    size_hint_x: 1  # Ensure it stretches to fill the width

                MDRectangleFlatButton:
                    text: 'Save Phone number to List'
                    on_release: root.save_phone_number_to_list()
                    size_hint_y: None
                    height: dp(48)

                Widget:
                    size_hint_y: None
                    height: dp(50)  # Spacer to push the buttons to the top of the screen
                
                
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(48)
                    spacing: dp(10)
                    padding: dp(10)
                    size_hint_x: 1  # Ensure it stretches to fill the width

                    MDCheckbox:
                        id: email_checkbox
                        size_hint: None, None
                        size: dp(48), dp(48)

                    MDLabel:
                        text: "Send Email"
                        size_hint_x: None
                        width: dp(200)
                        valign: 'center'
                        halign: 'left'

                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: dp(48)
                    spacing: dp(10)
                    padding: dp(10)
                    size_hint_x: 1  # Ensure it stretches to fill the width

                    MDCheckbox:
                        id: sms_checkbox
                        size_hint: None, None
                        size: dp(48), dp(48)

                    MDLabel:
                        text: "Send Text"
                        size_hint_x: None
                        width: dp(200)
                        valign: 'center'
                        halign: 'left'
"""
