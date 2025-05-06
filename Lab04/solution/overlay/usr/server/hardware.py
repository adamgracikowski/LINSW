import asyncio
from abc import ABC, abstractmethod
from typing import Optional, Dict

# import RPi.GPIO as GPIO

from enums import ProductCategory, DiodeColors

enfoce_input_float = 0

class HardwareModule(ABC):
    @abstractmethod
    async def detect_progress_category(self) -> Optional[ProductCategory]:
        """Detect key presses or GPIO events for progress reporting."""
        pass

    @abstractmethod
    def set_diode_state(self, color: DiodeColors, on: bool):
        """Set the state (ON/OFF) of the specified diode."""
        pass

    @abstractmethod
    def turn_off_all_diodes(self):
        """Turn off all diodes."""
        pass

    @abstractmethod
    def dispose(self):
        """Dispose or clean up resources when no longer needed."""
        pass

class KeyboardModule(HardwareModule):
    def __init__(self):
        self.diode_states = {color: False for color in DiodeColors}

    async def detect_progress_category(self) -> Optional[ProductCategory]:
        key = input("Press A, B, C or F then Enter: ").strip().upper()
        return {
            'A': ProductCategory.A,
            'B': ProductCategory.B,
            'C': ProductCategory.C,
            'F': ProductCategory.F
        }.get(key)

    def set_diode_state(self, color: DiodeColors, on: bool):
        self.diode_states[color] = on
        state = "ON" if on else "OFF"
        print(f"[DIODE] The {color.value.upper()} diode is now {state}.", flush=True)

    def turn_off_all_diodes(self):
        for color in DiodeColors:
            self.set_diode_state(color, on=False)

    def dispose(self):
        print("Disposing of KeyboardModule resources.")


class GPIOModule(HardwareModule):
    def __init__(
        self,
        progress_pins: Dict[ProductCategory, int],
        failure_pin: int,
        diode_pins: Dict[DiodeColors, int],
        bounce_time: float = 0.05
    ):
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setwarnings(False)

        # self._queue: asyncio.Queue[ProductCategory] = asyncio.Queue()
        # self._loop = asyncio.get_event_loop()

        # self._input_pins = []
        # for category, pin in progress_pins.items():
        #     self._setup_input(pin, category, bounce_time)

        # self._setup_input(failure_pin, ProductCategory.F, bounce_time)

        # self._led_pins = diode_pins
        # for pin in diode_pins.values():
        #     GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
        pass

    def _setup_input(self, pin: int, category: ProductCategory, bounce: float):
        # GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # self._input_pins.append(pin)
        # GPIO.add_event_detect(
        #     pin,
        #     GPIO.FALLING,
        #     callback=lambda channel, cat=category: self._handle_press(cat),
        #     bouncetime=int(bounce * 1000)
        # )
        pass

    def _handle_press(self, category: ProductCategory):
        self._loop.call_soon_threadsafe(self._queue.put_nowait, category)

    async def detect_progress_category(self) -> Optional[ProductCategory]:
        return await self._queue.get()

    def set_diode_state(self, color: DiodeColors, on: bool):
        # pin = self._led_pins.get(color)
        # if pin is None:
        #     return
        # GPIO.output(pin, GPIO.HIGH if on else GPIO.LOW)
        print(f"[DIODE] {color.value.upper()} set to {'ON' if on else 'OFF'}.", flush=True)

    def turn_off_all_diodes(self):
        # for pin in self._led_pins.values():
        #     GPIO.output(pin, GPIO.LOW)
        print("[DIODE] All LEDs turned OFF.", flush=True)

    def dispose(self):
        # for pin in self._input_pins:
        #     GPIO.remove_event_detect(pin)
        # for pin in self._led_pins.values():
        #     GPIO.output(pin, GPIO.LOW)
        # GPIO.cleanup()
        print("GPIO resources disposed.")