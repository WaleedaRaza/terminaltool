#!/usr/bin/env python3
"""
Simple FastAPI web server for Networking Tool Copilot
"""

import sys
import os
import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import our modules
from core.command_processor import CommandProcessor
from core.llm_client import LLMClient
from core.command_helper import CommandHelper

# Create FastAPI app
app = FastAPI(title="Networking Tool Copilot", version="0.1.0")

# Initialize components
llm_client = LLMClient()
processor = CommandProcessor(llm_client)
command_helper = CommandHelper()

class CommandRequest(BaseModel):
    command: str

@app.get("/")
async def root():
    """Main page"""
    suggestions = command_helper.get_suggestions()
    suggestions_html = ""
    for suggestion in suggestions:
        suggestions_html += f'<div class="suggestion" onclick="useCommand(\'{suggestion}\')">{suggestion}</div>'
    
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Networking Tool Copilot</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; margin-bottom: 40px; }}
            .command-input {{ width: 100%; padding: 15px; margin: 10px 0; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; }}
            .execute-btn {{ background: #007bff; color: white; padding: 15px 30px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; }}
            .execute-btn:hover {{ background: #0056b3; }}
            .results {{ margin-top: 20px; }}
            .result-item {{ border: 1px solid #ddd; padding: 20px; margin: 10px 0; border-radius: 5px; background: #f9f9f9; }}
            .loading {{ text-align: center; color: #666; }}
            .suggestions {{ margin-top: 20px; }}
            .suggestion {{ background: #e9ecef; padding: 10px; margin: 5px 0; border-radius: 5px; cursor: pointer; }}
            .suggestion:hover {{ background: #dee2e6; }}
            .error {{ color: red; }}
            .success {{ color: green; }}
            .warning {{ color: orange; }}
            .help-text {{ font-size: 14px; color: #666; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌐 Networking Tool Copilot</h1>
                <p>AI-powered network command analysis</p>
                <div class="help-text">
                    <strong>OS:</strong> {command_helper.get_os_info()['system']} | 
                    <strong>Available commands:</strong> Click suggestions below
                </div>
            </div>
            
            <div>
                <input type="text" id="command" class="command-input" 
                       placeholder="Enter command (e.g., ping -c 1 127.0.0.1)">
                <button onclick="executeCommand()" class="execute-btn">Execute</button>
            </div>
            
            <div class="suggestions">
                <h3>💡 Command Suggestions:</h3>
                {suggestions_html}
            </div>
            
            <div id="results" class="results"></div>
        </div>
        
        <script>
            function useCommand(command) {{
                document.getElementById('command').value = command;
            }}
            
            async function executeCommand() {{
                const command = document.getElementById('command').value;
                const resultsDiv = document.getElementById('results');
                
                if (!command.trim()) {{
                    resultsDiv.innerHTML = '<div class="result-item"><p class="error">Please enter a command</p></div>';
                    return;
                }}
                
                resultsDiv.innerHTML = '<div class="loading">Executing command...</div>';
                
                try {{
                    const response = await fetch('/api/execute', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{command: command}})
                    }});
                    
                    const result = await response.json();
                    displayResult(result);
                }} catch (error) {{
                    resultsDiv.innerHTML = '<div class="result-item"><p class="error">Error: ' + error.message + '</p></div>';
                }}
            }}
            
            function displayResult(result) {{
                const resultsDiv = document.getElementById('results');
                
                if (result.error) {{
                    let html = '<div class="result-item">';
                    html += '<h3 class="error">❌ Error</h3>';
                    html += '<p class="error">' + result.error + '</p>';
                    
                    // Add suggestion if available
                    if (result.suggestion) {{
                        html += '<p class="warning">💡 Try: <strong>' + result.suggestion + '</strong></p>';
                        if (result.help_text) {{
                            html += '<p class="help-text">' + result.help_text + '</p>';
                        }}
                    }}
                    
                    html += '</div>';
                    resultsDiv.innerHTML = html;
                    return;
                }}
                
                let html = '<div class="result-item">';
                html += '<h3>Command: ' + result.command + '</h3>';
                html += '<h4>Status: ' + result.status + '</h4>';
                
                if (result.original_output) {{
                    html += '<h4>Output:</h4><pre>' + result.original_output + '</pre>';
                }}
                
                if (result.explanation) {{
                    const exp = result.explanation;
                    html += '<h4>Analysis:</h4>';
                    if (exp.summary) html += '<p><strong>Summary:</strong> ' + exp.summary + '</p>';
                    if (exp.interfaces && Array.isArray(exp.interfaces)) {{
                        html += '<strong>Interfaces:</strong><ul>';
                        exp.interfaces.forEach(i => {{
                            html += '<li><strong>' + i.name + '</strong> (' + i.status + ') - ' + (i.ip || 'No IP') + '<br><em>' + i.explanation + '</em>';
                            if (i.concerns && i.concerns.length) html += '<br><span style="color:orange">Concerns: ' + i.concerns.join(', ') + '</span>';
                            html += '</li>';
                        }});
                        html += '</ul>';
                    }}
                    if (exp.key_findings && exp.key_findings.length) {{
                        html += '<strong>Key Findings:</strong><ul>';
                        exp.key_findings.forEach(f => html += '<li>' + f + '</li>');
                        html += '</ul>';
                    }}
                    if (exp.recommendations && exp.recommendations.length) {{
                        html += '<strong>Recommendations:</strong><ul>';
                        exp.recommendations.forEach(r => html += '<li>' + r + '</li>');
                        html += '</ul>';
                    }}
                }}
                
                html += '</div>';
                resultsDiv.innerHTML = html;
            }}
        </script>
    </body>
    </html>
    """)

@app.post("/api/execute")
async def execute_command(request: CommandRequest):
    """Execute command via API"""
    try:
        result = await processor.process_command(request.command)
        
        # Convert ProcessedCommand to dict for JSON serialization
        return {
            "command": result.command,
            "status": result.status.value,
            "original_output": result.original_output,
            "explanation": result.explanation,
            "execution_time": result.execution_time,
            "timestamp": result.timestamp.isoformat(),
            "metadata": result.metadata
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 Starting Networking Tool Copilot Web Server...")
    print("🌐 Access the web app at: http://localhost:3000")
    uvicorn.run(app, host="127.0.0.1", port=3000) 