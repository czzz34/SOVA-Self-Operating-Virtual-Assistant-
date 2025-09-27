# main.py (or run.py, etc.)

from flask import Flask, render_template, request, jsonify
import threading
import logging

app = Flask(__name__)

# Global reference for ChatBot instance (to be set from your GUI launcher)
chat_bot_instance = None

def set_chat_bot_instance(instance):
    global chat_bot_instance
    chat_bot_instance = instance

@app.route("/")
def index():
    # Flask will look for index.html in the "templates" folder
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send_command():
    global chat_bot_instance
    command = request.json.get("command", "").strip()

    if not command:
        return jsonify({"error": "No command provided"}), 400

    if chat_bot_instance is None:
        return jsonify({"error": "ChatBot not available"}), 500

    # 1) Post the user command into the Tkinter chat window as "You [web]"
    chat_bot_instance.root.after(
        0,
        lambda: chat_bot_instance.append_message("You [web]", command, "user_msg")
    )

    # 2) Check for "play <term>" first
    lower_cmd = command.lower()
    if lower_cmd.startswith("play "):
        query = command[5:].strip()
        if query:
            # Run handle_play_command in a background thread
            threading.Thread(
                target=chat_bot_instance.handle_play_command,
                args=(query,),
                daemon=True
            ).start()

        return jsonify({"status": "Playing audio", "query": query})

    # 3) Check for "open ..." or "can you open ..."
    if lower_cmd.startswith("open ") or lower_cmd.startswith("can you open "):
        threading.Thread(
            target=chat_bot_instance.run_macro_for_command,
            args=(command,),
            daemon=True
        ).start()
        return jsonify({"status": "Running macro", "command": command})

    # 4) Otherwise treat as a normal AI query
    threading.Thread(
        target=chat_bot_instance.process_ai_response,
        args=(command,),
        daemon=True
    ).start()
    return jsonify({"status": "Command received", "command": command})


def run_server(host="0.0.0.0", port=5000):
    # Start Flask without blocking (if you need to do other setup)
    app.run(host=host, port=port)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_server()
