# MCP (Model Context Protocol) - 30 Minute Lecture Notes

## Introduction (3 minutes)

**What is MCP?**
- Open protocol developed by Anthropic for connecting AI models to external data sources and tools
- Standardizes how AI assistants interact with different systems
- Think of it as USB-C for AI integrations - one universal connection standard

**Why MCP Matters**
- Eliminates need for custom integrations for each AI model
- Reduces fragmentation in AI ecosystem
- Enables secure, controlled access to enterprise data
- Shifts focus from building integrations to building capabilities

## Core Architecture (5 minutes)

**Three Key Components:**

1. **MCP Hosts** (AI Applications)
   - Claude Desktop, IDEs, AI tools
   - Initiate connections to servers
   - Present data/tools to users

2. **MCP Clients**
   - Protocol clients maintained by host applications
   - Handle connection lifecycle
   - Route requests between hosts and servers

3. **MCP Servers**
   - Lightweight programs exposing specific capabilities
   - Can provide resources, tools, or prompts
   - Run locally or remotely

**Communication Flow:**
- Host application contains MCP client
- Client connects to MCP servers via standard protocol
- Servers expose capabilities that AI can use
- Bi-directional, stateful connections

## Core Primitives (8 minutes)

**1. Resources**
- Data that servers expose for AI consumption
- Examples: files, database records, API responses
- Read-only by default
- Identified by URIs (e.g., `file:///project/data.json`)

**2. Prompts**
- Pre-written templates for common tasks
- Help users accomplish specific workflows
- Can include arguments for customization
- Example: "Analyze git commit" prompt with repository parameter

**3. Tools**
- Functions the AI can invoke to take actions
- Servers define available tools and their parameters
- AI decides when to call tools based on context
- Examples: database queries, API calls, file operations

**Key Distinction:**
- Resources = passive data sources
- Tools = active functions/actions
- Prompts = templated workflows

## Security Model (4 minutes)

**Design Principles:**
- Explicit user consent required
- Servers run in controlled environments
- Clear capability boundaries
- Audit trails for actions

**Trust Layers:**
1. User approves server connections
2. User reviews tool calls before execution
3. Servers operate with least-privilege access
4. Transport security (secure protocols)

**Best Practices:**
- Validate all inputs server-side
- Implement proper authentication
- Use environment variables for secrets
- Never expose sensitive data unnecessarily

## Building MCP Servers (7 minutes)

**Server Implementation Steps:**

1. **Choose SDK**
   - Python: `mcp` package
   - TypeScript: `@modelcontextprotocol/sdk`
   - Community SDKs for other languages

2. **Define Capabilities**
```python
# Example structure
@server.list_resources()
async def list_resources():
    return [Resource(uri="data://...", name="...")]

@server.list_tools()
async def list_tools():
    return [Tool(name="query_db", description="...")]
```

3. **Implement Handlers**
   - Resource readers
   - Tool executors
   - Prompt generators

4. **Configure Transport**
   - stdio (local processes)
   - HTTP with SSE (Server-Sent Events)

**Real-World Example:**
Building a database MCP server:
- Exposes database schema as resources
- Provides query execution as a tool
- Includes prompt templates for common queries
- Handles connection pooling and security

## Integration Patterns (5 minutes)

**Common Use Cases:**

1. **Data Access**
   - Connect to databases (PostgreSQL, MongoDB)
   - Access file systems
   - Query APIs (Slack, GitHub, Google Drive)

2. **Development Tools**
   - Git operations
   - Code execution
   - Testing frameworks

3. **Business Systems**
   - CRM data (Salesforce)
   - Analytics platforms
   - Internal knowledge bases

**Configuration Example:**
```json
{
  "mcpServers": {
    "database": {
      "command": "python",
      "args": ["server.py"],
      "env": {
        "DB_CONNECTION": "postgresql://..."
      }
    }
  }
}
```

## Enterprise Considerations (3 minutes)

**Deployment Models:**
- Local servers for development
- Centralized servers for shared resources
- Hybrid approaches for different security zones

**Governance:**
- Establish approval processes for new servers
- Monitor usage and audit logs
- Version control server configurations
- Document available capabilities

**Scalability:**
- Design servers to handle concurrent requests
- Implement caching where appropriate
- Consider rate limiting
- Plan for monitoring and observability

## Conclusion & Next Steps (2 minutes)

**Key Takeaways:**
- MCP standardizes AI-to-system connections
- Three primitives: Resources, Tools, Prompts
- Security through explicit consent and boundaries
- Growing ecosystem of servers and implementations

**Getting Started:**
1. Explore existing MCP servers (Anthropic's GitHub)
2. Try integrating one server with Claude Desktop
3. Build a simple custom server for your use case
4. Contribute to the open-source ecosystem

**Resources:**
- Official docs: modelcontextprotocol.io
- SDKs: Python, TypeScript on GitHub
- Community servers: growing marketplace
- Anthropic's reference implementations

---

**Q&A Time**