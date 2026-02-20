import { useState } from "react";
import { api } from "/src/api";

export default function RayleighForm() {
  const [gamma, setGamma] = useState(1.4);
  const [known, setKnown] = useState("M");
  const [value, setValue] = useState(2);
  const [branch, setBranch] = useState("subsonic");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function compute() {
    setError("");
    setResult(null);

    try {
      const payload = { gamma, known, value, branch };
      if (known === "M") delete payload.branch;
      const res = await api.rayleigh(payload);
      setResult(res);
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <div className="panel">
      <h2>Rayleigh Flow</h2>

      <div className="form-group">
        <label>Gamma (γ)</label>
        <input type="number" value={gamma} onChange={(e) => setGamma(+e.target.value)} />
      </div>

      <div className="form-group">
        <label>Known Property</label>
        <select value={known} onChange={(e) => setKnown(e.target.value)}>
          <option value="M">Mach (M)</option>
          <option value="p/p*">p / p*</option>
          <option value="T/T*">T / T*</option>
          <option value="rho/rho*">ρ / ρ*</option>
          <option value="Tt/Tt*">Tt / Tt*</option>
          <option value="pt/pt*">pt / pt*</option>
        </select>
      </div>

      <div className="form-group">
        <label>Value</label>
        <input type="number" value={value} onChange={(e) => setValue(+e.target.value)} />
      </div>

      {known !== "M" && (
        <div className="form-group">
          <label>Branch</label>
          <select value={branch} onChange={(e) => setBranch(e.target.value)}>
            <option value="subsonic">Subsonic</option>
            <option value="supersonic">Supersonic</option>
          </select>
        </div>
      )}

      <button onClick={compute}>Compute</button>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="results">
          {Object.entries(result).map(([k, v]) => (
            <div key={k}>{k}: {typeof v === "number" ? v.toFixed(4) : String(v)}</div>
          ))}
        </div>
      )}
    </div>
  );
}
