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


  Your Vision (Recap)
Flexible, Modular, and Extensible Framework:
The system should be adaptable to new technologies, LLMs, and data sources, not locked into any single provider or approach.
Generic Prompting Layer:
Use DSPy to create prompts that work across multiple LLMs, not just one.
Agentic Architecture:
Each data source (SharePoint, ServiceNow, etc.) has its own agent. A master agent coordinates these child agents, combining their outputs and making decisions.
MCP (Multi-Component Processing):
The system should be able to call tools, agents, or other components to attempt automated fixes, and if not possible, generate documentation or instructions for the user.
LangGraph as the Orchestration Layer:
Use LangGraph to manage the flow, state, and agent interactions. Open to other suggestions if they fit better.
End-to-End Automation:
When a pipeline fails, the system should:
Gather failed logs from all relevant sources.
Use agents/validators to find the most relevant context and possible fixes.
Attempt automated fixes via tools/MCP.
If fixed, re-run the pipeline and report the outcome.
If not, generate and send actionable documentation to the user.
Always keep the user in the loop with clear, detailed emails.
Goal:
Dramatically reduce troubleshooting time for data engineers.




```````````````````````````````````````````
                                        # Function to query data from Delta table using Spark SQL
def query_customer_data(sql_query):
    """Execute SQL query against the customer data table using Spark SQL."""
    try:
        # Execute the query using Spark SQL
        result = spark.sql(sql_query)

        # Convert to a more readable format
        pandas_df = result.toPandas()

        # If the result is empty, return a message
        if pandas_df.empty:
            return "No data found matching the query criteria."

        # Convert to a list of dictionaries for easier processing
        records = pandas_df.to_dict(orient="records")
        return records
    except Exception as e:
        return f"Error executing query: {str(e)}"

from langchain.agents import Tool

def tool_ingest_customer_data(_=None):
    """Tool to ingest customer data into Delta table."""
    return ingest_json_to_delta(
        "/Workspace/Users/naveen.kumar@enabledata.com/Experiments/sample_naveen.json",
        catalog="spsn",
        schema_name="naveen_poc",
        table_name="sample_naveen"
    )
    
def tool_query_customer_data(query=""):
    """Tool to query customer data from Delta table."""
    # Ensure the query is safe and properly formatted
    if not query.lower().startswith("select"):
        return "Error: Only SELECT queries are allowed for security reasons."

    # Make sure the query targets the correct table
    if "spsn.naveen_poc.sample_naveen" not in query:
        # If the query doesn't specify the table, assume it's targeting our table
        if "from" not in query.lower():
            query = f"{query} FROM spsn.naveen_poc.sample_naveen"
        else:
            return "Error: Query must target the spsn.naveen_poc.sample_naveen table."

    return query_customer_data(query)

# Create tools
tools = [
    Tool(
        name="ingest_customer_data",
        func=tool_ingest_customer_data,
        description="Ingests customer data from JSON file into the Delta table. Use this first before querying data."
    ),
    Tool(
        name="query_customer_data",
        func=tool_query_customer_data,
        description="Executes SQL queries against the customer data table. Input should be a valid SQL SELECT query targeting spsn.naveen_poc.sample_naveen."
    )
]




from langchain.prompts import PromptTemplate

# Create a prompt template
prompt_template = """You are an assistant that helps users find information about customers.
You have access to customer data with fields: CustomerID, Name, Age, City, and PurchaseAmount.

You have access to the following tools:

{tools}

When a user asks a question about customer data, you should:
1. First use the ingest_customer_data tool to ensure the data is loaded
2. Then use the query_customer_data tool with an appropriate SQL query to find the answer
3. Finally, provide a clear, concise answer to the user's question

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
"""

prompt = PromptTemplate.from_template(prompt_template)




from langchain.agents import Tool, AgentExecutor, create_react_agent

# Create the agent
agent = create_react_agent(
    llm=llm_multi_chain,
    tools=tools,
    prompt=prompt
)

# Create the agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

def process_user_question(question):
    """Process a user question about customer data."""
    return agent_executor.invoke({"input": question})

# Example
result = process_user_question("What is the customer ID for Alice and where does he live and what is the age of charlie?")
print(result)



from databricks import sql
import os

# Set up connection parameters
server_hostname = "your-workspace-url.cloud.databricks.com"  # Your workspace URL
http_path = "/sql/1.0/warehouses/your-warehouse-id"  # Your SQL warehouse HTTP path
access_token = "your-personal-access-token"  # Your PAT token

# Alternative: Use environment variables for security
# server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
# http_path = os.getenv("DATABRICKS_HTTP_PATH") 
# access_token = os.getenv("DATABRICKS_TOKEN")

# Connect to Databricks
connection = sql.connect(
    server_hostname=server_hostname,
    http_path=http_path,
    access_token=access_token
)

# Execute your query
cursor = connection.cursor()
catalog_name = "your_catalog"  # Replace with your catalog
schema_name = "your_schema"    # Replace with your schema
table_name = "sample_naveen"

query = f"SELECT * FROM {catalog_name}.{schema_name}.{table_name}"
cursor.execute(query)

# Fetch and display results
results = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]

# Convert to pandas DataFrame for better display
import pandas as pd
df = pd.DataFrame(results, columns=columns)
print(df)

# Close connection
cursor.close()
connection.close()

``````````````````````````````````````````````````````````````

def send_email_via_logic_app(
    self,
    error_message: str,
    suggestion: str,
    workspace_name: str,
    workspace_link: str,
    job_name: str,
    job_link: str,
    job_run_id: str,
    job_run_link: str,
    task_run_name: str,
    task_run_link: str,
    status: str,
    started_at: str,
    duration: str,
    launched_by: str,
    view_run_link: str
):
    import requests

    logic_app_email_url = "https://sendemailwithllmsuggestion.azurewebsites.net:443/..."  # Replace with yours

    # map status with color + icons
    status_icon = "❌" if status.lower() == "failed" else "✅"
    status_color = "#b00020" if status.lower() == "failed" else "#228B22"   # red or green

    html_body = f"""
    <html>
        <body style="font-family:Arial, sans-serif; color:#333;">
            <h2 style="color:{status_color};">{status_icon} A job run has terminated with the error: in Azure Databricks</h2>
            
            <p><strong>Message:</strong><br>
            <span style="color:{status_color};">&#x26A0; {error_message}</span></p>

            <h3>Run details</h3>
            <table cellspacing="0" cellpadding="6" style="border-collapse:collapse; width:100%;">
                <tr>
                    <td style="font-weight:bold; width:150px;">Workspace</td>
                    <td><a href="{workspace_link}">{workspace_name}</a></td>
                </tr>
                <tr>
                    <td style="font-weight:bold;">Job</td>
                    <td><a href="{job_link}">{job_name}</a></td>
                </tr>
                <tr>
                    <td style="font-weight:bold;">Job run</td>
                    <td><a href="{job_run_link}">{job_run_id}</a></td>
                </tr>
                <tr>
                    <td style="font-weight:bold;">Task run</td>
                    <td><a href="{task_run_link}">{task_run_name}</a></td>
                </tr>
                <tr>
                    <td style="font-weight:bold;">Status</td>
                    <td style="color:{status_color};">{status_icon} {status}</td>
                </tr>
                <tr>
                    <td style="font-weight:bold;">Started at</td>
                    <td>{started_at}</td>
                </tr>
                <tr>
                    <td style="font-weight:bold;">Duration</td>
                    <td>{duration}</td>
                </tr>
                <tr>
                    <td style="font-weight:bold;">Launched</td>
                    <td>{launched_by}</td>
                </tr>
            </table>

            <br>
            <p>
                <a href="{view_run_link}" 
                   style="display:inline-block; padding:10px 20px; background:#0078d4; color:white; 
                          text-decoration:none; border-radius:4px;">
                   View run in Databricks &gt;
                </a>
            </p>

            <hr>
            <p><strong>Suggestion:</strong><br>{suggestion}</p>
        </body>
    </html>
    """

    payload = {
        "subject": f"Databricks Job {status} Alert",
        "body": html_body
    }

    response = requests.post(logic_app_email_url, json=payload)
    return f"📧 Logic App Email Status: {response.status_code} - {response.text}"


    `````````````````````````````

    def send_email_via_logic_app(self, error_message: str, suggestion: str):
    import requests

    logic_app_email_url = "https://sendemailwithllmsuggestion.azurewebsites.net:443/..."  # your endpoint

    # HTML email body
    html_body = f"""
    <html>
        <body style="font-family:Arial, sans-serif; color:#333;">
            <h2 style="color:#b00020;">❌ A job run has terminated with the error: in Azure Databricks</h2>
            <p><strong>Message:</strong><br>
            <span style="color:#b00020;">&#x26A0; {error_message}</span></p>

            <h3>Run details</h3>
            <table cellspacing="0" cellpadding="6" style="border-collapse:collapse; width:100%;">
                <tr>
                    <td style="font-weight:bold; width:150px;">Workspace</td>
                    <td><a href="https://placeholder.workspace.link">CDS-DS-DATABRICKS-001-D</a></td>
                </tr>
                <tr>
                    <td style="font-weight:bold;">Job</td>
                    <td><a href="https://placeholder.job.link">Databricks Diagnostics One Model</a></td>
                </tr>
                <tr>
                    <td style="font-weight:bold;">Job run</td>
                    <td><a href="https://placeholder.jobrun.link">940987857908224</a></td>
                </tr>
                <tr>
                    <td style="font-weight:bold;">Task run</td>
                    <td><a href="https://placeholder.taskrun.link">Databricks_Failure_Log_One_Model</a></td>
                </tr>
                <tr>
                    <td style="font-weight:bold;">Status</td>
                    <td style="color:#b00020;">❌ Failed</td>
                </tr>
                <tr>
                    <td style="font-weight:bold;">Started at</td>
                    <td>2025-08-26 12:49:43 UTC</td>
                </tr>
                <tr>
                    <td style="font-weight:bold;">Duration</td>
                    <td>16s</td>
                </tr>
                <tr>
                    <td style="font-weight:bold;">Launched</td>
                    <td>By retry scheduler</td>
                </tr>
            </table>

            <br>
            <p><a href="https://placeholder.viewrun.link" 
                  style="display:inline-block; padding:10px 20px; background:#0078d4; color:white; 
                         text-decoration:none; border-radius:4px;">View run in Databricks &gt;</a></p>

            <hr>
            <p><strong>Suggestion:</strong><br>{suggestion}</p>
        </body>
    </html>
    """

    payload = {
        "subject": "Databricks Job Failure Alert",
        "body": html_body
    }

    response = requests.post(logic_app_email_url, json=payload)
    return f"📧 Logic App Email Status: {response.status_code} - {response.text}"













1````````````````````````````````````````````````````````````````````````````

PIPELINE_ERROR_AGENT_PROMPT = """
You are an expert Pipeline Error Analysis Agent specialized in Databricks pipeline troubleshooting.

STRICT EXECUTION SEQUENCE (DO NOT VIOLATE):
1. FIRST ACTION (MANDATORY): save_ai_suggestion
   - Generate a complete AI suggestion **in structured format**:
     Root Cause: [Explain the error cause clearly]
     Approach: [Method of analyzing or investigating the issue]
     Solution Steps: [Step-by-step remediation steps]
   - Then save this section to Delta table using save_ai_suggestion.

2. REMEDIATION ACTIONS (1–2 ONLY): 
   - Choose the most relevant remediation tool(s) based on your AI suggestion output.
   - If first remediation succeeds → immediately send email with details.
   - If it fails → acknowledge failure, continue with next remediation.
   - If both remediations fail → send email describing AI suggestions + attempted actions, ask for manual follow-up.
   - NEVER retry the same action in a loop.

3. FINAL ACTION (MANDATORY): save_ai_actions
   - Save the exact list of actions performed (success/failure included).

IMPORTANT RULES:
- ALWAYS begin with save_ai_suggestion (default first action).
- ALWAYS end with save_ai_actions (default last action).
- STRICTLY follow structured format for AI Suggestion (Root Cause, Approach, Solution Steps).
- Mail should only be sent after:
   * FIRST SUCCESSFUL remediation OR
   * After two failed remediations → with summary of failures.

AVAILABLE REMEDIATION TOOLS:
{tools}

Tool Names:
{tool_names}

STRICT RESPONSE FORMAT (must always follow):
Thought: [Analysis or reasoning for current step]
Action: [Tool name]
Action Input: [Input passed to tool]
Observation: [Result from tool]

Final Answer: [Clear summary of AI suggestions, remediation results, and final conclusion]
"""




actions
```````
def _save_ai_suggestion(self, ai_suggestion: str) -> str:
    """Save AI suggestion (root cause, approach, solution steps) into Delta"""
    try:
        # Validation
        if not self.workspace_client:
            return "❌ Cannot save suggestion: Workspace client not available"
        if not self.current_run_id:
            return "❌ Cannot save suggestion: No run_id set"

        # Table config
        catalog_name = "udm_tests"
        schema_name = "cdmebxpost"
        table_name = "classified_errors_new"
        warehouse_id = "aa8ca9405a7cb961"

        # Ensure mandatory structure
        if not all(x in ai_suggestion for x in ["Root Cause:", "Approach:", "Solution Steps:"]):
            ai_suggestion = f"""
            Root Cause: [Missing root cause info, please improve prompt]
            Approach: [Missing approach info, please improve prompt]
            Solution Steps: {ai_suggestion.strip()}
            """

        cleaned_suggestion = ai_suggestion.replace("'", "''").strip()

        update_sql = f"""
        UPDATE {catalog_name}.{schema_name}.{table_name}
        SET ai_suggestion = '{cleaned_suggestion}',
            is_processed = true,
            processed_timestamp = current_timestamp()
        WHERE run_id = '{self.current_run_id}'
        AND (is_processed = false OR is_processed IS NULL)
        """

        logger.info(f"Saving AI suggestion for run_id {self.current_run_id}")
        result = self.workspace_client.statement_execution.execute_statement(
            statement=update_sql, warehouse_id=warehouse_id
        )

        if result.status.state._name_ == 'SUCCEEDED':
            return f"✅ AI suggestion saved successfully for run {self.current_run_id}"
        return f"❌ Failed to save AI suggestion. Query status: {result.status.state._name_}"

    except Exception as e:
        logger.error(f"Error saving AI suggestion: {str(e)}")
        return f"❌ Error saving AI suggestion: {str(e)}"


  def _save_ai_actions(self, actions_performed: list) -> str:
    """
    Save list of actions performed with their status into Delta.
    Example: ["retry_pipeline:failed", "switch_cluster:success"]
    """
    try:
        if not self.workspace_client:
            return "❌ Cannot save actions: Workspace client not available"
        if not self.current_run_id:
            return "❌ Cannot save actions: No run_id set"

        catalog_name = "udm_tests"
        schema_name = "cdmebxpost"
        table_name = "classified_errors_new"
        warehouse_id = "aa8ca9405a7cb961"

        cleaned_actions = ",".join([a.replace("'", "''") for a in actions_performed])

        update_sql = f"""
        UPDATE {catalog_name}.{schema_name}.{table_name}
        SET ai_actions = '{cleaned_actions}',
            processed_timestamp = current_timestamp()
        WHERE run_id = '{self.current_run_id}'
        AND is_processed = true
        """

        logger.info(f"Saving AI actions for run_id {self.current_run_id}")
        result = self.workspace_client.statement_execution.execute_statement(
            statement=update_sql, warehouse_id=warehouse_id
        )

        if result.status.state._name_ == 'SUCCEEDED':
            return f"✅ AI actions saved successfully for run {self.current_run_id}"
        return f"❌ Failed to save AI actions. Status: {result.status.state._name_}"

    except Exception as e:
        logger.error(f"Error saving AI actions: {str(e)}")
        return f"❌ Error saving AI actions: {str(e)}"



    def retry_pipeline(self, action_input: str = None) -> str:
    run_id = self.current_run_id
    if not run_id:
        return "❌ retry_pipeline: No run_id available"

    try:
        warehouse_id = "aa8ca9405a7cb961"
        sql_query = f"SELECT job_id FROM udm_tests.cdmebxpost.all_runs_status WHERE run_id = '{run_id}' LIMIT 1"
        
        result = self.workspace_client.statement_execution.execute_statement(
            statement=sql_query, warehouse_id=warehouse_id
        )

        if result.status.state._name_ != 'SUCCEEDED' or not result.result.data_array:
            return f"❌ retry_pipeline: No job_id found for run_id {run_id}"

        job_id = result.result.data_array[0][0]
        run = self.workspace_client.jobs.run_now(job_id=job_id)

        return f"✅ retry_pipeline: Triggered job {job_id} for run_id {run_id}, new run {run.run_id}"

    except Exception as e:
        logger.error(f"retry_pipeline error: {str(e)}")
        return f"❌ retry_pipeline failed: {str(e)}"


      def send_email_via_logic_app(self, status="FAILED", ai_suggestion=None, ai_actions=None) -> str:
    try:
        # Format AI suggestion
        formatted_html = self.format_text_to_html(ai_suggestion or "None")

        payload = {
            "subject": f"Databricks Job {status} Alert",
            "body": f"""
            <html>
            <body>
              <h2 style="color:#0078d4;">Databricks Job {status}</h2>
              <h3>AI Suggestion</h3>
              {formatted_html}
              <h3>AI Actions Performed</h3>
              <p>{ai_actions or 'None'}</p>
            </body>
            </html>
            """
        }

        response = requests.post(self.logic_app_url, json=payload)
        return f"📨 Email sent: {response.status_code} {response.text}"

    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return f"❌ Failed to send email: {str(e)}"


      def format_text_to_html(self, text: str) -> str:
    """Ensure suggestion text is always structured with headers + steps"""
    if not text or not text.strip():
        return "<p>No suggestion available</p>"

    html = ""
    parts = {"Root Cause:": "", "Approach:": "", "Solution Steps:": ""}

    for key in parts.keys():
        if key in text:
            section = text.split(key, 1)[1]
            next_keys = [k for k in parts.keys() if k != key and k in section]
            if next_keys:
                # Take until next section
                next_key = min(section.find(k) for k in next_keys if section.find(k) != -1)
                section = section[:next_key]
            parts[key] = section.strip()

    for key, value in parts.items():
        if key == "Solution Steps:":
            html += f"<h3>{key}</h3>{self.format_numbered_steps(value)}"
        else:
            html += f"<h3>{key}</h3><p>{value}</p>"

    return html









    ````````````````````````````````````````````````````````````````

    def format_text_to_html(self, suggestion: dict) -> str:
    """
    Convert structured AI suggestion (dict) into formatted HTML.
    suggestion = {
       "Root Cause": "...",
       "Approach": "...",
       "Solution Steps": "1) step one 2) step two"
    }
    """
    if not suggestion or not isinstance(suggestion, dict):
        return "<p>No AI Suggestions available</p>"

    html = ""

    # Root Cause
    root = suggestion.get("Root Cause", "").strip()
    if root:
        html += f"<h3>Root Cause</h3><p>{root}</p>"

    # Approach
    approach = suggestion.get("Approach", "").strip()
    if approach:
        html += f"<h3>Approach</h3><p>{approach}</p>"

    # Solution Steps
    steps = suggestion.get("Solution Steps", "").strip()
    if steps:
        html += f"<h3>Solution Steps</h3>{self.format_numbered_steps(steps)}"

    return html or "<p>No valid suggestion found</p>"


def format_actions_to_html(self, ai_actions: list) -> str:
    """
    Convert list of AI actions into HTML.
    ai_actions = [
       {"action": "retry_pipeline", "status": "failed", "message": "No job found"},
       {"action": "switch_cluster", "status": "success", "message": "Switched cluster and restarted job"}
    ]
    """
    if not ai_actions or not isinstance(ai_actions, list):
        return "<p>No remediation actions recorded</p>"

    html = "<h3>AI Actions Taken</h3><ol>"
    for a in ai_actions:
        action = a.get("action", "unknown")
        status = a.get("status", "unknown")
        message = a.get("message", "")
        status_icon = "✅" if status.lower() == "success" else "❌"
        html += f"<li>{status_icon} <b>{action}</b> → {status}<br><small>{message}</small></li>"
    html += "</ol>"

    return html




    def format_numbered_steps(self, steps_text: str) -> str:
    """
    Extract and format numbered steps from plain text into <ol>.
    Handles inputs like "1) step one, 2) step two" or "1. step one 2. step two".
    """
    if not steps_text:
        return "<p>No steps provided</p>"

    parts = re.split(r"(?:\d+\)|\d+\.)", steps_text)
    steps = [p.strip() for p in parts if p.strip()]

    if steps:
        html = "<ol>"
        for step in steps:
            html += f"<li>{step}</li>"
        html += "</ol>"
        return html

    return f"<p>{steps_text}</p>"


    def format_paragraphs(self, text: str) -> str:
    """
    Break long text into paragraphs for better readability.
    """
    if not text:
        return "<p>No content</p>"

    sentences = text.split(". ")
    paragraphs, current_para = [], []

    for i, s in enumerate(sentences):
        sentence = s.strip()
        if not sentence:
            continue
        if not sentence.endswith("."):
            sentence += "."
        current_para.append(sentence)

        if len(current_para) >= 2:
            paragraphs.append(" ".join(current_para))
            current_para = []

    if current_para:
        paragraphs.append(" ".join(current_para))

    html = ""
    for p in paragraphs:
        html += f'<p style="margin-bottom:12px; line-height:1.5;">{p}</p>'

    return html

    def send_email_via_logic_app(self, status="FAILED", ai_suggestion=None, ai_actions=None):
    try:
        # ai_suggestion = dict
        suggestion_html = self.format_text_to_html(ai_suggestion or {})
        # ai_actions = list of dict
        actions_html = self.format_actions_to_html(ai_actions or [])

        payload = {
            "subject": f"Databricks Job {status} Alert",
            "body": f"""
            <html><body>
              <h2 style='color:#0078d4;'>Databricks Job {status}</h2>
              {suggestion_html}
              {actions_html}
            </body></html>
            """
        }
        response = requests.post(self.logic_app_url, json=payload)
        return f"📨 Email sent: {response.status_code} {response.text}"

    except Exception as e:
        return f"❌ Email failed: {str(e)}"
