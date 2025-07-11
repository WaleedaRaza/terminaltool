"""
Web Server - FastAPI server for web dashboard
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import json
import asyncio
from typing import List, Dict, Any
import uvicorn

from ..core.command_processor import CommandProcessor
from ..core.llm_client import LLMClient


class WebServer:
    """FastAPI web server for dashboard"""
    
    def __init__(self):
        self.app = FastAPI(title="Networking Tool Copilot", version="0.1.0")
        self.llm_client = LLMClient()
        self.processor = CommandProcessor(self.llm_client)
        self.active_connections: List[WebSocket] = []
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup API routes"""
        
        @self.app.get("/")
        async def root():
            return HTMLResponse("""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Networking Tool Copilot</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .container { max-width: 1200px; margin: 0 auto; }
                    .header { text-align: center; margin-bottom: 40px; }
                    .command-input { width: 100%; padding: 10px; margin: 10px 0; }
                    .results { margin-top: 20px; }
                    .result-item { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🌐 Networking Tool Copilot</h1>
                        <p>AI-powered network command analysis</p>
                    </div>
                    
                    <div>
                        <input type="text" id="command" class="command-input" 
                               placeholder="Enter command (e.g., ipconfig /all)">
                        <button onclick="executeCommand()">Execute</button>
                    </div>
                    
                    <div id="results" class="results"></div>
                </div>
                
                <script>
                    async function executeCommand() {
                        const command = document.getElementById('command').value;
                        const resultsDiv = document.getElementById('results');
                        
                        resultsDiv.innerHTML = '<p>Executing...</p>';
                        
                        try {
                            const response = await fetch('/api/execute', {
                                method: 'POST',
                                headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({command: command})
                            });
                            
                            const result = await response.json();
                            displayResult(result);
                        } catch (error) {
                            resultsDiv.innerHTML = '<p>Error: ' + error.message + '</p>';
                        }
                    }
                    
                    function displayResult(result) {
                        const resultsDiv = document.getElementById('results');
                        resultsDiv.innerHTML = `
                            <div class="result-item">
                                <h3>Command: ${result.command}</h3>
                                <pre>${result.output}</pre>
                                <h4>Analysis:</h4>
                                <pre>${JSON.stringify(result.explanation, null, 2)}</pre>
                            </div>
                        `;
                    }
                </script>
            </body>
            </html>
            """)
        
        @self.app.post("/api/execute")
        async def execute_command(request: Dict[str, Any]):
            """Execute command via API"""
            command = request.get('command', '')
            if not command:
                return {"error": "No command provided"}
            
            try:
                result = await self.processor.process_command(command)
                return result
            except Exception as e:
                return {"error": str(e)}
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket for real-time updates"""
            await websocket.accept()
            self.active_connections.append(websocket)
            
            try:
                while True:
                    data = await websocket.receive_text()
                    message = json.loads(data)
                    
                    if message.get('type') == 'execute':
                        result = await self.processor.process_command(message['command'])
                        await websocket.send_text(json.dumps(result))
                        
            except WebSocketDisconnect:
                self.active_connections.remove(websocket)
    
    def run(self, host: str = "localhost", port: int = 3000):
        """Run the web server"""
        uvicorn.run(self.app, host=host, port=port)


def create_app():
    """Create FastAPI app instance"""
    return WebServer().app 