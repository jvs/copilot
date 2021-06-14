import pwmio
import time


class Buzzer:
    def __init__(self, pin, duty_cycle=2 ** 8):
        self._pin = pin
        self._out = None
        self._duty_cycle = duty_cycle

    def buzz(self, frequency):
        if self._out is not None:
            if frequency > 0:
                self._out.frequency = frequency
            else:
                self._out.duty_cycle = 0
            return

        if frequency <= 0:
            return

        self._out = pwmio.PWMOut(
            pin=self._pin,
            duty_cycle=self._duty_cycle,
            frequency=frequency,
            variable_frequency=True,
        )

    def stop(self):
        if self._out is not None:
            self._out.duty_cycle = 0
            self._out.deinit()
            self._out = None

    def play_tune(self, *frequencies):
        for frequency in frequencies:
            self.buzz(frequency)
            time.sleep(0.1)
        self.stop()
