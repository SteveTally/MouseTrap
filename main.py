#from os import wait
from machine import SPI, Pin, lightsleep
import tinypico as TinyPICO
from dotstar import DotStar
import time, random, micropython
import config
import ubinascii
import urequests
import network
#import logging
import time

#todo: deal with inactive Wifi
#todo: set up logging
#todo: alternate light flashing to show current status, and if the trap has been triggered since last reset

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

# Configure DotStar LED
# Configure SPI for controlling the DotStar
# Internally we are using software SPI for this as the pins being used are not hardware SPI pins
class MouseTrap(): 

    def __init__(self):
        #logging.basicConfig(filename='myapp.log', level=logging.INFO)
  
        # initialize dotstar LED
        spi = SPI(sck=Pin( TinyPICO.DOTSTAR_CLK ), mosi=Pin( TinyPICO.DOTSTAR_DATA ), miso=Pin( TinyPICO.SPI_MISO) ) 
        self.dotstar = DotStar(spi, 1, brightness = 0.1 ) # Just one DotStar, half brightness
        TinyPICO.set_dotstar_power( True ) # Turn on the power to the DotStar
        self.dotstar[0] = ( 255, 255, 255, 0.5) # set initial dotstar color

        # initialize GPIO pin, set to input and pull up mode
        self.pin_in = Pin(33, mode=Pin.IN, pull=Pin.PULL_UP) # set GPIO pin to correct mode

        time.sleep(1)

        # if circut is not closed, trigger debug mode
        if self.pin_in.value():
            self.debug_mode = True
            print("Initial circuit state is open.  Eentering debug mode")
        else:
            self.debug_mode = False

        # recheck settings
        if self.debug_mode:
            self.recheck_count = 1 # how many times to re-check pin before firing an alert
            self.recheck_delay = 0 # how many seconds to wait between recheck loops
        else:
            self.recheck_count = 5 # how many times to re-check pin before firing an alert
            self.recheck_delay = 0.1 # how many seconds to wait between recheck loops

        # initialize Twillow SMS service
        self.sms = TwilioSMS(account_sid = config.tw_sid,
                            auth_token = config.tw_token)

        # state indicators
        self.message_sent = False
        self.trap1_triggered = False
        self.active = False

        # initialize wlan and set inactive
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(False)




    def sendsms(self, message):
        print("connecting..")
        # connect to Wifi and send a message
        self.wlan.active(True) # activate Wifi
        self.wlan.connect(config.ssid, config.ssid_pwd) # Connect to Wifi netwprk

        while not self.wlan.isconnected(): #wait for active Wifi connection
            self.dotstar[0] = ( 255, 255, 0, 0.5) # set initial dotstar color
            pass

        print("connected...")
        self.dotstar[0] = ( 0, 255, 0, 0.5) # set initial dotstar color
        self.sms.create(body = message, # send message
                        from_ = config.from_phone,
                        to = config.to_phone) 
        
        self.wlan.disconnect() #disconnect
        self.wlan.active(False) #deactivate Wifi 

    def check_traps(self):
        
        if not self.pin_in.value(): #check the trap
            self.trap1_triggered = False
            self.dotstar[0] = ( 0, 255, 0, 0.5) # green indicator light

        else:
            self.trap1_triggered = True # the trap was triggered

            # recheck the pre-determined number of times to be sure
            for i in range(self.recheck_count):
                if not self.trap1_triggered:
                    self.trap1_triggered = False
                    break
                time.sleep(self.recheck_delay)
            
            # take action if trap was triggered
            if self.trap1_triggered:
                self.dotstar[0] = ( 255, 0, 0, 0.5) # red indicator light
                if not self.message_sent and not self.debug_mode:
                    self.sendsms("We got one!  Go check the trap.")
                    self.message_sent = True

app = MouseTrap()

while True:
    TinyPICO.set_dotstar_power( True ) 
    app.check_traps()
    time.sleep(0.01)
    
    
    if not app.debug_mode:
        time.sleep(10)
        TinyPICO.set_dotstar_power( False ) 
        lightsleep(10000)
    
    

