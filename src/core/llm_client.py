"""
LLM Client - Handles communication with language models
"""

import os
import asyncio
import aiohttp
import json
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class LLMProvider(Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    MOCK = "mock"


@dataclass
class LLMConfig:
    """LLM configuration"""
    provider: LLMProvider
    api_key: Optional[str] = None
    model: str = "gpt-4"
    temperature: float = 0.3
    max_tokens: int = 1000
    timeout: int = 30


class LLMClient:
    """Client for interacting with LLM APIs"""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or self._load_config()
        self.logger = logging.getLogger(__name__)
        self.session: Optional[aiohttp.ClientSession] = None
    
    def _load_config(self) -> LLMConfig:
        """Load configuration from file or environment variables"""
        # Try to load from config file first
        try:
            import sys
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            from config import load_config, get_api_key
            
            config = load_config()
            provider_str = config.get('llm_provider', 'openai').lower()
            api_key = get_api_key() or os.getenv('OPENAI_API_KEY') or os.getenv('ANTHROPIC_API_KEY')
            
        except ImportError:
            # Fallback to environment variables
            provider_str = os.getenv('LLM_PROVIDER', 'openai').lower()
            api_key = os.getenv('OPENAI_API_KEY') or os.getenv('ANTHROPIC_API_KEY')
            config = {}
        
        try:
            provider = LLMProvider(provider_str)
        except ValueError:
            provider = LLMProvider.MOCK
        
        return LLMConfig(
            provider=provider,
            api_key=api_key,
            model=config.get('llm_model', os.getenv('LLM_MODEL', 'gpt-4')),
            temperature=float(config.get('llm_temperature', os.getenv('LLM_TEMPERATURE', '0.3'))),
            max_tokens=int(config.get('llm_max_tokens', os.getenv('LLM_MAX_TOKENS', '1000'))),
            timeout=int(config.get('llm_timeout', os.getenv('LLM_TIMEOUT', '30')))
        )
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.config.timeout)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def get_explanation(self, prompt: str) -> str:
        """Get explanation from LLM"""
        
        if not self.session:
            async with self:
                return await self._get_explanation_internal(prompt)
        else:
            return await self._get_explanation_internal(prompt)
    
    async def _get_explanation_internal(self, prompt: str) -> str:
        """Internal method to get explanation"""
        
        try:
            if self.config.provider == LLMProvider.OPENAI:
                return await self._call_openai(prompt)
            elif self.config.provider == LLMProvider.ANTHROPIC:
                return await self._call_anthropic(prompt)
            elif self.config.provider == LLMProvider.MOCK:
                return self._get_mock_response(prompt)
            else:
                raise ValueError(f"Unsupported LLM provider: {self.config.provider}")
                
        except Exception as e:
            self.logger.error(f"Error getting LLM explanation: {e}")
            return self._get_fallback_response(prompt)
    
    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        if not self.config.api_key:
            raise ValueError("OpenAI API key not configured")
        
        url = "https://api.openai.com/v1/chat/completions"
        
        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": "You are a network CLI expert. Provide clear, concise explanations in JSON format."},
                {"role": "user", "content": prompt}
            ],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens
        }
        
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        
        async with self.session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data['choices'][0]['message']['content']
            else:
                error_text = await response.text()
                raise Exception(f"OpenAI API error: {response.status} - {error_text}")
    
    async def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API"""
        if not self.config.api_key:
            raise ValueError("Anthropic API key not configured")
        
        url = "https://api.anthropic.com/v1/messages"
        
        payload = {
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        headers = {
            "x-api-key": self.config.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        async with self.session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data['content'][0]['text']
            else:
                error_text = await response.text()
                raise Exception(f"Anthropic API error: {response.status} - {error_text}")
    
    def _get_mock_response(self, prompt: str) -> str:
        """Return mock response for development"""
        
        # Simple keyword-based mock responses
        prompt_lower = prompt.lower()
        
        if any(cmd in prompt_lower for cmd in ['ipconfig', 'ifconfig']):
            return '''{
                "summary": "Network interface configuration analysis",
                "interfaces": [
                    {
                        "name": "Ethernet",
                        "ip": "192.168.1.120",
                        "explanation": "Your local IP address for LAN communication",
                        "status": "active",
                        "concerns": []
                    }
                ],
                "recommendations": ["Check DNS settings", "Verify gateway connectivity"],
                "key_findings": ["Active Ethernet interface detected"]
            }'''
        
        elif any(cmd in prompt_lower for cmd in ['traceroute', 'tracert']):
            return '''{
                "route": [
                    {
                        "hop": 1,
                        "ip": "192.168.1.1",
                        "name": "router",
                        "explanation": "Your home router - first hop",
                        "latency": "2ms",
                        "status": "normal"
                    }
                ],
                "analysis": "Route appears normal with low latency",
                "issues": [],
                "recommendations": ["Monitor for latency spikes"]
            }'''
        
        elif 'ping' in prompt_lower:
            return '''{
                "summary": "Connectivity test results",
                "status": "successful",
                "latency": "15ms",
                "packet_loss": "0%",
                "explanation": "Connection is working well with low latency",
                "recommendations": ["Connection is healthy"]
            }'''
        
        elif any(cmd in prompt_lower for cmd in ['netstat', 'ss']):
            return '''{
                "summary": "Network connection summary",
                "connections": [
                    {
                        "protocol": "TCP",
                        "local_address": "192.168.1.120:80",
                        "remote_address": "0.0.0.0:0",
                        "state": "LISTEN",
                        "explanation": "Web server listening on port 80"
                    }
                ],
                "listening_ports": ["80"],
                "concerns": [],
                "recommendations": ["Monitor for unusual connections"]
            }'''
        
        else:
            return '''{
                "summary": "Command executed successfully",
                "explanation": "This is a mock response for development",
                "key_points": ["Command processed", "Mock response generated"],
                "recommendations": ["Configure real LLM for production"]
            }'''
    
    def _get_fallback_response(self, prompt: str) -> str:
        """Get fallback response when LLM fails"""
        return '''{
            "summary": "Unable to get AI explanation",
            "error": true,
            "explanation": "LLM service unavailable. Please check your configuration.",
            "recommendations": ["Verify API keys", "Check network connectivity"]
        }''' 