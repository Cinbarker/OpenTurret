#include <Wire.h>

#define address 0x8
#define panStepPin 4
#define panDirPin 5
#define tiltStepPin 6
#define tiltDirPin 7
 
// LED on pin 13
const int ledPin = LED_BUILTIN; 

int minDelay = 10;
int maxDelay = 300;
long panLocation = 0;
long tiltLocation = 0;
 
byte dataArray[4];
byte panSpeed  = 0;
byte tiltSpeed = 0;
byte panDir    = 0;
byte tiltDir   = 0;
int currentDir = 0;

void setup(){
  Wire.begin(address);
  Wire.onReceive(receiveEvent); //you need to declare it in setup() to receive data from Master
  pinMode(panStepPin, OUTPUT);
  pinMode(panDirPin, OUTPUT);
  pinMode(tiltStepPin, OUTPUT);
  pinMode(tiltDirPin, OUTPUT);
  Serial.begin(9600);
}

void loop(){
  if (panDir == 0 && currentDir == 1) {
    digitalWrite(panDirPin, LOW);
    currentDir = 0;
  } 
  else if (panDir == 1 && currentDir == 0) {
    digitalWrite(panDirPin, HIGH);
    currentDir = 1;
  }

  if (panSpeed != 0) {
    int panDelay = map(panSpeed, 0, 255, maxDelay, minDelay);
    stepMotor(panStepPin, panDelay);
    
    if (panDir == 0) panLocation++;
    else panLocation--;
  }
  
//  if (tiltSpeed != 0) {
//    int tiltDelay = map(tiltSpeed, 0, 255, maxDelay, minDelay);
//    stepMotor(tiltStepPin, tiltDelay);
//  
//   if (tiltDir == 0) tiltLocation++;
//   else tiltLocation--;
//  }
//Serial.println(panSpeed, DEC);
//delay(100);
}

void stepMotor(int pin, int delayTime) {
  digitalWrite(pin, HIGH);
  delayMicroseconds(delayTime);
  digitalWrite(pin, LOW);
  delayMicroseconds(delayTime);
}

// Data Structure: dataArray[panSpeed, tiltSpeed, panDir, tiltDir] 
void receiveEvent(int howmany){ //howmany = Wire.write()executed by Master
  for(int i=0; i<howmany; i++){
    dataArray[i] = Wire.read();
    //Serial.println(dataArray[i], DEC);
  }
  panSpeed  = dataArray[1];
  tiltSpeed = dataArray[2];
  panDir    = dataArray[3];
  tiltDir   = dataArray[4];
}
