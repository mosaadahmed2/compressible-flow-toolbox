import { useState } from "react";
import IsentropicForm from "/components/IsentropicForm";
import NormalShockForm from "/components/NormalShockForm";
import ObliqueShockForm from "/components/ObliqueShockForm";

export default function App() {
  const [tab, setTab] = useState("isentropic");

  return (
    <div className="container">
      <h1>Compressible Flow Toolbox</h1>

      <div className="tabs">
        <button onClick={() => setTab("isentropic")}>
          Isentropic
        </button>
        <button onClick={() => setTab("normal")}>
          Normal Shock
        </button>
        <button onClick={() => setTab("oblique")}>
          Oblique Shock
        </button>
      </div>

      {tab === "isentropic" && <IsentropicForm />}
      {tab === "normal" && <NormalShockForm />}
      {tab === "oblique" && <ObliqueShockForm />}
    </div>
  );
}
