import typer
from rich.console import Console
from rich.table import Table
import spearmint_sdk
from spearmint_sdk.api import maintenance_api, reports_api
from spearmint_sdk.configuration import Configuration
from spearmint_sdk.api_client import ApiClient

app = typer.Typer()
console = Console()

# Configure SDK
# Point to the API Gateway
config = Configuration(host="http://localhost:8080/api")
client = ApiClient(config)

@app.command()
def status():
    """Check system status and API connectivity."""
    try:
        # We don't have a direct 'health' endpoint in the SDK unless we defined it in OpenAPI.
        # We'll try to fetch a simple report or list classifications to verify connectivity.
        # Actually, let's use the health check if available, but I didn't see it in the generation output.
        # I'll use reports_api.get_balance_report as a ping.
        api = reports_api.ReportsApi(client)
        response = api.get_balance_report()
        
        console.print("[bold green]✓ API is Online[/bold green]")
        console.print(f"Net Worth: ${response.summary.net_worth:,.2f}")
    except Exception as e:
        console.print("[bold red]✗ API Connection Failed[/bold red]")
        console.print(str(e))

@app.command()
def fix_classifications():
    """Run the classification fix routine."""
    api = maintenance_api.MaintenanceApi(client)
    try:
        with console.status("Running fixes..."):
            result = api.fix_classifications()
        
        console.print(f"[bold green]✓ Task: {result.task_name}[/bold green]")
        console.print(f"Status: {result.status}")
        console.print("Details:")
        for k, v in result.details.items():
            console.print(f"  - {k}: {v}")
            
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

@app.command()
def balances():
    """Show account balances."""
    api = reports_api.ReportsApi(client)
    try:
        report = api.get_balance_report()
        
        table = Table(title="Account Balances")
        table.add_column("Account", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Balance", justify="right", style="green")
        
        for account in report.accounts:
            table.add_row(
                account.account_name,
                account.account_type,
                f"${account.balance:,.2f}"
            )
            
        console.print(table)
        console.print(f"\n[bold]Total Net Worth: ${report.summary.net_worth:,.2f}[/bold]")
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    app()
