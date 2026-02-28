import { useState } from "react";
import { api } from "/src/api";

export default function FannoForm() {
  const [gamma, setGamma] = useState(1.4);
  const [known, setKnown] = useState("M");
  const [value, setValue] = useState(2);
  const [branch, setBranch] = useState("subsonic");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const labelMap = {
    gamma: "γ",
    M: "M",
    "p/p*": "p / p*",
    "T/T*": "T / T*",
    "rho/rho*": "ρ / ρ*",
    "Tt/Tt*": "Tₜ / Tₜ*",
    "pt/pt*": "Pₜ / Pₜ*",
    "Smax/R": "Smax / R",
  };
  

  async function compute() {
    setError("");
    setResult(null);

    try {
      const payload = { gamma, known, value, branch };
      if (known === "M") delete payload.branch;
      const res = await api.fanno(payload);
      setResult(res);
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <div className="panel">
      <h2>Fanno Flow</h2>

      <div className="form-group">
        <label>Gamma (γ)</label>
        <input type="number" value={gamma} onChange={(e) => setGamma(+e.target.value)} />
      </div>

      <div className="form-group">
        <label>Known Property</label>
        <select value={known} onChange={(e) => setKnown(e.target.value)}>
          <option value="M">Mach (M)</option>
          <option value="T/T*">T / T*</option>
          <option value="p/p*">p / p*</option>
          <option value="rho/rho*">ρ / ρ*</option>
          <option value="pt/pt*">pt / pt*</option>
          <option value="4fL/D">4fL/D</option>
        </select>
      </div>

      <div className="form-group">
        <label>Value</label>
        <input type="number" value={value} onChange={(e) => setValue(+e.target.value)} />
      </div>

      {known !== "M" && (
        <div className="form-group">
          <label>Flow Regime</label>
          <select value={branch} onChange={(e) => setBranch(e.target.value)}>
          <option value="subsonic">Subsonic (M &lt; 1)</option>
          <option value="supersonic">Supersonic (M &gt; 1)</option>
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
      <div key={k} className="result-row">
        <span className="result-label">
          {labelMap[k] || k}
        </span>
        <span className="result-value">
          {v === null ? "N/A" : Number(v).toFixed(4)}
        </span>
      </div>
    ))}
  </div>
)}

    </div>
  );
}
