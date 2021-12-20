
### Mouse Trap Notification App ###
# This app is designed to be used with the M5Stick ESP32 microcontroller
# Have you ever tried to live-trap mice?  If you have, and you don't check traps often, you are no longer live trapping.
# 

from m5stack import *
from m5ui import *
from uiflow import *
import ubinascii
import urequests

class TwilioSMS:
# TwillowSMS class from https://www.twilio.com/blog/sms-doorbell-micropython-twilio
    base_url = 'https://api.twilio.com/2010-04-01'

    def __init__(self, account_sid, auth_token):
        self.twilio_account_sid = account_sid
        self.twilio_auth = ubinascii.b2a_base64('{sid}:{token}'.format(
            sid=account_sid, token=auth_token)).strip()

    def create(self, body, from_, to):
        data = 'Body={body}&From={from_}&To={to}'.format(
            body=body, from_=from_.replace('+', '%2B'),
            to=to.replace('+', '%2B'))
        r = urequests.post(
            '{base_url}/Accounts/{sid}/Messages.json'.format(
                base_url=self.base_url, sid=self.twilio_account_sid),
            data=data,
            headers={'Authorization': b'Basic ' + self.twilio_auth,
                     'Content-Type': 'application/x-www-form-urlencoded'})
        print('SMS sent with status code', r.status_code)
        print('Response: ', r.text)

class MouseApp():
  
  def __init__(self):
    self.tmp = 1
    self.pin0 = machine.Pin(0, mode=machine.Pin.IN, pull=machine.Pin.PULL_UP) # set GPIO pin to correct mode
    self.sms = TwilioSMS(account_sid = 'sid',
                         auth_token = 'token')
    self.message_sent = False
    self.recheck_delay = 0
    self.recheck_count = 0
    self.trap1_triggered = False
    self.get_stats()
    self.active = False

  def get_stats(self):
    self.batt_voltage = axp.getBatVoltage()
    self.chg_st = axp.getChargeState()
    self.temp = axp.getTempInAXP192()

  def check_traps(self):
    
    if not self.pin0.value():
      self.trap1_triggered = False
      #M5Led.off()
    else:
      self.trap1_triggered = True
      self.refresh_interface()
      if self.message_sent == False:
        self.message_sent = True
        self.sms.create(body = "I got one !", from_ = 6163799822, to= 6169155426 )
      #M5Led.on()
      
      #wait(self.recheck_delay)
      #if self.pin0.value():
      #  self.trap1_triggered = False
      #  M5Led.off()
      #else:
      # self.trap1_triggered = True
      #  M5Led.on()
    self.refresh_interface()

  def send_sms()

  def draw_interface(self):
    setScreenColor(0xffffff)
    self.get_stats()
  
    text_start_line = 35
    text_spacing = 30
    col1 = 9
    col2 = 72 
    title = M5Title(title="Mouse Notifier", x=15, fgcolor=0x000000, bgcolor=0xd7d7d7)
  
    cursor = text_start_line
  
    # Labels
    self.active_label = M5TextBox(col1, cursor, "Active", lcd.FONT_Default, 0x4b4b4b, rotate=0)
    cursor += text_spacing
    self.voltage_label = M5TextBox(col1, cursor, "", lcd.FONT_Default, 0x4b4b4b, rotate=0)
    cursor += text_spacing
    self.temp_label = M5TextBox(col1, cursor, "Temp:" + str(round(self.temp,2)), lcd.FONT_Default, 0x4b4b4b, rotate=0)
    cursor += text_spacing
    self.trap1_label = M5TextBox(col1, cursor, "Trap1", lcd.FONT_Default, 0x4b4b4b, rotate=0)
    cursor += text_spacing
    self.sms_label = M5TextBox(col1, cursor, "SMS Sent?", lcd.FONT_Default, 0x00ff25, rotate=0)
  
  # Indicators
    cursor = text_start_line
    self.active_ind = M5Rect(col2, cursor, 25, 25, 0xd8d8d8, 0xFFFFFF)
    cursor += text_spacing*3
    self.trap1_ind = M5Rect(col2, cursor, 25, 25, 0xd8d8d8, 0xFFFFFF)
    cursor += text_spacing
    self.sms_ind = M5Rect(col2, cursor, 25, 25, 0xd8d8d8, 0xFFFFFF)
  #batt_voltage_label = M5TextBox(9, text_start_line+text_spacing*3, batt_voltage, lcd.FONT_Default, 0x4b4b4b, rotate=0)
  #batt_temp_label = M5TextBox(9, text_start_line+text_spacing*4, batt_voltage, lcd.FONT_Default, 0x4b4b4b, rotate=0)
  #temp_label = M5TextBox(9, text_start_line+text_spacing*5, temp, lcd.FONT_Default, 0x4b4b4b, rotate=0)

  def refresh_interface(self):
    #set trap status
    
    if self.trap1_triggered:
      self.trap1_ind.setBgColor(0xff0000)
    else:
      self.trap1_ind.setBgColor(0x00ff25)
     
    if self.message_sent:
      self.sms_ind.setBgColor(0x00ff25)
    else  
      self.sms_ind.setBgColor(0xd8d8d8)
      
    if self.active:
      self.active_ind.setBgColor(0x00ff25)
    else  
      self.active_ind.setBgColor(0xd8d8d8)
      
    # update battery voltage
    self.voltage_label.setText("battery v:" + str(self.batt_voltage))
    
# Initialize App
app = MouseApp()
app.draw_interface()

# Main Loop
while True:
  
  # Change active status when button A is pressed
  if btnA.wasPressed:
    if self.active:
      self.active = False
    else
      self.active = True
      
  # If active, check traps
  if self.active:
    app.get_stats()
    app.check_traps()
  
  # If button B is pressed, reset SMS sent indicator
  if btnB.wasPressed:
    self.message_sent = False


  
  #axp.setLcdBrightness(50)
  #axp.setLcdBrightness(0)

  

