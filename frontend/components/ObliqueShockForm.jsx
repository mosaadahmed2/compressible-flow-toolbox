import { useState } from "react";
import { api } from "/src/api";

export default function ObliqueShockForm() {
  const [gamma, setGamma] = useState(1.4);
  const [M1, setM1] = useState(2.5);
  const [beta_deg, setBetaDeg] = useState(35);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function compute() {
    setError("");
    setResult(null);

    try {
      const res = await api.obliqueShock({ gamma, M1, beta_deg });
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
    value={delta_deg}
    onChange={(e) => setDeltaDeg(+e.target.value)}
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
