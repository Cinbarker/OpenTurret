#include <Wire.h>

// Define constants
#define address 0x8 // I2C address of this slave device
#define panStepPin 4
#define panDirPin 5
#define tiltStepPin 6
#define tiltDirPin 7

// Initialize variables
byte data[5]; 
byte panSpeed = 0, tiltSpeed = 0, panDir = 0, tiltDir = 0, calibrate = 0;

// Configure stepper motor speed limits (lower minDelay => higher maxSpeed)
int minDelay = 40;
int maxDelay = 300;

//
long minTilt = -1800*16;
long maxTilt = 2000*16;

long panLocation = 0, tiltLocation = 0;

int currentPanDir = 0, currentTiltDir = 0;

unsigned long currentPanMicros = 0;
unsigned long previousPanMicros = 0;
unsigned long currentTiltMicros = 0;
unsigned long previousTiltMicros = 0;

int panState = 0, tiltState = 0;
int panDelay = 0, tiltDelay = 0;


void setup(){
  Serial.begin(9600);
  
  Wire.begin(address);
  Wire.onReceive(receiveEvent); // Declared in setup() to receive data from Master

  // Set in/out mode of pins
  pinMode(panStepPin, OUTPUT);
  pinMode(panDirPin, OUTPUT);
  pinMode(tiltStepPin, OUTPUT);
  pinMode(tiltDirPin, OUTPUT);
}

void loop(){

  ///// Control Pan Mechanism /////
  
  changeDirection(panDirPin, panDir, &currentPanDir);

  if (panSpeed != 0) {
    stepMotor(panStepPin, panDelay, &currentPanMicros, &previousPanMicros, &panState, panDir, &panLocation);
  }

  // Reset 128000 is one full rotation
  if (abs(panLocation/128000)== 1) { 
    panLocation = 0;
  }

  ///// Control Tilt Mechanism /////
  
  changeDirection(tiltDirPin, tiltDir, &currentTiltDir);

  if ((tiltSpeed != 0) && ((tiltLocation >= minTilt) || (tiltDir == 0)) && ((tiltLocation <= maxTilt) || (tiltDir == 1))) {
    
    stepMotor(tiltStepPin, tiltDelay, &currentTiltMicros, &previousTiltMicros, &tiltState, tiltDir, &tiltLocation);
  }
}

// Function for writing to the dir pin when motor direction is changed
void changeDirection(int dirPin, int dir, int* currentDir) {
  if (dir == 0 && *currentDir == 1) {
    digitalWrite(dirPin, LOW);
    *currentDir = 0;
  } 
  else if (dir == 1 && *currentDir == 0) {
    digitalWrite(dirPin, HIGH);
    *currentDir = 1;
  }
}

// Function for stepping the motor without incurring delays in the main loop
void stepMotor(int pin, int delayTime, long* currentMicros, long* previousMicros, int* state, byte dir, long* location) {
  *currentMicros = micros();
  if (*currentMicros - *previousMicros >= delayTime) {
    *previousMicros = *currentMicros;
    if (*state == LOW) {
      *state = HIGH;
    } else {
      *state = LOW;
      }
    digitalWrite(pin, *state);
    if (dir == 0) *location = *location+1;
    else *location= *location-1;
  }
}

// Function for recieving I2C data
// Data Structure: dataArray[panSpeed, tiltSpeed, panDir, tiltDir, calibrate] 
void receiveEvent(int howmany){ //howmany = Wire.write()executed by Master
  for(int i=0; i<howmany; i++){
    data[i] = Wire.read();
    //Serial.println(dataArray[i], DEC);
  }
  panSpeed  = data[1];
  tiltSpeed = data[2];
  panDir    = data[3];
  tiltDir   = data[4];
  calibrate = data[5];
  tiltDelay = map(tiltSpeed, 0, 255, maxDelay, minDelay);
  panDelay = map(panSpeed, 0, 255, maxDelay, minDelay);

  if (calibrate == 1) {
    panLocation = 0;
    tiltLocation = 0;
  }
  //Serial.println(panSpeed, DEC);
}
