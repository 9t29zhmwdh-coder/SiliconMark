"""SiliconMark CLI — entry point for all benchmark commands."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from siliconmark.core.models import BenchmarkConfig, ModelInfo
from siliconmark.core.registry import list_runtimes
from siliconmark.core.runner import get_device_name, run_benchmark
from siliconmark.exporters.json_exporter import export_result

app = typer.Typer(
    name="siliconmark",
    help="Apple Silicon LLM Benchmark Suite — measure Token/s, RAM, Power & Temperature.",
    add_completion=False,
    no_args_is_help=True,
)
console = Console()

_DEFAULT_PROMPT = (
    "Explain the key architectural differences between Apple Silicon and x86 processors, "
    "focusing on the unified memory architecture, Neural Engine, and energy efficiency. "
    "Be technical and detailed."
)


@app.command()
def run(
    runtime: str = typer.Option(
        ...,
        "--runtime",
        "-r",
        help="Runtime adapter: ollama | llamacpp | mlc | gguf",
    ),
    model: str = typer.Option(
        ...,
        "--model",
        "-m",
        help="Model name (e.g. llama3.2:3b for Ollama, or filename for GGUF)",
    ),
    model_path: str = typer.Option(
        None,
        "--model-path",
        "-p",
        help="Absolute path to .gguf file (required for gguf runtime)",
    ),
    max_tokens: int = typer.Option(200, "--tokens", "-t", help="Tokens to generate"),
    prompt: str = typer.Option(_DEFAULT_PROMPT, "--prompt", help="Benchmark prompt text"),
    output_dir: Path = typer.Option(
        Path.home() / ".siliconmark" / "results",
        "--output",
        "-o",
        help="Results directory",
    ),
    no_warmup: bool = typer.Option(False, "--no-warmup", help="Skip warmup inference"),
):
    """Run a benchmark for a single runtime/model combination."""
    config = BenchmarkConfig(
        runtime=runtime,
        model=ModelInfo(name=model, path=model_path),
        prompt=prompt,
        max_tokens=max_tokens,
        warmup=not no_warmup,
    )

    console.rule(f"[bold cyan]SiliconMark[/]  {runtime} / {model}")

    try:
        result = run_benchmark(config)
    except RuntimeError as e:
        console.print(f"[bold red]Error:[/] {e}")
        raise typer.Exit(1)

    _print_result(result)

    saved = export_result(result, output_dir)
    console.print(f"\n[dim]Saved →[/] [green]{saved}[/]")


@app.command(name="list-runtimes")
def list_runtimes_cmd():
    """List all available runtime adapters."""
    table = Table(title="Available Runtimes", show_header=True, header_style="bold cyan")
    table.add_column("Runtime", style="bold")
    table.add_column("Description")
    for name, desc in list_runtimes():
        table.add_row(name, desc)
    console.print(table)


@app.command()
def device():
    """Detect and print the current Apple Silicon device."""
    console.print(f"[bold]Device:[/] {get_device_name()}")


@app.command()
def dashboard(
    results_dir: Path = typer.Option(
        Path.home() / ".siliconmark" / "results",
        "--results",
        "-r",
        help="Results directory",
    ),
    host: str = typer.Option("127.0.0.1", "--host"),
    port: int = typer.Option(8080, "--port", "-p"),
):
    """Launch the web dashboard to compare benchmark results visually."""
    try:
        import uvicorn
    except ImportError:
        console.print("[red]uvicorn not installed.[/]  pip install uvicorn")
        raise typer.Exit(1)

    from siliconmark.dashboard.app import create_app

    results_dir.mkdir(parents=True, exist_ok=True)
    console.print(f"[bold]Dashboard:[/]  http://{host}:{port}")
    uvicorn.run(create_app(results_dir.resolve()), host=host, port=port, log_level="warning")


# ── helpers ──────────────────────────────────────────────────────────────────


def _print_result(result) -> None:
    p = result.performance
    s = result.system
    a = s.apple

    table = Table(
        title=f"{result.config.runtime}  /  {result.config.model.name}",
        show_header=False,
        box=None,
        padding=(0, 2),
    )
    table.add_column("Metric", style="bold dim")
    table.add_column("Value")

    table.add_row("Device", result.device)
    table.add_row("Tokens / s", f"[bold green]{p.tokens_per_second:.1f}[/]")
    table.add_row("Tokens generated", str(p.total_tokens))
    table.add_row("Duration", f"{p.total_duration_s:.2f} s")
    if p.time_to_first_token_ms:
        table.add_row("Time to first token", f"{p.time_to_first_token_ms:.0f} ms")
    if p.prompt_tokens:
        table.add_row("Prompt tokens", str(p.prompt_tokens))
    table.add_row("RAM mean", f"{s.ram_used_gb_mean:.2f} GB")
    table.add_row("RAM peak", f"{s.ram_used_gb_peak:.2f} GB")
    table.add_row("CPU usage", f"{s.cpu_percent_mean:.1f} %")

    if a.package_power_mw is not None:
        table.add_row("Package power", f"{a.package_power_mw:.0f} mW")
    if a.cpu_power_mw is not None:
        table.add_row("CPU power", f"{a.cpu_power_mw:.0f} mW")
    if a.gpu_power_mw is not None:
        table.add_row("GPU power", f"{a.gpu_power_mw:.0f} mW")
    if a.ane_power_mw is not None:
        table.add_row("ANE power", f"{a.ane_power_mw:.0f} mW")
    if a.cpu_die_temp_celsius is not None:
        table.add_row("CPU temp", f"{a.cpu_die_temp_celsius:.1f} °C")

    console.print()
    console.print(table)


if __name__ == "__main__":
    app()
