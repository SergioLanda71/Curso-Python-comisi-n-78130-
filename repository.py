from __future__ import annotations
from typing import Dict, Iterable, Optional, List
from .models import Cliente
from dataclasses import asdict
from pathlib import Path
import json

class InMemoryClienteRepository:
    def __init__(self) -> None:
        self._data: Dict[int, Cliente] = {}

    def add(self, cliente: Cliente) -> None:
        if cliente.id_cliente in self._data:
            raise KeyError(f"El id {cliente.id_cliente} ya existe.")
        self._data[cliente.id_cliente] = cliente

    def get(self, id_cliente: int) -> Optional[Cliente]:
        return self._data.get(id_cliente)

    def all(self) -> Iterable[Cliente]:
        return list(self._data.values())

    def update(self, cliente: Cliente) -> None:
        if cliente.id_cliente not in self._data:
            raise KeyError("Cliente inexistente.")
        self._data[cliente.id_cliente] = cliente

    def remove(self, id_cliente: int) -> None:
        self._data.pop(id_cliente, None)


class JSONClienteRepository:
    def __init__(self, filepath: str | Path) -> None:
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            self.filepath.write_text("[]", encoding="utf-8")

    def _read_all(self) -> List[dict]:
        raw = self.filepath.read_text(encoding="utf-8")
        return json.loads(raw or "[]")

    def _write_all(self, rows: List[dict]) -> None:
        self.filepath.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    def add(self, cliente: Cliente) -> None:
        rows = self._read_all()
        if any(r.get("id_cliente") == cliente.id_cliente for r in rows):
            raise KeyError(f"El id {cliente.id_cliente} ya existe.")
        row = asdict(cliente)
        if hasattr(cliente, "fecha_alta"):
            row["fecha_alta"] = cliente.fecha_alta.isoformat()
        rows.append(row)
        self._write_all(rows)

    def all(self) -> Iterable[Cliente]:
        rows = self._read_all()
        out = []
        for r in rows:
            out.append(Cliente(
                id_cliente=r["id_cliente"],
                nombre=r["nombre"],
                email=r["email"],
                direccion=r["direccion"],
                saldo=r.get("saldo", 0.0),
                activo=r.get("activo", True),
            ))
        return out

    def get(self, id_cliente: int) -> Optional[Cliente]:
        for c in self.all():
            if c.id_cliente == id_cliente:
                return c
        return None

    def update(self, cliente: Cliente) -> None:
        rows = self._read_all()
        for i, r in enumerate(rows):
            if r.get("id_cliente") == cliente.id_cliente:
                new = asdict(cliente)
                if hasattr(cliente, "fecha_alta"):
                    new["fecha_alta"] = cliente.fecha_alta.isoformat()
                rows[i] = new
                self._write_all(rows)
                return
        raise KeyError("Cliente inexistente.")

    def remove(self, id_cliente: int) -> None:
        rows = self._read_all()
        rows = [r for r in rows if r.get("id_cliente") != id_cliente]
        self._write_all(rows)
