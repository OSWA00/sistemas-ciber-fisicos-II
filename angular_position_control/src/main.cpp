#include <Arduino.h>

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
  float_t current_position;
  float_t target_position;

  float_t proportional_gain;
  float_t derivative_gain;
  float_t last_error;

  uint32_t last_time;
  uint32_t current_time;

  uint8_t foward_pin;
  uint8_t reverse_pin;
  uint8_t pwm_channel;
} Motor_1;

/** TODO
 * [x] Read encoder
 * [x] Convert pulses to degrees
 * [x] Implement P controller on radians
 * [X] Send u to PWM
 *
 * After controller synthonization
 * [] Receive reference from external source
 */
void init_encoder(Encoder &encoder);
void init_motor(Motor &motor);
void update_encoder_state(Encoder &encoder);
float_t convert_pulses_to_radians(int32_t pulse_counter);
float_t calculate_u(Motor &motor);
void send_power(Motor &motor, float_t speed);

void setup()
{
  Serial.begin(9600);

  Encoder_1.channel_A = 0x2;
  Encoder_1.channel_B = 0XF;

  Motor_1.foward_pin = 0x4;
  Motor_1.reverse_pin = 0x17;

  Motor_1.pwm_channel = 0x0;
  Motor_1.target_position = M_PI / float_t(2.0); //!  Remove on release
  Motor_1.last_error = 0.0;

  init_encoder(Encoder_1);
  init_motor(Motor_1);
}

void loop()
{
  update_encoder_state(Encoder_1);
  // Motor_1.current_position = convert_pulses_to_radians(Encoder_1.counter);
  // send_power(Motor_1, calculate_u(Motor_1));
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
  }
  encoder.last_state_A = encoder.current_state_A;
  //! Remove on release
  Serial.print("Positon: ");
  Serial.println(encoder.counter);
}

float_t convert_pulses_to_radians(int32_t pulse_counter)
{
  uint32_t pulses_per_revolution = 630; // Change according to motor
  float_t total_radians = 2 * M_PI;
  if (pulse_counter < 0)
  {
    pulse_counter = pulses_per_revolution + pulse_counter;
  }

  uint32_t angle = total_radians * pulse_counter / pulses_per_revolution;
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
  uint8_t resolution_bits = 0x10;

  ledcSetup(motor.pwm_channel, freq, resolution_bits);
  ledcAttachPin(motor.foward_pin, motor.pwm_channel);
  ledcAttachPin(motor.reverse_pin, motor.pwm_channel);

  digitalWrite(motor.foward_pin, LOW);
  digitalWrite(motor.reverse_pin, LOW);

  motor.last_time = millis();

  motor.proportional_gain = 0.1;
  motor.derivative_gain = 0.01;
}

// void send_power(Motor &motor, float_t u)
// {
//   if (motor.foward)
//   {
//     analogWrite(motor.foward_pin, HIGH);
//     digitalWrite(motor.reverse_pin, LOW);
//   }
//   else
//   {
//     digitalWrite(motor.foward_pin, LOW);
//     digitalWrite(motor.reverse_pin, HIGH);
//   }

//   uint32_t duty_cycle = map(u, 0x0, 0x1, 0x0, 0xFFFF); // 16 bit PWM

//   ledcWrite(motor.pwm_channel, duty_cycle);
// }
