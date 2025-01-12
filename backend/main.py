from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
import asyncio  # Ensure asyncio is properly used

# Create FastAPI app and Socket.IO server
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")  # Allow all origins
app.mount("/", socketio.ASGIApp(sio))

# Game state variables
game_state = {
    "paddles": {"player1": 50, "player2": 50},  # Paddle positions (percentage)
    "ball": {"x": 50, "y": 50, "dx": 1, "dy": 1},  # Ball position and direction
    "obstacles": [],  # Obstacle positions
    "scores": {"player1": 0, "player2": 0},  # Scores
}
connected_clients = {}  # Maps sid to player (player1 or player2)

@sio.event
async def connect(sid, environ):
    if len(connected_clients) < 2:
        # Assign player1 to the first client and player2 to the second
        player = "player1" if len(connected_clients) == 0 else "player2"
        connected_clients[sid] = player
        await sio.emit("assign_player", {"player": player}, room=sid)
        print(f"Client {sid} assigned as {player}")
    else:
        # Reject additional connections
        await sio.emit("game_full", {}, room=sid)
        print(f"Client {sid} rejected: game full")

    await sio.emit("update_game", game_state)

@sio.event
async def disconnect(sid):
    if sid in connected_clients:
        print(f"Client {sid} ({connected_clients[sid]}) disconnected.")
        del connected_clients[sid]

@sio.event
async def move_paddle(sid, data):
    # Ensure only the assigned player can move their paddle
    player = connected_clients.get(sid)
    if player and player in game_state["paddles"]:
        position = data["position"]
        game_state["paddles"][player] = position
        await sio.emit("update_game", game_state)

def update_ball_position():
    ball = game_state["ball"]
    paddle1_y = game_state["paddles"]["player1"]
    paddle2_y = game_state["paddles"]["player2"]

    # Update ball position
    ball["x"] += ball["dx"]
    ball["y"] += ball["dy"]

    # Bounce off top and bottom walls
    if ball["y"] <= 0 or ball["y"] >= 100:
        ball["dy"] *= -1

    # Paddle 1 collision (left paddle)
    if ball["x"] <= 5:  # Ball is at the left side
        if paddle1_y - 10 <= ball["y"] <= paddle1_y + 10:  # Paddle hit
            ball["dx"] *= -1  # Reverse horizontal direction
            adjust_ball_angle(ball, paddle1_y)

    # Paddle 2 collision (right paddle)
    elif ball["x"] >= 95:  # Ball is at the right side
        if paddle2_y - 10 <= ball["y"] <= paddle2_y + 10:  # Paddle hit
            ball["dx"] *= -1  # Reverse horizontal direction
            adjust_ball_angle(ball, paddle2_y)

    # Score handling (out of bounds)
    if ball["x"] <= 0:
        game_state["scores"]["player2"] += 1
        reset_ball()
    elif ball["x"] >= 100:
        game_state["scores"]["player1"] += 1
        reset_ball()

def adjust_ball_angle(ball, paddle_y):
    """
    Adjusts the ball's vertical direction (dy) based on where it hits the paddle.
    """
    offset = ball["y"] - paddle_y  # Distance from paddle center
    ball["dy"] += offset * 0.1  # Scale offset to adjust ball direction
    ball["dy"] = max(min(ball["dy"], 2), -2)  # Limit vertical speed

def reset_ball():
    game_state["ball"] = {"x": 50, "y": 50, "dx": 1, "dy": 1}

async def game_loop():
    while True:
        update_ball_position()
        await sio.emit("update_game", game_state)
        await asyncio.sleep(0.05)  # 20 updates per second
        print("Updating game state...")


@sio.event
async def restart_game(sid):
    """
    Resets the game state to its initial values and notifies all clients.
    """
    global game_state
    game_state = {
        "paddles": {"player1": 50, "player2": 50},  # Reset paddle positions
        "ball": {"x": 50, "y": 50, "dx": 1, "dy": 1},  # Reset ball position
        "obstacles": [],  # Reset obstacles (if any)
        "scores": {"player1": 0, "player2": 0},  # Reset scores
    }
    print("Game restarted by client:", sid)
    await sio.emit("update_game", game_state)  # Broadcast the reset game state

if __name__ == "__main__":
    import uvicorn

    async def start_server():
        # Run the game loop in the background
        asyncio.create_task(game_loop())
        # Start the Uvicorn server
        config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()

    # Run everything inside an asyncio event loop
    asyncio.run(start_server())
