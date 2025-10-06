# Diagram MCP Tools Setup Guide

## Overview
I've added 4 powerful diagram MCP tools to your Cursor configuration:

### 1. **UML-MCP Server** (`uml-mcp`)
- **Purpose**: Generate UML diagrams (class, sequence, use case, etc.)
- **Usage**: Natural language descriptions or PlantUML code
- **Example**: "Create a class diagram for an e-commerce system"

### 2. **Mermaid Server** (`mermaid`)
- **Purpose**: Create flowcharts, sequence diagrams, Gantt charts, etc.
- **Usage**: Mermaid syntax or natural language
- **Example**: "Draw a flowchart showing user authentication process"

### 3. **Diagrams Server** (`diagrams`)
- **Purpose**: Generate various technical diagrams
- **Usage**: Natural language descriptions
- **Example**: "Create an architecture diagram for microservices"

### 4. **Chart Plotter** (`chart-plotter`)
- **Purpose**: Data visualization and charts
- **Usage**: Data-driven chart generation
- **Example**: "Create a bar chart showing sales data"

## Setup Instructions

### Step 1: Restart Cursor
After the MCP configuration update, restart Cursor completely to load the new servers.

### Step 2: Verify Installation
The tools will be automatically installed via `npx` when first used. You may see installation messages in Cursor's output.

### Step 3: Test the Tools
Try these example prompts in Cursor:

#### UML Diagrams:
```
"Use the uml-mcp tool to create a class diagram for a library management system with classes: Book, User, Library, and their relationships."
```

#### Mermaid Diagrams:
```
"Use the mermaid tool to create a sequence diagram showing the flow of a user login process."
```

#### General Diagrams:
```
"Use the diagrams tool to create an architecture diagram showing a web application with frontend, backend, and database layers."
```

#### Charts:
```
"Use the chart-plotter tool to create a line chart showing monthly revenue data."
```

## Usage Tips

1. **Be Specific**: The more detailed your description, the better the diagram
2. **Iterate**: You can ask for modifications to existing diagrams
3. **Combine Tools**: Use different tools for different types of diagrams
4. **Natural Language**: Describe what you want in plain English

## Troubleshooting

If you encounter issues:

1. **Check Cursor Output**: Look for error messages in Cursor's output panel
2. **Restart Cursor**: Sometimes a full restart is needed
3. **Check Node.js**: Ensure you have Node.js installed (required for npx)
4. **Network Issues**: Some tools may need internet access for initial setup

## Example Workflows

### Software Architecture Documentation:
1. Use `uml-mcp` for class diagrams
2. Use `mermaid` for sequence diagrams
3. Use `diagrams` for system architecture

### Data Analysis:
1. Use `chart-plotter` for data visualizations
2. Use `mermaid` for process flowcharts

### Project Planning:
1. Use `mermaid` for Gantt charts
2. Use `diagrams` for project structure diagrams

Your MCP configuration is now ready for comprehensive diagram creation directly within Cursor!
