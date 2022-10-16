#include <Arduino.h>
#include "control_parameters.h"
#include "pins.h"

struct Encoder
{
  uint8_t channel_A;
  uint8_t channel_B;
  int32_t counter;
  uint32_t last_state_A;
  uint32_t current_state_A;
  uint32_t current_state_B;

} Encoder_1;

struct Motor
{
  uint32_t current_position;
  uint32_t target_position;
  uint8_t pwm_pin;
} Motor_1;

/** TODO
 * [x] Read encoder
 * [] Convert pulses to degrees
 * [] Implement P controller on degrees
 * [] Send u to PWM
 */
void init_encoder(Encoder &encoder);
void update_encoder_state(Encoder &encoder);
uint32_t convert_pulses_to_degrees(int32_t pulse_counter);

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
  Motor_1.current_position = convert_pulses_to_degrees(Encoder_1.counter);
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

uint32_t convert_pulses_to_degrees(int32_t pulse_counter)
{
  uint32_t pulses_per_revolution = 630; // Change according to motor
  uint32_t total_degrees = 360;
  if (pulse_counter < 0)
  {
    pulse_counter = pulses_per_revolution + pulse_counter;
  }

  uint32_t angle = total_degrees * pulse_counter / pulses_per_revolution;
  return angle;
}