/*
 * This sketch was designed for Arduino Unos to ask as a real time slave of a Raspberry Pi. 
 * If using another board, the things that must mbe changed are:
 *    - SDA and SCL pins for I2C bus (this is a hardware change, check Wire library for more info)
 *    - PORT registers will most likely be different. For more info: https://www.arduino.cc/en/Reference/PortManipulation
 */


#include <Wire.h>

// Define constants
#define address 0x8 // I2C address of this slave device
#define panStepPin 4 //B00010000 // Pin D4
#define panDirPin 5 // B00100000 // Pin D5
#define tiltStepPin 6 //B01000000 // Pin D6
#define tiltDirPin B10000000 // Pin D7
#define laserPin 9 //B00000100 // Pin D9

// Initialize variables
byte data[8];
byte panSpeed = 0, tiltSpeed = 0, panDir = 0, tiltDir = 0, calibrate = 0, laserPower = 0, laserFire = 0, returnHome = 0;

// Configure stepper motor speed limits (lower minDelay => higher maxSpeed)
int minDelay = 40;
int maxDelay = 300;

//
long minTilt = -1800 * 16;
long maxTilt = 2000 * 16;

long panLocation = 0, tiltLocation = 0;

byte currentPanDir = 0, currentTiltDir = 0;

unsigned long currentPanMicros = 0;
unsigned long previousPanMicros = 0;
unsigned long currentTiltMicros = 0;
unsigned long previousTiltMicros = 0;

byte panState = 0, tiltState = 0;
int panDelay = 0, tiltDelay = 0;


void setup() {
  Serial.begin(9600);
  pinMode(A5, OUTPUT);
  digitalWrite(A5, LOW);
  // Set in/out mode of pins
  pinMode(panStepPin, OUTPUT);
  pinMode(panDirPin, OUTPUT);
  pinMode(tiltStepPin, OUTPUT);
  pinMode(tiltDirPin, OUTPUT);
  pinMode(laserPin, OUTPUT);

  Wire.begin(address);
  Wire.onReceive(receiveEvent); // Declared in setup() to receive data from Master
}

void loop() {

  if (laserFire == 1) {
    //PORTB |= laserPort;
    digitalWrite(laserPin, HIGH);
    delay(10);
    //PORTB &= !laserPort;
    digitalWrite(laserPin, LOW);
    laserFire = 0;
  } else {
    analogWrite(laserPin, laserPower/8);
  }

  ///// Control Pan Mechanism /////

  if (panSpeed != 0) {
    //if (panDir == 1) PORTD |= panDirPin;
    //else PORTD &= !panDirPin;
    digitalWrite(panDirPin, panDir);
    stepMotor(panStepPin, panDelay, &currentPanMicros, &previousPanMicros, &panState, panDir, &panLocation);
  }

  // Reset 128000 is one full rotation
  if (abs(panLocation / 128000) == 1) {
    panLocation = 0;
  }

  ///// Control Tilt Mechanism /////

  if ((tiltSpeed != 0) && ((tiltLocation >= minTilt) || (tiltDir == 0)) && ((tiltLocation <= maxTilt) || (tiltDir == 1))) {
    if (tiltDir == 1) PORTD |= tiltDirPin;
    else PORTD &= !tiltDirPin;
    stepMotor(tiltStepPin, tiltDelay, &currentTiltMicros, &previousTiltMicros, &tiltState, tiltDir, &tiltLocation);
  }
}

// Function for stepping the motor without incurring delays in the main loop
void stepMotor(int pin, int delayTime, long* currentMicros, long* previousMicros, byte* state, byte dir, long* location) {
  *currentMicros = micros();
  if (*currentMicros - *previousMicros >= delayTime) {
    *previousMicros = *currentMicros;
    if (*state == LOW) {
      *state = HIGH;
    } else {
      *state = LOW;
    }
    digitalWrite(pin, *state);
    if (dir == 0) *location = *location + 1;
    else *location = *location - 1;
  }
}

// Function for recieving I2C data
// Data Structure: dataArray[panSpeed, tiltSpeed, panDir, tiltDir, calibrate, laserPower, laserFire]
void receiveEvent(int howmany) { //howmany = Wire.write() executed by Master
  for (int i = 0; i < howmany; i++) {
    data[i] = Wire.read();
    //Serial.println(dataArray[i], DEC);
  }
  panSpeed   = data[1];
  tiltSpeed  = data[2];
  panDir     = data[3];
  tiltDir    = data[4];
  calibrate  = data[5];
  laserPower = data[6];
  laserFire  = data[7];
  returnHome = data[8];
  tiltDelay = map(tiltSpeed, 0, 255, maxDelay, minDelay);
  panDelay = map(panSpeed, 0, 255, maxDelay, minDelay);

  if (calibrate == 1) {
    panLocation = 0;
    tiltLocation = 0;
    calibrate = 0;
  }
  Serial.print(laserPower, DEC);
  Serial.print("\t");
  Serial.println(laserFire, DEC);
}
