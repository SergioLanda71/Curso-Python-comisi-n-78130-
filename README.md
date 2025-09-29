# Sistema de Gestión de Clientes

## Cómo usar la CLI
Ejecute desde la carpeta raíz (`Segunda entrega final (en mi caso)`):

```bash
# 1. Agrega un cliente (solo una vez)
python3 -m ecommerce_clientes.cli add 1 "Ana" "ana@gmail.com" "Calle 123" 200

# 2. Lista los clientes
python3 -m ecommerce_clientes.cli list

# 3. Haz una compra
python3 -m ecommerce_clientes.cli buy 1 50

# 4. Recarga saldo
python3 -m ecommerce_clientes.cli topup 1 100

## para ejecutar los test, si o si desde la terminal se necesita instalar pytest
pip install pytest
python3 -m pytest ecommerce_clientes/ 