#include <Arduino.h>

struct Encoder
{
  uint8_t channel_A;
  uint8_t channel_B;
  int32_t counter;
} Encoder_1;

struct Motor
{
  float_t current_position;
  float_t target_position;

  float_t proportional_gain;
  float_t derivative_gain;
  float_t last_error;

  uint32_t last_time;
  uint32_t current_time;

  uint8_t foward_pin;
  uint8_t reverse_pin;
  uint8_t pwm_channel_foward;
  uint8_t pwm_channel_reverse;
} Motor_1;

void init_encoder(Encoder &encoder);
void init_motor(Motor &motor);
void encoder_1_ISR_handler();
float_t convert_pulses_to_radians(int32_t pulse_counter);
float_t calculate_u(Motor &motor);
void send_power(Motor &motor, float_t speed);

void setup()
{
  Serial.begin(9600);

  Encoder_1.channel_A = 0x2;
  Encoder_1.channel_B = 0XF;

  Motor_1.foward_pin = 0x17;
  Motor_1.reverse_pin = 0x4;

  Motor_1.pwm_channel_foward = 0x0;
  Motor_1.pwm_channel_reverse = 0x1;
  Motor_1.target_position = M_PI; //!  Remove on release
  Motor_1.last_error = 0.0;

  init_encoder(Encoder_1);
  attachInterrupt(digitalPinToInterrupt(Encoder_1.channel_A), encoder_1_ISR_handler, RISING);

  init_motor(Motor_1);
}

void loop()
{
  Motor_1.current_position = convert_pulses_to_radians(Encoder_1.counter);
  send_power(Motor_1, calculate_u(Motor_1));
}

void init_encoder(Encoder &encoder)
{
  pinMode(encoder.channel_A, INPUT_PULLUP);
  pinMode(encoder.channel_B, INPUT);
  encoder.counter = 0x0;
}

float_t convert_pulses_to_radians(int32_t pulse_counter)
{
  float_t pulses_per_revolution = 630.0; // Change according to motor
  float_t total_radians = 2.0 * M_PI;
  float_t angle = total_radians * pulse_counter / pulses_per_revolution;
  return angle;
}

float_t calculate_u(Motor &motor)
{
  motor.current_time = millis();
  uint32_t delta_time = motor.current_time - motor.last_time;
  motor.last_time = motor.current_time;

  float_t angle_error = motor.current_position - motor.target_position;
  float_t derivative_error = angle_error - motor.last_error / delta_time;
  motor.last_error = angle_error;

  float_t u = motor.proportional_gain * angle_error + motor.derivative_gain * derivative_error;
  if (u > float_t(1.0))
  {
    u = 1.0;
  }
  if (u < float_t(-1.0))
  {
    u = -1.0;
  }
  return u;
}

void init_motor(Motor &motor)
{
  pinMode(motor.foward_pin, OUTPUT);
  pinMode(motor.reverse_pin, OUTPUT);

  uint32_t freq = 0x3E8;
  uint8_t resolution_bits = 0x8;

  ledcSetup(motor.pwm_channel_foward, freq, resolution_bits);
  ledcSetup(motor.pwm_channel_reverse, freq, resolution_bits);

  ledcAttachPin(motor.foward_pin, motor.pwm_channel_foward);
  ledcAttachPin(motor.reverse_pin, motor.pwm_channel_reverse);

  digitalWrite(motor.foward_pin, LOW);
  digitalWrite(motor.reverse_pin, LOW);

  motor.last_time = millis();

  motor.proportional_gain = 0.1;
  motor.derivative_gain = 0.1;
}

void send_power(Motor &motor, float_t u)
{

  if (u > 0) // Reverse
  {
    uint32_t duty_cycle = u * 255;
    digitalWrite(motor.foward_pin, LOW);
    ledcWrite(motor.pwm_channel_reverse, duty_cycle);
  }
  else
  {
    uint32_t duty_cycle = -u * 255;
    digitalWrite(motor.reverse_pin, LOW);
    ledcWrite(motor.pwm_channel_foward, duty_cycle);
  }
}

void encoder_1_ISR_handler()
{
  if (digitalRead(Encoder_1.channel_B) == LOW)
  {
    Encoder_1.counter++;
  }
  else
  {
    Encoder_1.counter--;
  }
}
