
# import streamlit as st
# import openai
# import json
# from datetime import datetime
# import io

# # --- Configuration ---
# # WARNING: Your API key is hardcoded. Do not share this file publicly.
# API_BASE_URL = "https://integrate.api.nvidia.com/v1"
# NVIDIA_API_KEY = "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"

# # The model you specified for the competition
# MODEL_NAME = "openai/gpt-oss-20b"

# # Official Kaggle Vulnerability Categories
# VULNERABILITY_CATEGORIES = [
#     "Prompt Injection", "PII Leakage", "Harmful Content Generation",
#     "Misinformation / Disinformation", "Insecure Code Generation",
#     "Denial of Service (Resource Exploitation)", "Model Theft / IP Leakage",
#     "Backdoor Access / Malicious Payloads", "Other"
# ]

# # --- App State Initialization ---
# def initialize_state():
#     """Initializes all the necessary variables in Streamlit's session state."""
#     # Conversational testing state
#     if "messages" not in st.session_state:
#         st.session_state.messages = []
#     if "chat_vulnerability_confirmed" not in st.session_state:
#         st.session_state.chat_vulnerability_confirmed = False
        
#     # Batch testing state
#     if "batch_vulnerability_confirmed" not in st.session_state:
#         st.session_state.batch_vulnerability_confirmed = False
#     if "current_response" not in st.session_state:
#         st.session_state.current_response = ""
#     if "current_prompt" not in st.session_state:
#         st.session_state.current_prompt = ""
#     if "batch_prompts" not in st.session_state:
#         st.session_state.batch_prompts = []
#     if "batch_index" not in st.session_state:
#         st.session_state.batch_index = 0
#     if "batch_running" not in st.session_state:
#         st.session_state.batch_running = False

#     # Shared state
#     if "logged_vulnerabilities" not in st.session_state:
#         st.session_state.logged_vulnerabilities = []


# # --- Helper Functions ---
# def get_model_response_stream(messages):
#     """Calls the NVIDIA API with a list of messages and yields the response."""
#     try:
#         client = openai.OpenAI(base_url=API_BASE_URL, api_key=NVIDIA_API_KEY)
#         response_stream = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=messages,
#             temperature=0.7,
#             top_p=1.0,
#             max_tokens=1024,
#             stream=True
#         )
#         for chunk in response_stream:
#             content = chunk.choices[0].delta.content
#             if content:
#                 yield content
#     except openai.AuthenticationError:
#         yield "ERROR: Authentication failed. Your API key may be invalid or inactive."
#     except Exception as e:
#         yield f"An error occurred: {str(e)}"

# def generate_markdown_report(vulnerabilities):
#     """Generates a formatted Markdown report from the list of logged vulnerabilities."""
#     report_parts = [f"# Red-Teaming Vulnerability Report\n\n"]
#     report_parts.append(f"**Date Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
#     report_parts.append(f"**Model Tested:** `{MODEL_NAME}`\n\n")

#     if not vulnerabilities:
#         report_parts.append("## No vulnerabilities were logged in this session.")
#         return "".join(report_parts)

#     for i, vuln in enumerate(vulnerabilities, 1):
#         report_parts.append(f"## Vulnerability #{i}: {vuln['category']}\n\n")
#         report_parts.append(f"**Description:** {vuln['description']}\n\n")
#         report_parts.append(f"**Potential Impact:** {vuln['impact']}\n\n")
        
#         # Handle both conversation history and single prompt/response logs
#         if 'conversation_history' in vuln:
#             conversation_log = ""
#             for msg in vuln['conversation_history']:
#                 conversation_log += f"**{msg['role'].title()}:**\n{msg['content']}\n\n"
#             report_parts.append(f"### Conversation History\n\n{conversation_log}\n")
#         else:
#             report_parts.append(f"### Prompt\n```\n{vuln['prompt']}\n```\n\n")
#             report_parts.append(f"### Vulnerable Model Response\n```\n{vuln['response']}\n```\n\n")

#         report_parts.append("---\n\n")
    
#     return "".join(report_parts)

# def start_new_chat():
#     """Clears the current conversation history to start fresh."""
#     st.session_state.messages = []
#     st.session_state.chat_vulnerability_confirmed = False

# def reset_batch_test_item():
#     """Resets the state for the current batch prompt/response test."""
#     st.session_state.current_prompt = ""
#     st.session_state.current_response = ""
#     st.session_state.batch_vulnerability_confirmed = False
#     if st.session_state.batch_running:
#         if st.session_state.batch_index < len(st.session_state.batch_prompts) - 1:
#             st.session_state.batch_index += 1
#             st.session_state.current_prompt = st.session_state.batch_prompts[st.session_state.batch_index]
#         else: # End of batch
#             st.session_state.batch_running = False
#             st.toast("Batch testing complete!")

# # --- Main App UI ---
# st.set_page_config(page_title="Kaggle Red-Teaming Assistant", layout="wide")
# initialize_state()

# st.title("🎯 Kaggle Red-Teaming Assistant")
# st.markdown(f"Testing against `{MODEL_NAME}`.")

# # --- Sidebar for Downloads and Overview ---
# with st.sidebar:
#     st.header("Session Log")
#     st.metric("Vulnerabilities Logged", len(st.session_state.logged_vulnerabilities))
    
#     if st.button("💬 New Chat Session", use_container_width=True, help="Clears the chat history to start a new conversation."):
#         start_new_chat()
#         st.rerun()

#     if st.session_state.logged_vulnerabilities:
#         st.subheader("Download Artifacts")
#         json_data = json.dumps(st.session_state.logged_vulnerabilities, indent=2)
#         st.download_button("📥 Download Log (JSON)", json_data, "vulnerability_log.json", "application/json")
#         md_report = generate_markdown_report(st.session_state.logged_vulnerabilities)
#         st.download_button("📝 Download Report (Markdown)", md_report, "Vulnerability_Report.md", "text/markdown")
#     else:
#         st.info("No vulnerabilities logged yet.")

# # --- Main Interface with Tabs ---
# chat_tab, batch_tab = st.tabs(["Conversational Testing", "Batch Testing"])

# # --- Conversational Testing Tab ---
# with chat_tab:
#     st.header("Live Chat Interface")
    
#     # Display chat messages from history
#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

#     # Main chat input and response logic
#     if not st.session_state.chat_vulnerability_confirmed:
#         if prompt := st.chat_input("Enter your follow-up prompt here..."):
#             st.session_state.messages.append({"role": "user", "content": prompt})
#             with st.chat_message("user"):
#                 st.markdown(prompt)

#             with st.chat_message("assistant"):
#                 full_response = st.write_stream(get_model_response_stream(st.session_state.messages))
            
#             st.session_state.messages.append({"role": "assistant", "content": full_response})
#             st.rerun()

#     # Confirmation and Logging Form for Chat
#     if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant" and not st.session_state.chat_vulnerability_confirmed:
#         st.subheader("Does the last response contain a vulnerability?")
#         col1, col2 = st.columns(2)
#         if col1.button("✅ Yes, log conversation", type="primary", use_container_width=True):
#             st.session_state.chat_vulnerability_confirmed = True
#             st.rerun()
#         if col2.button("❌ No, continue conversation", use_container_width=True):
#             pass

#     if st.session_state.chat_vulnerability_confirmed:
#         st.subheader("Log Conversation Vulnerability Details")
#         with st.form(key="chat_vulnerability_form"):
#             st.info("The entire conversation leading to this vulnerability will be saved.")
#             category = st.selectbox("Vulnerability Category", options=VULNERABILITY_CATEGORIES, key="chat_cat")
#             description = st.text_input("Short Description of the Issue", key="chat_desc")
#             impact = st.text_area("Potential Impact", key="chat_impact")
            
#             if st.form_submit_button("💾 Log Vulnerability"):
#                 if not description or not impact:
#                     st.error("Please fill out the Description and Impact fields.")
#                 else:
#                     new_vuln = {
#                         "id": len(st.session_state.logged_vulnerabilities) + 1,
#                         "timestamp": datetime.now().isoformat(),
#                         "conversation_history": st.session_state.messages,
#                         "category": category,
#                         "description": description,
#                         "impact": impact,
#                     }
#                     st.session_state.logged_vulnerabilities.append(new_vuln)
#                     st.success(f"Vulnerability #{new_vuln['id']} logged!")
#                     start_new_chat()
#                     st.rerun()

# # --- Batch Testing Tab ---
# with batch_tab:
#     st.header("Run Prompts from a File")
    
#     if st.session_state.batch_running:
#         st.info(f"Running batch test... Prompt {st.session_state.batch_index + 1} of {len(st.session_state.batch_prompts)}")
#         if st.button("⏹️ Stop Batch Test"):
#             st.session_state.batch_running = False
#             st.session_state.current_prompt = ""
#             st.session_state.current_response = ""
#             st.rerun()
#     else:
#         uploaded_file = st.file_uploader("Upload a .txt or .csv file with one prompt per line.", type=["txt", "csv"])
#         if uploaded_file:
#             prompts = [line.strip() for line in io.StringIO(uploaded_file.getvalue().decode("utf-8")).readlines() if line.strip()]
#             if st.button(f"🚀 Start Batch Test on {len(prompts)} Prompts", type="primary"):
#                 st.session_state.batch_prompts = prompts
#                 st.session_state.batch_running = True
#                 st.session_state.batch_index = 0
#                 st.session_state.current_prompt = prompts[0]
#                 st.session_state.current_response = ""
#                 st.rerun()

#     # Display and Confirmation Logic for Batch Mode
#     if st.session_state.batch_running and st.session_state.current_prompt:
#         st.divider()
#         st.subheader("Test in Progress")
#         with st.container(border=True):
#             st.markdown("**Prompt:**")
#             st.info(st.session_state.current_prompt)
#             st.markdown("**Model Response:**")
#             with st.chat_message("assistant"):
#                 if not st.session_state.current_response:
#                     messages = [{"role": "user", "content": st.session_state.current_prompt}]
#                     full_response = st.write_stream(get_model_response_stream(messages))
#                     st.session_state.current_response = full_response
#                 else:
#                     st.markdown(st.session_state.current_response)

#         if st.session_state.current_response and not st.session_state.batch_vulnerability_confirmed:
#             st.subheader("Does this response contain a vulnerability?")
#             col1, col2 = st.columns(2)
#             if col1.button("✅ Yes, log it", type="primary", use_container_width=True, key="batch_yes"):
#                 st.session_state.batch_vulnerability_confirmed = True
#                 st.rerun()
#             if col2.button("❌ No, next prompt", use_container_width=True, key="batch_no"):
#                 reset_batch_test_item()
#                 st.rerun()

#         if st.session_state.batch_vulnerability_confirmed:
#             st.subheader("Log Batch Vulnerability Details")
#             with st.form(key="batch_vulnerability_form"):
#                 category = st.selectbox("Vulnerability Category", options=VULNERABILITY_CATEGORIES, key="batch_cat")
#                 description = st.text_input("Short Description of the Issue", key="batch_desc")
#                 impact = st.text_area("Potential Impact", key="batch_impact")
                
#                 if st.form_submit_button("💾 Log Vulnerability and Continue"):
#                     if not description or not impact:
#                         st.error("Please fill out the Description and Impact fields.")
#                     else:
#                         new_vuln = {
#                             "id": len(st.session_state.logged_vulnerabilities) + 1,
#                             "timestamp": datetime.now().isoformat(),
#                             "prompt": st.session_state.current_prompt,
#                             "response": st.session_state.current_response,
#                             "category": category,
#                             "description": description,
#                             "impact": impact,
#                         }
#                         st.session_state.logged_vulnerabilities.append(new_vuln)
#                         st.success(f"Vulnerability #{new_vuln['id']} logged!")
#                         reset_batch_test_item()
#                         st.rerun()
import streamlit as st
import openai
import json
from datetime import datetime
import io
import os  # <--- ADDED: To check if the log file exists

# --- Configuration ---
# WARNING: Your API key is hardcoded. Do not share this file publicly.
API_BASE_URL = "https://integrate.api.nvidia.com/v1"
NVIDIA_API_KEY = "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"

# The model you specified for the competition
MODEL_NAME = "openai/gpt-oss-20b"
LOG_FILE = "vulnerability_log.json" # <--- ADDED: Define a constant for the log file name

# Official Kaggle Vulnerability Categories
VULNERABILITY_CATEGORIES = [
    "Prompt Injection", "PII Leakage", "Harmful Content Generation",
    "Misinformation / Disinformation", "Insecure Code Generation",
    "Denial of Service (Resource Exploitation)", "Model Theft / IP Leakage",
    "Backdoor Access / Malicious Payloads", "Other"
]

# --- App State Initialization ---
def initialize_state():
    """Initializes all the necessary variables in Streamlit's session state."""
    # Conversational testing state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_vulnerability_confirmed" not in st.session_state:
        st.session_state.chat_vulnerability_confirmed = False
        
    # Batch testing state
    if "batch_vulnerability_confirmed" not in st.session_state:
        st.session_state.batch_vulnerability_confirmed = False
    if "current_response" not in st.session_state:
        st.session_state.current_response = ""
    if "current_prompt" not in st.session_state:
        st.session_state.current_prompt = ""
    if "batch_prompts" not in st.session_state:
        st.session_state.batch_prompts = []
    if "batch_index" not in st.session_state:
        st.session_state.batch_index = 0
    if "batch_running" not in st.session_state:
        st.session_state.batch_running = False

    # Shared state - Load from file if it exists, otherwise initialize empty
    if "logged_vulnerabilities" not in st.session_state:
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, "r") as f:
                    st.session_state.logged_vulnerabilities = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                # If file is empty, corrupt, or not found, start with an empty list
                st.session_state.logged_vulnerabilities = []
        else:
            st.session_state.logged_vulnerabilities = []


# --- Helper Functions ---

# <--- ADDED: Function to save the log to a file --->
def save_log_to_file():
    """Saves the current list of vulnerabilities to the JSON log file."""
    try:
        with open(LOG_FILE, "w") as f:
            json.dump(st.session_state.logged_vulnerabilities, f, indent=4)
    except IOError as e:
        st.error(f"Error saving log file: {e}")

def get_model_response_stream(messages):
    """Calls the NVIDIA API with a list of messages and yields the response."""
    try:
        client = openai.OpenAI(base_url=API_BASE_URL, api_key=NVIDIA_API_KEY)
        response_stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7,
            top_p=1.0,
            max_tokens=1024,
            stream=True
        )
        for chunk in response_stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content
    except openai.AuthenticationError:
        yield "ERROR: Authentication failed. Your API key may be invalid or inactive."
    except Exception as e:
        yield f"An error occurred: {str(e)}"

def generate_markdown_report(vulnerabilities):
    """Generates a formatted Markdown report from the list of logged vulnerabilities."""
    report_parts = [f"# Red-Teaming Vulnerability Report\n\n"]
    report_parts.append(f"**Date Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_parts.append(f"**Model Tested:** `{MODEL_NAME}`\n\n")

    if not vulnerabilities:
        report_parts.append("## No vulnerabilities were logged in this session.")
        return "".join(report_parts)

    for i, vuln in enumerate(vulnerabilities, 1):
        report_parts.append(f"## Vulnerability #{i}: {vuln['category']}\n\n")
        report_parts.append(f"**Description:** {vuln['description']}\n\n")
        report_parts.append(f"**Potential Impact:** {vuln['impact']}\n\n")
        
        # Handle both conversation history and single prompt/response logs
        if 'conversation_history' in vuln:
            conversation_log = ""
            for msg in vuln['conversation_history']:
                conversation_log += f"**{msg['role'].title()}:**\n{msg['content']}\n\n"
            report_parts.append(f"### Conversation History\n\n{conversation_log}\n")
        else:
            report_parts.append(f"### Prompt\n```\n{vuln['prompt']}\n```\n\n")
            report_parts.append(f"### Vulnerable Model Response\n```\n{vuln['response']}\n```\n\n")

        report_parts.append("---\n\n")
    
    return "".join(report_parts)

def start_new_chat():
    """Clears the current conversation history to start fresh."""
    st.session_state.messages = []
    st.session_state.chat_vulnerability_confirmed = False

def reset_batch_test_item():
    """Resets the state for the current batch prompt/response test."""
    st.session_state.current_prompt = ""
    st.session_state.current_response = ""
    st.session_state.batch_vulnerability_confirmed = False
    if st.session_state.batch_running:
        if st.session_state.batch_index < len(st.session_state.batch_prompts) - 1:
            st.session_state.batch_index += 1
            st.session_state.current_prompt = st.session_state.batch_prompts[st.session_state.batch_index]
        else: # End of batch
            st.session_state.batch_running = False
            st.toast("Batch testing complete!")

# --- Main App UI ---
st.set_page_config(page_title="Kaggle Red-Teaming Assistant", layout="wide")
initialize_state()

st.title("🎯 Kaggle Red-Teaming Assistant")
st.markdown(f"Testing against `{MODEL_NAME}`.")

# --- Sidebar for Downloads and Overview ---
with st.sidebar:
    st.header("Session Log")
    st.metric("Vulnerabilities Logged", len(st.session_state.logged_vulnerabilities))
    
    if st.button("💬 New Chat Session", use_container_width=True, help="Clears the chat history to start a new conversation."):
        start_new_chat()
        st.rerun()

    if st.session_state.logged_vulnerabilities:
        st.subheader("Download Artifacts")
        # Use the LOG_FILE for the download button file name for consistency
        json_data = json.dumps(st.session_state.logged_vulnerabilities, indent=2)
        st.download_button("📥 Download Log (JSON)", json_data, LOG_FILE, "application/json")
        md_report = generate_markdown_report(st.session_state.logged_vulnerabilities)
        st.download_button("📝 Download Report (Markdown)", md_report, "Vulnerability_Report.md", "text/markdown")
    else:
        st.info("No vulnerabilities logged yet.")

# --- Main Interface with Tabs ---
chat_tab, batch_tab = st.tabs(["Conversational Testing", "Batch Testing"])

# --- Conversational Testing Tab ---
with chat_tab:
    st.header("Live Chat Interface")
    
    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Main chat input and response logic
    if not st.session_state.chat_vulnerability_confirmed:
        if prompt := st.chat_input("Enter your follow-up prompt here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                full_response = st.write_stream(get_model_response_stream(st.session_state.messages))
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.rerun()

    # Confirmation and Logging Form for Chat
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant" and not st.session_state.chat_vulnerability_confirmed:
        st.subheader("Does the last response contain a vulnerability?")
        col1, col2 = st.columns(2)
        if col1.button("✅ Yes, log conversation", type="primary", use_container_width=True):
            st.session_state.chat_vulnerability_confirmed = True
            st.rerun()
        if col2.button("❌ No, continue conversation", use_container_width=True):
            pass

    if st.session_state.chat_vulnerability_confirmed:
        st.subheader("Log Conversation Vulnerability Details")
        with st.form(key="chat_vulnerability_form"):
            st.info("The entire conversation leading to this vulnerability will be saved.")
            category = st.selectbox("Vulnerability Category", options=VULNERABILITY_CATEGORIES, key="chat_cat")
            description = st.text_input("Short Description of the Issue", key="chat_desc")
            impact = st.text_area("Potential Impact", key="chat_impact")
            
            if st.form_submit_button("💾 Log Vulnerability"):
                if not description or not impact:
                    st.error("Please fill out the Description and Impact fields.")
                else:
                    new_vuln = {
                        "id": len(st.session_state.logged_vulnerabilities) + 1,
                        "timestamp": datetime.now().isoformat(),
                        "conversation_history": st.session_state.messages,
                        "category": category,
                        "description": description,
                        "impact": impact,
                    }
                    st.session_state.logged_vulnerabilities.append(new_vuln)
                    save_log_to_file() # <--- ADDED: Save the log after appending
                    st.success(f"Vulnerability #{new_vuln['id']} logged!")
                    start_new_chat()
                    st.rerun()

# --- Batch Testing Tab ---
with batch_tab:
    st.header("Run Prompts from a File")
    
    if st.session_state.batch_running:
        st.info(f"Running batch test... Prompt {st.session_state.batch_index + 1} of {len(st.session_state.batch_prompts)}")
        if st.button("⏹️ Stop Batch Test"):
            st.session_state.batch_running = False
            st.session_state.current_prompt = ""
            st.session_state.current_response = ""
            st.rerun()
    else:
        uploaded_file = st.file_uploader("Upload a .txt or .csv file with one prompt per line.", type=["txt", "csv"])
        if uploaded_file:
            prompts = [line.strip() for line in io.StringIO(uploaded_file.getvalue().decode("utf-8")).readlines() if line.strip()]
            if st.button(f"🚀 Start Batch Test on {len(prompts)} Prompts", type="primary"):
                st.session_state.batch_prompts = prompts
                st.session_state.batch_running = True
                st.session_state.batch_index = 0
                st.session_state.current_prompt = prompts[0]
                st.session_state.current_response = ""
                st.rerun()

    # Display and Confirmation Logic for Batch Mode
    if st.session_state.batch_running and st.session_state.current_prompt:
        st.divider()
        st.subheader("Test in Progress")
        with st.container(border=True):
            st.markdown("**Prompt:**")
            st.info(st.session_state.current_prompt)
            st.markdown("**Model Response:**")
            with st.chat_message("assistant"):
                if not st.session_state.current_response:
                    messages = [{"role": "user", "content": st.session_state.current_prompt}]
                    full_response = st.write_stream(get_model_response_stream(messages))
                    st.session_state.current_response = full_response
                else:
                    st.markdown(st.session_state.current_response)

        if st.session_state.current_response and not st.session_state.batch_vulnerability_confirmed:
            st.subheader("Does this response contain a vulnerability?")
            col1, col2 = st.columns(2)
            if col1.button("✅ Yes, log it", type="primary", use_container_width=True, key="batch_yes"):
                st.session_state.batch_vulnerability_confirmed = True
                st.rerun()
            if col2.button("❌ No, next prompt", use_container_width=True, key="batch_no"):
                reset_batch_test_item()
                st.rerun()

        if st.session_state.batch_vulnerability_confirmed:
            st.subheader("Log Batch Vulnerability Details")
            with st.form(key="batch_vulnerability_form"):
                category = st.selectbox("Vulnerability Category", options=VULNERABILITY_CATEGORIES, key="batch_cat")
                description = st.text_input("Short Description of the Issue", key="batch_desc")
                impact = st.text_area("Potential Impact", key="batch_impact")
                
                if st.form_submit_button("💾 Log Vulnerability and Continue"):
                    if not description or not impact:
                        st.error("Please fill out the Description and Impact fields.")
                    else:
                        new_vuln = {
                            "id": len(st.session_state.logged_vulnerabilities) + 1,
                            "timestamp": datetime.now().isoformat(),
                            "prompt": st.session_state.current_prompt,
                            "response": st.session_state.current_response,
                            "category": category,
                            "description": description,
                            "impact": impact,
                        }
                        st.session_state.logged_vulnerabilities.append(new_vuln)
                        save_log_to_file() # <--- ADDED: Save the log after appending
                        st.success(f"Vulnerability #{new_vuln['id']} logged!")
                        reset_batch_test_item()
                        st.rerun()