import React, { useMemo, useRef, useEffect, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";

function lerp(a, b, t) {
  return a + (b - a) * t;
}

export default function NetworkGraph({ routers = [], links = [], fullPath = [], packetProgress = 0 }) {
  const fgRef = useRef();
  const containerRef = useRef();
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });

  useEffect(() => {
    const updateSize = () => {
      if (containerRef.current) {
        setDimensions({
          width: containerRef.current.clientWidth,
          height: containerRef.current.clientHeight,
        });
      }
    };
    updateSize();
    window.addEventListener("resize", updateSize);
    return () => window.removeEventListener("resize", updateSize);
  }, []);

  const graphData = useMemo(
    () => ({
      nodes: routers.map((r) => ({
        id: r.id,
        x: Math.random() * 2000 - 1000,
        y: Math.random() * 1600 - 800,
      })),
      links: links.map((l) => ({ source: l.source, target: l.target, cost: l.cost })),
    }),
    [routers, links]
  );

  useEffect(() => {
    if (fgRef.current) {
      const chargeForce = fgRef.current.d3Force("charge");
      if (chargeForce) chargeForce.strength(-300);
      fgRef.current.d3Force("collide", (node) => 18);
    }
  }, [graphData]);

  // Compute packet position
  let packetPos = null;
  if (fullPath.length >= 2) {
    const stepIndex = Math.floor(packetProgress);
    const t = packetProgress - stepIndex;
    const startId = fullPath[stepIndex];
    const endId = fullPath[stepIndex + 1] || startId;

    const startNode = graphData.nodes.find((n) => n.id === startId);
    const endNode = graphData.nodes.find((n) => n.id === endId);

    if (startNode && endNode) {
      packetPos = {
        x: lerp(startNode.x, endNode.x, t),
        y: lerp(startNode.y, endNode.y, t),
      };
    }
  }

  const handleZoomIn = () => {
    const fg = fgRef.current;
    if (!fg) return;
    const currentZoom = fg.zoom();
    fg.zoom(currentZoom * 1.2, 400);
  };

  const handleZoomOut = () => {
    const fg = fgRef.current;
    if (!fg) return;
    const currentZoom = fg.zoom();
    fg.zoom(currentZoom / 1.2, 400);
  };

  return (
    <div
      ref={containerRef}
      className="NetworkGraphContainer"
      style={{ width: "100%", height: "100%", position: "relative" }}
    >
      <ForceGraph2D
        ref={fgRef}
        graphData={graphData}
        width={dimensions.width}
        height={dimensions.height}
        nodeCanvasObject={(node, ctx, globalScale) => {
          const fontSize = 10 / globalScale;
          ctx.beginPath();
          ctx.arc(node.x, node.y, 12, 0, 2 * Math.PI);
          ctx.fillStyle = "skyblue";
          ctx.fill();

          ctx.fillStyle = "white";
          ctx.font = `${fontSize}px Sans-Serif`;
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillText(node.id, node.x, node.y - 16);
        }}
        nodePointerAreaPaint={(node, color, ctx) => {
          ctx.fillStyle = color;
          ctx.beginPath();
          ctx.arc(node.x, node.y, 14, 0, 2 * Math.PI);
          ctx.fill();
        }}
        linkCanvasObject={(link, ctx, globalScale) => {
          const start = link.source;
          const end = link.target;
          if (start && end && start.x !== undefined && end.x !== undefined) {
            const startIndex = fullPath.indexOf(start.id);
            const endIndex = fullPath.indexOf(end.id);
            let color = "gray";
            if (startIndex !== -1 && endIndex !== -1) {
              const maxIndex = Math.max(startIndex, endIndex);
              if (maxIndex <= Math.floor(packetProgress)) color = "#FFA07A";
            }

            ctx.strokeStyle = color;
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(start.x, start.y);
            ctx.lineTo(end.x, end.y);
            ctx.stroke();

            const midX = (start.x + end.x) / 2;
            const midY = (start.y + end.y) / 2;
            ctx.fillStyle = "white";
            ctx.font = `${10 / globalScale}px Sans-Serif`;
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText(link.cost || "", midX, midY);
          }
        }}
        onRenderFramePost={(ctx) => {
          if (packetPos) {
            ctx.beginPath();
            ctx.arc(packetPos.x, packetPos.y, 6, 0, 2 * Math.PI);
            ctx.fillStyle = "orange";
            ctx.fill();
          }
        }}
        d3AlphaDecay={0.00005}
        d3VelocityDecay={0.5}
        linkDistance={400}
        cooldownTicks={400}
      />

      {/* Zoom Controls */}
      <div className="zoom-controls">
        <button className="zoom-btn zoom-in" onClick={handleZoomIn}>
          +
        </button>
        <button className="zoom-btn zoom-out" onClick={handleZoomOut}>
          −
        </button>
      </div>
    </div>
  );
}
