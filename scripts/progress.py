#!/usr/bin/env python3
"""Avance de Lupa a partir de specs/ROADMAP.md (única fuente de verdad del estado).

Uso:  python3 scripts/progress.py            # resumen + tareas listas para tomar
      python3 scripts/progress.py --roadmap otra/ruta.md
Solo biblioteca estándar. Puntos: S=1, M=2. Las tareas H (humanas) se cuentan aparte.
"""
import argparse
import re
import sys
from collections import OrderedDict
from pathlib import Path

POINTS = {"S": 1, "M": 2}
STATUS_DONE, STATUS_WIP, STATUS_BLOCKED = "[x]", "[~]", "[!]"


def parse(text):
    specs, current = OrderedDict(), None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 7 and re.fullmatch(r"T\d{3}\.\d+", cells[0]) and current:
            tid, title, role, size, profile, deps, status = cells
            specs.setdefault(current, []).append({
                "id": tid, "title": title, "role": role, "size": size, "profile": profile,
                "deps": [d.strip() for d in deps.split(",") if d.strip() and d.strip() != "—"],
                "status": status,
            })
    return specs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--roadmap", default="specs/ROADMAP.md")
    path = Path(ap.parse_args().roadmap)
    if not path.exists():
        sys.exit(f"No existe {path}")
    specs = parse(path.read_text(encoding="utf-8"))
    tasks = [t for ts in specs.values() for t in ts]
    if not tasks:
        sys.exit("No encontré tareas en la hoja de ruta.")
    done_ids = {t["id"] for t in tasks if t["status"] == STATUS_DONE}

    print(f"{'Spec':<44}{'tareas':>8}{'puntos':>9}{'avance':>8}")
    tot_pts = done_pts = tot_h = done_h = 0
    for name, ts in specs.items():
        pts = sum(POINTS.get(t["size"], 0) for t in ts)
        dpts = sum(POINTS.get(t["size"], 0) for t in ts if t["status"] == STATUS_DONE)
        dn = sum(1 for t in ts if t["status"] == STATUS_DONE)
        pct = f"{dpts / pts:.0%}" if pts else "—"
        print(f"{name[:43]:<44}{f'{dn}/{len(ts)}':>8}{f'{dpts}/{pts}':>9}{pct:>8}")
        tot_pts += pts
        done_pts += dpts
        tot_h += sum(1 for t in ts if t["size"] == "H")
        done_h += sum(1 for t in ts if t["size"] == "H" and t["status"] == STATUS_DONE)
    n_done = len(done_ids)
    print("-" * 69)
    print(f"{'TOTAL':<44}{f'{n_done}/{len(tasks)}':>8}{f'{done_pts}/{tot_pts}':>9}{done_pts / tot_pts:>8.0%}")
    print(f"Tareas humanas (no delegables): {done_h}/{tot_h}")
    wip = [t["id"] for t in tasks if t["status"] == STATUS_WIP]
    blocked = [t["id"] for t in tasks if t["status"] == STATUS_BLOCKED]
    if wip:
        print("En curso:", ", ".join(wip))
    if blocked:
        print("Bloqueadas:", ", ".join(blocked))

    ready = [t for t in tasks if t["status"] == "[ ]" and all(d in done_ids for d in t["deps"])]
    print("\nListas para tomar (dependencias cumplidas):")
    for t in ready:
        who = "humano" if t["size"] == "H" else f"{t['role']}, perfil {t['profile']}"
        print(f"  {t['id']}  [{t['size']}] {t['title'][:70]}  ({who})")
    if not ready:
        print("  (ninguna)")


if __name__ == "__main__":
    main()
