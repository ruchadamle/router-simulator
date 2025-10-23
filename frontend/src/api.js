import axios from "axios";

const API = axios.create({ baseURL: "http://127.0.0.1:5000/api" });

export const getTopology = () => API.get("/topology");
export const routePacket = (src, dest, payload = "Hello") =>
  API.post("/route", { src, dest, payload });
