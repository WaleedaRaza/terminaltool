"""
Tests for Command Processor
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from src.core.command_processor import CommandProcessor, ProcessedCommand
from src.core.llm_client import LLMClient
from src.core.command_executor import CommandStatus


class TestCommandProcessor:
    """Test CommandProcessor class"""
    
    @pytest.fixture
    def mock_llm_client(self):
        """Create mock LLM client"""
        client = AsyncMock(spec=LLMClient)
        client.get_explanation.return_value = '{"summary": "Test explanation"}'
        return client
    
    @pytest.fixture
    def processor(self, mock_llm_client):
        """Create CommandProcessor with mock LLM client"""
        return CommandProcessor(mock_llm_client)
    
    @pytest.mark.asyncio
    async def test_process_command_success(self, processor):
        """Test successful command processing"""
        result = await processor.process_command("echo test")
        
        assert isinstance(result, ProcessedCommand)
        assert result.command == "echo test"
        assert result.status == CommandStatus.SUCCESS
        assert result.explanation['summary'] == "Test explanation"
        assert isinstance(result.timestamp, datetime)
        assert result.execution_time > 0
    
    @pytest.mark.asyncio
    async def test_process_command_validation_error(self, processor):
        """Test command validation error"""
        result = await processor.process_command("rm -rf /")  # Dangerous command
        
        assert isinstance(result, ProcessedCommand)
        assert result.status == CommandStatus.ERROR
        assert "Dangerous command" in result.explanation['summary']
    
    @pytest.mark.asyncio
    async def test_process_command_execution_error(self, processor):
        """Test command execution error"""
        result = await processor.process_command("nonexistent_command_xyz123")
        
        assert isinstance(result, ProcessedCommand)
        assert result.status == CommandStatus.ERROR
        assert "not found" in result.explanation['summary'].lower()
    
    @pytest.mark.asyncio
    async def test_process_command_with_user_context(self, processor):
        """Test command processing with user context"""
        user_context = {"user_level": "beginner", "network_type": "home"}
        
        result = await processor.process_command("echo test", user_context)
        
        assert isinstance(result, ProcessedCommand)
        assert result.command == "echo test"
        assert result.status == CommandStatus.SUCCESS
    
    def test_initialize_supported_commands(self, processor):
        """Test supported commands initialization"""
        commands = processor.supported_commands
        
        assert isinstance(commands, dict)
        assert 'available' in commands
        assert 'by_category' in commands
        assert isinstance(commands['available'], list)
        assert isinstance(commands['by_category'], dict)
    
    def test_is_command_supported(self, processor):
        """Test command support checking"""
        # Test supported commands
        assert processor.is_command_supported("ping google.com")
        assert processor.is_command_supported("traceroute 8.8.8.8")
        
        # Test unsupported commands
        assert not processor.is_command_supported("rm -rf /")
        assert not processor.is_command_supported("sudo shutdown")
    
    def test_get_available_commands(self, processor):
        """Test getting available commands"""
        commands = processor.get_available_commands()
        
        assert isinstance(commands, dict)
        assert 'available' in commands
        assert 'by_category' in commands
    
    @pytest.mark.asyncio
    async def test_process_command_llm_error(self, processor, mock_llm_client):
        """Test LLM error handling"""
        mock_llm_client.get_explanation.side_effect = Exception("LLM error")
        
        result = await processor.process_command("echo test")
        
        assert isinstance(result, ProcessedCommand)
        assert result.status == CommandStatus.SUCCESS  # Command executed successfully
        assert "Error getting explanation" in result.explanation['summary']
    
    @pytest.mark.asyncio
    async def test_process_command_json_parse_error(self, processor, mock_llm_client):
        """Test JSON parse error handling"""
        mock_llm_client.get_explanation.return_value = "invalid json"
        
        result = await processor.process_command("echo test")
        
        assert isinstance(result, ProcessedCommand)
        assert result.status == CommandStatus.SUCCESS
        assert "Unable to parse LLM response" in result.explanation['summary']
    
    @pytest.mark.asyncio
    async def test_process_command_timeout(self, processor):
        """Test command timeout handling"""
        # Use a command that will timeout
        result = await processor.process_command("sleep 20")
        
        assert isinstance(result, ProcessedCommand)
        assert result.status == CommandStatus.TIMEOUT
        assert "timeout" in result.explanation['summary'].lower()
    
    def test_get_system_info(self, processor):
        """Test system info retrieval"""
        system_info = processor._get_system_info()
        
        assert isinstance(system_info, dict)
        assert 'system' in system_info
        assert 'release' in system_info
        assert 'version' in system_info
        assert 'machine' in system_info
        assert 'processor' in system_info
    
    @pytest.mark.asyncio
    async def test_process_command_empty_command(self, processor):
        """Test empty command processing"""
        result = await processor.process_command("")
        
        assert isinstance(result, ProcessedCommand)
        assert result.status == CommandStatus.ERROR
        assert "Empty command" in result.explanation['summary']
    
    @pytest.mark.asyncio
    async def test_process_command_very_long_command(self, processor):
        """Test very long command processing"""
        long_command = "echo " + "x" * 2000  # Exceeds max length
        
        result = await processor.process_command(long_command)
        
        assert isinstance(result, ProcessedCommand)
        assert result.status == CommandStatus.ERROR
        assert "too long" in result.explanation['summary'].lower()