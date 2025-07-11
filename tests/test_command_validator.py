"""
Tests for Command Validator
"""

import pytest
from src.core.command_validator import CommandValidator, ValidationResult


class TestCommandValidator:
    """Test CommandValidator class"""
    
    @pytest.fixture
    def validator(self):
        """Create CommandValidator instance"""
        return CommandValidator()
    
    def test_validate_command_success(self, validator):
        """Test successful command validation"""
        result = validator.validate_command("ping google.com")
        
        assert result.valid is True
        assert result.error == ""
        assert result.sanitized_command == "ping google.com"
    
    def test_validate_command_empty(self, validator):
        """Test empty command validation"""
        result = validator.validate_command("")
        
        assert result.valid is False
        assert "Empty command" in result.error
    
    def test_validate_command_whitespace_only(self, validator):
        """Test whitespace-only command validation"""
        result = validator.validate_command("   ")
        
        assert result.valid is False
        assert "Empty command" in result.error
    
    def test_validate_command_too_long(self, validator):
        """Test command too long validation"""
        long_command = "echo " + "x" * 2000
        result = validator.validate_command(long_command)
        
        assert result.valid is False
        assert "too long" in result.error
    
    def test_validate_command_dangerous(self, validator):
        """Test dangerous command validation"""
        dangerous_commands = [
            "rm -rf /",
            "sudo shutdown",
            "format c:",
            "dd if=/dev/zero of=/dev/sda"
        ]
        
        for cmd in dangerous_commands:
            result = validator.validate_command(cmd)
            assert result.valid is False
            assert "Dangerous command" in result.error
    
    def test_validate_command_special(self, validator):
        """Test special command validation"""
        special_commands = [
            "sudo ls",
            "su -",
            "ssh user@host",
            "telnet host"
        ]
        
        for cmd in special_commands:
            result = validator.validate_command(cmd)
            assert result.valid is False
            assert "Special command" in result.error
    
    def test_validate_command_invalid_chars(self, validator):
        """Test invalid characters validation"""
        invalid_commands = [
            "ping google.com; rm -rf /",
            "echo test && rm -rf /",
            "ping google.com | rm -rf /",
            "echo test `rm -rf /`"
        ]
        
        for cmd in invalid_commands:
            result = validator.validate_command(cmd)
            assert result.valid is False
            assert "invalid characters" in result.error.lower()
    
    def test_validate_command_not_networking(self, validator):
        """Test non-networking command validation"""
        non_networking_commands = [
            "ls -la",
            "cat file.txt",
            "grep pattern file.txt",
            "sort file.txt"
        ]
        
        for cmd in non_networking_commands:
            result = validator.validate_command(cmd)
            assert result.valid is False
            assert "networking command" in result.error.lower()
    
    def test_validate_command_networking(self, validator):
        """Test networking command validation"""
        networking_commands = [
            "ping google.com",
``` 