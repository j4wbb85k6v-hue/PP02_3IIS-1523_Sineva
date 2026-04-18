// Master Code (Arduino Uno)
// Считывает потенциометр на A0 и отправляет значение на Slave (адрес 8)

#include <Wire.h>

#define SLAVE_ADDRESS 8
#define POT_PIN A0

void setup() {
  Wire.begin(); // Запуск I2C шины в режиме Master
  Serial.begin(9600);
  Serial.println("Master Ready");
}

void loop() {
  int sensorValue = analogRead(POT_PIN); // Чтение 0-1023
  byte valueToSend = map(sensorValue, 0, 1023, 0, 255); // Упаковываем в 1 байт для простоты

  Wire.beginTransmission(SLAVE_ADDRESS);
  Wire.write(valueToSend); 
  Wire.endTransmission();

  Serial.print("Sent: ");
  Serial.println(sensorValue);
  
  delay(100); // Небольшая задержка
}
1.3. Код Slave (Arduino Nano)
cpp
// Slave Code (Arduino Nano)
// Принимает 1 байт по I2C (адрес 8). Включает LED на D13 если значение > 127

#include <Wire.h>

#define SLAVE_ADDRESS 8
#define LED_PIN 13

volatile byte receivedData = 0;

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  
  Wire.begin(SLAVE_ADDRESS); // Запуск в режиме Slave с адресом 8
  Wire.onReceive(receiveEvent); // Регистрация обработчика прерывания
  
  Serial.begin(9600);
  Serial.println("Slave Ready. Address: 8");
}

void loop() {
  // Критическое условие: включаем по порогу (512 -> соответствует байту 127)
  if (receivedData > 127) { 
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
  
  Serial.print("Received: ");
  Serial.println(receivedData);
  delay(50);
}

// Функция вызывается автоматически при получении данных от Master
void receiveEvent(int howMany) {
  if (Wire.available()) {
    receivedData = Wire.read(); // Читаем 1 байт
  }
}

