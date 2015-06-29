#Arduino Protocol

The protocol is used for the communication between Raspberry-Pi and Arduino(that handles the movement).

You can use two ways to move **XM**: the asynchronous mode, that use lowercase letters as ID
and the synchronous mode, that instead use uppercase.
Each response from Arduino will be only **ACK**, **NACK** or a message that identify an unsupported command. To check if the received message is **ACK** or **NACK** just do the binary AND between the received message and **ACK**. If is **1** is **ACK** otherwise is **NACK**.

##Commands
The protocol provides 4 commands for the synchronous movement, 5 commands for
the asynchronous movement and a couple for the settings:

 - **FORWARD**;
 - **BACKWORD**;
 - **LEFT**;
 - **RIGHT**;

These 4 commands match respectively 'F', 'B', 'L', 'R' for the synchronous mode and
'f', 'b', 'l', 'r' for the asynchronous. The asynchronous movement also has a new one
command:

 - **ASYNC\_STOP**;

that correspond to the 'z' letter: this command is used to stop **XM**.

The setters command are:

 - **SET\_SPEED**;
 - **SET\_MOVE\_TIME**;

These commands match respectively to the 'X' and 'T' letters. The first command sets the speed of the motors and it requires 1 additional byte while the second sets the time during which the motors will move (only in the synchronous communication) and requires 2 bytes in big endian order.



##How to add new commands

To add new messages just follow these rules:

 - **COMMANDS**: commands must be a **positive even number**;
 - **ERROR MESSAGES**: error messages must be a **negative even number**.
