/*
 *    *** MOTORS ***
 * CONTROL pins 5,6 are PWM speed controls while
 * DIR_CONTROL 4,7 are digital pins used to control direcection.
 * Speed must be an integer between 0 and 255.
 * If DIR_CONTROL is HIGH the motors move backword, otherwise
 * they move forward.
 */
int M1_CONTROL = 5;
int M1_DIR_CONTROL = 4;
int M2_CONTROL = 6;
int M2_DIR_CONTROL = 7;

int SERIAL_BAUDRATE = 9600;      // baudrate for the serial connection

int moveTime = 1000;             // ms
int motorSpeed = 255;

/*
 *    *** COMUNICATION PROTOCOL ***
 * Comunication Protocol is used for the transmission of messages
 * between Arduino and Raspberry-Pi.
 * Commands are identified by 1 byte as well the responses.
 * Each response is the binary OR between the message received and ACK or NACK
 * Messages forms a bitmask where the LSB is 1 if and only if
 * the response is ACK.
 * Arduino can receives four command from the client:
 *   - FORWARD;
 *   - BACKWORD;
 *   - LEFT;
 *   - RIGHT;
 */

const char UNSUPPORTED_CMD      = -2;
const char NACK                 = 0;
const char ACK                  = 1;

// blocking 
const char FORWARD              = 'F';
const char BACKWORD             = 'B';
const char LEFT                 = 'L';
const char RIGHT                = 'R';

// non-blocking 
const char ASYNC_FORWARD        = 'f';
const char ASYNC_BACKWARD       = 'b';
const char ASYNC_LEFT           = 'l';
const char ASYNC_RIGHT          = 'r';
const char ASYNC_STOP           = 'z';  

// setters
const char SET_SPEED            = 'X';       //requires 1 additional Byte for the speed value
const char SET_MOVE_TIME        = 'T';       //requires 2 additional Bytes(big endian order) for mtimeout value


void setup()
{
  Serial.begin(SERIAL_BAUDRATE);
  pinMode(M1_DIR_CONTROL, OUTPUT);
  pinMode(M2_DIR_CONTROL, OUTPUT);
}

void loop()
{
  dispatch();
}

void setMotors(int m1dir, int m1speed, int m2dir, int m2speed)
{
  digitalWrite(M1_DIR_CONTROL, m1dir);
  digitalWrite(M2_DIR_CONTROL, m2dir);
  analogWrite(M1_CONTROL, m1speed);
  analogWrite(M2_CONTROL, m2speed);
}

void stopMotors()
{
  analogWrite(M1_CONTROL, 0);
  analogWrite(M2_CONTROL, 0);
}

void start_forward(int spd)
{
  setMotors(LOW, spd, LOW, spd);
}

void forward(int spd, int time)
{
  start_forward(spd);
  delay(time);
  stopMotors();
}

void start_backward(int spd)
{
    setMotors(HIGH, spd, HIGH, spd);
}

void backward(int spd, int time)
{
  start_backward(spd);
  delay(time);
  stopMotors();
}

void start_left(int spd)
{
  setMotors(HIGH, spd, LOW, spd);
}

void left(int spd, int time)
{
  start_left(spd);
  delay(time);
  stopMotors();
}

void start_right(int spd)
{
  setMotors(LOW, spd, HIGH, spd);
}

void right(int spd, int time)
{
  start_right(spd);
  delay(time);
  stopMotors();
}

char createAck(char msg)
{
  return  msg | ACK;
}

char createNack(char msg)
{
  return msg | NACK;
}

void setMotorSpeed(int value)
{
    motorSpeed = value;
}

void setMoveTime(int time)
{
    moveTime = time;
}

int assembleUShort(int b1, int b2)    // big endian
{
    return (b1 << 8) + b2;
}

int readFirstValid()
{
    int v = Serial.read();
    while (v < 0) {
       v = Serial.read(); 
    }
    return v;
}

void dispatch()
{
  if (Serial.available() > 0)
  {
    const char cmd = Serial.read();
    char resp = createAck(cmd); // by default the response is ACK

    if (cmd == FORWARD)
    {
      forward(motorSpeed, moveTime);
    }
    else if (cmd == BACKWORD)
    {
      backward(motorSpeed, moveTime);
    }
    else if (cmd == LEFT)
    {
      left(motorSpeed, moveTime);
    }
    else if (cmd == RIGHT)
    {
      right(motorSpeed, moveTime);
    }
    else if (cmd == ASYNC_FORWARD) {
       start_forward(motorSpeed); 
    }
    else if (cmd == ASYNC_BACKWARD) {
       start_backward(motorSpeed); 
    }
    else if (cmd == ASYNC_LEFT) {
       start_left(motorSpeed); 
    }
    else if (cmd == ASYNC_RIGHT) {
       start_right(motorSpeed); 
    }
    else if (cmd == ASYNC_STOP) {
       stopMotors(); 
    }
    else if (cmd == SET_SPEED)
    {
      int value = readFirstValid();
      setMotorSpeed(value);
    }
    else if (cmd == SET_MOVE_TIME)
    {      
      const int b1 = readFirstValid();
      const int b2 = readFirstValid();
      
      int time = assembleUShort(b1, b2);
      setMoveTime(time);
        
    }
    else
    {
      resp = createNack(UNSUPPORTED_CMD); // overwrite default resp
    }
    Serial.write(resp);
  }
}
