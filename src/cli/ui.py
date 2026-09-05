from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


console = Console()


def banner():
    console.print()
    console.print(
        Panel(
            "[bold cyan]FACECHAIN VERIFIER[/bold cyan]\n"
            "[dim]Face Identification & Blockchain Verification[/dim]",
            border_style="cyan",
            padding=(1, 4),
        )
    )


def section(title: str):
    console.print()
    console.print(f"[bold cyan]◆ {title}[/bold cyan]")


def success(label: str, value=None):
    if value is None:
        console.print(f"  [bold green]✓[/bold green] {label}")
    else:
        console.print(
            f"  [bold green]✓[/bold green] {label}: [white]{value}[/white]"
        )


def failure(label: str, value=None):
    if value is None:
        console.print(f"  [bold red]✗[/bold red] {label}")
    else:
        console.print(
            f"  [bold red]✗[/bold red] {label}: [white]{value}[/white]"
        )


def info(label: str, value=None):
    if value is None:
        console.print(f"  [bold yellow]•[/bold yellow] {label}")
    else:
        console.print(
            f"  [bold yellow]•[/bold yellow] {label}: [white]{value}[/white]"
        )


def matches_table(results: list[dict]):
    table = Table(
        title="Top Visual Matches",
        show_lines=False,
        header_style="bold cyan",
    )

    table.add_column("#", justify="right", width=4)
    table.add_column("Source", width=15)
    table.add_column("Title", width=45)
    table.add_column("Similarity", justify="right", width=12)
    table.add_column("Match", justify="center", width=10)

    for result in results[:10]:
        similarity = result.get("similarity")

        if similarity is None:
            score = "N/A"
            match = "[red]ERROR[/red]"
        else:
            score = f"{similarity:.4f}"
            match = (
                "[green]YES[/green]"
                if result.get("match")
                else "[dim]NO[/dim]"
            )

        title = result.get("title") or "Untitled"
        title = title[:42] + "..." if len(title) > 45 else title

        table.add_row(
            str(result.get("rank", "-")),
            result.get("source") or "Unknown",
            title,
            score,
            match,
        )

    console.print(table)


def complete(block_index: int, fingerprint: str):
    console.print()
    console.print(
        Panel(
            Text.from_markup(
                "[bold green]✓ VERIFICATION COMPLETE[/bold green]\n\n"
                f"Blockchain Block : [cyan]{block_index}[/cyan]\n"
                f"SHA-256          : [dim]{fingerprint}[/dim]\n"
                "Status            : [bold green]VALID[/bold green]"
            ),
            border_style="green",
            padding=(1, 3),
        )
    )
