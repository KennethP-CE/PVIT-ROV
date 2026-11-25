// Arduino Mega control program.
// Receives a CSV line of numeric control values over serial and sends a
// confirmation message back to the Raspberry Pi.
// Arduino Mega appears as /dev/ttyACM0 on the Raspberry Pi.

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for the serial port to connect (USB CDC)
  }
}

void loop() {
  if (Serial.available() > 0) {
    String csvLine = Serial.readStringUntil('\n');
    csvLine.trim();
    if (csvLine.length() > 0) {
      Serial.println("RECV_OK: " + csvLine);
    }
  }
}
