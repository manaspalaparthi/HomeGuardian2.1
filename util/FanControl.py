import os
import time


class FanControl:
    def __init__(self, fan_pin=35, pwm_chip=4, pwm_channel=1, period=10000000):
        self.fan_pin = fan_pin  # Not used directly here
        self.pwm_chip = pwm_chip
        self.pwm_channel = pwm_channel
        self.period = period  # Period in nanoseconds (10ms)

        # Paths to the PWM chip and channel
        self.pwm_path = f"/sys/class/pwm/pwmchip{self.pwm_chip}/pwm{self.pwm_channel}"

        # Export the PWM channel if not already done
        if not os.path.exists(self.pwm_path):
            with open(f"/sys/class/pwm/pwmchip{self.pwm_chip}/export", "w") as f:
                f.write(str(self.pwm_channel))
            time.sleep(1)  # Wait for the channel to be exported

        # Set the PWM period
        with open(f"{self.pwm_path}/period", "w") as f:
            f.write(str(self.period))

        # Initially disable the PWM
        self.disable_pwm()

    def enable_pwm(self):
        """Enables the PWM signal (turn the fan on)."""
        with open(f"{self.pwm_path}/enable", "w") as f:
            f.write("1")
        print("Fan PWM enabled")

    def disable_pwm(self):
        """Disables the PWM signal (turn the fan off)."""
        with open(f"{self.pwm_path}/enable", "w") as f:
            f.write("0")
        print("Fan PWM disabled")

    def set_duty_cycle(self, duty_cycle_ns):
        """Sets the duty cycle in nanoseconds."""
        with open(f"{self.pwm_path}/duty_cycle", "w") as f:
            f.write(str(duty_cycle_ns))
        print(f"Duty cycle set to {duty_cycle_ns} ns")

    def fan_on(self):
        """Turns the fan on with a default duty cycle (50% speed)."""
        self.set_duty_cycle(self.period // 2)  # 50% duty cycle
        self.enable_pwm()

    def fan_off(self):
        """Turns the fan off by disabling PWM."""
        self.disable_pwm()


if __name__ == '__main__':
    fan = FanControl(fan_pin=35, pwm_chip=4, pwm_channel=1, period=10000000)

    # Turn the fan on
    fan.fan_on()
    time.sleep(5)  # Fan stays on for 5 seconds

    # Turn the fan off
    fan.fan_off()
