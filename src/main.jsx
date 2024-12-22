import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { BloomFilterProvider } from "./Context/bloom";
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <BloomFilterProvider>
    <App />
  </BloomFilterProvider>
);
