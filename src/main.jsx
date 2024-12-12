import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { registerLicense } from "@syncfusion/ej2-base";
import App from "./App.jsx";
registerLicense(
  "Ngo9BigBOggjHTQxAR8/V1NMaF5cXmBCf1FpRmJGdld5fUVHYVZUTXxaS00DNHVRdkdnWH1fcnRQR2ldWURwWUQ="
);

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>
);
