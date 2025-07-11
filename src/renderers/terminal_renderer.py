"""
Terminal Renderer - Handles output formatting for terminal
"""

import json
from typing import Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.syntax import Syntax


class TerminalRenderer:
    """Renders command results in terminal with rich formatting"""
    
    def __init__(self):
        self.console = Console()
    
    def render_result(self, result, simple: bool = False, debug: bool = False):
        """Render command result in terminal"""
        
        # Handle ProcessedCommand object
        if hasattr(result, 'command'):
            command = result.command
            output = result.original_output
            explanation = result.explanation
            status = result.status
            error = result.metadata.get('error', None)
        else:
            # Handle dict for backward compatibility
            command = result.get('command', '')
            output = result.get('output', '')
            explanation = result.get('explanation', {})
            status = result.get('status', 'unknown')
            error = result.get('error', None)
        
        if error:
            self._render_error({'error': error, 'command': command})
            return
        
        # Header
        self.console.print(f"\n[bold blue]🔍 Command:[/bold blue] {command}")
        self.console.print(f"[bold green]✅ Executed successfully[/bold green]\n")
        
        # Original output
        if debug:
            self._render_original_output(output)
        
        # LLM explanation
        if explanation:
            self._render_explanation(explanation, simple)
        
        # Footer
        self.console.print(f"\n[dim]💡 Tip: Use --simple for beginner explanations[/dim]")
    
    def _render_error(self, result: Dict[str, Any]):
        """Render error message"""
        self.console.print(f"\n[bold red]❌ Error:[/bold red] {result['error']}")
        self.console.print(f"[dim]Command: {result['command']}[/dim]")
    
    def _render_original_output(self, output: str):
        """Render original command output"""
        self.console.print("[bold yellow]�� Original Output:[/bold yellow]")
        
        # Syntax highlighting for common outputs
        if 'ipconfig' in output.lower() or 'ifconfig' in output.lower():
            syntax = Syntax(output, "bash", theme="monokai")
        else:
            syntax = Syntax(output, "text", theme="monokai")
        
        self.console.print(Panel(syntax, title="Command Output"))
        self.console.print()
    
    def _render_explanation(self, explanation: Dict[str, Any], simple: bool):
        """Render LLM explanation"""
        
        if simple:
            self._render_simple_explanation(explanation)
        else:
            self._render_detailed_explanation(explanation)
    
    def _render_simple_explanation(self, explanation: Dict[str, Any]):
        """Render simplified explanation"""
        self.console.print("[bold green]�� Simple Explanation:[/bold green]")
        
        if 'summary' in explanation:
            self.console.print(f"📝 {explanation['summary']}")
        
        if 'explanation' in explanation:
            self.console.print(f"�� {explanation['explanation']}")
        
        self.console.print()
    
    def _render_detailed_explanation(self, explanation: Dict[str, Any]):
        """Render detailed explanation with tables and panels"""
        self.console.print("[bold green]�� AI Analysis:[/bold green]")
        
        # Summary
        if 'summary' in explanation:
            self.console.print(Panel(
                explanation['summary'],
                title="📋 Summary",
                border_style="green"
            ))
        
        # Interfaces table
        if 'interfaces' in explanation:
            self._render_interfaces_table(explanation['interfaces'])
        
        # Route table
        if 'route' in explanation:
            self._render_route_table(explanation['route'])
        
        # Connections table
        if 'connections' in explanation:
            self._render_connections_table(explanation['connections'])
        
        # Open ports table
        if 'open_ports' in explanation:
            self._render_ports_table(explanation['open_ports'])
        
        # Recommendations
        if 'recommendations' in explanation:
            self._render_recommendations(explanation['recommendations'])
        
        # Issues
        if 'issues' in explanation and explanation['issues']:
            self._render_issues(explanation['issues'])
        
        # Key findings
        if 'key_findings' in explanation:
            self._render_key_findings(explanation['key_findings'])
    
    def _render_interfaces_table(self, interfaces: list):
        """Render network interfaces table"""
        table = Table(title="�� Network Interfaces")
        table.add_column("Interface", style="cyan")
        table.add_column("IP Address", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Explanation", style="white")
        
        for interface in interfaces:
            status_color = "green" if interface.get('status') == 'active' else "red"
            table.add_row(
                interface.get('name', 'N/A'),
                interface.get('ip', 'N/A'),
                f"[{status_color}]{interface.get('status', 'N/A')}[/{status_color}]",
                interface.get('explanation', 'N/A')
            )
        
        self.console.print(table)
        self.console.print()
    
    def _render_route_table(self, route: list):
        """Render traceroute table"""
        table = Table(title="��️ Route Analysis")
        table.add_column("Hop", style="cyan")
        table.add_column("IP Address", style="green")
        table.add_column("Name", style="yellow")
        table.add_column("Latency", style="blue")
        table.add_column("Explanation", style="white")
        
        for hop in route:
            status_color = "green" if hop.get('status') == 'normal' else "red"
            table.add_row(
                str(hop.get('hop', 'N/A')),
                hop.get('ip', 'N/A'),
                hop.get('name', 'N/A'),
                f"[{status_color}]{hop.get('latency', 'N/A')}[/{status_color}]",
                hop.get('explanation', 'N/A')
            )
        
        self.console.print(table)
        self.console.print()
    
    def _render_connections_table(self, connections: list):
        """Render netstat connections table"""
        table = Table(title="🔗 Network Connections")
        table.add_column("Protocol", style="cyan")
        table.add_column("Local Address", style="green")
        table.add_column("Remote Address", style="yellow")
        table.add_column("State", style="blue")
        table.add_column("Purpose", style="white")
        
        for conn in connections:
            table.add_row(
                conn.get('protocol', 'N/A'),
                conn.get('local_address', 'N/A'),
                conn.get('remote_address', 'N/A'),
                conn.get('state', 'N/A'),
                conn.get('explanation', 'N/A')
            )
        
        self.console.print(table)
        self.console.print()
    
    def _render_ports_table(self, ports: list):
        """Render nmap ports table"""
        table = Table(title="🚪 Open Ports")
        table.add_column("Port", style="cyan")
        table.add_column("Service", style="green")
        table.add_column("State", style="yellow")
        table.add_column("Security", style="red")
        table.add_column("Explanation", style="white")
        
        for port in ports:
            security_color = "red" if port.get('security_implication') == 'high' else "yellow"
            table.add_row(
                str(port.get('port', 'N/A')),
                port.get('service', 'N/A'),
                port.get('state', 'N/A'),
                f"[{security_color}]{port.get('security_implication', 'N/A')}[/{security_color}]",
                port.get('explanation', 'N/A')
            )
        
        self.console.print(table)
        self.console.print()
    
    def _render_recommendations(self, recommendations: list):
        """Render recommendations"""
        if recommendations:
            self.console.print("[bold yellow]�� Recommendations:[/bold yellow]")
            for i, rec in enumerate(recommendations, 1):
                self.console.print(f"  {i}. {rec}")
            self.console.print()
    
    def _render_issues(self, issues: list):
        """Render issues"""
        if issues:
            self.console.print("[bold red]⚠️ Issues Found:[/bold red]")
            for i, issue in enumerate(issues, 1):
                self.console.print(f"  {i}. {issue}")
            self.console.print()
    
    def _render_key_findings(self, findings: list):
        """Render key findings"""
        if findings:
            self.console.print("[bold blue]🔍 Key Findings:[/bold blue]")
            for i, finding in enumerate(findings, 1):
                self.console.print(f"  {i}. {finding}")
            self.console.print() 