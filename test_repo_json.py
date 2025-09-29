from ecommerce_clientes.models import Cliente
from ecommerce_clientes.repository import JSONClienteRepository

def test_repo_json_crud(tmp_path):
    f = tmp_path / "clientes.json"
    r = JSONClienteRepository(f)
    c = Cliente(1, "Ana", "ana@gmail.com", "Calle", saldo=100)
    r.add(c); assert r.get(1) is not None
    c.recargar_saldo(20); r.update(c); assert r.get(1).saldo == 120
    assert len(list(r.all())) == 1
    r.remove(1); assert r.get(1) is None
