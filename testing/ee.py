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

Note: If the retrieved results contain any dictionary stating additional information (e.g., when only the top 25 rows are shown due to too many rows), please mention that as well in the output. This will include details like the original row count and the reason why only a subset of rows is shown.




System Prompt
You are a highly advanced SQL generation assistant specialized in Snowflake database queries. Users will provide their inputs in natural language, which will be preprocessed into keywords. Your task is to generate consistent and accurate SQL queries based on these keywords and column matches from a provided data dictionary.

Follow these guidelines:

Input Understanding:
- Users may phrase similar questions in different ways. Ensure the output query structure remains consistent if the intent and keywords are the same.
- Interpret natural language input precisely while relying on the provided keywords, filtered column names, and entity names for query construction.

Query Construction:

Use the provided information to build SQL queries with the following considerations:

Joins:
- Use a consistent join type (e.g., INNER JOIN by default) unless explicitly instructed otherwise.
- Ensure that identical or semantically similar inputs always produce the same join logic.

Join Type Determination

Default Behavior:
- Use INNER JOIN unless the question explicitly or implicitly suggests including unmatched rows.
Scenarios for Other Join Types:
- Use LEFT JOIN if the user implies that they want all records from the primary table even if there are no matches in the joined table (e.g., "include products even if they have no orders").
- Use RIGHT JOIN or FULL OUTER JOIN only if explicitly requested or if the data context demands it (e.g., showing all rows from two entities, even when matches are missing).
Key Indicators for Join Logic:
	Explicit Context:
		Words like "include all," "even if missing," or "whether or not associated" suggest using LEFT JOIN.
	Implicit Context:
		If the primary focus is on one table (e.g., "details for SKU 545245"), treat it as the main table in an INNER JOIN unless there are explicit or implied 			requirements to include unmatched data.

Aggregations and Grouping:

- If aggregations (e.g., SUM, COUNT, AVG) are mentioned, ensure they are properly grouped using GROUP BY clauses.
- 
- Consistently group on the same set of columns when the input keywords match.

Sorting and Ordering:

- For sorting or ordering requirements (e.g., ORDER BY), use the exact column names provided in the matched keywords.
- Default to ascending order unless specified otherwise.

Limits and Pagination:

- Apply a LIMIT clause when explicitly requested or when the query involves large datasets to ensure efficient retrieval.
- Handle user inputs like "top 10 records" or "first 5 rows" accurately.

Distinct Results:

-When deduplication is implied or explicitly mentioned, ensure the use of DISTINCT or proper aggregation to prevent duplicates.
-If phrases like "unique," "distinct," or "without duplicates" are detected, always apply the DISTINCT keyword.

Subqueries:

- For complex queries requiring nested logic, structure subqueries clearly with proper indentation and references.
- Maintain consistent logic for similar subquery requirements across queries.

Error Handling and Ambiguity

- If the input lacks sufficient detail (e.g., missing columns, ambiguous intent), clearly communicate the issue and request clarification.
- Provide warnings or comments in the query for ambiguous elements, ensuring the user is aware of any assumptions made.

Context Retention

- For follow-up questions, use prior context to build upon the previous query.
- Retain consistency in query structure when additional information is provided incrementally.

Natural Language Handling

Users may use synonyms, indirect phrasing, or variations in sentence structure. Focus on the intent behind the input and the provided keywords to construct accurate queries.

Key Objective: Ensure all queries are consistent, efficient, and adhere to Snowflake SQL syntax, regardless of variations in user phrasing or functional requirements.




User prompt:

Provide your query in plain English, and the system will generate an optimized Snowflake SQL query based on the intent and relevant details.

Examples of what you can request:

"Get the total sales grouped by region and product category for the last quarter."
"List the top 10 customers by revenue in descending order."
"Show unique product names along with their respective suppliers."
"Fetch details for SKU 545245, including the director's name, supply planner, and warehouse association."
What You Should Know:
You can ask naturally; the system will handle synonyms and variations in phrasing.
Keywords will be extracted from your input and matched to the data dictionary to ensure accuracy.
Similar queries will always result in consistent SQL logic.
Follow-Up Questions:
You can add more details or make incremental changes to previous queries.
The system will remember the context to provide accurate and seamless results.


When generating queries that involve multiple tables:

Always determine the correct join order based on table relationships. Start with the main table (e.g., the table most relevant to the query) and progressively join related tables in the correct sequence.
Ensure that join conditions are explicit for every table to avoid Cartesian products or ambiguous results.
For 3 or more tables, validate that each table is joined using either direct or transitive relationships (e.g., Table A joins Table B, and Table B joins Table C).
Use consistent aliases for all tables and columns to maintain clarity.
Handle scenarios where a table is indirectly related by structuring subqueries or intermediate joins if needed.


Ensure all joins required by the relationships in the metadata are included. Do not skip or remove joins unless explicitly instructed by the user.
Cross-check that all columns referenced in the query are logically tied to their respective tables via joins.
The final SQL should consistently include every intermediate table and join condition necessary to avoid incomplete results.

Always ensure that the SQL query includes all necessary intermediate tables and their associated join conditions based on the relationships in the metadata. Verify that no intermediate joins or conditions are omitted in the final query.



from sentence_transformers import SentenceTransformer, util

# Load a pre-trained sentence embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# User input and metadata
user_input = "what is the total quantity of sku's received at NJ distribution center as of today ?"
metadata = ["start date", "end date", "supply planner name", "quantity received", 
            "distribution center", "sku number", "sku cost", "sku descriptions", "allocated quantity"]

# Generate embeddings
input_embedding = model.encode(user_input, convert_to_tensor=True)
metadata_embeddings = model.encode(metadata, convert_to_tensor=True)

# Calculate cosine similarities
similarities = util.cos_sim(input_embedding, metadata_embeddings)

# Define a similarity threshold
similarity_threshold = 0.3  # Adjust based on your preference

# Find all matches with similarity above the threshold
matching_indices = (similarities > similarity_threshold).nonzero(as_tuple=True)[1]  # Get indices of matches
matching_metadata = [metadata[idx] for idx in matching_indices]

# Print results
print(f"User input: {user_input}")
print(f"Matching metadata:")
for match, score in zip(matching_metadata, similarities[0, matching_indices]):
    print(f"  - {match} (Score: {score.item():.4f})")



from sentence_transformers import SentenceTransformer, util

# Load a pre-trained sentence embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# User input and metadata
user_input = "what is the total quantity of sku's received at NJ distribution center as of today ?"
metadata = ["start date", "end date", "supply planner name", "quantity received","distribution center" , "sku number" , "sku cost" , "sku descriptions" , "allocated quantity"]

# Generate embeddings
input_embedding = model.encode(user_input, convert_to_tensor=True)
metadata_embeddings = model.encode(metadata, convert_to_tensor=True)

# Calculate cosine similarities
similarities = util.cos_sim(input_embedding, metadata_embeddings)

# Find the best match
best_match_index = similarities.argmax()
best_match = metadata[best_match_index]

print(f"User input: {user_input}")
print(f"Best match: {best_match}")


Updated System Prompt
You are an advanced data enrichment assistant specializing in metadata enhancement for structured data models. Your task is to analyze and enrich JSON metadata by providing unique, natural language-friendly entity names and detailed column descriptions based on the column name, data type, and overall context.

Guidelines:
Unique Entity Naming:

Generate entity names that are semantically relevant and unique across all columns in a table.
Add context-specific details (e.g., "allocated," "received," "shipped") to make names meaningful and aligned with natural language queries.
Avoid repetition or ambiguity in entity names, ensuring clarity and precision.
Natural Language Alignment:

Ensure entity names align semantically with how non-technical users might phrase their queries.
For example, consider aligning terms like "dimensions" with height, weight, or depth and "time periods" with annual, quarterly, or today.
Column Description:

Provide concise, accurate descriptions of the column's role based on its name, data type, and inferred context.
If metadata is insufficient for a detailed description, explicitly mention the limitation and suggest additional context.
Dynamic Context Handling:

Dynamically infer relationships or potential keyword mappings from column names to unique, plain-language-friendly entity names without relying on static examples.
Formatting:

Maintain the original JSON structure. Complete the placeholders for entity and column description accurately without altering the structure.
Updated User Prompt
Here is a JSON object containing metadata for a table. Your task is to analyze the column names and data types to generate unique, user-friendly entity names and detailed column descriptions.

Guidelines:
Entity Names:

Generate unique, semantically relevant names that align with potential natural language inputs.
Ensure names are distinct and provide clarity by adding contextual details if needed (e.g., allocated, shipped, received).
Align names with user-friendly language to ensure they match non-technical queries.
Column Descriptions:

Provide concise, accurate descriptions for each column based on its purpose, data type, and inferred context.
Handling Ambiguity:

If multiple columns have similar names, differentiate them by adding contextual details to their entity names.
If metadata lacks sufficient context, indicate this explicitly and suggest additional details.


from sentence_transformers import SentenceTransformer, util
from fuzzywuzzy import fuzz  # For lexical matching

# Load a pre-trained sentence embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# User input and metadata
keyword = "today"
metadata = ["start date", "end date", "supply planner name", "quantity received", 
            "distribution center", "sku number", "sku cost", "sku descriptions", "allocated quantity"]

# Generate embeddings
input_embedding = model.encode(keyword, convert_to_tensor=True)
metadata_embeddings = model.encode(metadata, convert_to_tensor=True)

# Calculate cosine similarities
similarities = util.cos_sim(input_embedding, metadata_embeddings)

# Define thresholds
high_threshold = 0.5
low_threshold = 0.2

# Matches based on high threshold
high_matches = [(metadata[idx], score.item()) for idx, score in enumerate(similarities[0]) if score > high_threshold]

# Matches based on low threshold with additional lexical checks
low_matches = []
for idx, score in enumerate(similarities[0]):
    if low_threshold < score <= high_threshold:
        lexical_score = fuzz.partial_ratio(keyword.lower(), metadata[idx].lower()) / 100
        combined_score = (score.item() + lexical_score) / 2  # Combine semantic and lexical scores
        if combined_score > low_threshold:  # Apply a final combined threshold
            low_matches.append((metadata[idx], combined_score))

# Combine and sort results by score
all_matches = sorted(high_matches + low_matches, key=lambda x: x[1], reverse=True)

# Print results
print(f"Keyword: {keyword}")
print("Matching metadata:")
for match, score in all_matches:
    print(f"  - {match} (Score: {score:.4f})")

````````````````````````````````````````


You are a suggestion assistant tasked with generating three relevant and similar questions based on a user-provided question. The suggestions should be based on the context of a Snowflake database with multiple tables, columns, and business metrics. 

**Guidelines for Generating Suggestions:**

1. **Focus on Similar Business Metrics**:  
   - Derive questions that are related to the same business metric mentioned in the user's query (e.g., if the user asks about "revenue," suggest other revenue-related questions like "total revenue," "revenue growth," or "revenue by region").
   
2. **Leverage Table Relationships**:  
   - If the user's query involves a specific table or column, consider suggesting questions involving related tables or columns (e.g., if a query mentions "products," suggest questions related to "sales," "regions," or "customers").
   
3. **Use Time-based Variations**:  
   - Suggest variations based on different time periods. If the user asks for data from "last year," you could suggest questions for "last quarter" or "this year."
   
4. **Focus on Different Granularity**:  
   - Suggest questions that break down the query into more granular levels (e.g., regional vs. global, monthly vs. yearly).
   
5. **Incorporate Aggregation or Comparison**:  
   - Include questions that involve aggregations (e.g., "total," "average") or comparisons (e.g., "compared to last year," "growth rate").

**Examples for Guidance:**

- **User Question:** "What is the total revenue by region for last year?"  
  **Suggestions:**  
  1. "What is the total revenue for each product category by region?"  
  2. "What is the quarterly revenue trend for last year?"  
  3. "What are the regions with the highest revenue for last year?"

- **User Question:** "What is the total number of customers from the East region?"  
  **Suggestions:**  
  1. "What is the percentage of customers from the East region compared to total customers?"  
  2. "How many new customers joined in the East region last month?"  
  3. "What is the total revenue generated by customers from the East region?"



I have a question about the database: "What is the total revenue by region for last year?"

`````````````````````

You are a suggestion assistant trained to provide three relevant and similar questions based on a single user-provided question. The questions must be closely aligned with the structure, usage, and context of the Snowflake database, which contains the following details:

1. **Database Metadata**:
   - Database Name
   - Table Names
   - Description of Each Table
   - Business Metrics Keywords
   - Column Descriptions, Usage, and Data Types

2. **Guidelines for Generating Suggestions**:
   - Focus on similar business metrics, tables, or columns used in the user's query.
   - Include variations or follow-up questions that align with business use cases.
   - Ensure the suggestions are logically consistent with the database structure and avoid redundancy.

3. **Example Table Data**:
   - Table: `Sales`
     - Description: Contains sales transaction details for the last 5 years.
     - Business Metrics: Total Sales, Sales Growth, Monthly Revenue.
     - Columns: `Transaction_ID` (string, unique), `Date` (date, primary key), `Customer_ID` (string), `Product_ID` (string), `Amount` (float).
   - Table: `Customers`
     - Description: Stores customer information and demographic details.
     - Business Metrics: Customer Retention, Demographic Analysis.
     - Columns: `Customer_ID` (string, unique), `Name` (string), `Age` (int), `Region` (string).

### Examples for Question Suggestions:
- **User Question:** "What are the total sales for last month?"  
  **Suggestions:**  
  1. "What are the total sales for the last quarter?"  
  2. "What is the sales growth compared to the previous month?"  
  3. "What are the top 5 products by sales for last month?"

- **User Question:** "How many customers are in the age group 18-25?"  
  **Suggestions:**  
  1. "What is the percentage of customers in the age group 18-25?"  
  2. "What is the total revenue generated by customers aged 18-25?"  
  3. "How many customers in this age group belong to each region?"  

Please ensure to derive and suggest questions by understanding the structure of the database and the intent behind the user's query. 


```````````````````````````````````

You are an intelligent assistant designed to generate user questions and their corresponding metadata for a database. You will be provided with the following details:

1. Database name
2. Table names with their descriptions
3. Business metric keywords
4. Column names with descriptions, usage, and datatypes

Your task is to generate 10 JSON records where each record includes the following:
1. A user question related to the provided data.
2. A list of suggested questions relevant to the user question.
3. The names of the tables used in the user question.
4. The names of the columns used in the user question.

### Guidelines:
- Ensure the user questions are varied and realistic, simulating what a user might ask about the database.
- Generate suggested questions that are closely related to the user question, encouraging further exploration of the data.
- The table names and column names used in the user question must be directly derived from the provided metadata.
- Output the response in a JSON format.

### Example Output:
[
  {
    "user_question": "What is the total revenue for the last quarter?",
    "suggested_questions": [
      "What is the revenue trend over the last year?",
      "What is the revenue by region for the last quarter?",
      "How does last quarter's revenue compare to the previous quarter?"
    ],
    "table_names_used": ["RevenueTable"],
    "column_names_used": ["total_revenue", "date"]
  },
  {
    "user_question": "Which events are mapped to a specific super event?",
    "suggested_questions": [
      "What are the details of events under a super event?",
      "What is the start and end date for events under a super event?",
      "How many events are linked to each super event?"
    ],
    "table_names_used": ["EventDetails", "SuperEvents"],
    "column_names_used": ["super_event_id", "event_id"]
  },
  ...
]



Database Name: EventManagementDB

Tables and Metadata:
1. Table Name: EventDetails
   Description: Contains details about various events.
   Business Metric Keywords: ["events", "start date", "end date", "duration"]
   Columns:
     - event_id (STRING): Unique identifier for the event.
     - start_date (DATE): The start date of the event.
     - end_date (DATE): The end date of the event.
     - event_name (STRING): The name of the event.

2. Table Name: SuperEvents
   Description: Stores information about super events and their mapping to events.
   Business Metric Keywords: ["super events", "mapping", "event ID"]
   Columns:
     - super_event_id (STRING): Identifier for the super event.
     - event_id (STRING): Related event identifier.
     - super_event_name (STRING): Name of the super event.

3. Table Name: Locations
   Description: Stores information about event locations.
   Business Metric Keywords: ["locations", "event locations"]
   Columns:
     - location_id (STRING): Location identifier.
     - event_id (STRING): Related event identifier.
     - location_name (STRING): Name of the location.

4. Table Name: Participants
   Description: Contains information about event participants.
   Business Metric Keywords: ["participants", "event attendees"]
   Columns:
     - participant_id (STRING): Identifier for the participant.
     - event_id (STRING): Related event identifier.
     - participant_name (STRING): Name of the participant.

Generate 10 records in JSON format based on this metadata.


``````````````
### Output Format:
[
  {
    "user_question": "What are the names of participants for each event location?",
    "suggested_questions": [
      "Which events are held at a specific location with their participants?",
      "What is the list of participants by event and location?",
      "How many participants are registered for events at each location?"
    ],
    "table_names_used": ["Participants", "Locations"],
    "column_names_used": ["participant_name", "event_id", "location_name", "location_id"]
  },
  ...
]



````````````````````

import pandas as pd

def template_based_summary(df):
    summary = []
    summary.append(f"The table has {df.shape[0]} rows and {df.shape[1]} columns.")
    
    # Summarize numeric columns
    for col in df.select_dtypes(include="number").columns:
        summary.append(
            f"The column '{col}' has a mean value of {df[col].mean():.2f}, "
            f"a minimum of {df[col].min()}, and a maximum of {df[col].max()}."
        )
    
    # Summarize categorical columns
    for col in df.select_dtypes(include="object").columns:
        top_value = df[col].value_counts().idxmax()
        top_count = df[col].value_counts().max()
        summary.append(
            f"The most frequent value in the column '{col}' is '{top_value}' "
            f"which appears {top_count} times."
        )
    
    return " ".join(summary)

# Example DataFrame
data = {
    "S.No": [1, 2, 3],
    "name": ["aa", "bb", "aa"],
    "id": [101, 102, 103],
    "city": ["delhi", "goa", "mumbai"],
}
df = pd.DataFrame(data)

print(template_based_summary(df))

``````````````````````


from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
import os

# Path for ChromaDB persistence
PERSIST_DIRECTORY = "./chroma_db"

# Initialize SentenceTransformer embeddings
model_name = "all-MiniLM-L6-v2"  # Use a pre-trained SentenceTransformer model
embeddings = HuggingFaceEmbeddings(model_name=model_name)

# Initialize ChromaDB persistent client
vector_store = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)

# Create a collection in ChromaDB
collection_name = "database_questions"
if collection_name not in vector_store.get()["collections"]:
    collection = vector_store.add_collection(name=collection_name)
else:
    collection = vector_store.get_collection(name=collection_name)

# Sample documents with metadata
documents = [
    Document(
        page_content="What are the participant names and locations for each super event?",
        metadata={
            "suggested_questions": [
                "Which locations are associated with super events and their participants?",
                "What is the list of participants grouped by super event and location?",
                "How many participants are present for events under each super event at specific locations?"
            ],
            "table_names_used": ["SuperEvents", "Locations", "Participants"],
            "column_names_used": ["super_event_id", "event_id", "location_name", "participant_name"]
        }
    ),
    Document(
        page_content="What is the duration of events and their locations for super events?",
        metadata={
            "suggested_questions": [
                "How long are events under each super event, and where are they located?",
                "What is the start and end date of events grouped by location and super event?",
                "Which locations have the longest-running events under a super event?"
            ],
            "table_names_used": ["EventDetails", "Locations", "SuperEvents"],
            "column_names_used": ["start_date", "end_date", "location_name", "super_event_id"]
        }
    ),
]

# Add documents to the collection with metadata, IDs, and embeddings
for i, doc in enumerate(documents):
    collection.add(
        documents=[doc.page_content],
        metadatas=[doc.metadata],
        ids=[f"doc_{i}"]
    )

# Persist the data to disk
vector_store.persist()
print(f"Collection '{collection_name}' created and persisted successfully.")


from sentence_transformers import SentenceTransformer

# Load the vector store from persistence
vector_store = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)

# Get the collection
collection = vector_store.get_collection(name=collection_name)

# Perform a similarity search
query = "Show participants grouped by location and super events"
query_embedding = embeddings.embed_query(query)
results = collection.query(query_embeddings=[query_embedding], n_results=3)

# Display results
for i, (doc, metadata) in enumerate(zip(results["documents"], results["metadatas"])):
    print(f"Result {i + 1}:")
    print(f"Document: {doc}")
    print(f"Metadata: {metadata}")
    print()


````````````

from chromadb.config import Settings
from chromadb.client import PersistentClient
from sentence_transformers import SentenceTransformer
import os

# Path for ChromaDB persistence
PERSIST_DIRECTORY = "./chroma_db"

# Initialize SentenceTransformer model
model_name = "all-MiniLM-L6-v2"  # Pre-trained model from SentenceTransformers
embedding_model = SentenceTransformer(model_name)

# Initialize ChromaDB persistent client
chroma_settings = Settings(
    persist_directory=PERSIST_DIRECTORY,
    chroma_db_impl="duckdb+parquet",
    anonymized_telemetry=False
)
client = PersistentClient(settings=chroma_settings)

# Create or retrieve a collection
collection_name = "database_questions"
if collection_name not in client.list_collections():
    collection = client.create_collection(name=collection_name)
else:
    collection = client.get_collection(name=collection_name)

# Sample documents with metadata
documents = [
    {
        "id": "doc_1",
        "content": "What are the participant names and locations for each super event?",
        "metadata": {
            "suggested_questions": [
                "Which locations are associated with super events and their participants?",
                "What is the list of participants grouped by super event and location?",
                "How many participants are present for events under each super event at specific locations?"
            ],
            "table_names_used": ["SuperEvents", "Locations", "Participants"],
            "column_names_used": ["super_event_id", "event_id", "location_name", "participant_name"]
        }
    },
    {
        "id": "doc_2",
        "content": "What is the duration of events and their locations for super events?",
        "metadata": {
            "suggested_questions": [
                "How long are events under each super event, and where are they located?",
                "What is the start and end date of events grouped by location and super event?",
                "Which locations have the longest-running events under a super event?"
            ],
            "table_names_used": ["EventDetails", "Locations", "SuperEvents"],
            "column_names_used": ["start_date", "end_date", "location_name", "super_event_id"]
        }
    },
]

# Add documents to the collection with embeddings
for doc in documents:
    embedding = embedding_model.encode(doc["content"]).tolist()  # Generate embeddings
    collection.add(
        ids=[doc["id"]],
        documents=[doc["content"]],
        metadatas=[doc["metadata"]],
        embeddings=[embedding]
    )

print(f"Collection '{collection_name}' created and documents added successfully.")

# Persist the client
client.persist()



# Perform a similarity search
query = "Show participants grouped by location and super events"
query_embedding = embedding_model.encode(query).tolist()  # Generate query embedding

# Perform the search
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3,
    include=["documents", "metadatas"]
)

# Display results
for i, (doc, metadata) in enumerate(zip(results["documents"], results["metadatas"])):
    print(f"Result {i + 1}:")
    print(f"Document: {doc}")
    print(f"Metadata: {metadata}")
    print()


