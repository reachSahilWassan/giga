# Multiplayer Ping Pong Game with Dynamic Obstacles

This project is a real-time multiplayer ping pong game where two players can compete across different browser tabs. The game includes dynamic obstacles, paddle controls using the keyboard, a scoring system, and a restart functionality. While there are limitations, the foundational features of a multiplayer game are implemented effectively within the given constraints.

---

## **Setup Instructions**

### **Backend Setup**
1. **Install Python dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate   # For Windows
   pip install fastapi uvicorn python-socketio
   ```
2. **Run the backend server:**
   ```bash
   python main.py
   ```
   This will start the backend server on `http://127.0.0.1:8000`.

### **Frontend Setup**
1. **Install Node.js dependencies:**
   ```bash
   npm install
   ```
2. **Start the React development server:**
   ```bash
   npm run dev
   ```
   The frontend will run on `http://localhost:3000`.

---

## **How to Run the Game**

1. Start the **backend server** as described above.
2. Start the **frontend server**.
3. Open the game in **two browser tabs**:
   - The first tab will be assigned as `Player 1`.
   - The second tab will be assigned as `Player 2`.
4. **Controls:**
   - Use the **Arrow Keys** to move your paddle (Up/Down).
   - Click the **Restart Game** button to reset the game state.

---

## **Technical Choices**

### **Backend**
- **Framework:** FastAPI for lightweight, asynchronous server handling.
- **Real-Time Communication:** Python-SocketIO for WebSocket communication between the server and clients.
- **Game Logic:** Game state, ball physics, and collision detection are implemented on the backend to ensure consistent gameplay.

### **Frontend**
- **Framework:** React (JavaScript) for building a responsive and dynamic user interface.
- **WebSocket Client:** Socket.IO for real-time communication with the backend.
- **Keyboard Controls:** Used `keydown` events for paddle movement, ensuring responsive gameplay.

---

## **Known Limitations**

1. **Basic Graphics:** The game's visual design is minimal to focus on core functionality.
2. **Edge Case Handling:** Limited handling for unusual scenarios (e.g., rapid disconnections or multiple reconnects).
3. **Physics Simplifications:** Ball collision logic and movement are basic and may not mimic real-world physics perfectly.
4. **Single Server:** The backend does not support scaling or distributed deployment.
5. **Player Assignment:** Currently supports only two players per session.

---

