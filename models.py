from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar

@dataclass
class Cliente:
    id_cliente: int
    nombre: str
    email: str
    direccion: str
    saldo: float = 0.0
    activo: bool = True
    fecha_alta: datetime = field(default_factory=datetime.utcnow)
    dominios_permitidos: ClassVar[set[str]] = {"gmail.com", "outlook.com", "hotmail.com", "yahoo.com"}

    def __post_init__(self) -> None:
        if "@" not in self.email:
            raise ValueError("Email inválido.")
        dominio = self.email.split("@", 1)[1]
        if dominio not in self.dominios_permitidos:
            self.activo = False
        if self.saldo < 0:
            raise ValueError("Saldo negativo no permitido.")

    def __str__(self) -> str:
        estado = "Activo" if self.activo else "Inactivo"
        return f"Cliente({self.id_cliente}) {self.nombre} <{self.email}> - {estado} - Saldo: ${self.saldo:,.2f}"

    def comprar(self, monto: float) -> None:
        if not self.activo:
            raise PermissionError("Cliente inactivo.")
        if monto <= 0:
            raise ValueError("Monto inválido.")
        if self.saldo < monto:
            raise ValueError("Saldo insuficiente.")
        self.saldo -= monto

    def recargar_saldo(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("Monto inválido.")
        self.saldo += monto

    def actualizar_direccion(self, nueva_direccion: str) -> None:
        if not nueva_direccion or len(nueva_direccion.strip()) < 3:
            raise ValueError("Dirección inválida.")
        self.direccion = nueva_direccion.strip()

    def desactivar(self) -> None:
        self.activo = False

    def activar(self) -> None:
        self.activo = True


class ClientePremium(Cliente):
    descuento: float = 0.10
    def comprar(self, monto: float) -> None:
        super().comprar(monto * (1 - self.descuento))
