"""
Command Validator - Validates and sanitizes commands
"""

import re
import shlex
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of command validation"""
    valid: bool
    error: str = ""
    warnings: List[str] = None
    sanitized_command: str = ""


class CommandValidator:
    """Validates and sanitizes commands for security and correctness"""
    
    def __init__(self):
        # Dangerous commands that should be blocked
        self.dangerous_commands = {
            'rm', 'del', 'format', 'dd', 'mkfs', 'fdisk',
            'shutdown', 'reboot', 'halt', 'poweroff',
            'sudo', 'su', 'chmod', 'chown'
        }
        
        # Commands that require special handling
        self.special_commands = {
            'sudo', 'su', 'ssh', 'telnet', 'ftp'
        }
        
        # Maximum command length
        self.max_command_length = 1000
        
        # Allowed characters in commands
        self.allowed_chars = re.compile(r'^[a-zA-Z0-9\s\-_./\\:;=@#$%^&*()\[\]{}|<>"\'`~]+$')
    
    def validate_command(self, command: str) -> ValidationResult:
        """Validate command for security and correctness"""
        
        if not command or not command.strip():
            return ValidationResult(
                valid=False,
                error="Empty command"
            )
        
        # Check command length
        if len(command) > self.max_command_length:
            return ValidationResult(
                valid=False,
                error=f"Command too long (max {self.max_command_length} characters)"
            )
        
        # Check for dangerous commands
        base_cmd = command.split()[0].lower()
        if base_cmd in self.dangerous_commands:
            return ValidationResult(
                valid=False,
                error=f"Dangerous command '{base_cmd}' is not allowed"
            )
        
        # Check for special commands that need handling
        if base_cmd in self.special_commands:
            return ValidationResult(
                valid=False,
                error=f"Special command '{base_cmd}' requires special handling"
            )
        
        # Validate character set
        if not self.allowed_chars.match(command):
            return ValidationResult(
                valid=False,
                error="Command contains invalid characters"
            )
        
        # Try to parse command
        try:
            parsed = shlex.split(command)
            if not parsed:
                return ValidationResult(
                    valid=False,
                    error="Invalid command syntax"
                )
        except ValueError as e:
            return ValidationResult(
                valid=False,
                error=f"Invalid command syntax: {str(e)}"
            )
        
        # Check for common networking command patterns
        if not self._is_networking_command(command):
            return ValidationResult(
                valid=False,
                error="Command does not appear to be a networking command"
            )
        
        return ValidationResult(
            valid=True,
            sanitized_command=command.strip(),
            warnings=self._get_warnings(command)
        )
    
    def _is_networking_command(self, command: str) -> bool:
        """Check if command appears to be a networking command"""
        networking_patterns = [
            r'\b(ipconfig|ifconfig|ip|traceroute|tracert|ping|netstat|nmap|dig|nslookup|route|ss|netstat)\b',
            r'\b(host|whois|telnet|ssh|ftp|scp|rsync)\b',
            r'\b(arp|arping|iwconfig|iwlist|wpa_supplicant)\b',
            r'\b(ethtool|mii-tool|ifup|ifdown)\b'
        ]
        
        command_lower = command.lower()
        for pattern in networking_patterns:
            if re.search(pattern, command_lower):
                return True
        
        return False
    
    def _get_warnings(self, command: str) -> List[str]:
        """Get warnings for command"""
        warnings = []
        
        # Check for potential issues
        if '>' in command or '>>' in command:
            warnings.append("Command contains output redirection")
        
        if '|' in command:
            warnings.append("Command contains pipe operator")
        
        if '&' in command:
            warnings.append("Command contains background execution")
        
        if ';' in command:
            warnings.append("Command contains command separator")
        
        return warnings
    
    def sanitize_command(self, command: str) -> str:
        """Sanitize command for safe execution"""
        # Remove any potential shell injection
        sanitized = re.sub(r'[;&|`$()]', '', command)
        
        # Remove multiple spaces
        sanitized = re.sub(r'\s+', ' ', sanitized)
        
        return sanitized.strip() 