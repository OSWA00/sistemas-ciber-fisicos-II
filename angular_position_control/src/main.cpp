#include <Arduino.h>
#include "control_parameters.h"
#include "pins.h"

struct Encoder
{
  uint8_t channel_A;
  uint8_t channel_B;
  uint32_t counter;
  uint32_t last_state_A;
  uint32_t current_state_A;
  uint32_t current_state_B;
} Encoder_1;

/** TODO
 * Read encoder check
 * Convert pulses to degrees
 * Implement P controller on degrees
 * Send u to PWM
 */

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(115200);

  Encoder_1.channel_A = 0x1;
  Encoder_1.channel_B = 0X2;

  init_encoder(Encoder_1);
}

void loop()
{
  // put your main code here, to run repeatedly:
  update_encoder_state(Encoder_1);
}

void init_encoder(Encoder &encoder)
{
  pinMode(encoder.channel_A, INPUT);
  pinMode(encoder.channel_B, INPUT);
  encoder.counter = 0;
  encoder.last_state_A = digitalRead(encoder.channel_A);
}

void update_encoder_state(Encoder &encoder)
{
  encoder.current_state_A = digitalRead(encoder.channel_A);
  if (encoder.current_state_A != encoder.last_state_A)
  {
    encoder.current_state_B = digitalRead(encoder.channel_B);
    if (encoder.current_state_B != encoder.current_state_A)
    {
      encoder.counter++;
    }
    else
    {
      encoder.counter--;
    }
    //! Remove on release
    Serial.print("Positon: ");
    Serial.println(encoder.counter);
  }
  encoder.last_state_A = encoder.current_state_A;
}
