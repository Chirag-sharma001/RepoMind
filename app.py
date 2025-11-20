import streamlit as st
import google.generativeai as genai
# model = genai.GenerativeModel("gemini-1.5-flash")
from PIL import Image
import zipfile
import os
import tempfile
import shutil
genai.configure(api_key="Your API-KEY")
# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="RepoMind Vision",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS (CYBERPUNK THEME) ---
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }
    /* Headings */
    h1, h2, h3 {
        color: #58A6FF !important;
        font-family: 'Source Code Pro', monospace;
    }
    /* Text Area / Inputs */
    .stTextInput > div > div > input {
        background-color: #0D1117;
        color: #C9D1D9;
        border: 1px solid #30363D;
    }
    /* Buttons */
    .stButton > button {
        background-color: #238636;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #2EA043;
    }
    /* Chat Messages */
    .stChatMessage {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
    }
    /* Spinner/Loader */
    .stSpinner > div {
        border-top-color: #58A6FF !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE SETUP ---


if "repo_context" not in st.session_state:
    st.session_state.repo_context = None
if "files" not in st.session_state:
    st.session_state.files = []
if "context" not in st.session_state:
    st.session_state.context = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- 4. HELPER FUNCTION: PROCESS ZIP ---
def process_codebase(zip_path):
    code_context = ""
    file_structure = []
    
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
                
            for root, dirs, files in os.walk(temp_dir):
                # Skip hidden folders
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv', '__pycache__']]
                
                for file in files:
                    # Only read code files
                    if file.endswith(('.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.java', '.cpp', '.json', '.sql', '.md')):
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, temp_dir)
                        file_structure.append(rel_path)
                        
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                code_context += f"\n--- START FILE: {rel_path} ---\n{content}\n--- END FILE: {rel_path} ---\n"
                        except:
                            pass
        except Exception as e:
            return None, None
            
    return code_context, file_structure

# --- 5. SIDEBAR: CONFIG & UPLOAD ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/10435/10435170.png", width=60)
    st.title("RepoMind Vision")
    st.caption("Use Gemini 1.5 Pro to see bugs.")

    api_key = st.text_input("🔑 Gemini API Key", type="password")

    uploaded_file = st.file_uploader("📂 Upload Project (.zip)", type="zip")

    # --- Combined Submit Button ---
    if st.button("🚀 Submit & Analyze Repository"):
        if not api_key:
            st.error("❌ Please enter your API Key.")
            st.stop()
        if not uploaded_file:
            st.error("❌ Please upload a valid ZIP file.")
            st.stop()

        # SHOW STATUS
        with st.status("🧠 Processing repository...", expanded=True) as status:
            # Save uploaded zip temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name

            # Process Codebase
            status.write("📂 Extracting files...")
            context_str, structure = process_codebase(tmp_path)

            if context_str:
                st.session_state.context = context_str
                st.session_state.files = structure
                st.session_state.repo_context = True

                status.update(label="✅ Repository Loaded!", state="complete", expanded=False)
                st.success(f"Loaded {len(structure)} files.")
            else:
                status.update(label="❌ Error reading ZIP", state="error")

# --- 6. MAIN INTERFACE ---

# HEADER
st.title("👁️ RepoMind Vision")
st.markdown("Multimodal Debugging: **Code + Visuals** powered by Gemini 1.5 Pro.")

# IF NO CONTEXT LOADED YET
if not st.session_state.repo_context:
    st.info("👈 Please upload a ZIP file in the sidebar to begin.")
    st.markdown("""
    ### 💡 How to use:
    1. Enter your **Gemini API Key**.
    2. Upload your project **ZIP file** (Code).
    3. Click **Analyze Repository**.
    4. Once loaded, you can chat and upload **Screenshots** of bugs!
    """)
    st.stop() # Stop execution here until uploaded

# IF CONTEXT IS LOADED -> SHOW CHAT INTERFACE
if st.session_state.repo_context:
    
    genai.configure(api_key=api_key)
    
    # Display Chat History
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # INPUT AREA LAYOUT
    # We use a form or columns to organize the inputs
    col_input, col_img = st.columns([3, 1])

    with col_img:
        bug_screenshot = st.file_uploader(
            "📸 2. Add Screenshot (Optional)", 
            type=["png", "jpg", "jpeg"], 
            key="vision_uploader"
        )
        if bug_screenshot:
            st.image(bug_screenshot, caption="Attached", width=100)

    user_query = st.chat_input("Ex: 'Why is the button invisible?'")

    if user_query:
        # 1. Show User Message
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)
            if bug_screenshot:
                img = Image.open(bug_screenshot)
                st.image(img, caption="Visual Context", width=300)

        # 2. AI Processing
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("🧠 *Analyzing Code + Pixels...*")
            
            try:
                # --- PROMPT ENGINEERING ---
                system_instruction = """
                Role: You are 'RepoMind Vision', an expert Full-Stack Architect.
                
                Goal: Analyze the code and the visual screenshot to find the bug.
                
                Rules:
                1. If an image is provided, start by describing what you see (UI bugs, alignment, colors).
                2. Link the visual error to specific lines of code in the provided codebase.
                3. Provide the FIX in a code block.
                """
                
                code_block = f"""
                --- BEGIN REPOSITORY CONTEXT ---
                File Structure: {st.session_state.files}
                
                {st.session_state.context}
                --- END REPOSITORY CONTEXT ---
                """
                
                # Build Input List (Text + Image)
                prompt_parts = [system_instruction, code_block, "User Question: " + user_query]
                
                if bug_screenshot:
                    img_obj = Image.open(bug_screenshot)
                    prompt_parts.append(img_obj)
                    prompt_parts.append("Instruction: Compare this screenshot with the code above.")
                
                # Generate
                model = genai.GenerativeModel("gemini-2.5-flash")
                response = model.generate_content(prompt_parts, stream=True)
                
                full_response = ""
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"API Error: {e}")