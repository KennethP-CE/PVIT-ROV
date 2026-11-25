// Arduino Mega program: receives a numeric CSV line over Serial and sends
// back a confirmation message to the Raspberry Pi.
//
// CSV format sent by the Pi (no strings, numeric values):
//   left_x,left_y,right_x,right_y,a_button,b_button,x_button,y_button,
//   left_button,right_button
//
// Confirmation reply format:
//   CSV_RECV: n=<field_count> line=<csv_line>

#include <string.h>

constexpr size_t kMaxLineLen = 128;  // longest CSV line we accept
constexpr size_t kMaxFields = 32;    // safety cap while parsing

char lineBuf[kMaxLineLen];

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for the serial port to connect (USB CDC)
  }
  Serial.println("ARD_READY");
}

// Parse every numeric field in the line, then confirm receipt with a count
// and the original line. `echo` is a copy used for parsing because strtok
// inserts NUL bytes; `line` itself stays intact for the reply.
void confirmReceipt(const char* line, size_t len) {
  char echo[kMaxLineLen];
  size_t copyLen = len < kMaxLineLen ? len : kMaxLineLen - 1;
  memcpy(echo, line, copyLen);
  echo[copyLen] = '\0';

  int fields = 0;
  char* token = strtok(echo, ",");
  while (token != NULL && fields < kMaxFields) {
    (void)strtod(token, nullptr);  // validate: parses a leading number
    token = strtok(nullptr, ",");
    fields++;
  }

  Serial.print("CSV_RECV: n=");
  Serial.print(fields);
  Serial.print(" line=");
  Serial.println(line);
}

void loop() {
  static size_t idx = 0;
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      if (idx > 0 && idx < kMaxLineLen) {
        lineBuf[idx] = '\0';
        confirmReceipt(lineBuf, idx);
      }
      idx = 0;
    } else if (idx < kMaxLineLen - 1) {
      lineBuf[idx++] = c;
    }
    // Bytes beyond the line buffer are dropped.
  }
}
