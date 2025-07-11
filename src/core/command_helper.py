"""
Command Helper - Provides OS-specific networking command suggestions
"""

import platform
import subprocess
from typing import Dict, List, Optional


class CommandHelper:
    """Helper for OS-specific networking commands"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.command_suggestions = self._get_command_suggestions()
    
    def _get_command_suggestions(self) -> Dict[str, List[str]]:
        """Get OS-specific command suggestions"""
        suggestions = {
            'darwin': [  # macOS
                'ifconfig',
                'ping -c 1 127.0.0.1',
                'traceroute 8.8.8.8',
                'netstat -an',
                'dig google.com',
                'nslookup google.com',
                'route -n',
                'arp -a'
            ],
            'linux': [
                'ip addr',
                'ifconfig',
                'ping -c 1 127.0.0.1',
                'traceroute 8.8.8.8',
                'netstat -tuln',
                'ss -tuln',
                'dig google.com',
                'nslookup google.com',
                'route -n',
                'arp -a'
            ],
            'windows': [
                'ipconfig /all',
                'ping 127.0.0.1',
                'tracert 8.8.8.8',
                'netstat -an',
                'nslookup google.com',
                'route print',
                'arp -a'
            ]
        }
        return suggestions
    
    def get_suggestions(self) -> List[str]:
        """Get command suggestions for current OS"""
        return self.command_suggestions.get(self.system, [])
    
    def suggest_alternative(self, command: str) -> Optional[str]:
        """Suggest an alternative for a failed command"""
        base_cmd = command.split()[0].lower()
        
        alternatives = {
            'darwin': {
                'ipconfig': 'ifconfig',
                'tracert': 'traceroute',
                'netstat': 'netstat -an'
            },
            'linux': {
                'ipconfig': 'ip addr',
                'tracert': 'traceroute',
                'netstat': 'netstat -tuln'
            },
            'windows': {
                'ifconfig': 'ipconfig /all',
                'traceroute': 'tracert',
                'ip': 'ipconfig'
            }
        }
        
        os_alternatives = alternatives.get(self.system, {})
        return os_alternatives.get(base_cmd)
    
    def is_command_available(self, command: str) -> bool:
        """Check if a command is available on the current system"""
        try:
            result = subprocess.run(
                ['which', command] if self.system != 'windows' else ['where', command],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def get_os_info(self) -> Dict[str, str]:
        """Get OS information"""
        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor()
        }
    
    def format_command_help(self, command: str) -> str:
        """Format help text for a command"""
        help_texts = {
            'ifconfig': 'Shows network interface configuration (macOS/Linux)',
            'ipconfig': 'Shows network interface configuration (Windows)',
            'ping': 'Tests network connectivity to a host',
            'traceroute': 'Shows the network path to a destination',
            'tracert': 'Shows the network path to a destination (Windows)',
            'netstat': 'Shows network connections and routing table',
            'dig': 'DNS lookup tool (macOS/Linux)',
            'nslookup': 'DNS lookup tool',
            'route': 'Shows routing table',
            'arp': 'Shows ARP cache'
        }
        
        base_cmd = command.split()[0].lower()
        return help_texts.get(base_cmd, f'Network command: {base_cmd}') 