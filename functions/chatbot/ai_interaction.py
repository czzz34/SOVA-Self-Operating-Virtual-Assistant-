import asyncio
import logging
from functions.model_loader import chat_with_model
from functions.personalized_prompt import build_personalized_prompt

class AIInteraction:
    def chat_with_ai(self, user_input: str) -> str:
        """
        Synchronous version: Updates status, builds a personalized prompt, calls the AI model,
        updates chat history, and returns the AI's reply.
        """
        self.status_var.set("Status: TARS is thinking...")
        
        # Build conversation history from previous messages
        conversation_history_str = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in self.chat_history]
        )
        
        # Build a personalized prompt that includes system info, conversation history, and the current query
        prompt = build_personalized_prompt(user_input, conversation_history_str)
        
        try:
            response = chat_with_model("gemma2:9b", messages=[{"role": "system", "content": prompt}])
            ai_reply = response["message"]["content"].strip()
        except Exception as e:
            logging.error("Error during AI chat: %s", e)
            ai_reply = "Oops, something went wrong while thinking."
        
        self.last_ai_question = ai_reply if ai_reply.endswith("?") else None
        self.chat_history.append({"role": "assistant", "content": ai_reply})
        self.root.after(0, lambda: self.status_var.set("Status: Idle"))
        return ai_reply

    async def chat_with_ai_async(self, user_input: str) -> str:
        """
        Asynchronous version: Uses asyncio to run the blocking chat_with_model call in a thread pool.
        This method allows multiple such tasks to run in parallel without blocking the main event loop.
        """
        self.status_var.set("Status: TARS is thinking (async)...")
        
        # Build conversation history string from previous messages
        conversation_history_str = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in self.chat_history]
        )
        prompt = build_personalized_prompt(user_input, conversation_history_str)
        
        # Get the current event loop
        loop = asyncio.get_event_loop()
        try:
            # Run the blocking call in a separate thread via run_in_executor
            response = await loop.run_in_executor(
                None, chat_with_model, "gemma2:9b", [{"role": "system", "content": prompt}]
            )
            ai_reply = response["message"]["content"].strip()
        except Exception as e:
            logging.error("Error during async AI chat: %s", e)
            ai_reply = "Oops, something went wrong while thinking."
        
        self.last_ai_question = ai_reply if ai_reply.endswith("?") else None
        self.chat_history.append({"role": "assistant", "content": ai_reply})
        self.root.after(0, lambda: self.status_var.set("Status: Idle"))
        return ai_reply

    def is_health_query(self, message: str) -> bool:
        message_lower = message.lower()
        keywords = ["how are you feeling right now"]
        return any(keyword in message_lower for keyword in keywords)
