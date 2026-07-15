#include <Servo.h>

int Mq2_Pin = A0;
int Buzzer_Pin = 8;
int Fan_Pin = 6;
int Smoke_Threshold = 350;

Servo My_Servo;
int Servo_Pin = 9;

bool Smoke_Active = false;

void setup() {
  pinMode(Buzzer_Pin, OUTPUT);
  pinMode(Fan_Pin, OUTPUT);
  My_Servo.attach(Servo_Pin);
  My_Servo.write(0);
  analogWrite(Fan_Pin, 0);
  Serial.begin(9600);
  Serial.println("Gas_Smoke_Detector_Ready");
}

void loop() {
  int Gas_Value = analogRead(Mq2_Pin);
  Serial.print("Gas_Level: ");
  Serial.println(Gas_Value);

  if (Gas_Value > Smoke_Threshold) {
    Smoke_Active = true;

    Serial.println("Smoke_Detected");

    My_Servo.write(180);
    analogWrite(Fan_Pin, 255);

    tone(Buzzer_Pin, 3000);
    delay(500);
    noTone(Buzzer_Pin);
    delay(500);

  } else {
    if (Smoke_Active) {
      Serial.println("Air_Clear_Resetting");
      Smoke_Active = false;
    }

    My_Servo.write(0);
    analogWrite(Fan_Pin, 0);
    noTone(Buzzer_Pin);

    delay(500);
  }
}