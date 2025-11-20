from databricks.labs.dqx.profiler.profiler import DQProfiler
from databricks.labs.dqx.profiler.generator import DQGenerator
from databricks.labs.dqx.engine import DQEngine,FileChecksStorageConfig
from databricks.sdk import WorkspaceClient

ws = WorkspaceClient()

# Step 1: Profile the data to generate statistics-based (technical) rules
profiler = DQProfiler(ws)
input_df = spark.read.table("example.quality_data.experiments")
summary_stats, profiles = profiler.profile(input_df)

generator = DQGenerator(ws)

# Generate profiler-based rules
profiler_checks = generator.generate_dq_rules(profiles)

# Step 2: Generate business logic rules using AI
business_requirements = """

-Name should not start with 'system'.
-All names must have a valid versions attached.
-All latest versions must have a user identifier attached.

"""

ai_checks = generator.generate_dq_rules_ai_assisted(
    user_input=business_requirements,
    table_name="example.quality_data.experiments"
)

# Step 3: Combine both sets of rules
all_checks = profiler_checks + ai_checks

# Step 4: Save combined checks
dq_engine = DQEngine(ws)
dq_engine.save_checks(
  checks=all_checks,
  config=FileChecksStorageConfig(
    location="/dbfs/tmp/quality_checks.json"
  )
)

print(f"Combined {len(profiler_checks)} profiler rules with {len(ai_checks)} AI rules")
print(f"Total: {len(all_checks)} quality checks")


def update_delta_table_of_dq_rules(config_df):
    """
    Updates a Delta table with new configurations from a DataFrame.

    This function checks if a Delta table exists. If it does, it merges the new configurations
    from the provided DataFrame into the existing Delta table. If the table does not exist, it
    creates a new Delta table with the provided configurations.

    Args:
        config_df (DataFrame): A Spark DataFrame containing the new configurations to be merged
                               into the Delta table.

    Returns:
        None
    """
    table_name = "default.dqx_quality_checks_configs"

    try:
        delta_table = spark.table(table_name)
        #display(delta_table)
    except AnalysisException:
        # If the table does not exist or is not a Delta table, create it as a Delta table
        config_df.write.format("delta").mode("overwrite").saveAsTable(table_name)
        delta_table = spark.table(table_name)

    delta_table = DeltaTable.forName(spark, table_name)

    delta_table.alias("target").merge(
        config_df.alias("source"),
        "target.table_name = source.table_name"  # Replace with your actual join condition
    ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
    display(spark.table(table_name))


spark.sql("USE CATALOG example")
sample_size = 100000
config_df = generate_dqx_rules_parallel("quality_data", sample_size)

update_delta_table_of_dq_rules(config_df)

```````````````````````````








import os
from databricks.connect import DatabricksSession

print("HOST:", os.getenv("DATABRICKS_HOST"))
print("CLUSTER:", os.getenv("DATABRICKS_CLUSTER_ID"))
print("WAREHOUSE:", os.getenv("DATABRICKS_SERVERLESS_SQL_WAREHOUSE_ID"))

spark = DatabricksSession.builder.getOrCreate()
print("Spark version:", spark.version)

df = spark.range(5)
df.show()



from databricks.labs.dqx.config import LLMModelConfig
from databricks.labs.dqx.profiler.generator import DQGenerator
from databricks.sdk import WorkspaceClient

# Configure LLM model
llm_config = LLMModelConfig(
    model_name="databricks/databricks-claude-sonnet-4-5",
    # api_key and api_base are optional for foundation models
)

# Initialize the generator
ws = WorkspaceClient()
generator = DQGenerator(workspace_client=ws, llm_model_config=llm_config,custom_check_functions=None)

# Generate rules from natural language description
user_input = """
name should not start with 'system'.
All names must have a valid versions attached.
All latest versions must have a user identifier attached.
"""

checks = generator.generate_dq_rules_ai_assisted(user_input=user_input,table_name='example.quality_data.experiments')

print(checks)

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



````````````````````````````````````

PIPELINE_ERROR_AGENT_PROMPT = """
You are an expert Pipeline Error Analysis Agent specialized in Databricks pipeline troubleshooting.

STRICT EXECUTION SEQUENCE (MANDATORY):
1. FIRST ACTION: Always call `save_ai_suggestion` immediately.
   - The Action Input must STRICTLY be a JSON object containing:
       {
         "Root Cause": "...",
         "Approach": "...",
         "Solution Steps": "1. ..., 2. ..."
       }
   - Save this using save_ai_suggestion.

2. REMEDIATION ACTIONS (1–2 ONLY):
   - Choose the most relevant remediation tool(s) based on the saved AI suggestion.
   - If first remediation succeeds → immediately call `send_email`.
   - If first fails → attempt one more remediation.
   - If both fail → call `send_email` with status FAILED.
   - NEVER repeat the same tool in a loop.

3. FINAL ACTION: Always call `save_ai_actions`.
   - Include full list of attempted actions with success/failure in JSON format.

IMPORTANT RULES:
- "Thought:" is ONLY for reasoning which tool to use next.
- DO NOT put Root Cause, Approach, or Solution Steps directly in Thought.
- AI Suggestions MUST only appear inside Action Input of `save_ai_suggestion`.
- EVERY Thought MUST be immediately followed by Action and Action Input.
- Action Input MUST always be STRICT JSON (double quotes only).
- NEVER use single quotes, never output Python dicts.
- If no content exists, use empty JSON {}.

AVAILABLE TOOLS:
{tools}

Tool Names:
{tool_names}

STRICT OUTPUT FORMAT (MANDATORY):
Thought: [Reasoning about which tool to call next]
Action: [Tool name]
Action Input: [Valid JSON object with double quotes]
Observation: [Tool result]

Final Answer: [Clear summary of root cause, approach, steps, actions, outcome]

---

⚠️ EXAMPLE FORMAT (follow exactly):

Thought: I should first save my AI suggestion.
Action: save_ai_suggestion
Action Input: {
  "Root Cause": "Cluster ran out of memory",
  "Approach": "Check cluster size and retry or move to larger cluster",
  "Solution Steps": "1. Retry the pipeline, 2. Switch to a larger cluster"
}
Observation: ✅ Suggestion saved successfully

Thought: Since retrying is the simplest remediation, I should try that next.
Action: retry_pipeline
Action Input: {"reason":"Retrying job execution"}
Observation: ❌ Retry failed due to cluster OOM again.

Thought: Retry failed, I should now switch cluster.
Action: switch_cluster
Action Input: {"reason":"Move workload to larger serverless cluster"}
Observation: ✅ Cluster switched and job restarted.

Thought: I must now record the actions performed.
Action: save_ai_actions
Action Input: [
  {"action":"retry_pipeline","status":"failed","message":"Retry OOM"},
  {"action":"switch_cluster","status":"success","message":"Switched to serverless"}
]
Observation: ✅ Actions saved

Thought: Finally, I should send an email with the results.
Action: send_email
Action Input: {
  "status": "SUCCESS",
  "ai_suggestion": {
      "Root Cause":"Cluster OOM",
      "Approach":"Scale cluster",
      "Solution Steps":"1. Retry pipeline, 2. Switch cluster"
  },
  "ai_actions":[
      {"action":"retry_pipeline","status":"failed","message":"Retry OOM"},
      {"action":"switch_cluster","status":"success","message":"Switched to serverless"}
  ]
}
Observation: 📨 Email sent successfully

Final Answer: AI suggestion and remediation applied. Retry failed, cluster switch succeeded, job restarted, email sent.
---

Question: {input}
Thought: {agent_scratchpad}
"""

```````````````````


PIPELINE_ERROR_AGENT_PROMPT = """
You are an expert Pipeline Error Analysis Agent specialized in Databricks pipeline troubleshooting.

STRICT EXECUTION SEQUENCE (MANDATORY):
1. FIRST ACTION: Always call `save_ai_suggestion` immediately.
   - The Action Input MUST STRICTLY be a JSON object with keys:
       {
         "Root Cause": "...",
         "Approach": "...",
         "Solution Steps": "1. ..., 2. ..."
       }
   - Save this using save_ai_suggestion.

2. REMEDIATION ACTIONS (1–2 ONLY):
   - Choose the remediation tool(s) based on your AI suggestion.
   - If the first remediation succeeds → immediately call `send_email` with status SUCCESS.
   - If the first fails → attempt a second remediation.
   - If both fail → call `send_email` with status FAILED.
   - NEVER repeat the same tool in a loop.

3. FINAL ACTION: Always call `save_ai_actions`.
   - Input = JSON list of attempted actions with their status and message.

IMPORTANT RULES:
- "Thought:" MUST only contain reasoning about which tool to use next.
- DO NOT include Root Cause, Approach, or Solution Steps inside Thought.
- AI Suggestions MUST only appear inside Action Input of save_ai_suggestion.
- EVERY Thought MUST be immediately followed by Action and Action Input.
- Action Input MUST always be VALID JSON with double quotes ("...").
- Do NOT output Python dicts or use single quotes.
- If no data exists, use {}.

AVAILABLE TOOLS:
{tools}

Tool Names:
{tool_names}

STRICT OUTPUT FORMAT (MANDATORY):
Thought: [Brief reasoning about which tool to use next]
Action: [Tool name]
Action Input: [Valid JSON object]
Observation: [Result from tool]

Final Answer: [Summary of root cause, approach, remediation, and outcome]

---

⚠️ FORMAT EXAMPLES (for syntax ONLY, not actual tool choices):

Thought: I should record the AI suggestion now.
Action: save_ai_suggestion
Action Input: {
  "Root Cause": "Cluster ran out of memory",
  "Approach": "Check cluster size and adjust",
  "Solution Steps": "1. Retry pipeline, 2. Use bigger cluster"
}
Observation: ✅ Suggestion saved

Thought: Since one remediation is retrying, I should try that.
Action: retry_pipeline
Action Input: {"reason": "Retry pipeline execution"}
Observation: ❌ Retry failed

Thought: I need to record the actions performed.
Action: save_ai_actions
Action Input: [
  {"action": "retry_pipeline", "status": "failed", "message": "Retry did not resolve OOM"}
]
Observation: ✅ Actions saved

Thought: I should inform via email.
Action: send_email
Action Input: {
  "status": "FAILED",
  "ai_suggestion": {"Root Cause":"...", "Approach":"...", "Solution Steps":"..."},
  "ai_actions":[{"action":"retry_pipeline","status":"failed","message":"Retry did not resolve OOM"}]
}
Observation: 📨 Email sent successfully

⚠️ These are only FORMAT EXAMPLES.
Do NOT copy the same tool sequence. Choose tools dynamically based on the actual error context.

---

Question: {input}
Thought: {agent_scratchpad}
"""



````````````````````````````````````````````
sample = """
---
DocumentType: JobFailureReport
DocumentVersion: 1.0.0
CreatedBy: siva.kumar@example.com
CreatedAt: 2025-09-17T08:45:12Z
Environment: prod
TeamOwner: DataEngineering
DatabricksJobID: job-12345
DatabricksRunID: run-20250917-01
ServiceNowTicket: SNOW-2025-234
Severity: High
FailureType: Timeout
Tags: databricks,parquet,schema-regression
DataSensitivity: Internal
Filename: prod_DataEngineering_JobFailureReport_job-12345_20250917_v1.0.0.md
---
### Job Failure Report — Sample (for SharePoint)

#### Metadata
- DocumentType: JobFailureReport
- DocumentVersion: 1.0.0
- CreatedBy: siva.kumar@example.com
- CreatedAt: 2025-09-17T08:45:12Z
- Environment: prod
- TeamOwner: DataEngineering
- DatabricksJobID: job-12345
- DatabricksRunID: run-20250917-01
- ServiceNowTicket: SNOW-2025-234
- Severity: High
- FailureType: Timeout
- Tags: databricks, parquet, schema-regression
- DataSensitivity: Internal

#### Short summary
A scheduled Databricks job (job-12345) timed out while processing parquet partition date=2025-09-17, delaying downstream analytics dashboards by approximately 3 hours.

#### Full description
At 2025-09-17T07:30:00Z the nightly run for job-12345 started. Around 07:33:14Z multiple executors began failing with TaskKilled and network timeout errors. The driver retried tasks until the job ultimately timed out at 08:40:00Z. Affected dataset: s3://prod-bucket/data/events/date=2025-09-17. Business impact: nightly dashboards were not refreshed and dependent pipelines experienced delays.

#### Reproduction steps
1. Trigger job-12345 with partition date=2025-09-17 via the scheduler.
2. Monitor stage 4 map tasks processing parquet files — failures typically appear within 2–4 minutes of task start.
3. Inspect executor and driver logs for GC pauses and network timeout traces.

#### Logs & Artifacts
- Error snippet (excerpted from executor logs; timestamps aligned with failures):
    java.util.concurrent.TimeoutException: Task timed out after 120000 ms
        at com.databricks.spark...
        at org.apache.spark.scheduler.Task...
        at org.apache.spark.executor.Executor...

- Full logs (compressed): /RAG-Context/sharepoint/prod/DataEngineering/databricks/job-failures/prod_DataEngineering_JobFailureReport_job-12345_20250917_v1.0.0_logs.txt
- Cluster config: 8 workers (r5.2xlarge), spark.executor.memory=30g, spark.executor.cores=4
- Job config: attached job-12345-config.json (link in attachments)
- Sample failing input path: s3://prod-bucket/data/events/date=2025-09-17/part-0001.parquet
- GC log excerpt: long young-gen pauses observed at 07:33:10Z–07:33:40Z aligned to task failures

#### Root cause analysis
Hypothesis: Upstream schema drift introduced nested field type changes in parquet files for column "event.details", increasing deserialization cost and causing extended GC pauses which led to task timeouts. Evidence: parquet footers show mismatched types for "event.details", GC logs show long young-gen pauses that correlate with task failures, and executor heap usage spikes before timeout events.

#### Mitigation & Recommended Fixes
- Short-term (P0): Re-run the job with increased executor memory and extended task timeout; temporarily reroute downstream refresh to the last successful snapshot. Owner: DataEngineering. ETA: 2 hours.
- Medium-term (P1): Add schema enforcement and pre-job schema validation step in ingestion pipeline; add alerting for schema drift. Owner: IngestionTeam. ETA: 2 weeks.
- Long-term (P2): Implement schema-regression tests for producers, producer-side schema checks, and automated blocking of incompatible schema writes. Owner: Platform. ETA: 1 quarter.

#### Related items & references
- ServiceNow: SNOW-2025-234 — https://servicenow.example.com/SNOW-2025-234
- PR: https://github.com/org/repo/pull/456
- Dataset contract: /datasets/events/contract.md
- Monitoring alert: grafana.company/alerts/alert-789

#### Search keywords
databricks, job-12345, timeout, parquet, schema-drift, gc, task-timeout

#### RAG context snippet
Job job-12345 (prod) timed out on 2025-09-17 while processing parquet partition date=2025-09-17. Logs indicate a schema mismatch for column "event.details" and prolonged GC pauses; immediate recommendation is to re-run with larger executors and increase task timeouts while implementing upstream schema validation.

#### Chunking & Embedding hints
- Suggested chunk size: 400–800 words per chunk
- Preferred split boundaries: split after Logs & Artifacts, after Reproduction steps, after Mitigation
- EmbeddingVersion: v1.0

#### File naming convention (used)
prod_DataEngineering_JobFailureReport_job-12345_20250917_v1.0.0.md

#### Folder (SharePoint)
 /RAG-Context/sharepoint/prod/DataEngineering/databricks/job-failures/prod_DataEngineering_JobFailureReport_job-12345_20250917_v1.0.0.md

#### Access & Permissions
- Read: DataEngineering, Analytics, Platform
- Edit: DataEngineering
- Retention policy: 1 year
- PII present: No

#### Version history & change log
- v1.0.0 — siva.kumar — 2025-09-17 — initial upload

#### Checklist before upload
- [x] Metadata filled
- [x] Filename follows pattern
- [x] Document placed in correct folder
- [x] Log snippets & links included
- [x] RAG context snippet present
- [x] Sensitive data redacted or flagged (none)

#### Notes / uploader guidance
- Keep raw logs as separate attachments (link them under Logs & Artifacts) and keep only key excerpts in the main document to keep RAG snippets concise.
- Ensure the YAML frontmatter remains at the very top of the file for automated parsers.
- Use the exact filename and folder structure to allow ingestion pipelines to map documents to Databricks Job IDs and ServiceNow tickets.
- Flag any PII explicitly and avoid pasting PII directly into logs or samples.

"""

`````````````````````````````

BASELINE_TABLE_GENERATOR_PROMPT = """
You are a data quality assistant that synthesizes baseline tables for drift checks.

Your task:
- Generate a synthetic baseline table that:
  - Matches exactly the provided schema (column names, order, and data types).
  - Respects all dynamic characteristics and constraints provided by the user.
  - Produces realistic but fabricated values guided by the sample rows when helpful.
- Do NOT generate code, instructions, or explanations.
- Output ONLY the table, in a parseable format.

OUTPUT CONTRACT (STRICT):
- Format: CSV without index, with a single header row.
- Delimiter: comma.
- Quote fields containing commas with double quotes.
- Null representation: empty field (,,) unless a rule forbids nulls.
- Datetime: ISO 8601 UTC as YYYY-MM-DDTHH:MM:SSZ unless schema specifies otherwise.
- Date: YYYY-MM-DD.
- Boolean: true/false.
- Numeric: no thousands separators; dot as decimal point.
- Row count: 100–200 rows unless dynamic characteristics specify otherwise.
- Column order: exactly as in the schema input.
- No text before or after the CSV. No code fences. No explanations.

Conflict handling:
- If a dynamic characteristic conflicts with the schema (e.g., "no nulls" but a column is nullable),
  keep types and constraints from the schema authoritative while satisfying the rule as closely as possible.
- If a rule cannot be fully satisfied, pick the closest valid alternative and continue.

Sampling guidance:
- Use the provided sample rows to infer realistic distributions, categories, ranges, formats, and patterns.
- Do not copy sample values verbatim for identifiers or sensitive fields; synthesize similar-looking values.

Keys and relations:
- Respect primary keys and uniqueness if the schema specifies them.
- For foreign keys, fabricate plausible parent values that maintain referential consistency.

INPUTS YOU WILL RECEIVE:
Schema information:
{schema_table}

Sample data (up to 100 rows):
{sample_data}

Dynamic characteristics and rules to apply:
{dynamic_characteristics}

INSTRUCTIONS TO EXECUTE:
- Generate the baseline table now following the OUTPUT CONTRACT exactly.
- Remember: Output CSV only, no explanations, no markdown, no code fences.
"""

``````````````````````

BASELINE_TABLE_GENERATOR_PROMPT = """
You are a data quality assistant that synthesizes baseline tables for drift checks.

Your task:
- Generate a synthetic baseline table that:
  - Matches exactly the provided schema (column names, order, and data types).
  - STRICTLY satisfies all dynamic characteristics and constraints provided by the user.
  - Produces realistic but fabricated values guided by the sample rows when helpful.
- Do NOT generate code, instructions, or explanations.
- Output ONLY the table, in a parseable format.

OUTPUT CONTRACT (STRICT):
- Format: CSV without index, with a single header row.
- Delimiter: comma.
- Quote fields containing commas with double quotes.
- Null representation: empty field (,,) unless a rule forbids nulls.
- Datetime: ISO 8601 UTC as YYYY-MM-DDTHH:MM:SSZ unless schema specifies otherwise.
- Date: YYYY-MM-DD.
- Boolean: true/false.
- Numeric: no thousands separators; dot as decimal point.
- Row count target: 100–200 rows unless the dynamic characteristics specify otherwise.
- Column order: exactly as in the schema input.
- IMPORTANT: Emit only COMPLETE rows. If you run out of tokens, STOP BEFORE starting an incomplete row.
  - Guarantee that every emitted line after the header has the exact number of columns.
  - Do NOT output any partially written row or trailing comma at end.
- No text before or after the CSV. No code fences. No explanations.

RULE ADHERENCE (MANDATORY):
- Enforce dynamic characteristics exactly. Example: if asked for "today only" dates, all date/datetime columns constrained by that rule MUST be on today's date in the specified timezone/format; if "no nulls", ensure every column value is present and type-valid.
- If multiple rules apply, satisfy all simultaneously without violating the schema types.
- If a rule cannot be fully satisfied due to schema constraints, choose the closest valid alternative and continue, but NEVER violate data types or required uniqueness.

Sampling guidance:
- Use the provided sample rows to infer realistic distributions, categories, ranges, formats, and patterns.
- Do not copy sample values verbatim for identifiers or sensitive fields; synthesize similar-looking values.

Keys and relations:
- Respect primary keys and uniqueness if the schema specifies them.
- For foreign keys, fabricate plausible parent values that maintain referential consistency.

VALIDATION BEFORE EMITTING:
- Internally verify that every data row:
  - Has the exact number of columns in the schema order.
  - Satisfies all dynamic characteristics (e.g., dates within requested window, no nulls if requested, uniqueness if required).
- If any generated row would be incomplete due to length limits, omit it entirely.

INPUTS YOU WILL RECEIVE:
Schema information:
{schema_table}

Sample data (up to 100 rows):
{sample_data}

Dynamic characteristics and rules to apply:
{dynamic_characteristics}

INSTRUCTIONS TO EXECUTE:
- Generate the baseline table now following the OUTPUT CONTRACT exactly.
- Remember: Output CSV only, no explanations, no markdown, no code fences.
"""
