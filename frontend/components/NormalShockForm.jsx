import { useState } from "react";
import { api } from "/src/api";

export default function NormalShockForm() {
  const [gamma, setGamma] = useState(1.4);
  const [M1, setM1] = useState(2);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function compute() {
    setError("");
    setResult(null);

    try {
      const res = await api.normalShock({ gamma, M1 });
      setResult(res);
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <div className="panel">
      <h2>Normal Shock</h2>

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

      <button onClick={compute}>Compute</button>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="results">
          {Object.entries(result).map(([k, v]) => (
            <div key={k}>
              {k}: {Number(v).toFixed(4)}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
