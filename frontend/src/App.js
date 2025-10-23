// src/App.js
import './App.css';
import React, { useEffect, useState } from "react";
import { getTopology, routePacket } from "./api";
import NetworkGraph from "./components/NetworkGraph";

function App() {
  const [topology, setTopology] = useState({ routers: [], links: [] });
  const [fullPath, setFullPath] = useState([]);
  const [packetProgress, setPacketProgress] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);

  const [srcNode, setSrcNode] = useState("");
  const [dstNode, setDstNode] = useState("");

  // Fetch topology
  useEffect(() => {
    getTopology()
      .then(res => {
        setTopology(res.data);
        if (res.data.routers.length > 0) {
          setSrcNode(res.data.routers[0].id);
          setDstNode(res.data.routers[res.data.routers.length - 1].id);
        }
      })
      .catch(err => console.error("Failed to fetch topology:", err));
  }, []);

  // Animate packet
  const handleSend = async () => {
    if (isAnimating || !srcNode || !dstNode) return;
    setIsAnimating(true);

    try {
      const res = await routePacket(srcNode, dstNode);
      const pathData = res.data.path;
      setFullPath(pathData);
      setPacketProgress(0);

      let progress = 0;
      const interval = setInterval(() => {
        progress += 0.03; // smooth animation
        if (progress >= pathData.length - 1) {
          progress = pathData.length - 1;
          clearInterval(interval);
          setTimeout(() => {
            setFullPath([]);
            setPacketProgress(0);
            setIsAnimating(false);
          }, 500);
        }
        setPacketProgress(progress);
      }, 40);
    } catch (err) {
      console.error("Failed to route packet:", err);
      setIsAnimating(false);
    }
  };

  return (
    <div
    style={{
        display: "flex",
        flexDirection: "column",
        width: "100vw",
        height: "100vh",
        overflow: "hidden",
        backgroundColor: "#1e1e2f",
        color: "#f0f0f0",
        boxSizing: "border-box",
        padding: "0 20px 0 20px", // horizontal padding only
    }}
    >
      <h1 style={{ fontSize: "24px", marginBottom: "10px" }}>Router Simulator</h1>

      <div style={{ marginBottom: "10px" }}>
        <label>
          Source:{" "}
          <select value={srcNode} onChange={e => setSrcNode(e.target.value)}>
            {topology.routers.map(r => (
              <option key={r.id} value={r.id}>{r.id}</option>
            ))}
          </select>
        </label>

        <label style={{ marginLeft: "20px" }}>
          Destination:{" "}
          <select value={dstNode} onChange={e => setDstNode(e.target.value)}>
            {topology.routers.map(r => (
              <option key={r.id} value={r.id}>{r.id}</option>
            ))}
          </select>
        </label>

        <button
          style={{ marginLeft: "20px" }}
          onClick={handleSend}
          disabled={isAnimating || srcNode === dstNode}
        >
          {isAnimating ? "Packet in progress..." : `Send Packet ${srcNode} → ${dstNode}`}
        </button>
      </div>

      <div style={{ flex: 1, width: "100%", position: "relative", minHeight: 0 }}>
      <NetworkGraph
        routers={topology.routers}
        links={topology.links}
        fullPath={fullPath}
        packetProgress={packetProgress}
      />
    </div>


      {fullPath.length > 0 && (
        <div style={{ marginTop: "10px" }}>
          <strong>Packet Path:</strong>{" "}
          {fullPath.slice(0, Math.floor(packetProgress) + 1).join(" → ")}
        </div>
      )}
    </div>
  );
}

export default App;
