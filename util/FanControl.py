# import RPi.GPIO as GPIO
import wiringpi as GPIO
import time
import logging
import signal
import sys
import os

logger = logging.getLogger(__name__)

fan_pin = 35
pwm_chip = 4
pwm_channel = 1
period = 10000000  # Period in nanoseconds (10ms)


class Fan:
    def __init__(self, initial_speed=40) -> None:
        self.speed = initial_speed

        try:
            GPIO.wiringPiSetup()

            """This is required because there seems to be a bug at the time of development where WiringPi cannot re-gain control
            of a PWM pin AFTER the service has ended for the first time. Unexporting provides the same behavior."""
            if not os.path.exists(f"/sys/class/pwm/pwmchip{pwm_chip}/pwm{pwm_channel}"):
                # Export the PWM channel
                with open(
                    f"/sys/class/pwm/pwmchip{pwm_chip}/export", "w"
                ) as export_file:
                    export_file.write(str(pwm_channel))

            # Set the PWM period and duty cycle
            with open(
                f"/sys/class/pwm/pwmchip{pwm_chip}/pwm{pwm_channel}/period", "w"
            ) as period_file:
                period_file.write(str(period))

            with open(
                f"/sys/class/pwm/pwmchip{pwm_chip}/pwm{pwm_channel}/duty_cycle", "w"
            ) as duty_cycle_file:
                duty_cycle_file.write(str(self.speed * 100000))

            # Enable the PWM channel
            with open(
                f"/sys/class/pwm/pwmchip{pwm_chip}/pwm{pwm_channel}/enable", "w"
            ) as enable_file:
                enable_file.write("1")

        except Exception:
            logger.info(f"Failed to start Fan on pin {fan_pin}")
            raise
        else:
            logger.info(f"Successfully started Fan on pin {fan_pin}")

    def speed_to_duty_cycle(self, speed):
        return speed * 100000

    def setFanPwm(self, speed):
        logger.info(f"Setting fan speed to {speed}")
        if 40 <= speed <= 100 or speed == 0:
            duty_cycle = self.speed_to_duty_cycle(speed)

            with open(
                f"/sys/class/pwm/pwmchip{pwm_chip}/pwm{pwm_channel}/duty_cycle", "w"
            ) as duty_cycle_file:
                duty_cycle_file.write(str(duty_cycle))
        else:
            logger.error(
                f"Invalid value {speed}. Fan only accepts pwm width from 40-100. Skipping..."
            )

    # Setup the GPIO cleanup on exit for sigterm
    @staticmethod
    def handle_exit(signal_number, stack):
        # Log the shutdown and raise SystemExit
        logging.info("Signal {} received, shutting down".format(signal_number))

        # Disable the PWM channel
        with open(
            f"/sys/class/pwm/pwmchip{pwm_chip}/pwm{pwm_channel}/enable", "w"
        ) as enable_file:
            enable_file.write("0")

        sys.exit(0)


if __name__ == "__main__":
    fan = Fan()

    # Handle exits properly
    signal.signal(signal.SIGTERM, fan.handle_exit)
    signal.signal(signal.SIGINT, fan.handle_exit)

    while True:
        try:
            time.sleep(1)

        except SystemExit:
            break
