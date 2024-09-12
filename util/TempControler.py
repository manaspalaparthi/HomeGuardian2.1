# This module is intended for use with RPI4 versions of the Homeguardian device with a fan.

# As this is a critical service which once an instance is initiated, it will manage itself

# Import native libs
import os, subprocess

# Import non-native libs
import gpiozero

class RPI4_THERMAL():
    def __init__(self, sp=75, fan_pin=12):

        self.sp = sp
        self.fan_pin = fan_pin
        self.fan_duty_cycle = 0.4

        # Check which scaling governor is being used, it should be performance
        results = subprocess.run('cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor', shell=True,
                                 capture_output=True, text=True).stdout.split('\n')[:-1]

        for idx, result in enumerate(results):
            if result != 'performance':
                subprocess.run('echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor',
                               shell=True)

        # Check which frequencies are available
        results = subprocess.run('cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_available_frequencies', shell=True,
                                 capture_output=True, text=True).stdout.split('\n')[:-1]
        self.clk_freqencies = results[-1].split(' ')[:-1]
        self.clk_freq_idx = len(self.clk_freqencies) - 1

        # Start by setting the frequency to maximum on the cores
        try:
            subprocess.run(
                f'echo {self.clk_freqencies[self.clk_freq_idx]} | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq',
                shell=True)
            self.cur_frequencies = subprocess.run('cat /sys/devices/system/cpu/cpu*/cpufreq/cpuinfo_cur_freq',
                                                  shell=True, capture_output=True, text=True).stdout.split('\n')[:-1]
            self.status = True
        except:
            self.status = False

        # Set up fan
        self.fan_pwm = gpiozero.PWMOutputDevice(pin=self.fan_pin, active_high=True, initial_value=0)

    def check_temp(self):
        zone0, zone1 = self.read_temp()
        if zone0 is not None:
            if zone0 > self.sp:
                freq = self.reduce_clk_freq()
            else:
                freq = self.increase_clk_freq()
        return zone0, zone1, freq

    def read_temp(self):
        # Get temperature from both thermal zones
        try:
            f = open('/sys/class/thermal/thermal_zone0/temp')  # SoC zone 0
            zone0 = int(f.read().strip('\n')) / 1000
            f.close()
            return zone0, 0
        except:
            return None, None

    def reduce_clk_freq(self):
        self.set_fan_speed()
        if self.clk_freq_idx > 0:
            self.clk_freq_idx -= 1
            try:
                subprocess.run(
                    f'echo {self.clk_freqencies[self.clk_freq_idx]} | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq',
                    shell=True)
                self.cur_frequencies = subprocess.run('cat /sys/devices/system/cpu/cpu*/cpufreq/cpuinfo_cur_freq',
                                                      shell=True, capture_output=True, text=True).stdout.split('\n')[
                                       :-1]
                return self.cur_frequencies
            except:
                return None
        return self.cur_frequencies

    def increase_clk_freq(self):
        if self.clk_freq_idx < len(self.clk_freqencies) - 1:
            self.clk_freq_idx += 1
            try:
                subprocess.run(
                    f'echo {self.clk_freqencies[self.clk_freq_idx]} | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq',
                    shell=True)
                self.cur_frequencies = subprocess.run('cat /sys/devices/system/cpu/cpu*/cpufreq/cpuinfo_cur_freq',
                                                      shell=True, capture_output=True, text=True).stdout.split('\n')[
                                       :-1]
                return self.cur_frequencies
            except:
                return None
        return self.cur_frequencies

    def set_fan_speed(self, duty_cycle=0.4):
        try:
            self.fan_pwm.value = duty_cycle
            return duty_cycle
        except:
            return 0


# This is a test module for the thermal manager. It will monitor the temperature and if it goes over a

# specified set point it will reduce the clock frequency of the CPU

if __name__ == "__main__":

    import time

    thermal = RPI4_THERMAL()

    thermal.set_fan_speed(0.3)
    
    while True:
        thermal.check_temp()
        print(thermal.cur_frequencies)
        time.sleep(10)
      

