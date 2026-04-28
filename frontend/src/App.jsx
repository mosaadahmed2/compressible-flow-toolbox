import { useState } from "react";
import IsentropicForm from "/components/IsentropicForm";
import NormalShockForm from "/components/NormalShockForm";
import ObliqueShockForm from "/components/ObliqueShockForm";
import FannoForm from "/components/FannoForm";
import RayleighForm from "/components/RayleighForm";

export default function App() {
  const [tab, setTab] = useState("isentropic");

  return (
    <div className="app">
      <div className="header">
        <img
          src="/logo.png"
          alt="Rollins Engineering Solutions"
          className="logo"
        />
        <h1>Compressible Flow Toolbox</h1>
      </div>

      <div className="container">
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

      <div className="contributors">
        <h3>Contributors</h3>
        <p>
          Mosaad Ahmed <br />
          Andrew J. Rollins <br />
          William Strain <br />
          Michael Davis <br />
          David Rodriguez
        </p>
      </div>
    </div>
  );
}