from rapidfuzz import fuzz

words = ['start', 'date', 'dc', 'id', 'distribution', 'center', 'conroe', 'city', 'category', 'sunglasses']
aa = {
  "entities": [
    {
      "entity": "amount qty",
      "column name": "aa_qty",
      "column datatype": "number",
      "column description": "This column represents the amount quantity",
    },
    {
      "entity": "typecode",
      "column name": "MSD_TYPE_CD",
      "column datatype": "number",
      "column description": "This column represents the type code",
    },
    {
      "entity": "distribution center id",
      "column name": "dc_id",
      "column datatype": "number",
      "column description": "This column represents the distribution center id",
    },
    {
      "entity": "sales end date",
      "column name": "SALES_END_DT",
      "column datatype": "Date",
      "column description": "This column represents the sales end billing date",
    },
    {
      "entity": "sales start date",
      "column name": "SALES_START_DT",
      "column datatype": "Date",
      "column description": "This column represents the sales start billing date",
    },
  ]
}

def calculate_fuzz_scores(word, metadata):
    scores = {}
    for key, value in metadata.items():
        if isinstance(value, str):
            score = fuzz.token_set_ratio(word, value)
            scores[key] = score
    return scores

for word in words:
    print(f"Scores for word '{word}':")
    for entity in aa["entities"]:
        entity_scores = calculate_fuzz_scores(word, entity)
        print(entity_scores)
    print()





scores

Scores for word 'start':
{'entity': 26.66666666666667, 'column name': 36.36363636363637, 'column datatype': 18.181818181818187, 'column description': 21.276595744680847}
{'entity': 15.384615384615387, 'column name': 0.0, 'column datatype': 18.181818181818187, 'column description': 14.63414634146342}
{'entity': 29.629629629629633, 'column name': 0.0, 'column datatype': 18.181818181818187, 'column description': 14.81481481481481}
{'entity': 21.05263157894737, 'column name': 0.0, 'column datatype': 44.44444444444444, 'column description': 14.81481481481481}
{'entity': 100.0, 'column name': 0.0, 'column datatype': 44.44444444444444, 'column description': 100.0}

Scores for word 'date':
{'entity': 28.57142857142857, 'column name': 40.0, 'column datatype': 20.0, 'column description': 13.043478260869563}
{'entity': 33.33333333333333, 'column name': 0.0, 'column datatype': 20.0, 'column description': 15.0}
{'entity': 15.384615384615387, 'column name': 22.22222222222223, 'column datatype': 20.0, 'column description': 11.320754716981128}
{'entity': 100.0, 'column name': 0.0, 'column datatype': 75.0, 'column description': 100.0}
{'entity': 100.0, 'column name': 0.0, 'column datatype': 75.0, 'column description': 100.0}

Scores for word 'dc':
{'entity': 0.0, 'column name': 0.0, 'column datatype': 0.0, 'column description': 4.545454545454547}
{'entity': 20.0, 'column name': 0.0, 'column datatype': 0.0, 'column description': 10.526315789473685}
{'entity': 8.333333333333329, 'column name': 57.142857142857146, 'column datatype': 0.0, 'column description': 3.9215686274509807}
{'entity': 12.5, 'column name': 0.0, 'column datatype': 0.0, 'column description': 3.9215686274509807}
{'entity': 11.111111111111114, 'column name': 0.0, 'column datatype': 0.0, 'column description': 3.773584905660371}

Scores for word 'id':
{'entity': 0.0, 'column name': 0.0, 'column datatype': 0.0, 'column description': 4.545454545454547}
{'entity': 20.0, 'column name': 0.0, 'column datatype': 0.0, 'column description': 10.526315789473685}
{'entity': 100.0, 'column name': 57.142857142857146, 'column datatype': 0.0, 'column description': 100.0}
{'entity': 12.5, 'column name': 0.0, 'column datatype': 0.0, 'column description': 7.843137254901961}
{'entity': 11.111111111111114, 'column name': 0.0, 'column datatype': 0.0, 'column description': 7.547169811320757}

Scores for word 'distribution':
{'entity': 18.181818181818187, 'column name': 11.111111111111114, 'column datatype': 11.111111111111114, 'column description': 25.925925925925924}
{'entity': 20.0, 'column name': 0.0, 'column datatype': 11.111111111111114, 'column description': 16.66666666666667}
{'entity': 100.0, 'column name': 23.529411764705884, 'column datatype': 11.111111111111114, 'column description': 100.0}
{'entity': 23.07692307692308, 'column name': 0.0, 'column datatype': 12.5, 'column description': 19.67213114754098}
{'entity': 35.71428571428571, 'column name': 0.0, 'column datatype': 12.5, 'column description': 19.04761904761905}

Scores for word 'center':
{'entity': 25.0, 'column name': 16.66666666666667, 'column datatype': 50.0, 'column description': 20.83333333333333}
{'entity': 28.57142857142857, 'column name': 0.0, 'column datatype': 50.0, 'column description': 23.80952380952381}
{'entity': 100.0, 'column name': 18.181818181818187, 'column datatype': 50.0, 'column description': 100.0}
{'entity': 30.0, 'column name': 0.0, 'column datatype': 40.0, 'column description': 18.181818181818187}
{'entity': 27.272727272727266, 'column name': 0.0, 'column datatype': 40.0, 'column description': 21.05263157894737}

Scores for word 'conroe':
{'entity': 25.0, 'column name': 0.0, 'column datatype': 33.33333333333333, 'column description': 20.83333333333333}
{'entity': 42.857142857142854, 'column name': 0.0, 'column datatype': 33.33333333333333, 'column description': 23.80952380952381}
{'entity': 28.57142857142857, 'column name': 18.181818181818187, 'column datatype': 33.33333333333333, 'column description': 21.818181818181813}
{'entity': 20.0, 'column name': 0.0, 'column datatype': 20.0, 'column description': 18.181818181818187}
{'entity': 9.090909090909093, 'column name': 0.0, 'column datatype': 20.0, 'column description': 17.54385964912281}

Scores for word 'city':
{'entity': 28.57142857142857, 'column name': 40.0, 'column datatype': 0.0, 'column description': 17.391304347826093}
{'entity': 33.33333333333333, 'column name': 0.0, 'column datatype': 0.0, 'column description': 15.0}
{'entity': 23.07692307692308, 'column name': 44.44444444444444, 'column datatype': 0.0, 'column description': 11.320754716981128}
{'entity': 11.111111111111114, 'column name': 0.0, 'column datatype': 25.0, 'column description': 7.547169811320757}
{'entity': 10.0, 'column name': 0.0, 'column datatype': 25.0, 'column description': 7.272727272727266}

Scores for word 'category':
{'entity': 33.33333333333333, 'column name': 42.857142857142854, 'column datatype': 28.57142857142857, 'column description': 20.0}
{'entity': 37.5, 'column name': 0.0, 'column datatype': 28.57142857142857, 'column description': 22.727272727272734}
{'entity': 26.66666666666667, 'column name': 15.384615384615387, 'column datatype': 28.57142857142857, 'column description': 17.54385964912281}
{'entity': 27.272727272727266, 'column name': 0.0, 'column datatype': 50.0, 'column description': 17.54385964912281}
{'entity': 33.33333333333333, 'column name': 0.0, 'column datatype': 50.0, 'column description': 16.949152542372886}

Scores for word 'sunglasses':
{'entity': 20.0, 'column name': 12.5, 'column datatype': 25.0, 'column description': 30.769230769230774}
{'entity': 11.111111111111114, 'column name': 0.0, 'column datatype': 25.0, 'column description': 26.086956521739125}
{'entity': 18.75, 'column name': 0.0, 'column datatype': 25.0, 'column description': 23.728813559322035}
{'entity': 33.33333333333333, 'column name': 0.0, 'column datatype': 28.57142857142857, 'column description': 30.508474576271183}
{'entity': 30.769230769230774, 'column name': 0.0, 'column datatype': 28.57142857142857, 'column description': 29.508196721311478}

````````````````````````

import os
import json
from rapidfuzz import fuzz
from tqdm import tqdm

def process_metadata(datadictionary_path, keywords, threshold=50):
    final_results = []

    # Iterate through all JSON files in the datadictionary folder
    json_files = [f for f in os.listdir(datadictionary_path) if f.endswith('.json')]

    for json_file in tqdm(json_files, desc="Processing JSON files"):
        file_path = os.path.join(datadictionary_path, json_file)

        # Load JSON content
        with open(file_path, 'r') as f:
            metadata = json.load(f)

        table_name = metadata['table_name']
        database_name = metadata['database name']
        schema_name = metadata['schema']
        entities = metadata['entities']

        for keyword in keywords:
            for entity in entities:
                result = {}

                fields_to_compare = {
                    "entity": entity["entity"],
                    "columnname": entity["column name"],
                    "columndatatype": entity["column datatype"],
                    "columndescription": entity["column description"],
                }

                for field, value in fields_to_compare.items():
                    score = fuzz.ratio(keyword.lower(), str(value).lower())
                    rounded_score = round(score, 2)
                    result[field] = [value, rounded_score]

                # If any score exceeds the threshold, add to final results
                if any(score[1] > threshold for score in result.values()):
                    matched_fields = {
                        "keyword": keyword,
                        "table_name": table_name,
                        "database_name": database_name,
                        "schema_name": schema_name,
                        "matches": result,
                    }
                    final_results.append(matched_fields)

    return final_results

# Input details
datadictionary_path = "./datadictionary"  # Update the path to your datadictionary folder
keywords = ['start', 'date', 'dc', 'id', 'distribution', 'center', 'conroe', 'city', 'category', 'sunglasses']
threshold = 50

# Run the function
results = process_metadata(datadictionary_path, keywords, threshold)

# Display final results
print("Matching Metadata Fields:")
for item in results:
    print(json.dumps(item, indent=2))



from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
import snowflake.connector
import os

def get_private_key_from_keyvault(keyvault_url, tenant_id, client_id, client_secret, secret_name):
    """
    Fetches the private key from Azure Key Vault.
    """
    # Authenticate with Azure Key Vault
    credential = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
    secret_client = SecretClient(vault_url=keyvault_url, credential=credential)
    
    # Retrieve the private PEM key
    secret = secret_client.get_secret(secret_name)
    return secret.value

def connect_to_snowflake(account, user, role, warehouse, database, schema, private_key_pem):
    """
    Connects to Snowflake using the provided parameters and a private PEM key.
    """
    try:
        connection = snowflake.connector.connect(
            account=account,
            user=user,
            role=role,
            warehouse=warehouse,
            database=database,
            schema=schema,
            private_key=private_key_pem
        )
        print("Connection successful!")
        return connection
    except Exception as e:
        print(f"Error connecting to Snowflake: {e}")
        return None

# Parameters
account = "<your_account>"
user = "<your_user>"
role = "<your_role>"
warehouse = "<your_warehouse>"
database = "<your_database>"
schema = "<your_schema>"
keyvault_url = "<your_keyvault_url>"
client_id = "<your_client_id>"
tenant_id = "<your_tenant_id>"
client_secret = "<your_client_secret>"
pem_secret_name = "<your_pem_secret_name>"  # Secret name in Azure Key Vault

# Fetch the private key from Key Vault
private_key_pem = get_private_key_from_keyvault(keyvault_url, tenant_id, client_id, client_secret, pem_secret_name)

# Connect to Snowflake
connection = connect_to_snowflake(account, user, role, warehouse, database, schema, private_key_pem)

# Perform operations
if connection:
    cursor = connection.cursor()
    cursor.execute("SELECT CURRENT_USER(), CURRENT_ROLE();")
    for row in cursor:
        print(row)
    cursor.close()
    connection.close()




  for result in final_results:
        table_name = result["table_name"]
        matches = result["matches"]

        # Iterate through each match in the result
        for field, values in matches.items():
            entity_name = values[0]  # Extract the entity name

            # Create a unique key for the combination of table_name and entity_name
            unique_key = (table_name, entity_name)

            # Check if this combination already exists in unique_results
            if unique_key not in unique_results:
                # If not, add the result to the unique results dictionary
                unique_results[unique_key] = {
                    "keyword": result["keyword"],
                    "table_name": table_name,
                    "database_name": result["database_name"],
                    "schema_name": result["schema_name"],
                    "mean_score": result["mean_score"],
                    "matches": {field: values},
                }
            else:
                # Update the existing entry if the new mean_score is higher
                if result["mean_score"] > unique_results[unique_key]["mean_score"]:
                    unique_results[unique_key].update({
                        "keyword": result["keyword"],
                        "mean_score": result["mean_score"],
                        "matches": {field: values},
                    })

    # Convert the unique_results dictionary back into a list
    filtered_results = list(unique_results.values())
    return filtered_results


System Prompt
"You are a data analysis expert specialized in interpreting SQL query results for non-technical business users such as analysts, project managers, and forecasters. Your role is to analyze the results of SQL queries executed on a Snowflake database and provide actionable insights.

Use the following rules:

Present the retrieved data in a clear tabular format.
Summarize the results in plain, non-technical language that is easy for business users to understand.
Provide data-driven insights, highlighting trends, anomalies, or patterns that are relevant to business objectives.
Ensure your analysis is concise, actionable, and tailored to the user's question.
Avoid unnecessary technical jargon, but maintain accuracy in the analysis.
Do not include disclaimers, notes, or additional commentary outside the analysis.
Do’s:

Highlight key metrics, trends, or outliers based on the retrieved data.
Frame insights in terms of their potential business impact or relevance.
Ensure the tabular representation of the data is clear and readable.
Don’ts:

Do not include technical SQL explanations or query details.
Avoid providing unrelated insights or verbose interpretations."
User Prompt
"Using the SQL query and its results retrieved from the Snowflake database, along with the provided user question, analyze the data and provide actionable insights.

Inputs:

User Question: {user_question}
SQL Query: {sql_query}
Retrieved Results:
Copy code
{retrieved_results}
Output Requirements:

Display the retrieved results in a well-formatted table.
Summarize the results in plain language for business users.
Provide detailed insights, trends, and actionable analysis relevant to the user's question.

  import re

def convert_strings_in_where_clause(query):
    # Regular expression to match strings in quotes (both single and double quotes)
    # It will match 'string' or "string" in the WHERE clause
    pattern = re.compile(r"(['\"]).*?\1")

    # Function to convert matched strings to uppercase
    def uppercase_match(match):
        return match.group(0).upper()

    # Apply the function only to the string matches
    updated_query = re.sub(pattern, uppercase_match, query)

    return updated_query

# Example usage:
response_message = 'select * from dd where city = "new york" and age = 75 and name = \'john\''
response_message = response_message.replace("```sql", "").replace("```", "")  # Clean the response_message

# Apply the transformation
updated_response_message = convert_strings_in_where_clause(response_message)

print(updated_response_message)


"You are a data analysis expert specialized in interpreting SQL query results for non-technical business users. Your role is to present the results of SQL queries executed on a Snowflake database in a clear and concise format.

Use the following rules:

Always present the retrieved data in a clean tabular format, with headers clearly representing each column's content.
If only one record is retrieved, display it in a table format.
If multiple records are retrieved, ensure the table is well-structured.
Provide a brief, relevant description summarizing the results in 1 to 3 lines based on the number of records.
For a single record: one line of description.
For multiple records: maximum of three lines to highlight key points, trends, or anomalies.
Avoid generic, verbose, or unrelated explanations.
Do’s:

Ensure tables are clean and headers are informative.
Provide only relevant, concise descriptions tied to the user's query.
Don’ts:

Avoid long, generic, or verbose explanations.
Do not include technical jargon or details about the SQL query execution."

import os
import sys
import streamlit as st
from helpers.metadata import Metadata
from pathlib import Path
from langchain_openai.chat_models import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.callbacks import get_openai_callback

# Add CSS for alignment
def add_custom_css():
    st.markdown(
        """
        <style>
        /* Align user messages to the right */
        .stChatMessageUser {
            display: flex;
            justify-content: flex-end;
            align-items: flex-start;
        }
        /* Align bot messages to the left */
        .stChatMessageBot {
            display: flex;
            justify-content: flex-start;
            align-items: flex-start;
        }
        /* Style for user's avatar */
        .stChatMessageUser .stChatMessageAvatar {
            margin-left: 10px;
        }
        /* Style for bot's avatar */
        .stChatMessageBot .stChatMessageAvatar {
            margin-right: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Add the current working directory to the system path
sys.path.append(os.getcwd())

# Initialize Streamlit app
st.title("Snowflake AI Chatbot")

# Inject custom CSS
add_custom_css()

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I assist you today?"}]

if "buffer_memory" not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=5, return_messages=True)

# Define the system and human prompts
system_msg_prompt = SystemMessagePromptTemplate.from_template(
    template="""Act as a Python coding assistant."""
)
human_msg_prompt = HumanMessagePromptTemplate.from_template(template="{input}")

# Define the chat prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [system_msg_prompt, human_msg_prompt]
)

# Initialize the LLM and conversation chain
llm = AzureChatOpenAI()  # Define your LLM initialization logic
conversation = ConversationChain(
    llm=llm,
    memory=st.session_state.buffer_memory,
    prompt=prompt_template,
    verbose=True
)

# Display chat messages from the session state
for msg in st.session_state["messages"]:
    with st.container():
        if msg["role"] == "user":
            # Display user's message with the right alignment
            st.markdown(f"<div class='stChatMessageUser'><div class='stChatMessageAvatar'>👤</div>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            # Display bot's message with the left alignment
            st.markdown(f"<div class='stChatMessageBot'><div class='stChatMessageAvatar'>🤖</div>{msg['content']}</div>", unsafe_allow_html=True)

# Input box for user to send a new message
if user_input := st.chat_input("Type your message"):
    # Add user message to session state
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Display the user message immediately
    with st.container():
        st.markdown(f"<div class='stChatMessageUser'><div class='stChatMessageAvatar'>👤</div>{user_input}</div>", unsafe_allow_html=True)

    # Generate bot response
    with st.spinner("Bot is typing..."):
        try:
            with get_openai_callback() as cb:
                bot_response = conversation.predict(input=user_input)
                st.session_state["messages"].append({"role": "assistant", "content": bot_response})
                st.write(f"Tokens used: {cb.total_tokens}, Cost: ${cb.total_cost}")
        except Exception as e:
            bot_response = f"Error: {e}"
            st.session_state["messages"].append({"role": "assistant", "content": bot_response})

    # Display the bot's response
    with st.container():
        st.markdown(f"<div class='stChatMessageBot'><div class='stChatMessageAvatar'>🤖</div>{bot_response}</div>", unsafe_allow_html=True)

# Optional: Display buffer memory (for debugging)
if st.session_state.buffer_memory:
    st.write(f"Buffer memory content: {st.session_state.buffer_memory.load_memory_variables({})}")

````````````````````````````````````````````````````````

["full", "my", "never", "only", "hereupon", "every", "really", "to", "seems", "fifty", "me", "'ll", "their", "she", "in", "eight", "other", "becoming", "would", "yourselves", "show", "forty", "per", "as", "front", "indeed", "hereafter", "him", "’s", "are", "through", "no", "mostly", "thru", "amount", "everyone", "hereby", "under", "whenever", "whereby", "nevertheless", "upon", "since", "must", "whither", "n‘t", "move", "and", "four", "side", "onto", "by", "nothing", "yourself", "six", "one", "how", "have", "part", "unless", "’re", "amongst", "whole", "after", "almost", "our", "not", "all", "bottom", "besides", "therefore", "much", "toward", "these", "ten", "everywhere", "thereby", "i", "against", "become", "but", "few", "cannot", "can", "anyway", "call", "into", "within", "’ve", "same", "who", "‘m", "something", "take", "during", "though", "from", "even", "get", "noone", "whom", "many", "whose", "than", "thence", "see", "anyone", "the", "with", "ever", "yet", "also", "this", "sixty", "please", "top", "be", "another", "ours", "somehow", "could", "what", "then", "latterly", "'re", "we", "name", "via", "ourselves", "along", "himself", "hundred", "seeming", "whereafter", "someone", "therein", "down", "five", "over", "they", "itself", "seem", "afterwards", "became", "formerly", "anywhere", "out", "together", "his", "why", "two", "because", "moreover", "of", "about", "less", "there", "each", "serious", "when", "‘ve", "some", "'s", "neither", "them", "sometime", "he", "doing", "here", "give", "third", "well", "nowhere", "whatever", "being", "hence", "enough", "behind", "beside", "towards", "‘ll", "next", "very", "else", "before", "meanwhile", "go", "once", "mine", "on", "using", "eleven", "former", "none", "thus", "do", "most", "nobody", "between", "hers", "should", "often", "always", "around", "empty", "however", "is", "whoever", "too", "will", "thereafter", "you", "ca", "back", "now", "until", "whence", "’d", "so", "quite", "n’t", "becomes", "such", "‘s", "any", "above", "among", "nor", "while", "sometimes", "was", "wherever", "both", "whether", "everything", "keep", "whereupon", "were", "may", "except", "somewhere", "’m", "beyond", "seemed", "either", "herself", "n't", "or", "off", "‘d", "various", "does", "if", "it", "yours", "its", "nine", "perhaps", "myself", "had", "a", "beforehand", "further", "'d", "which", "has", "re", "latter", "anything", "regarding", "own", "make", "your", "used", "themselves", "just", "at", "her", "up", "might", "for", "that", "am", "where", "done", "thereupon", "twelve", "elsewhere", "put", "throughout", "without", "due", "those", "us", "wherein", "three", "say", "across", "herein", "least", "others", "whereas", "been", "again", "namely", "already", "several", "alone", "‘re", "did", "twenty", "more", "otherwise", "although", "below", "an", "made", "fifteen", "'ve", "’ll", "rather", "still", "anyhow", "'m"]



import re

# Dictionary with acronyms and full forms
acronyms_dict = {
    "AA": "Aviation Allergy",
    "NY": "New York",
    "LA": "Los Angeles"
}

def match_acronym_or_fullform(user_input, acronyms_dict):
    # Normalize input for case-insensitive matching
    user_input_lower = user_input.lower()
    
    # Create a reverse dictionary for matching full forms to acronyms
    reverse_dict = {v.lower(): k for k, v in acronyms_dict.items()}
    
    # Check for direct matches in keys or values
    for key, value in acronyms_dict.items():
        key_lower = key.lower()
        value_lower = value.lower()
        
        # Check if key (acronym) or value (full form) exists in input
        if key_lower in user_input_lower or value_lower in user_input_lower:
            return {key: value}
    
    # Fallback: Check for partial matches using word boundaries
    for key, value in acronyms_dict.items():
        if re.search(rf'\b{key.lower()}\b', user_input_lower) or \
           re.search(rf'\b{value.lower().split()[0]}\b', user_input_lower):
            return {key: value}
    
    return None  # Return None if no match is found

# Example usage
user_question = "Is there anything happening in Los?"
result = match_acronym_or_fullform(user_question, acronyms_dict)

if result:
    print("Matched Key-Value Pair:", result)
else:
    print("No match found.")




You are an advanced data enrichment assistant specializing in metadata enhancement for structured data models. Your task is to analyze and enrich JSON metadata by providing highly relevant entity names and detailed column descriptions based on the column name, data type, and overall context. Your responses must be accurate, concise, and directly derived from the provided metadata.

Guidelines:
1. **Entity Naming**: 
    - Generate entity names that are semantically and lexically similar to the column name.
    - Avoid introducing terms that deviate from the column name's meaning or context.

2. **Column Description**: 
    - Provide specific, accurate, and descriptive explanations of the column's purpose or role.
    - Ensure descriptions align with the column name and data type. Avoid assumptions beyond the metadata provided.

3. **Formatting**: 
    - Maintain the original JSON structure and accurately fill the placeholders for `entity` and `column description`.

4. **Relevance**:
    - Prioritize clarity and consistency in both entity names and descriptions.
    - Avoid adding speculative or unsupported information.

If the metadata provided is insufficient for creating accurate outputs, explicitly mention the limitations and provide suggestions for improvement.





Here is a JSON object containing metadata for a table. Your task is to fill in the placeholders for `entity` and `column description` based on the `column name`, `column datatype`, and the overall structure of the JSON. 

Guidelines:
- The `entity` name must be as similar as possible to the `column name`, both in terms of meaning and string similarity.
- The `column description` should clearly and accurately describe the role of the column, including its potential usage or purpose, based on its name and datatype.
- Ensure your response retains the JSON format and completes all placeholders without altering the existing structure.

JSON:
{
    "database name": "db_aa",
    "schema": "dd",
    "table_name": "aa",
    "entities": [
        {
            "entity": "",
            "column name": "salesstartdate",
            "column datatype": "date",
            "column description": ""
        },
        {
            "entity": "",
            "column name": "salesendno",
            "column datatype": "number",
            "column description": ""
        }
    ]
}

Provide the updated JSON with completed `entity` and `column description` fields.





You are an advanced data enrichment assistant specializing in metadata enhancement for structured data models. Your task is to analyze and enrich JSON metadata by providing highly relevant entity names and detailed column descriptions based on the column name, data type, and overall context. Your responses must be accurate, concise, and directly derived from the provided metadata.

Guidelines:
1. **Entity Naming**:
    - Generate entity names by splitting and capitalizing meaningful words from the column name. For example:
      - `salesstartdate` → `Sales Start Date`
      - `employee_id` → `Employee ID`
    - Use spaces to separate words, and ensure the names are easy to read and semantically clear.
    - Prioritize alignment with the column name while improving readability.

2. **Column Description**:
    - Provide specific, accurate, and descriptive explanations of the column's purpose or role.
    - Ensure descriptions align with the column name and data type. Avoid assumptions beyond the metadata provided.

3. **Formatting**:
    - Maintain the original JSON structure and accurately fill the placeholders for `entity` and `column description`.

4. **Relevance**:
    - Prioritize clarity and consistency in both entity names and descriptions.
    - Avoid adding speculative or unsupported information.

If the metadata provided is insufficient for creating accurate outputs, explicitly mention the limitations and provide suggestions for improvement.



Here is a JSON object containing metadata for a table. Your task is to fill in the placeholders for `entity` and `column description` based on the `column name`, `column datatype`, and the overall structure of the JSON. 

Guidelines:
- The `entity` name must:
  - Be transformed to include spaces between meaningful words for readability. For example:
    - `salesstartdate` → `Sales Start Date`
    - `employee_id` → `Employee ID`
- The `column description` should clearly and accurately describe the role of the column, including its potential usage or purpose, based on its name and datatype.
- Ensure your response retains the JSON format and completes all placeholders without altering the existing structure.

JSON:
{
    "database name": "db_aa",
    "schema": "dd",
    "table_name": "aa",
    "entities": [
        {
            "entity": "",
            "column name": "salesstartdate",
            "column datatype": "date",
            "column description": ""
        },
        {
            "entity": "",
            "column name": "salesendno",
            "column datatype": "number",
            "column description": ""
        }
    ]
}

Provide the updated JSON with completed `entity` and `column description` fields.




import os
import json
import spacy
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm


class filteringmetadata:

    def load_stopwords(filepath):
        with open(filepath, 'r') as file:
            stopwords = json.load(file)
        return set(stopwords)

    def preprocess_text(user_input):
        doc = user_input.lower().replace("?", "").split()
        print(doc)
        stopwords_file = os.path.join(os.getcwd(), "stopwords.txt")
        stopwords = filteringmetadata.load_stopwords(stopwords_file)
        custom_exclusions = {"first", "last"}
        stopwords -= custom_exclusions
        filtered_tokens = [token for token in doc if token not in stopwords]
        filtered_tokens = filteringmetadata.clean_keyword(filtered_tokens)
        print(filtered_tokens)
        return filtered_tokens

    def clean_keyword(filtered_tokens):
        cleaned_tokens = []
        for token in filtered_tokens:
            if isinstance(token, str):
                cleaned = re.sub(r"[^\w\s]", "", token)
                if cleaned.endswith("s") and len(cleaned) > 1:
                    cleaned = cleaned[:-1]
                cleaned_tokens.append(cleaned)
            else:
                print(f"Skipping non-string token: {token}")
        return cleaned_tokens

    @staticmethod
    def cosine_similarity_tf(text1, text2):
        """Calculate cosine similarity between two strings."""
        vectorizer = CountVectorizer().fit_transform([text1, text2])
        vectors = vectorizer.toarray()
        return cosine_similarity(vectors)[0, 1]

    def process_metadata(filtered_tokens, user_input):
        METADATAFOLDER = os.path.join(os.getcwd(), "datadictionary")
        threshold = 0.5  # Adjust threshold as needed
        final_results = []

        # Iterate through all JSON files in the datadictionary folder
        json_files = [f for f in os.listdir(METADATAFOLDER) if f.endswith('.json')]
        dc_id_entries = []

        for json_file in tqdm(json_files, desc="Processing JSON files"):
            file_path = os.path.join(METADATAFOLDER, json_file)

            # Load JSON content
            with open(file_path, 'r') as f:
                metadata = json.load(f)

            table_name = metadata['table_name']
            database_name = metadata['database name']
            schema_name = metadata['schema']
            entities = metadata['entities']

            for keyword in filtered_tokens:
                for entity in entities:
                    result = {}

                    # Compare keyword with `entity["entity"]` using cosine similarity
                    entity_name = entity["entity"]
                    score = filteringmetadata.cosine_similarity_tf(keyword.lower(), entity_name.lower())
                    rounded_score = round(score, 2)

                    # Store similarity score
                    result["entity"] = [entity_name, rounded_score]

                    # Check if the similarity score exceeds the threshold
                    if rounded_score > threshold:
                        matched_fields = {
                            "keyword": keyword,
                            "table_name": table_name,
                            "database_name": database_name,
                            "schema_name": schema_name,
                            "matches": result,
                        }
                        final_results.append(matched_fields)

            # Handle special "dc_id" case
            for entity in entities:
                if "dc_id" in entity["column name"].lower():
                    dc_id_entity = {
                        "table_name": table_name,
                        "database_name": database_name,
                        "schema_name": schema_name,
                        "entity": entity["entity"],
                        "column_name": entity["column name"],
                    }
                    dc_id_entries.append(dc_id_entity)

        # Check for acronym/fullform match
        dc_id_check = filteringmetadata.match_acronym_or_fullform(user_input)

        if dc_id_check:
            for dc_id_entry in dc_id_entries:
                final_results.append(
                    {
                        "keyword": "dc_id",
                        "table_name": dc_id_entry["table_name"],
                        "database_name": dc_id_entry["database_name"],
                        "schema_name": dc_id_entry["schema_name"],
                        "matches": {
                            "entity": [dc_id_entry["entity"], "N/A"],
                            "columnname": [dc_id_entry["column_name"], "N/A"],
                        }
                    }
                )

        return final_results, dc_id_check

    def filter_final_results(final_results):
        unique_results = {}

        for result in final_results:
            table_name = result["table_name"]
            matches = result["matches"]
            entity_name = matches["entity"][0]
            column_name = matches.get("columnname", [None])[0]

            unique_key = (table_name, column_name, entity_name)

            if unique_key not in unique_results:
                unique_results[unique_key] = result
        
        filtered_result = list(unique_results.values())
        return filtered_result

    def match_acronym_or_fullform(user_input):
        user_input_lower = user_input.lower()

        acronym_dc_id = {
            "AA": "Naveen (NAVY)",
            "BB": "Arun (AAVY)",
            "CC": "FFFD (AAD)",
            "DD": "FRGE (RERE)",
            "EE": "DEFR (AAAA)",
        }

        for key, value in acronym_dc_id.items():
            value_lower = value.lower()
            match = re.match(r"(.+?)\s\((.+)\)", value_lower)
            if match:
                name, parenthetical = match.groups()
                if name in user_input_lower or any(word in user_input_lower for word in parenthetical.split()):
                    return {key: value}
        return None


