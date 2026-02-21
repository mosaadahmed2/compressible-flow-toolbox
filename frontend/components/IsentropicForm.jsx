import { useState } from "react";
import { api } from "/src/api";

export default function IsentropicForm() {
  const [gamma, setGamma] = useState(1.4);
  const [known, setKnown] = useState("M");
  const [value, setValue] = useState(2);
  const [branch, setBranch] = useState("supersonic");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function compute() {
    setError("");
    setResult(null);

    try {
      const payload = { gamma, known, value };
      if (known === "A/A*") payload.branch = branch;
      const res = await api.isentropic(payload);
      setResult(res);
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <div className="panel">
      
      <h2>Isentropic</h2>
      <div className="form-group">
  <label>Gamma (γ)</label>
  <input
    type="number"
    value={gamma}
    onChange={e => setGamma(+e.target.value)}
  />
</div>

<div className="form-group">
  <label>Known Property</label>
  <select value={known} onChange={e => setKnown(e.target.value)}>
  <option value="M">Mach (M)</option>
  <option value="P_P0">P / P₀</option>
  <option value="T_T0">T / T₀</option>
  <option value="A_Astar">A / A*</option>
</select>
</div>

<div className="form-group">
  <label>Value</label>
  <input
    type="number"
    value={value}
    onChange={e => setValue(+e.target.value)}
  />
</div>


{known === "A/Astar" && (
  <div className="form-group">
    <label>Branch</label>
    <select value={branch} onChange={e => setBranch(e.target.value)}>
      <option value="subsonic">Subsonic</option>
      <option value="supersonic">Supersonic</option>
    </select>
  </div>
)}

<div className="button-row">
  <button onClick={compute}>Compute</button>
</div>


      {error && <p className="error">{error}</p>}

      {result && (
        <div className="results">
          {Object.entries(result).map(([k, v]) => (
            <div key={k}>{k}: {Number(v).toFixed(4)}</div>
          ))}
        </div>
      )}
    </div>
  );
}
