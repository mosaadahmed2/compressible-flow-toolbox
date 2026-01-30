import csv
from pathlib import Path
from backend.solvers.isentropic_solvers import solve_isentropic


HERE = Path(__file__).resolve().parent

def main():
    path = HERE / "reference_table.csv"
    failures = 0

    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["module"] != "isentropic":
                continue

            gamma = float(row["gamma"])
            known = row["known"]
            value = float(row["value"])
            branch = row["branch"].strip() or None

            out = solve_isentropic(gamma, known, value, branch=branch)
            expected = float(row["expected_M"])
            tol = float(row["tol_M"])
            err = abs(out["M"] - expected)

            ok = err <= tol
            print(row["case_id"], "PASS" if ok else "FAIL", f"M={out['M']:.6f}, err={err:g}")
            failures += (0 if ok else 1)

    raise SystemExit(0 if failures == 0 else 1)

if __name__ == "__main__":
    main()
