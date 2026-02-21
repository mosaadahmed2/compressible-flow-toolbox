import { useState } from "react";
import IsentropicForm from "/components/IsentropicForm";
import NormalShockForm from "/components/NormalShockForm";
import ObliqueShockForm from "/components/ObliqueShockForm";
import FannoForm from "/components/FannoForm";
import RayleighForm from "/components/RayleighForm";


export default function App() {
  const [tab, setTab] = useState("isentropic");

  return (
    <div className="container">
      <h1>Compressible Flow Toolbox</h1>

      <div className="tabs">
      <button
            className={tab === "isentropic" ? "active" : ""}
            onClick={() => setTab("isentropic")}
          >
            Isentropic
          </button>
        <button
            className={tab === "normal" ? "active" : ""}
            onClick={() => setTab("normal")}
          >
            Normal Shock
          </button>
        
        <button
            className={tab === "oblique" ? "active" : ""}
            onClick={() => setTab("oblique")}
          >
            Oblique Shock
          </button>

        <button
            className={tab === "fanno" ? "active" : ""}
            onClick={() => setTab("fanno")}
          >
            Fanno
          </button>
        <button
            className={tab === "rayleigh" ? "active" : ""}
            onClick={() => setTab("rayleigh")}
          >
            Rayleigh
          </button>


      </div>

      {tab === "isentropic" && <IsentropicForm />}
      {tab === "normal" && <NormalShockForm />}
      {tab === "oblique" && <ObliqueShockForm />}
      {tab === "fanno" && <FannoForm />}
      {tab === "rayleigh" && <RayleighForm />}

    </div>
  );
}
