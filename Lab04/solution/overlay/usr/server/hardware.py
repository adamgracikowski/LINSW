import asyncio
from abc import ABC, abstractmethod
from typing import Optional, Dict
import time
from functools import partial

import pigpio

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
        # Initialize pigpio and connect to daemon
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise RuntimeError("Could not connect to pigpio daemon")

        # Asyncio queue for GPIO events
        self._queue: asyncio.Queue[ProductCategory] = asyncio.Queue()
        self._callbacks = []

        # Configure GPIO inputs with pull-up and debounce
        # For pigpio, setting the mode implies pull-up/down configuration
        for category, pin in progress_pins.items():
            self.pi.set_mode(pin, pigpio.INPUT)
            self.pi.set_pull_up_down(pin, pigpio.PUD_UP)
            self.pi.set_glitch_filter(pin, int(bounce_time * 1_000_000))
            # Register a callback that debounces in handler
            cb = self.pi.callback(
                pin,
                pigpio.FALLING_EDGE,
                partial(self._on_button_event, category)
            )
            self._callbacks.append(cb)

        # Failure button setup
        self.pi.set_mode(failure_pin, pigpio.INPUT)
        self.pi.set_pull_up_down(failure_pin, pigpio.PUD_UP)
        self.pi.set_glitch_filter(failure_pin, int(bounce_time * 1_000_000))
        cb_fail = self.pi.callback(
            failure_pin,
            pigpio.FALLING_EDGE,
            partial(self._on_button_event, ProductCategory.F)
        )
        self._callbacks.append(cb_fail)

        # Configure GPIO outputs for LEDs
        for pin in diode_pins.values():
            self.pi.set_mode(pin, pigpio.OUTPUT)
            self.pi.write(pin, 0)
        self._led_pins = diode_pins

    def _on_button_event(self, category: ProductCategory, gpio: int, level: int, tick):
        # Simple debounce: confirm button still pressed after short delay
        time.sleep(0.05)
        if self.pi.read(gpio) != 0:
            # Button released or bounce
            return
        # Log and enqueue
        print(f"[BUTTON] Press detected on pin {gpio} for category {category.value}", flush=True)
        self._queue.put_nowait(category)

    async def detect_progress_category(self) -> Optional[ProductCategory]:
        # Await next GPIO event
        return await self._queue.get()

    def set_diode_state(self, color: DiodeColors, on: bool):
        pin = self._led_pins.get(color)
        if pin is None:
            return
        # Turn LED on or off
        self.pi.write(pin, 1 if on else 0)
        print(f"[DIODE] {color.value.upper()} set to {'ON' if on else 'OFF'}.", flush=True)

    def turn_off_all_diodes(self):
        for pin in self._led_pins.values():
            self.pi.write(pin, 0)
        print("[DIODE] All LEDs turned OFF.", flush=True)

    def dispose(self):
        # Cancel all callbacks and cleanup
        for cb in self._callbacks:
            cb.cancel()
        for pin in self._led_pins.values():
            self.pi.write(pin, 0)
        self.pi.stop()
        print("Pigpio resources disposed.")
