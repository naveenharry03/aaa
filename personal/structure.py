project_root/
│
├── agents/
│   ├── __init__.py
│   ├── base_agent.py           # Base class, inherits from dspy.Module
│   ├── master_agent.py         # Orchestrates child agents, inherits from dspy.Module
│   ├── sharepoint_agent.py     # SharePoint-specific logic, dspy.Module
│   ├── servicenow_agent.py     # ServiceNow-specific logic, dspy.Module
│   └── ... (other data source agents)
│
├── dspy_flows/
│   ├── __init__.py
│   ├── main_flow.py            # Main DSPy program, composes agents/tools
│   └── ... (other flows, e.g., rag_flow.py)
│
├── prompts/
│   ├── __init__.py
│   ├── base_prompt.py
│   ├── generic_prompts.py
│   └── dspy_prompt_templates.py
│
├── tools/
│   ├── __init__.py
│   ├── base_tool.py            # Base class, optionally dspy.Module
│   ├── mcp_client.py           # MCP protocol client for tool integration
│   ├── pipeline_executor.py    # Databricks pipeline management
│   ├── email_sender.py         # Email notifications
│   ├── vector_search_manager.py# Vector search endpoint/index management
│   └── ... (other tools)
│
├── validators/
│   ├── __init__.py
│   ├── base_validator.py
│   ├── response_critique.py
│   └── ... (other validators)
│
├── orchestrator/
│   ├── __init__.py
│   ├── langgraph_orchestrator.py # (Optional) For LangGraph orchestration
│   └── state_manager.py
│
├── data/
│   ├── __init__.py
│   ├── data_ingestor.py        # Ingests data from sources
│   ├── delta_table_manager.py  # Delta table CRUD/checks
│   ├── file_converter.py       # Binary-to-original file conversion
│   ├── rag_pipeline.py         # RAG-specific data processing
│   └── ... (other data connectors)
│
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   ├── config.py               # Secrets, tokens, config
│   └── helpers.py              # Misc helpers (blob storage, etc.)
│
├── docs/
│   └── ... (architecture, prompt examples, etc.)
│
├── tests/
│   └── ... (unit/integration tests)
│
├── main.py                     # Entry point: runs DSPy flow
├── requirements.txt
└── README.md
