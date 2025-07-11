"""
Networking Tool Copilot - CLI Interface
Real-time terminal copilot for networking commands
"""

import click
import asyncio
import subprocess
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import os

from ..core.command_processor import CommandProcessor
from ..core.llm_client import LLMClient
from ..renderers.terminal_renderer import TerminalRenderer


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Networking Tool Copilot - Smart CLI assistant for network commands"""
    pass


@cli.command()
@click.argument('command', nargs=-1, required=True)
@click.option('--simple', is_flag=True, help='Explain like I\'m 5')
@click.option('--debug', is_flag=True, help='Enable debug mode')
@click.option('--export', type=str, help='Export results to file')
def run(command, simple, debug, export):
    """Execute a networking command with AI-powered explanations"""
    command_str = ' '.join(command)
    
    # Initialize components
    llm_client = LLMClient()
    processor = CommandProcessor(llm_client)
    renderer = TerminalRenderer()
    
    try:
        # Execute command and get output
        result = asyncio.run(processor.process_command(command_str))
        
        # Render output
        renderer.render_result(result, simple=simple, debug=debug)
        
        # Export if requested
        if export:
            processor.export_result(result, export)
            
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--port', default=3000, help='Web dashboard port')
def shell(port):
    """Start interactive shell mode"""
    click.echo("Starting interactive shell mode...")
    click.echo("Type 'exit' to quit")
    
    # TODO: Implement interactive shell
    click.echo("Interactive shell mode coming soon!")


@cli.command()
@click.option('--port', default=3000, help='Web dashboard port')
def dashboard(port):
    """Start web dashboard"""
    click.echo(f"Starting web dashboard on http://localhost:{port}")
    
    # TODO: Implement web dashboard
    click.echo("Web dashboard coming soon!")


if __name__ == '__main__':
    cli() 