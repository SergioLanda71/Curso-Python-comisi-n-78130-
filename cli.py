# cli.py
import sys
from pathlib import Path
from .models import Cliente, ClientePremium
from .repository import JSONClienteRepository  # ← usamos JSON en vez de memoria

# Archivo donde se guardarán los clientes
DB_PATH = Path("clientes.json")

def main() -> None:
    repo = JSONClienteRepository(DB_PATH)
    if len(sys.argv) < 2:
        print("Uso: python -m ecommerce_clientes.cli <comando> [args]")
        print("Comandos: add, list, buy, topup")
        raise SystemExit(0)
    
    cmd, *args = sys.argv[1:]
    
    if cmd == "add":
        id_cliente = int(args[0])
        nombre = args[1]
        email = args[2]
        direccion = args[3]
        saldo = float(args[4]) if len(args) > 4 else 0.0
        c = Cliente(id_cliente, nombre, email, direccion, saldo=saldo)
        repo.add(c)
        print("OK:", c)
    
    elif cmd == "list":
        for c in repo.all():
            print(c)
    
    elif cmd == "buy":
        id_cliente = int(args[0])
        monto = float(args[1])
        premium = (len(args) > 2 and args[2].lower() == "premium")
        c = repo.get(id_cliente)
        if c is None:
            # Crear cliente temporal si no existe (solo para demo)
            c = ClientePremium(id_cliente, "Demo", "demo@gmail.com", "Calle 123", saldo=1000) if premium else Cliente(id_cliente, "Demo", "demo@gmail.com", "Calle 123", saldo=1000)
            repo.add(c)
        c.comprar(monto)
        repo.update(c)
        print("Compra OK:", c)
    
    elif cmd == "topup":
        id_cliente = int(args[0])
        monto = float(args[1])
        c = repo.get(id_cliente)
        if c is None:
            c = Cliente(id_cliente, "Demo", "demo@gmail.com", "Calle 123")
            repo.add(c)
        c.recargar_saldo(monto)
        repo.update(c)
        print("Recarga OK:", c)
    
    else:
        print("Comando desconocido.")
if __name__ == "__main__":
           main()