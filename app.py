from webSocketServer import WebSocketServer, socketio, app
import random
import time
import threading

app = WebSocketServer().create_app()

connected_clients = 0
chat_messages = [
    "Hello there!",
    "How's it going?",
    "What's up?",
    "Nice to meet you!",
    "Let's chat!",
    "Real-time messaging is awesome!",
    "WebSockets are so cool!",
    "Enjoying this conversation?",
]

def broadcast_random_messages():
    """Send random chat messages periodically to all connected clients."""
    while True:
        time.sleep(3) 
        random_message = random.choice(chat_messages)
        print(f"Broadcasting: {random_message}")
        socketio.emit("message", {"text": random_message})

@socketio.on("connect")
def handle_connect():
    global connected_clients
    connected_clients += 1
    print("Client connected. Total clients:", connected_clients)

@socketio.on("disconnect")
def handle_disconnect():
    global connected_clients
    connected_clients -= 1
    print("Client disconnected. Total clients:", connected_clients)

@socketio.on("message")
def handle_message(message):
    print(f"Received message: {message}")
    socketio.emit("message", message)

if __name__ == "__main__":
    # this uses multithreading for the broadcaster thread to ensure that the server is never blocked by the message broadcasting
    broadcaster_thread = threading.Thread(target=broadcast_random_messages, daemon=True)
    broadcaster_thread.start()
    
    socketio.run(app)
