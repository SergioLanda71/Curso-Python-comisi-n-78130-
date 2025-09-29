from ecommerce_clientes.models import Cliente
from ecommerce_clientes.repository import InMemoryClienteRepository

def test_repo_memoria_crud():
    r = InMemoryClienteRepository()
    c = Cliente(1, "Ana", "ana@gmail.com", "Calle", saldo=100)
    r.add(c); assert r.get(1) is c
    c.recargar_saldo(50); r.update(c); assert r.get(1).saldo == 150
    assert len(list(r.all())) == 1
    r.remove(1); assert r.get(1) is None
