const BASE_URL =
  window.location.hostname === "localhost"
    ? "http://127.0.0.1:8000/api"
    : "https://compressible-flow-toolbox.onrender.com/api";

async function post(endpoint, payload) {
  const response = await fetch(`${BASE_URL}/${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "API error");
  }

  return response.json();
}

export const api = {
  isentropic: (data) => post("isentropic", data),
  normalShock: (data) => post("normal-shock", data),
  obliqueShock: (data) => post("oblique-shock", data),
  fanno: (data) => post("fanno", data),
  rayleigh: (data) => post("rayleigh", data),
};
