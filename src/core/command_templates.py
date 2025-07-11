"""
Command Templates - LLM prompt templates for different commands
"""

def get_command_template(command: str) -> str:
    """Get appropriate template for command"""
    
    base_cmd = command.split()[0].lower()
    
    templates = {
        'ipconfig': IPCONFIG_TEMPLATE,
        'ifconfig': IFCONFIG_TEMPLATE,
        'ip': IP_TEMPLATE,
        'traceroute': TRACEROUTE_TEMPLATE,
        'tracert': TRACEROUTE_TEMPLATE,
        'ping': PING_TEMPLATE,
        'netstat': NETSTAT_TEMPLATE,
        'nmap': NMAP_TEMPLATE,
        'dig': DIG_TEMPLATE,
        'nslookup': NSLOOKUP_TEMPLATE,
        'route': ROUTE_TEMPLATE
    }
    
    return templates.get(base_cmd, DEFAULT_TEMPLATE)


# Template definitions
IPCONFIG_TEMPLATE = """
You are a network CLI interpreter. Analyze this ipconfig output:

COMMAND: {command}
OUTPUT: {output}

Provide a JSON response with this structure:
{{
    "summary": "Brief network overview",
    "interfaces": [
        {{
            "name": "Interface name",
            "ip": "IP address",
            "explanation": "What this IP means",
            "status": "active/inactive",
            "concerns": ["Any issues found"]
        }}
    ],
    "recommendations": ["Action items"],
    "key_findings": ["Important discoveries"]
}}

Focus on:
- Identifying active interfaces
- Explaining IP addresses and their purpose
- Highlighting any configuration issues
- Providing actionable recommendations
"""

IFCONFIG_TEMPLATE = """
You are a network CLI interpreter. Analyze this ifconfig output:

COMMAND: {command}
OUTPUT: {output}

Provide a JSON response with this structure:
{{
    "summary": "Brief network overview",
    "interfaces": [
        {{
            "name": "Interface name",
            "ip": "IP address",
            "explanation": "What this IP means",
            "status": "UP/DOWN",
            "concerns": ["Any issues found"]
        }}
    ],
    "recommendations": ["Action items"],
    "key_findings": ["Important discoveries"]
}}

Focus on:
- Identifying active interfaces
- Explaining IP addresses and their purpose
- Highlighting any configuration issues
- Providing actionable recommendations
"""

TRACEROUTE_TEMPLATE = """
You are a network CLI interpreter. Analyze this traceroute output:

COMMAND: {command}
OUTPUT: {output}

Provide a JSON response with this structure:
{{
    "route": [
        {{
            "hop": 1,
            "ip": "IP address",
            "name": "Hostname if available",
            "explanation": "What this hop represents",
            "latency": "Response time",
            "status": "normal/timeout/error"
        }}
    ],
    "analysis": "Overall route analysis",
    "issues": ["Problems found"],
    "recommendations": ["Action items"]
}}

Focus on:
- Identifying each hop and its purpose
- Explaining latency patterns
- Detecting routing issues
- Highlighting security concerns
"""

PING_TEMPLATE = """
You are a network CLI interpreter. Analyze this ping output:

COMMAND: {command}
OUTPUT: {output}

Provide a JSON response with this structure:
{{
    "summary": "Connectivity test results",
    "status": "successful/failed/partial",
    "latency": "Average response time",
    "packet_loss": "Loss percentage",
    "explanation": "What the results mean",
    "recommendations": ["Action items"]
}}

Focus on:
- Overall connectivity status
- Latency analysis
- Packet loss patterns
- Troubleshooting suggestions
"""

NETSTAT_TEMPLATE = """
You are a network CLI interpreter. Analyze this netstat output:

COMMAND: {command}
OUTPUT: {output}

Provide a JSON response with this structure:
{{
    "summary": "Network connection summary",
    "connections": [
        {{
            "protocol": "TCP/UDP",
            "local_address": "Local endpoint",
            "remote_address": "Remote endpoint",
            "state": "Connection state",
            "explanation": "What this connection is for"
        }}
    ],
    "listening_ports": ["Ports accepting connections"],
    "concerns": ["Security or performance issues"],
    "recommendations": ["Action items"]
}}

Focus on:
- Identifying active connections
- Highlighting listening ports
- Security implications
- Performance analysis
"""

NMAP_TEMPLATE = """
You are a network CLI interpreter. Analyze this nmap output:

COMMAND: {command}
OUTPUT: {output}

Provide a JSON response with this structure:
{{
    "summary": "Port scan results",
    "target": "Scanned target",
    "open_ports": [
        {{
            "port": "Port number",
            "service": "Service name",
            "state": "open/closed/filtered",
            "explanation": "What this port is for",
            "security_implication": "Security concern level"
        }}
    ],
    "security_assessment": "Overall security analysis",
    "recommendations": ["Action items"]
}}

Focus on:
- Identifying open ports and services
- Security implications
- Service explanations
- Hardening recommendations
"""

DIG_TEMPLATE = """
You are a network CLI interpreter. Analyze this dig output:

COMMAND: {command}
OUTPUT: {output}

Provide a JSON response with this structure:
{{
    "summary": "DNS query results",
    "query": "What was queried",
    "records": [
        {{
            "type": "Record type",
            "value": "Record value",
            "ttl": "Time to live",
            "explanation": "What this record means"
        }}
    ],
    "dns_servers": ["DNS servers used"],
    "recommendations": ["Action items"]
}}

Focus on:
- DNS record explanations
- TTL implications
- DNS server analysis
- Troubleshooting insights
"""

NSLOOKUP_TEMPLATE = """
You are a network CLI interpreter. Analyze this nslookup output:

COMMAND: {command}
OUTPUT: {output}

Provide a JSON response with this structure:
{{
    "summary": "DNS lookup results",
    "query": "What was looked up",
    "results": [
        {{
            "type": "Record type",
            "value": "Record value",
            "explanation": "What this means"
        }}
    ],
    "dns_server": "DNS server used",
    "recommendations": ["Action items"]
}}

Focus on:
- DNS resolution results
- Server responses
- Troubleshooting insights
"""

ROUTE_TEMPLATE = """
You are a network CLI interpreter. Analyze this route output:

COMMAND: {command}
OUTPUT: {output}

Provide a JSON response with this structure:
{{
    "summary": "Routing table analysis",
    "routes": [
        {{
            "destination": "Route destination",
            "gateway": "Next hop",
            "interface": "Outgoing interface",
            "explanation": "What this route is for"
        }}
    ],
    "default_gateway": "Default route",
    "recommendations": ["Action items"]
}}

Focus on:
- Route explanations
- Gateway analysis
- Network topology insights
"""

IP_TEMPLATE = """
You are a network CLI interpreter. Analyze this ip command output:

COMMAND: {command}
OUTPUT: {output}

Provide a JSON response with this structure:
{{
    "summary": "IP command results",
    "interfaces": [
        {{
            "name": "Interface name",
            "state": "Interface state",
            "addresses": ["IP addresses"],
            "explanation": "What this interface is for"
        }}
    ],
    "recommendations": ["Action items"]
}}

Focus on:
- Interface states
- IP address assignments
- Network configuration
"""

DEFAULT_TEMPLATE = """
You are a network CLI interpreter. Analyze this command output:

COMMAND: {command}
OUTPUT: {output}

Provide a JSON response with this structure:
{{
    "summary": "Command execution summary",
    "explanation": "What the command does and what the output means",
    "key_points": ["Important findings"],
    "recommendations": ["Action items"]
}}

Focus on:
- Command purpose
- Output interpretation
- Key insights
- Next steps
""" 