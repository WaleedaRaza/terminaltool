"""
Command Processor - Handles command execution and LLM processing
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime

from .command_executor import CommandExecutor, CommandResult, CommandStatus
from .llm_client import LLMClient
from .command_templates import get_command_template
from .command_validator import CommandValidator
from .command_helper import CommandHelper


@dataclass
class ProcessedCommand:
    """Result of command processing"""
    command: str
    original_output: str
    explanation: Dict[str, Any]
    execution_time: float
    status: CommandStatus
    timestamp: datetime
    metadata: Dict[str, Any]


class CommandProcessor:
    """Processes networking commands and generates explanations"""
    
    def __init__(self, llm_client: LLMClient, timeout: int = 30):
        self.llm_client = llm_client
        self.executor = CommandExecutor(timeout=timeout)
        self.validator = CommandValidator()
        self.command_helper = CommandHelper()
        self.logger = logging.getLogger(__name__)
        
        # Initialize supported commands
        self.supported_commands = self._initialize_supported_commands()
    
    def _initialize_supported_commands(self) -> Dict[str, List[str]]:
        """Initialize supported commands based on system"""
        system_commands = self.executor.get_system_commands()
        
        # Combine all available commands
        all_commands = []
        for commands in system_commands.values():
            all_commands.extend(commands)
        
        return {
            'available': all_commands,
            'by_category': system_commands
        }
    
    async def process_command(self, command: str, user_context: Optional[Dict[str, Any]] = None) -> ProcessedCommand:
        """Execute command and process with LLM"""
        
        start_time = asyncio.get_event_loop().time()
        
        try:
            # Validate command
            validation_result = self.validator.validate_command(command)
            if not validation_result.valid:
                return self._create_error_result(command, validation_result.error)
            
            # Execute command
            execution_result = await self.executor.execute(command)
            
            # Process with LLM if execution was successful
            if execution_result.status == CommandStatus.SUCCESS:
                explanation = await self._get_explanation(command, execution_result.output, user_context)
            else:
                explanation = self._create_error_explanation(execution_result)
            
            execution_time = asyncio.get_event_loop().time() - start_time
            
            return ProcessedCommand(
                command=command,
                original_output=execution_result.output,
                explanation=explanation,
                execution_time=execution_time,
                status=execution_result.status,
                timestamp=datetime.now(),
                metadata={
                    'return_code': execution_result.return_code,
                    'error_output': execution_result.error,
                    'validation': validation_result
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error processing command '{command}': {e}")
            return self._create_error_result(command, str(e))
    
    async def _get_explanation(self, command: str, output: str, user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get LLM explanation for command output"""
        
        try:
            # Get appropriate template
            template = get_command_template(command)
            
            # Prepare context
            context = {
                'command': command,
                'output': output,
                'system_info': self._get_system_info(),
                'user_context': user_context or {}
            }
            
            # Prepare prompt
            prompt = template.format(**context)
            
            # Get LLM response
            response = await self.llm_client.get_explanation(prompt)
            
            # Parse response
            try:
                explanation = json.loads(response)
                explanation['raw_llm_response'] = response
                return explanation
            except json.JSONDecodeError as e:
                self.logger.warning(f"Failed to parse LLM response as JSON: {e}")
                return {
                    'summary': 'Unable to parse LLM response',
                    'raw_response': response,
                    'parse_error': str(e)
                }
                
        except Exception as e:
            self.logger.error(f"Error getting explanation: {e}")
            return {
                'summary': f'Error getting explanation: {str(e)}',
                'error': True
            }
    
    def _create_error_explanation(self, execution_result: CommandResult) -> Dict[str, Any]:
        """Create explanation for failed command execution"""
        base_cmd = execution_result.command.split()[0]
        alternative = self.command_helper.suggest_alternative(execution_result.command)
        
        error_messages = {
            CommandStatus.NOT_FOUND: f"Command '{base_cmd}' not found on this system",
            CommandStatus.PERMISSION_DENIED: f"Permission denied when executing '{execution_result.command}'",
            CommandStatus.TIMEOUT: f"Command timed out after {self.executor.timeout} seconds",
            CommandStatus.ERROR: f"Command failed with return code {execution_result.return_code}"
        }
        
        explanation = {
            'summary': error_messages.get(execution_result.status, 'Command execution failed'),
            'error': True,
            'error_type': execution_result.status.value,
            'return_code': execution_result.return_code,
            'error_output': execution_result.error
        }
        
        # Add alternative suggestion if available
        if alternative:
            explanation['suggestion'] = alternative
            explanation['help_text'] = self.command_helper.format_command_help(alternative)
        
        return explanation
    
    def _create_error_result(self, command: str, error: str) -> ProcessedCommand:
        """Create error result for processing failures"""
        return ProcessedCommand(
            command=command,
            original_output="",
            explanation={
                'summary': f'Processing error: {error}',
                'error': True
            },
            execution_time=0.0,
            status=CommandStatus.ERROR,
            timestamp=datetime.now(),
            metadata={'error': error}
        )
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get system information for context"""
        import platform
        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor()
        }
    
    def get_available_commands(self) -> Dict[str, List[str]]:
        """Get list of available commands"""
        return self.supported_commands
    
    def is_command_supported(self, command: str) -> bool:
        """Check if command is supported"""
        base_cmd = command.split()[0].lower()
        return base_cmd in self.supported_commands['available'] 