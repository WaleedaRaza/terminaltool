"""
Command Executor - Handles actual command execution with proper error handling
"""

import asyncio
import subprocess
import platform
import shlex
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class CommandStatus(Enum):
    """Command execution status"""
    SUCCESS = "success"
    ERROR = "error"
    NOT_FOUND = "not_found"
    TIMEOUT = "timeout"
    PERMISSION_DENIED = "permission_denied"


@dataclass
class CommandResult:
    """Result of command execution"""
    command: str
    output: str
    error: str
    status: CommandStatus
    return_code: int
    execution_time: float


class CommandExecutor:
    """Handles command execution with proper error handling and timeout"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.system = platform.system().lower()
    
    async def execute(self, command: str) -> CommandResult:
        """Execute command and return detailed result"""
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Parse command safely
            cmd_parts = self._parse_command(command)
            
            # Execute with timeout
            process = await asyncio.wait_for(
                self._create_subprocess(cmd_parts),
                timeout=self.timeout
            )
            
            stdout, stderr = await process.communicate()
            execution_time = asyncio.get_event_loop().time() - start_time
            
            # Determine status
            status = self._determine_status(process.returncode, stderr)
            
            return CommandResult(
                command=command,
                output=stdout.decode('utf-8', errors='replace'),
                error=stderr.decode('utf-8', errors='replace'),
                status=status,
                return_code=process.returncode,
                execution_time=execution_time
            )
            
        except asyncio.TimeoutError:
            return CommandResult(
                command=command,
                output="",
                error=f"Command timed out after {self.timeout} seconds",
                status=CommandStatus.TIMEOUT,
                return_code=-1,
                execution_time=self.timeout
            )
            
        except FileNotFoundError:
            return CommandResult(
                command=command,
                output="",
                error=f"Command not found: {command.split()[0]}",
                status=CommandStatus.NOT_FOUND,
                return_code=-1,
                execution_time=0.0
            )
            
        except PermissionError:
            return CommandResult(
                command=command,
                output="",
                error=f"Permission denied: {command}",
                status=CommandStatus.PERMISSION_DENIED,
                return_code=-1,
                execution_time=0.0
            )
            
        except Exception as e:
            return CommandResult(
                command=command,
                output="",
                error=f"Unexpected error: {str(e)}",
                status=CommandStatus.ERROR,
                return_code=-1,
                execution_time=0.0
            )
    
    def _parse_command(self, command: str) -> list:
        """Parse command string into list of arguments"""
        try:
            return shlex.split(command)
        except ValueError:
            # Fallback for malformed commands
            return command.split()
    
    async def _create_subprocess(self, cmd_parts: list) -> asyncio.subprocess.Process:
        """Create subprocess with proper configuration"""
        return await asyncio.create_subprocess_exec(
            *cmd_parts,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.DEVNULL
        )
    
    def _determine_status(self, return_code: int, stderr: bytes) -> CommandStatus:
        """Determine command status based on return code and stderr"""
        if return_code == 0:
            return CommandStatus.SUCCESS
        elif return_code == 127:  # Command not found
            return CommandStatus.NOT_FOUND
        elif return_code == 126:  # Permission denied
            return CommandStatus.PERMISSION_DENIED
        else:
            return CommandStatus.ERROR
    
    def is_command_available(self, command: str) -> bool:
        """Check if command is available on the system"""
        try:
            result = subprocess.run(
                ['which', command] if self.system != 'windows' else ['where', command],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def get_system_commands(self) -> Dict[str, list]:
        """Get available commands for current system"""
        base_commands = {
            'common': ['ping', 'traceroute', 'netstat', 'nslookup'],
            'linux': ['ip', 'ifconfig', 'dig', 'route', 'ss'],
            'windows': ['ipconfig', 'tracert', 'netstat', 'nbtstat'],
            'macos': ['ifconfig', 'dig', 'route', 'netstat']
        }
        
        available = {}
        for category, commands in base_commands.items():
            available[category] = [
                cmd for cmd in commands 
                if self.is_command_available(cmd)
            ]
        
        return available 