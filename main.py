import tkinter as tk
import threading
from functions.chatbot.chatbot import ChatBot
from functions.web_server import run_server, set_chat_bot_instance
from functions.conversation_logger import init_chat_csv

if __name__ == "__main__":
    # Initialize conversation logging (creates chat.csv if not exists)
    init_chat_csv()
    
    # Create the main window and ChatBot instance
    root = tk.Tk()
    
    # Optionally, print screen dimensions or add dynamic sizing:
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    desired_width = int(screen_width * 0.4)   # 40% of screen width
    desired_height = int(screen_height * 0.649)  # 65% of screen height
    root.geometry(f"{desired_width}x{desired_height}")
    
    # Create the ChatBot instance
    bot = ChatBot(root)
    print("ChatBot initialized successfully.")
    
    # Pass the ChatBot instance to the web server so it can process commands
    set_chat_bot_instance(bot)
    
    # Set the protocol to ensure proper cleanup on close
    root.protocol("WM_DELETE_WINDOW", bot.on_closing)
    
    # Start the web server in a background thread
    threading.Thread(target=run_server, daemon=True).start()
    
    # Start the Tkinter main loop
    root.mainloop()
