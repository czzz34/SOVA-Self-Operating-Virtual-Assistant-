import asyncio
import random
import time

class FollowUp:
    async def follow_up_async(self) -> None:
        """
        Asynchronous follow-up method.
        Checks if the user has been silent for 30 seconds (with a dynamic sleep)
        and then posts a follow-up message via self.root.after().
        """
        follow_up_variants = [
            "Are you still there?",
            "You got quiet all of a sudden.",
            "Did I say something wrong?",
            "I'm still here if you want to talk.",
            "You haven't replied, everything okay?"
        ]
        while not self.stop_event.is_set():
            # Calculate how long to sleep based on last input time
            sleep_duration = max(5, 30 - (time.time() - self.last_input_time))
            await asyncio.sleep(sleep_duration)
            
            # If waiting for reply and it's been 30+ seconds, send a follow-up
            if self.waiting_for_reply and (time.time() - self.last_input_time >= 30):
                follow_up_msg = self.last_ai_question if self.last_ai_question else random.choice(follow_up_variants)
                self.root.after(0, lambda msg=follow_up_msg: self.append_message("TARS", msg, "ai_msg"))
                self.last_input_time = time.time()  # Reset the timer
                self.waiting_for_reply = False

    def start_followup_async(self) -> None:
        """
        Sets up and runs an asyncio event loop for follow-up in a separate thread.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.follow_up_async())
