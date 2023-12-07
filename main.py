from nicegui import app, ui
from nicegui.events import KeyEventArguments

from clicker import Clicker
from titlebar import titlebar
clicker = Clicker()



def set_hotkey(hotkey_button: ui.button, hotkey_label: ui.label) -> None:
    """Function to safe the pressed Key Combination and assign the Hotkey to the Clicker
    The UI Button and Label are also updated within this function"""

    def safe_key(key: KeyEventArguments):
        """Callback function for the Keyboard Listener"""
        # Save the pressed key
        keys_pressed.append(key)
        # If a key is lifted start evaluating the input
        if key.action.keyup:
            hotkey_list = []
            for hotkey in keys_pressed:
                # Get  string representation of pressed key
                hotkey_str = str(hotkey.key)
                # Modify the string for output
                hotkey_str = hotkey_str.upper() if len(hotkey_str) == 1 else hotkey_str
                # A set comprehension does not work correctly, because it does not preserve the order
                if not hotkey.action.keyup and hotkey_str not in hotkey_list:
                    hotkey_list.append(hotkey_str)

            # String representation of the combination
            hotkey = " + ".join([hotkey.lower() for hotkey in hotkey_list])
            clicker.hotkey = hotkey
            keyboard_listener.active = False
            hotkey_label.set_text(" + ".join(hotkey_list))
            hotkey_button.enable()
            hotkey_button.set_text("Change Hotkey")

    keys_pressed = []
    hotkey_button.disable()
    hotkey_button.set_text("Waiting for input...")
    keyboard_listener = ui.keyboard(on_key=lambda e: safe_key(e))


def main():
    """The whole UI part could be outsourced to a different UI-State Class. But it works for now"""
    app.native.window_args["resizable"] = False
    app.native.window_args["easy_drag"] = True
    app.native.start_args["debug"] = True

    ui.dark_mode().enable()

    # Titlebar
    def close_window():
        app.native.main_window.destroy()

    def minimize_window():
        app.native.main_window.minimize()

    with ui.header().classes(f"w-full h-8 p-2 bg-[#121212] pywebview-drag-region"):
        with ui.row().classes("gap-1 relative left-[1px] top-[1px] ml-auto mr-0"):
            ui.icon("circle").classes(
                "text-[13px] text-yellow-400").on("click", minimize_window)
            ui.icon("circle").classes(
                "text-[13px] text-red-400").on("click", close_window)
        ui.label("Clicky").classes(
            "text-lg text-[#03DAC6] absolute left-1/2 top-[6px]").style("transform: translateX(-50%)")

    with (ui.row().classes("w-full no-wrap")):
        # Card for Mouse Button selection
        with ui.card().classes("w-1/2 items-center h-32"):
            ui.label("Mouse Button").classes("font-bold")
            button_selection = ui.toggle(["Left", "Middle", "Right"],
                                         value="Left",
                                         on_change=lambda e: clicker.set_mouse_button(e.value)
                                         ).props("toggle-color=cyan-12 toggle-text-color=black")

        # Card for Clicks per second slider
        with ui.card().classes("w-1/2 items-center h-32"):
            ui.label("Clicks per second").classes("font-bold")
            slider = ui.slider(value=20,
                               min=1,
                               max=100,
                               step=1,
                               on_change=lambda e: clicker.set_clicks_per_second(int(e.value))).classes("items-center").props("inline color=cyan-12")
            ui.label().bind_text_from(slider, "value")

    with ((ui.row().classes("w-full no-wrap"))):
        # Card for Mode Selection
        with ui.card().classes("w-1/2 items-center h-32"):
            ui.label("Mode Selection").classes("font-bold")
            mode_selection = ui.toggle(["Hold down", "Press once"],
                                       value="Hold down",
                                       on_change=lambda e: clicker.set_mode(e.value)
                                       ).props("toggle-color=cyan-12 toggle-text-color=black")

        # Card for Hotkey Selection
        with ui.card().classes("w-1/2 items-center h-32"):
            hotkey_label = ui.label("F20").classes("font-bold")
            hotkey_button = ui.button("Change Hotkey",
                                      on_click=lambda: set_hotkey(hotkey_button, hotkey_label)
                                      ).classes("text-black").props("color=cyan-12")

    # Start and stop Button
    with ui.row().classes("w-full no-wrap"):
        async def on_start() -> None:
            start_button.disable()
            slider.disable()
            button_selection.disable()
            mode_selection.disable()
            hotkey_button.disable()
            start_button.set_text("Waiting for Hotkey...")
            await clicker.start()

        def on_stop() -> None:
            clicker.stop()
            start_button.enable()
            start_button.set_text("Start")
            slider.enable()
            button_selection.enable()
            mode_selection.enable()
            hotkey_button.enable()

        start_button = ui.button("Start", on_click=on_start).classes("w-3/4 text-black").props("color=cyan-12")
        ui.button("Stop", on_click=on_stop).classes("w-1/4 text-black").props("color=cyan-12")

    ui.run(native=True, window_size=(700, 388), reload=False, title="Clicky", frameless=True)


if __name__ in ("__main__", "__mp_main__"):
    main()
