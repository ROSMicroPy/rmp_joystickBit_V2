import gc
import time

from ROSMicroPy import registerDataType, dumpDataType, registerEventSubscription
from ROSMicroPy import run_ROS_Stack, init_ROS_Stack, registerROSPublisher, publishMsg
from ROSMicroPy import setNodeName, setAgentIP, setAgentPort

from rostype.Twist import Twist
from rostype.Attachment import Attachment

from mbits.lib.JoystickBit import joystickbit

#rosInit is set to True on successfull init of the ROS Stack
rosInit = False

#In Debug Mode, ROS is not iniitalized and won't send messages.
#it will only print the value on change

rosDebug = False


setNodeName("JoystickController")

#
#
# Joystick:Bit V2
#
# Right <= 0  (neg numbers)
# Left >= 0  (pos numbers
#
# Down <= 0  (neg numbers)
# Up >= 0  (pos numbers
#
# Buttons Up = 1, Down = 0
#
#

emptyMsg = {
    "linear":  { "x": 0.0, "y": 0.0,  "z": 0.0 },
    "angular": { "x": 0.0, "y": 0.0,  "z": 0.0 }
}

attachMsg = { "attachment": 0.0 }


#
# Increase Speed on Right, passing a Pos value for Linear.z
# 
def onButton_Right(val:int) -> None:
    print("bRight:{val}")
    mesg = emptyMsg
    if (val == 0):
        mesg['linear']['z']=2
        if( rosInit and not rosDebug ): publishMsg(pubCmdVel, mesg);

#
# Decrese Speed, passing Neg value for linear.z
#
def onButton_Left(val:int) -> None:
    print("bLeft:{val}")
    mesg = emptyMsg
    if (val == 0):
        mesg['linear']['z']=-2
        if( rosInit and not rosDebug ): publishMsg(pubCmdVel, mesg);


#
# Raise Attachment using angular.z
#
def onButton_Up(val:int) -> None:
    print(f"bUp: {val}")
    mesg = attachMsg
    if (val == 0):
        mesg['attachment']=1
        if( rosInit and not rosDebug): publishMsg(pubAttach, mesg);
    

#
# Lower Attachment using angular.z
#  
def onButton_Down(val:int) -> None:
    print(f"bDown:{val}")

    mesg = attachMsg
    if (val == 0):
        mesg['attachment']=-1
        if( rosInit and not rosDebug): publishMsg(pubAttach, mesg);

#
# If a Positive value, turn left by angular.y
#
def onJoystick_X(val:int) -> None:
    
    print(f"Joy X: {val}")

    mesg = emptyMsg
    if (abs(val) < 10): val = 0
    
    if (val > 0):
        mesg['angular']['y']=2
    elif (val < 0):
        mesg['angular']['y']=-2
    else:
        mesg['angular']['y']=0
    if( rosInit and not rosDebug ): publishMsg(pubCmdVel, mesg);



def onJoystick_Y(val:int) -> None:
    print(f"Joy Y: {val}")
    mesg = emptyMsg
    if (abs(val) < 10): val = 0
    
    if (val > 0):
        mesg['linear']['x']=2
    elif (val < 0):
        mesg['linear']['x']=-2
    else:
        mesg['linear']['x']=0

    if( rosInit and not rosDebug): publishMsg(pubCmdVel, mesg);


if (not rosDebug): 
    print("\r\nInit ROS Stack\r\n")
    init_ROS_Stack()

    print("Registgering Data Type\r\n")

    typeTwist = registerDataType(Twist.dataMap)
    dumpDataType(typeTwist)
    
    typeAttach = registerDataType(Attachment.dataMap)
    dumpDataType(typeAttach)
    
    print("Registgering Event Publishers\r\n")
    pubCmdVel = registerROSPublisher("turtle1/cmd_vel", typeTwist)
    pubAttach = registerROSPublisher("turtle1/attachment", typeAttach)

    print("Run ROS Stack\r\n")
    run_ROS_Stack()
    
    rosInit = True


joystick = joystickbit()
joystick.onButton_Up( onButton_Up )
joystick.onButton_Down( onButton_Down )
joystick.onButton_Right( onButton_Right )
joystick.onButton_Left( onButton_Left )

joystick.onJoystick_X( onJoystick_X )
joystick.onJoystick_Y( onJoystick_Y )



