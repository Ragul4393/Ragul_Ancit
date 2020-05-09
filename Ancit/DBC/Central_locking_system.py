'''
Created on 08-May-2020

@author: ragul
'''
import can
import cantools
import threading

bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)
db = cantools.db.load_file('/home/ragul/Downloads/comfort.dbc')

centrallockingMsg = db.get_message_by_name('CentralLockingSystemState')
vehiclemotionMsg = db.get_message_by_name('VehicleMotion')
windowcontrolMsg = db.get_message_by_name('WindowControl')
LockingRemoteMsg = db.get_message_by_name('LockingRemoteControlRequest')

def door_lock():
    data = centrallockingMsg.encode({'LockState':1,'AntiTheftSystemActive':0})
    message = can.Message(arbitration_id=centrallockingMsg.frame_id, data=data, is_extended_id=False)
    try:
        bus.send(message)
        print("vehicle start move so door closed")
    except:
        print("Message not sent")
        
def door_lock_with_window_close():
    data = centrallockingMsg.encode({'LockState':1,'AntiTheftSystemActive':0})
    message = can.Message(arbitration_id=centrallockingMsg.frame_id, data=data, is_extended_id=False)
    try:
        bus.send(message)
        print("lock the vehicle by key")
    except:
        print("Message NOT sent")    
def door_unlock():
    data = centrallockingMsg.encode({'LockState':0,'AntiTheftSystemActive':0})
    message = can.Message(arbitration_id=centrallockingMsg.frame_id, data=data, is_extended_id=False)
    try:
        bus.send(message)
        print("unlock the vehicle by key")
    except:
        print("Message not sent")
        
def door_unlock_with_window_open():
    data = centrallockingMsg.encode({'LockState':0,'AntiTheftSystemActive':0})
    message = can.Message(arbitration_id=centrallockingMsg.frame_id, data=data, is_extended_id=False)
    try:
        bus.send(message)
        print("all doors and windows are unlock")
    except:
        print("Message NOT sent")
def Theft_System_Active():
    data = centrallockingMsg.encode({'LockState':1,'AntiTheftSystemActive':1})
    message = can.Message(arbitration_id=centrallockingMsg.frame_id, data=data, is_extended_id=False)
    try:
        bus.send(message)
        print("theft Alert system activated")
    except:
        print("Message NOT sent")
def on_Message():
    while True:
        message = bus.recv()
        msgData = db.decode_message(message.arbitration_id, message.data)
        if message.arbitration_id == vehiclemotionMsg.frame_id:
            vehicleState = (msgData['EngineRunning'])
            vehicleCondition = (msgData['CrashDetected'])
            if (vehicleState==1):
                if(vehicleCondition==0):
                    door_lock()
                elif (vehicleCondition==1):
                    door_unlock_with_window_open()
                
        if message.arbitration_id == LockingRemoteMsg.frame_id:
            LockStates = (msgData['LockRequest'])
            if(LockStates==1):
                door_lock_with_window_close()
            elif (LockStates==2):
                door_unlock()
        if message.arbitration_id == centrallockingMsg.frame_id:
            vehicle = (msgData['AntiTheftSystemActive'])
            if (vehicle == 1):
                Theft_System_Active()
                
if __name__ == '__main__':
    threading.Thread(on_Message()).start()