# 🛰️ Network Router Simulator

A web-based interactive network simulator that visualizes how packets move through a network of routers.  
Built with **Flask** (backend) and **React + ForceGraph2D** (frontend).

👉 **Live Demo:** [router-simulator-omega.vercel.app](https://router-simulator-omega.vercel.app/)  

---

## 🚀 Features

- Dynamic, randomly generated network graph (20 routers)
- Real-time packet routing visualization
- Animated packet movement along shortest paths
- Shortest path computation using Dijkstra’s algorithm
- Adjustable source and destination nodes via dropdowns
- Edge weights displayed directly on links
- Responsive graph layout with zoom controls
- Flask REST API for network topology and routing data

---

## 🧩 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | React, ForceGraph2D, JavaScript, CSS |
| **Backend** | Python, Flask, Flask-CORS |
| **Deployment** | Render (API), Vercel (Frontend) |

---

### **Backend (Flask)**

```bash
cd backend
python -m venv venv
source venv/bin/activate      # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```
Backend runs on http://127.0.0.1:5000

---

### **Frontend (React)**
```bash
cd frontend
npm install
npm start
```
Frontend runs on http://localhost:3000

---

## 🩺 **API Endpoints**

| Endpoint       | Method | Description                                   |
|----------------|---------|-----------------------------------------------|
| `/api/topology` | GET     | Returns all routers and links in JSON         |
| `/api/route`    | POST    | Returns optimal path for given source/destination using Dijkstra's algorithm |

### Example request:

#### POST `/api/route`
```bash
{
  "src": "R1",
  "dest": "R12",
  "payload": "Hello"
}
```

#### Example response:
```bash
{
  "path": ["R1", "R5", "R9", "R12"],
  "delivered": true
}
```

## 🧭 **Future Improvements**
- Dynamic topology editing (add/remove routers live)
- Real-time congestion simulation
- Dijkstra and Bellman-Ford algorithm comparison mode
