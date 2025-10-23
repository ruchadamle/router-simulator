import axios from "axios";

const API = axios.create({
  baseURL: "https://router-simulator.onrender.com/api"
});

export const getTopology = () => API.get("/topology");
export const routePacket = (src, dest, payload = "Hello") =>
  API.post("/route", { src, dest, payload });
