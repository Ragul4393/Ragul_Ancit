'''
Created on 08-May-2020

@author: ragul
'''
import can
import cantools
from pynput import keyboard
import threading

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)
db = cantools.db.load_file('/home/ragul/Downloads/comfort.dbc')

centrallockingMsg = db.get_message_by_name('CentralLockingSystemState')
vehiclemotionMsg = db.get_message_by_name('VehicleMotion')
windowcontrolMsg = db.get_message_by_name('WindowControl')
LockingRemoteMsg = db.get_message_by_name('LockingRemoteControlRequest')

def Remote_locking():
    data = LockingRemoteMsg.encode({'LockRequest':1})
    message = can.Message(arbitration_id=LockingRemoteMsg.frame_id, data=data, is_extended_id=False)
    try:
        bus.send(message)
        print("door locked")
    except can.CanError:
        print("Message NOT sent")
 
def Remote_unlocking():
    data = LockingRemoteMsg.encode({'LockRequest':2})
    message = can.Message(arbitration_id=LockingRemoteMsg.frame_id, data=data, is_extended_id=False)
    try:
        bus.send(message)
        print("door unlocked")
    except can.CanError:
        print("Message NOT sent")
def vehicle_start_runing():
    data = vehiclemotionMsg.encode({'Velocity':0,'CrashDetected':0,'EngineRunning':1})
    message = can.Message(arbitration_id=vehiclemotionMsg.frame_id, data=data, is_extended_id=False)
    try:
        bus.send(message)
        print(" vehicle start moving and door Locked")
    except can.CanError:
        print("Message NOT sent")
def emergency_exit():
    data = vehiclemotionMsg.encode({'Velocity':0,'CrashDetected':1,'EngineRunning':1})
    message = can.Message(arbitration_id=vehiclemotionMsg.frame_id, data=data, is_extended_id=False)
    try:
        bus.send(message)
        print("all the doors and windows are open")
    except can.CanError:
        print("Message NOT sent")
def Theft_founded():
    data = centrallockingMsg.encode({'LockState':1, 'AntiTheftSystemActive':1})
    message = can.Message(arbitration_id=centrallockingMsg.frame_id, data=data, is_extended_id=False)
    try:
        bus.send(message)
        print("vehicle theft founded")
    except:
        print("Message NOT sent")

def on_press(key):
    try:
        if key.char == 'l':
            Remote_locking()
        if key.char == 'u':
            Remote_unlocking()
        if key.char == 's':
            vehicle_start_runing()
        if key.char == 'e':
            emergency_exit()
        if key.char == 't': 
            Theft_founded()
        if key == keyboard.Key.esc:
            return False  
    except AttributeError:
        print(" Unknown Key Event")
                         
def on_Key():
    keyboard.Listener(on_press=on_press).start()
                
def on_Message():
    while True:
        response = bus.recv()
        msgData = db.decode_message(response.arbitration_id, response.data)
        if response.arbitration_id == centrallockingMsg.frame_id:
            lockstatus = (msgData['LockState'])
            security = (msgData['AntiTheftSystemActive'])
            if (lockstatus == 'Locked'):
                print("vehicle door locked")
            if (lockstatus == 'Unlocked'):
                print("vehicle door unlocked")
                 
            if (security == 1):
                print("vehicle alert system active")
                
def instruction():
    print("Simulation Keys:\n\
            l: Lock door\n\
            u: Unlock door\n\
            s: engine start\n\
            e: crash detected\n\
            t: theft detected\n")
    print("--Test Msg--\t\t--Evaluated Msg--")

if __name__ == '__main__':
    instruction()
    on_Key()
    threading.Thread(on_Message()).start()