import requests
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import box

console = Console()

def obtener_tasa(origen, destino):
    url = f"https://api.frankfurter.app/latest?from={origen}&to={destino}"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        if "rates" in datos and destino in datos["rates"]:
            return datos["rates"][destino]
    return None

def listar_monedas():
    url = "https://api.frankfurter.app/currencies"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        return respuesta.json()
    return {}

# --- Programa principal ---
console.print("[bold cyan]=== Conversor de Divisas (Tiempo Real) ===[/bold cyan]")

monedas = listar_monedas()
if not monedas:
    console.print("[bold red]❌ No se pudo obtener la lista de monedas.[/bold red]")
    exit()

# Mostrar tabla de monedas
tabla = Table(title="Monedas Disponibles", box=box.ROUNDED, style="bold green")
tabla.add_column("Código", style="cyan", justify="center")
tabla.add_column("Nombre", style="white")

for codigo, nombre in sorted(monedas.items()):
    tabla.add_row(codigo, nombre)

console.print(tabla)

while True:
    try:
        cantidad = float(Prompt.ask("[yellow]Cantidad[/yellow]"))
        origen = Prompt.ask("[yellow]Moneda origen[/yellow]").upper()
        destino = Prompt.ask("[yellow]Moneda destino[/yellow]").upper()

        if origen not in monedas or destino not in monedas:
            console.print("[bold red]❌ Moneda no válida. Intenta de nuevo.[/bold red]")
            continue

        tasa = obtener_tasa(origen, destino)
        if tasa:
            resultado = cantidad * tasa
            console.print(f"[bold green]✅ {cantidad} {origen}[/bold green] son "
                          f"[bold cyan]{resultado:.2f} {destino}[/bold cyan] "
                          f"(Tasa: {tasa:.4f})")
        else:
            console.print("[bold red]❌ No se pudo obtener la tasa de cambio.[/bold red]")
    except ValueError:
        console.print("[bold red]❌ Por favor, introduce un número válido para la cantidad.[/bold red]")

    otra = Prompt.ask("[magenta]¿Quieres hacer otra conversión? (s/n)[/magenta]").lower()
    if otra != "s":
        console.print("[bold blue]👋 ¡Gracias por usar el conversor![/bold blue]")
        break