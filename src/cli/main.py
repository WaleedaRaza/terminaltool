#!/usr/bin/env python3
"""
Networking Tool Copilot - CLI Interface
Real-time terminal copilot for networking commands
"""

import click
import asyncio
import json
import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import os

from ..core.command_processor import CommandProcessor
from ..core.llm_client import LLMClient, LLMConfig
from ..renderers.terminal_renderer import TerminalRenderer


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@click.group()
@click.version_option(version="0.1.0")
@click.option('--debug', is_flag=True, help='Enable debug mode')
@click.option('--config', type=str, help='Configuration file path')
def cli(debug, config):
    """Networking Tool Copilot - Smart CLI assistant for network commands"""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Load configuration if provided
    if config:
        load_config(config)


def load_config(config_path: str):
    """Loa 