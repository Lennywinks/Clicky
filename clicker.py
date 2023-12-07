import asyncio
import keyboard

import pydirectinput


class Clicker:

    def __init__(self) -> None:
        self.hotkey = "F20"
        self.mouse_button = "left"
        # Bool for the start button
        self.running = False
        # Bool for the press once mode
        self.press_mode_running = False
        # Pause in seconds for pydirectinput.PAUSE
        self.pause = 0.05
        # Only the first letter matters - either "H" or "P"
        self.mode = "Hold down"

    def set_mouse_button(self, mouse_button: str) -> None:
        self.mouse_button = mouse_button.lower()

    def set_hotkey(self, hotkey: str) -> None:
        self.hotkey = hotkey

    def set_clicks_per_second(self, clicks_per_second: int) -> None:
        """Takes the CPS (int) from the slider as input. Converts it into seconds (float)
        The calculated value does not translate exactly into the right amount of seconds
        The amplifier of 10% is used to make up for that difference"""
        self.pause = 1/(clicks_per_second*1.1)

    def set_mode(self, mode: str) -> None:
        self.mode = mode

    async def start(self) -> None:
        """Start button"""
        self.running = True
        if self.mode.startswith("P"):
            keyboard.add_hotkey(self.hotkey, self.switch_press_mode)
        await self.autoclick()

    def stop(self) -> None:
        """Stop button"""
        self.running = False

    def switch_press_mode(self) -> None:
        """Used to as callback function for keyboard.add_hotkey"""
        self.press_mode_running = not self.press_mode_running

    async def autoclick(self) -> None:
        """Coroutine to wait for inputs and execute the mouse clicks alongside the UI"""
        pydirectinput.PAUSE = self.pause

        if self.mode.startswith("H"):
            while self.running:
                while keyboard.is_pressed(self.hotkey):
                    pydirectinput.click(button=self.mouse_button)
                    await asyncio.sleep(0)
                await asyncio.sleep(0.1)

        if self.mode.startswith("P"):
            while self.running:
                while self.press_mode_running:
                    pydirectinput.click(button=self.mouse_button)
                    await asyncio.sleep(0)
                await asyncio.sleep(0.1)
