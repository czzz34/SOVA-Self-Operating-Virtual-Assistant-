import asyncio
import threading
from functions.hardware import generate_response

class HardwareHandler:
    async def show_hardware_status_async(self) -> None:
        """
        Asynchronously generate hardware status and update the UI.
        This runs the blocking generate_response() in an executor.
        """
        loop = asyncio.get_event_loop()
        status_message = await loop.run_in_executor(None, generate_response)
        # Update the UI on the main thread:
        self.root.after(0, lambda: self.append_message("TARS", status_message, "ai_msg"))

    def start_hardware_status_async(self) -> None:
        """
        Set up an asyncio event loop and run the asynchronous hardware status function.
        """
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        new_loop.run_until_complete(self.show_hardware_status_async())

    def show_hardware_status(self) -> None:
        """
        Display the hardware status by generating a mood-based response asynchronously,
        using a separate thread to run the asyncio loop.
        """
        threading.Thread(target=self.start_hardware_status_async, daemon=True).start()
