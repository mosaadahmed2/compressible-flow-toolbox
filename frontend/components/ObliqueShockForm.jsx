import { useState } from "react";
import { api } from "/src/api";

export default function ObliqueShockForm() {
  const [gamma, setGamma] = useState(1.4);
  const [M1, setM1] = useState(2.5);
  const [deltaDeg, setDeltaDeg] = useState(10);
  const [shockType, setShockType] = useState("weak");  // ✅ added
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const labelMap = {
    gamma: "γ",
  
    M1: "M₁",
    M2: "M₂",
    Mn1: "Mₙ₁",
    Mn2: "Mₙ₂",
  
    beta_deg: "β (deg)",
    delta_deg: "δ (deg)",
  
    "p2/p1": "P₂ / P₁",
    "rho2/rho1": "ρ₂ / ρ₁",
    "T2/T1": "T₂ / T₁",
  };
  

  async function compute() {
    setError("");
    setResult(null);

    try {
      const payload = {
        gamma,
        M1,
        delta_deg: deltaDeg,
        shock_type: shockType,   // ✅ send to backend
      };

      const res = await api.obliqueShock(payload);
      setResult(res);
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <div className="panel">
      <h2>Oblique Shock</h2>

      <div className="form-group">
        <label>Gamma (γ)</label>
        <input
          type="number"
          value={gamma}
          onChange={(e) => setGamma(+e.target.value)}
        />
      </div>

      <div className="form-group">
        <label>Upstream Mach (M₁)</label>
        <input
          type="number"
          value={M1}
          onChange={(e) => setM1(+e.target.value)}
        />
      </div>

      <div className="form-group">
        <label>Deflection Angle δ (deg)</label>
        <input
          type="number"
          value={deltaDeg}
          onChange={(e) => setDeltaDeg(+e.target.value)}
        />
      </div>

      {/* ✅ Shock Selector Added */}
      <div className="form-group">
        <label>Shock Solution</label>
        <select
          value={shockType}
          onChange={(e) => setShockType(e.target.value)}
        >
          <option value="weak">
            Weak (smaller β, usually M₂ &gt; 1)
          </option>
          <option value="strong">
            Strong (larger β, M₂ &lt; 1)
          </option>
        </select>
      </div>

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
