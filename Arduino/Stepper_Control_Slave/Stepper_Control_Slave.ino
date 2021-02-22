#include <Wire.h>

#define address 0x8
#define panStepPin 4
#define panDirPin 5
#define tiltStepPin 6
#define tiltDirPin 7
 
// LED on pin 13
const int ledPin = LED_BUILTIN; 

// Initialize variables
int minDelay = 10;
int maxDelay = 300;

long minTilt = -900*16;
long maxTilt = 900*16;

long panLocation = 0;
long tiltLocation = 0;

byte dataArray[5];
byte panSpeed  = 0;
byte tiltSpeed = 0;
byte panDir    = 0;
byte tiltDir   = 0;
byte calibrate = 0;

int currentPanDir = 0;
int currentTiltDir = 0;

unsigned long currentMicros = 0;
unsigned long previousMicros = 0;

int state = 0;

void setup(){
  Serial.begin(9600);
  
  Wire.begin(address);
  Wire.onReceive(receiveEvent); //you need to declare it in setup() to receive data from Master

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
    int panDelay = map(panSpeed, 0, 255, maxDelay, minDelay);
    stepMotor(panStepPin, panDelay);
    
    if (panDir == 0) panLocation++;
    else panLocation--;
  }

  if (abs(panLocation/4/64000)== 1) {
    panLocation = 0;
  }

  ///// Control Tilt Mechanism /////
  
  changeDirection(tiltDirPin, tiltDir, &currentTiltDir);

  if ((tiltSpeed != 0) && ((tiltLocation >= minTilt) || (tiltDir == 0)) && ((tiltLocation <= maxTilt) || (tiltDir == 1))) {
    int tiltDelay = map(tiltSpeed, 0, 255, maxDelay, minDelay);
    stepMotor(tiltStepPin, tiltDelay);
  
   if (tiltDir == 0) tiltLocation++;
   else tiltLocation--;
  }
  
//delay(100);
}

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

void stepMotor(int pin, int delayTime) {
  currentMicros = micros();
  if (currentMicros - previousMicros >= delayTime) {
    previousMicros = currentMicros;
    if (state == LOW) {
      state = HIGH;
    } else {
      state = LOW;
      }
    digitalWrite(pin, state);
  }
}

// Data Structure: dataArray[panSpeed, tiltSpeed, panDir, tiltDir, calibrate] 
void receiveEvent(int howmany){ //howmany = Wire.write()executed by Master
  for(int i=0; i<howmany; i++){
    dataArray[i] = Wire.read();
    //Serial.println(dataArray[i], DEC);
  }
  panSpeed  = dataArray[1];
  tiltSpeed = dataArray[2];
  panDir    = dataArray[3];
  tiltDir   = dataArray[4];
  calibrate = dataArray[5];

  if (calibrate == 1) {
    panLocation = 0;
    tiltLocation = 0;
  }
  Serial.println(panLocation, DEC);
}
