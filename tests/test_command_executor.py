"""
Tests for Command Executor
"""

import pytest
import asyncio
import platform
from unittest.mock import patch, AsyncMock

from src.core.command_executor import CommandExecutor, CommandStatus, CommandResult


class TestCommandExecutor:
    """Test CommandExecutor class"""
    
    @pytest.fixture
    def executor(self):
        """Create CommandExecutor instance"""
        return CommandExecutor(timeout=10)
    
    @pytest.mark.asyncio
    async def test_execute_success(self, executor):
        """Test successful command execution"""
        result = await executor.execute("echo test")
        
        assert result.status == CommandStatus.SUCCESS
        assert result.output.strip() == "test"
        assert result.error == ""
        assert result.return_code == 0
        assert result.execution_time > 0
    
    @pytest.mark.asyncio
    async def test_execute_command_not_found(self, executor):
        """Test command not found"""
        result = await executor.execute("nonexistent_command_xyz123")
        
        assert result.status == CommandStatus.NOT_FOUND
        assert result.output == ""
        assert "not found" in result.error.lower()
        assert result.return_code == -1
    
    @pytest.mark.asyncio
    async def test_execute_timeout(self, executor):
        """Test command timeout"""
        # Use sleep command that will timeout
        result = await executor.execute("sleep 20")
        
        assert result.status == CommandStatus.TIMEOUT
        assert "timeout" in result.error.lower()
        assert result.return_code == -1
    
    @pytest.mark.asyncio
    async def test_execute_with_error_output(self, executor):
        """Test command with error output"""
        # Use a command that produces stderr
        result = await executor.execute("ls nonexistent_file_xyz123")
        
        assert result.status == CommandStatus.ERROR
        assert result.return_code != 0
        assert result.error != ""
    
    @pytest.mark.asyncio
    async def test_execute_complex_command(self, executor):
        """Test complex command with arguments"""
        result = await executor.execute("echo 'hello world' | wc -w")
        
        assert result.status == CommandStatus.SUCCESS
        assert result.output.strip() == "2"  # "hello world" has 2 words
        assert result.return_code == 0
    
    def test_parse_command_simple(self, executor):
        """Test simple command parsing"""
        cmd_parts = executor._parse_command("echo test")
        assert cmd_parts == ["echo", "test"]
    
    def test_parse_command_with_quotes(self, executor):
        """Test command parsing with quotes"""
        cmd_parts = executor._parse_command('echo "hello world"')
        assert cmd_parts == ["echo", "hello world"]
    
    def test_parse_command_malformed(self, executor):
        """Test malformed command parsing"""
        cmd_parts = executor._parse_command("echo 'unclosed quote")
        # Should handle gracefully
        assert isinstance(cmd_parts, list)
    
    def test_determine_status_success(self, executor):
        """Test status determination for success"""
        status = executor._determine_status(0, b"")
        assert status == CommandStatus.SUCCESS
    
    def test_determine_status_not_found(self, executor):
        """Test status determination for not found"""
        status = executor._determine_status(127, b"command not found")
        assert status == CommandStatus.NOT_FOUND
    
    def test_determine_status_permission_denied(self, executor):
        """Test status determination for permission denied"""
        status = executor._determine_status(126, b"permission denied")
        assert status == CommandStatus.PERMISSION_DENIED
    
    def test_determine_status_error(self, executor):
        """Test status determination 