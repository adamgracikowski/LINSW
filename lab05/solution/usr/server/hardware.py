import asyncio
from abc import ABC, abstractmethod
from typing import Optional, Dict
import time

import UniversalGPIO.GPIO as GPIO

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
        debounce_time: float = 0.05,
    ):
        self._queue: asyncio.Queue[ProductCategory] = asyncio.Queue()
        self._debounce_time = debounce_time

        self._input_pins: Dict[GPIO.Pin, ProductCategory] = {}
        for category, pin_num in progress_pins.items():
            pin = GPIO.setup(pin_num, GPIO.INPUT)
            self._input_pins[pin] = category

        self._failure_pin = GPIO.setup(failure_pin, GPIO.INPUT)
        self._input_pins[self._failure_pin] = ProductCategory.F

        self._led_pins: Dict[DiodeColors, GPIO.Pin] = {}
        for color, pin_num in diode_pins.items():
            pin = GPIO.setup(pin_num, GPIO.OUTPUT, initial_state=GPIO.LOW)
            self._led_pins[color] = pin

        self._polling_task: Optional[asyncio.Task] = None
        self._disposed = False

    async def start_polling(self):
        async def poll():
            last_pressed = {}

            while not self._disposed:
                now = time.monotonic()
                for pin, category in self._input_pins.items():
                    try:
                        val = pin.read()
                    except Exception as e:
                        print(f"[ERROR] Reading pin: {e}")
                        continue

                    if val == 0:
                        last_time = last_pressed.get(pin, 0)
                        if now - last_time > self._debounce_time:
                            print(f"[BUTTON] Press detected for category {category.value}")
                            await self._queue.put(category)
                            last_pressed[pin] = now
                    else:
                        last_pressed[pin] = 0

                await asyncio.sleep(0.05)

        self._polling_task = asyncio.create_task(poll())

    async def detect_progress_category(self) -> Optional[ProductCategory]:
        return await self._queue.get()

    def set_diode_state(self, color: DiodeColors, on: bool):
        pin = self._led_pins.get(color)
        if pin is None:
            return
        try:
            if on:
                pin.high()
            else:
                pin.low()
            print(f"[DIODE] {color.value.upper()} set to {'ON' if on else 'OFF'}.")
        except Exception as e:
            print(f"[ERROR] Setting diode {color.value} state: {e}")

    def turn_off_all_diodes(self):
        for color, pin in self._led_pins.items():
            try:
                pin.low()
            except Exception as e:
                print(f"[ERROR] Turning off diode {color.value}: {e}")
        print("[DIODE] All LEDs turned OFF.")

    def dispose(self):
        self._disposed = True
        if self._polling_task:
            self._polling_task.cancel()

        for pin in self._input_pins.keys():
            try:
                pin.cleanup()
            except Exception as e:
                print(f"[WARN] Cleanup input pin failed: {e}")

        for pin in self._led_pins.values():
            try:
                pin.low()
                pin.cleanup()
            except Exception as e:
                print(f"[WARN] Cleanup LED pin failed: {e}")

        print("UniversalGPIO resources disposed.")