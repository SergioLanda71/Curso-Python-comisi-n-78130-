import pytest
from ecommerce_clientes.models import Cliente, ClientePremium

def test_cliente_basico_y_metodos():
    c = Cliente(1, "Ana", "ana@gmail.com", "Calle 123", saldo=200)
    assert "Cliente(1)" in str(c)
    c.recargar_saldo(100); assert c.saldo == 300
    c.comprar(50); assert c.saldo == 250
    c.actualizar_direccion("Av. Siempre Viva 742"); assert c.direccion == "Av. Siempre Viva 742"
    c.desactivar(); assert not c.activo
    c.activar(); assert c.activo

def test_cliente_premium_descuento():
    p = ClientePremium(2, "Luis", "luis@gmail.com", "Calle 2", saldo=100)
    p.comprar(100)  # 10% off => descuenta 90
    assert p.saldo == 10

def test_email_invalido_y_saldo_negativo():
    with pytest.raises(ValueError):
        Cliente(3, "Pepe", "pepemail.com", "Calle", saldo=0)
    with pytest.raises(ValueError):
        Cliente(4, "Lau", "lau@gmail.com", "Calle", saldo=-1)
