from Core.IService import IService
from Core.TelegramBotManager import TelegramBotManager
from Files.MessageListeners.MiscMessageListener import MiscMessageListener
import RPi.GPIO as GPIO
import logging
from Core.Util.Util import Util
from Files.Database.BotDatabase import BotDatabase, Tables
from Files.Database.TableMaps import UsersTableMap, UsersAccessMode

from gpiozero import Button

button = None
blueled = 0
class GpioService(IService):
    def __init__(self):
        super(GpioService, self).__init__(2)

    def initialize(self):
        try:
            #print("GPIO listener is initialized!")
            message = 'Alarm sistemi baslatildi.'
            TelegramBotManager().send_broadcast_message(message, None)
            global button
            global blueled
            
            GPIO.setmode(GPIO.BCM)  # set up BCM GPIO numbering
            GPIO.setup (25, GPIO.IN)  # set GPIO25 as input (sensor)
            GPIO.setup(22, GPIO.OUT)  # set GPIO22 as an output (LED)
            GPIO.setup(23, GPIO.OUT)  # set GPIO22 as an output (ALARM)
            button = Button(25)
        except Exception as e:
            logging.error(str(e))
            TelegramBotManager().send_broadcast_message(text='Exception' + str(e),user_access=None)

    def run_service(self):
        try:
  
            GPIO.output(22, GPIO.LOW)
            global blueled
            blueled = blueled + 1
            if (blueled%2) == 0:
                #logging.error('BB0\n')
                GPIO.output(23, GPIO.HIGH)
                blueled = 0
            else:
                #logging.error('BB1\n')
                GPIO.output(23, GPIO.LOW)              
            #logging.error('Alarm State'+ str(MiscMessageListener.alarm_state))
            if MiscMessageListener.alarm_state == True:
                if GPIO.input(25):  # if port 25 == 1
                    GPIO.output(22, GPIO.HIGH)
                    global button
                    button.wait_for_press()
                    message = "Hareket algilandi! Video cekiliyor..."
                    TelegramBotManager().send_broadcast_message(text=message,user_access=None)
                    filter_result = BotDatabase().filter(Tables.USERS,
                                         lambda row: row[UsersTableMap.ACCESS] == UsersAccessMode.ADMIN) 
                    #logging.error('Capturing video\n')
                    Util.capture_video(5)
                    if filter_result.count > 0:
                        for user in filter_result.rows:
                            if UsersTableMap.CHAT_ID in user:
                                chat_id = user[UsersTableMap.CHAT_ID]
                                #Util.capture_video(5)
                                file = open('out.avi', 'rb')
                                TelegramBotManager().bot.send_document(chat_id=chat_id, document=file, timeout=300)
                #logging.error('blue led '+ str(blueled)+'\n')
        except Exception as e:
            TelegramBotManager().send_broadcast_message(text='Exception' + str(e),user_access=None)
            logging.error('Gpio run service error'+ str(e))