import os
import json
import streamlit as st
import requests
from groq import Groq

# Initialize session states
if 'analysis_messages' not in st.session_state:
    st.session_state.analysis_messages = []
if 'execution_messages' not in st.session_state:
    st.session_state.execution_messages = []
if 'code_submitted' not in st.session_state:
    st.session_state.code_submitted = False
if 'page' not in st.session_state:
    st.session_state.page = "Login"
if 'theme' not in st.session_state:
    st.session_state.theme = "dark"
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

class CodeExecutor:
    def __init__(self):
        self.jdoodle_endpoint = "https://api.jdoodle.com/v1/execute"
        self.client_id = "3c4fb59a8a02dc00ab802d11675fca85"
        self.client_secret = "3d123a4e7ced42b684c4bb180b8983ed8d1758c2ac41e9f6c320dea06c665100"
        
        self.language_mapping = {
            "Python": "python3",
            "JavaScript": "nodejs",
            "Java": "java",
            "C++": "cpp17",
            "Ruby": "ruby",
            "Go": "go"
        }

    def execute_code(self, code, language, input_data=""):
        try:
            headers = {
                "Content-Type": "application/json"
            }
            
            jdoodle_language = self.language_mapping.get(language, "python3")
            
            payload = {
                "clientId": self.client_id,
                "clientSecret": self.client_secret,
                "script": code,
                "language": jdoodle_language,
                "versionIndex": "0",
                "stdin": input_data
            }
            
            response = requests.post(
                self.jdoodle_endpoint,
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "output": result.get("output", ""),
                    "memory": result.get("memory", ""),
                    "cpu_time": result.get("cpuTime", "")
                }
            else:
                return {
                    "success": False,
                    "error": f"API Error: {response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

class LLMInterface:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.1-70b-versatile"

    def generate_response(self, prompt, max_tokens=1000):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating response: {e}")
            return None

class BugDetector:
    def __init__(self):
        self.llm = LLMInterface()

    def detect_bugs(self, code_snippet):
        prompt = f"Identify potential bugs or issues in the following code snippet:\n\n{code_snippet}\n\nPotential bugs or issues:"
        return self.llm.generate_response(prompt)

class CodeAnalyzer:
    def __init__(self):
        self.llm = LLMInterface()

    def explain_code(self, code_snippet):
        prompt = f"Explain the following code snippet in simple terms:\n\n{code_snippet}\n\nExplanation:"
        return self.llm.generate_response(prompt)

class Optimizer:
    def __init__(self):
        self.llm = LLMInterface()

    def optimize_code(self, code_snippet):
        prompt = f"Optimize the following code snippet for better performance and readability:\n\n{code_snippet}\n\nOptimized code:"
        return self.llm.generate_response(prompt)

def process_code(code, action, language=None):
    if language is None:
        prompt = code
    else:
        prompt = f"Language: {language}\n\nCode:\n{code}"
    
    if action == "Explain":
        analyzer = CodeAnalyzer()
        return analyzer.explain_code(prompt)
    elif action == "Detect Bugs":
        detector = BugDetector()
        return detector.detect_bugs(prompt)
    else:  # Optimize
        optimizer = Optimizer()
        return optimizer.optimize_code(prompt)

# Hardcoded user credentials
USERS = {
    "ap@gmail.com": "12345678",
    "dd@ap.com": "12345678",
}

# Theme configurations
THEMES = {
    "light": {
        "background": "#ffffff",
        "text": "#000000",
        "input_bg": "#f0f2f6",
        "panel_bg": "rgba(59, 130, 246, 0.1)",
        "code_bg": "#f6f8fa"
    },
    "dark": {
        "background": "#110a36",
        "text": "#E0E0E0",
        "input_bg": "#1E3A8A",
        "panel_bg": "rgba(59, 130, 246, 0.1)",
        "code_bg": "#1E3A8A"
    }
}

def get_theme_css():
    theme = THEMES[st.session_state.theme]
    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');

        body {{
            color: {theme['text']};
            background: {theme['background']};
            font-family: 'Roboto Mono', monospace;
        }}
        .stButton>button {{
            color: {theme['text']};
            background-color: #3B82F6;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            background-color: #2563EB;
        }}
        .stTextInput>div>div>input, .stTextArea textarea {{
            color: {theme['text']};
            background-color: {theme['input_bg']};
            border: 1px solid #3B82F6;
            font-family: 'Roboto Mono', monospace;
        }}
        .split-container {{
            display: flex;
            gap: 20px;
        }}
        .left-panel {{
            flex: 3;
            padding: 20px;
            background-color: {theme['panel_bg']};
            border-radius: 10px;
        }}
        .right-panel {{
            flex: 2;
            padding: 20px;
            background-color: rgba(34, 197, 94, 0.1);
            border-radius: 10px;
        }}
        .theme-toggle {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
        }}
        .login-container {{
            max-width: 400px;
            margin: 100px auto;
            padding: 20px;
            background-color: {theme['panel_bg']};
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .login-header {{
            text-align: center;
            margin-bottom: 20px;
        }}

    </style>
    """

def login_page():
    st.markdown(get_theme_css(), unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        st.markdown("<div class='login-header'><h1>Login</h1></div>", unsafe_allow_html=True)
        
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if email in USERS and USERS[email] == password:
                st.session_state.logged_in = True
                st.session_state.page = "Home"
                st.rerun()
            else:
                st.error("Invalid email or password")
        
        st.markdown("</div>", unsafe_allow_html=True)

def theme_toggle():
    col1, col2 = st.columns([0.9, 0.1])
    with col2:
        if st.button("🌓"):
            st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
            st.rerun()

# Set page config
st.set_page_config(page_title="SHA Clarifies", page_icon="🤖", layout="wide")

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap');

    .stButton>button {
        color: #E0E0E0;
        background-color: #3B82F6;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2563EB;
    }
    .stTextInput>div>div>input, .stTextArea textarea {
        color: #E0E0E0;
        background-color: #1E3A8A;
        border: 1px solid #3B82F6;
        font-family: 'Roboto Mono', monospace;
    }
    .stSelectbox>div>div>select {
        color: #E0E0E0;
        background-color: #1E3A8A;
        border: 1px solid #3B82F6;
        font-family: 'Roboto Mono', monospace;
    }
    .sidebar .sidebar-content {
        background-color: #1E3A8A;
    }
    .custom-box {
        background-color: rgba(30, 58, 138, 0.5);
        border: 1px solid #3B82F6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .feature-box {
        background-color: rgba(59, 130, 246, 0.1);
        border: 1px solid #3B82F6;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    body {
        color: #E0E0E0;
        background: #110a36;
        font-family: 'Roboto Mono', monospace;
    }
    .stButton>button {
        color: #E0E0E0;
        background-color: #3B82F6;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2563EB;
    }
    .stTextInput>div>div>input, .stTextArea textarea {
        color: #E0E0E0;
        background-color: #1E3A8A;
        border: 1px solid #3B82F6;
        font-family: 'Roboto Mono', monospace;
    }
    .split-container {
        display: flex;
        gap: 20px;
    }
    .left-panel {
        flex: 3;
        padding: 20px;
        background-color: rgba(59, 130, 246, 0.1);
        border-radius: 10px;
    }
    .right-panel {
        flex: 2;
        padding: 20px;
        background-color: rgba(34, 197, 94, 0.1);
        border-radius: 10px;
    }
    .panel-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        color: #E0E0E0;
    }
    .custom-box {
        background-color: rgba(30, 58, 138, 0.5);
        border: 1px solid #3B82F6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .output-box {
        background-color: #1E3A8A;
        border: 2px solid #3B82F6;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        color: #FFFFFF;
    }
    .custom-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #1E3A8A;
        color: #E0E0E0;
        text-align: center;
        padding: 5px;
        font-size: 12px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .sidebar-toggle {
        position: fixed;
        top: 0;
        left: 0;
        z-index: 99999;
        padding: 5px;
    }
    .sidebar-toggle img {
        width: 30px;
        height: 30px;
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    .welcome-animation {
        animation: fadeIn 2s ease-in-out;
    }
    .action-box {
        background-color: rgba(59, 130, 246, 0.2);
        border: 2px solid #3B82F6;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .output-box {
        background-color: #1E3A8A;
        border: 2px solid #3B82F6;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        color: #FFFFFF;
    }
    .stSelectbox [data-baseweb="select"] {
        border: 2px solid #3B82F6;
    }
    
    .bold-text {
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Main app logic
if not st.session_state.logged_in:
    login_page()
else:
    # Apply theme CSS
    st.markdown(get_theme_css(), unsafe_allow_html=True)
    
    # Theme toggle
    theme_toggle()

# Sidebar
with st.sidebar:
        st.image("logo.png", width=100)
        st.title("SHA Clarifies")
        
        if st.button("Home"):
            st.session_state.page = "Home"
        if st.button("About"):
            st.session_state.page = "About"
        if st.button("FAQ"):
            st.session_state.page = "FAQ"
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "Login"
            st.rerun()

# Main content
if st.session_state.page == "Home":
    st.title("SHA Clarifies - AI Code Assistant")

    # Create two columns for the split layout
    left_col, right_col = st.columns([3, 2])

    # Left Column - Code Assistant
    with left_col:
        st.markdown("<div class='panel-title'>Code Assistant</div>", unsafe_allow_html=True)
        
        # Code input and analysis options
        with st.form(key='analysis_form'):
            code_input = st.text_area("Enter your code for analysis:", height=200)
            action = st.selectbox("Choose analysis action:", 
                ["Explain", "Detect Bugs", "Optimize"])
            language = st.selectbox("Language:", 
                ["Python", "JavaScript", "Java", "C++", "Ruby", "Go"])
            analyze_button = st.form_submit_button("Analyze Code")
        
        # Display analysis results
        if analyze_button and code_input:
            with st.spinner("Analyzing code..."):
                result = process_code(code_input, action, language)
                st.session_state.analysis_messages.append({
                    "code": code_input,
                    "action": action,
                    "result": result
                })
        
        # Show analysis history
        if st.session_state.analysis_messages:
            st.markdown("### Analysis History")
            for msg in reversed(st.session_state.analysis_messages):
                with st.expander(f"{msg['action']} Analysis"):
                    st.code(msg['code'], language=language.lower())
                    st.markdown(msg['result'])

    # Right Column - Code Executor
    with right_col:
        st.markdown("<div class='panel-title'>Code Executor</div>", unsafe_allow_html=True)
        
        # Code execution interface
        with st.form(key='execution_form'):
            exec_code_input = st.text_area("Enter code to execute:", height=200)
            exec_language = st.selectbox("Execution language:", 
                ["Python", "JavaScript", "Java", "C++", "Ruby", "Go"],
                key="exec_language")
            input_data = st.text_area("Input (optional):", 
                help="Enter input data for your code")
            run_button = st.form_submit_button("Run Code")
        
        # Execute code and display results
        if run_button and exec_code_input:
            with st.spinner("Executing code..."):
                executor = CodeExecutor()
                result = executor.execute_code(exec_code_input, exec_language, input_data)
                
                st.session_state.execution_messages.append({
                    "code": exec_code_input,
                    "result": result
                })
        
        # Show execution history
        if st.session_state.execution_messages:
            st.markdown("### Execution History")
            for msg in reversed(st.session_state.execution_messages):
                with st.expander("Execution Result"):
                    st.code(msg['code'], language=exec_language.lower())
                    if msg['result']['success']:
                        st.code(msg['result']['output'])
                        st.markdown(f"""
                            **Memory:** {msg['result']['memory']}  
                            **CPU Time:** {msg['result']['cpu_time']}
                        """)
                    else:
                        st.error(msg['result']['error'])


elif st.session_state.page == "About":
    st.title("About SHA Clarifies")
    
    st.markdown("""
    <div class="custom-box">
    <h2>Our Mission</h2>
    <p>SHA Clarifies is a cutting-edge AI-powered code analysis tool developed by the talented team at AP Solutions. 
    Our mission is to make programming more accessible and enjoyable for developers of all skill levels.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background-color: rgba(59, 130, 246, 0.1);border: 1px solid #3B82F6;border-radius: 10px;padding: 15px;margin-bottom: 15px;">
    <h3>🚀 Key Features</h3>
    <ul>
        <li>Code Explanation</li>
        <li>Bug Detection</li>
        <li>Optimization Suggestions</li>
        <li>Multi-Language Support</li>
        <li>Code Executor</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: rgba(59, 130, 246, 0.1);border: 1px solid #3B82F6;border-radius: 10px;padding: 15px;margin-bottom: 15px;">
    <h3>💡 How It Works</h3>
    <p>SHA Clarifies uses advanced AI to analyze your code and provide insights. Simply paste your code and choose an action to get started!</p><p>ALso has a <b>Built-in Online Executor</b> for many a serious of Languages such as<b> R,Python,C++,Java,Javascript and many more (●'◡'●)</b> </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: rgba(59, 130, 246, 0.1);border: 1px solid #3B82F6;border-radius: 10px;padding: 15px;margin-bottom: 15px;">
    <h3>🛠️ Powered By</h3>
    <ul>
        <li>CodeLlama Model</li>
        <li>Ollama</li>
        <li>Streamlit</li>
        <li>JDoodle</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("The SHA Clarifies Team")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
    <div style="background-color: rgba(59, 130, 246, 0.1);border: 1px solid #3B82F6;border-radius: 10px;padding: 15px;margin-bottom: 15px;">
        <h3>Abishek Palani</h3>
        <p>Team Lead & AI/ML Specialist</p>
        <ul>
            <li>Expert in NLP and Code Analysis</li>
            <li>Specializes in intuitive interfaces</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    

    st.subheader("Contact Us")
    st.markdown("""
    <div class="custom-box">
    For inquiries, please email us at: <a href="mailto:CodeExe@apsolutions.com">CodeExe@apsolutions.com</a>
    </div>
    """, unsafe_allow_html=True)

# Add this in your main content section:
elif st.session_state.page == "FAQ":
    st.title("Frequently Asked Questions")
    
    st.markdown("""
    <style>
    .faq-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    .faq-item {
        background-color: rgba(59, 130, 246, 0.1);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    .faq-question {
        font-size: 1.2em;
        font-weight: bold;
        color: #3B82F6;
        margin-bottom: 10px;
    }
    .faq-answer {
        line-height: 1.6;
    }
    .faq-category {
        font-size: 1.5em;
        font-weight: bold;
        margin: 30px 0 20px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #3B82F6;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="faq-container">', unsafe_allow_html=True)

    # General Questions
    st.markdown('<div class="faq-category">General Questions</div>', unsafe_allow_html=True)

    with st.expander("What is SHA Clarifies?"):
        st.markdown("""
        <div class="faq-item">
            <div class="faq-answer">
            SHA Clarifies is an AI-powered code assistant that helps developers understand, debug, and optimize their code. 
            It supports multiple programming languages and provides features like:
            <ul>
                <li>Code explanation in simple terms</li>
                <li>Bug detection and analysis</li>
                <li>Code optimization suggestions</li>
                <li>Real-time code execution</li>
            </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Which programming languages are supported?"):
        st.markdown("""
        <div class="faq-item">
            <div class="faq-answer">
            SHA Clarifies currently supports the following programming languages:
            <ul>
                <li>Python</li>
                <li>JavaScript</li>
                <li>Java</li>
                <li>C++</li>
                <li>Ruby</li>
                <li>Go</li>
            </ul>
            We're continuously working to add support for more languages!
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Features and Usage
    st.markdown('<div class="faq-category">Features and Usage</div>', unsafe_allow_html=True)

    with st.expander("How do I use the code analyzer?"):
        st.markdown("""
        <div class="faq-item">
            <div class="faq-answer">
            Using the code analyzer is simple:
            <ol>
                <li>Paste your code in the "Enter your code for analysis" text area</li>
                <li>Select the appropriate programming language</li>
                <li>Choose an analysis action (Explain, Detect Bugs, or Optimize)</li>
                <li>Click the "Analyze Code" button</li>
            </ol>
            The results will appear below the input area, and you can find your analysis history in the expandable sections.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("What's the difference between Code Analysis and Code Execution?"):
        st.markdown("""
        <div class="faq-item">
            <div class="faq-answer">
            <strong>Code Analysis:</strong>
            <ul>
                <li>Provides explanations and insights about your code</li>
                <li>Identifies potential bugs and issues</li>
                <li>Suggests optimizations</li>
                <li>Doesn't actually run the code</li>
            </ul>
            <strong>Code Execution:</strong>
            <ul>
                <li>Actually runs your code in a secure environment</li>
                <li>Provides real output and results</li>
                <li>Shows execution metrics (memory usage, CPU time)</li>
                <li>Allows input data for testing</li>
            </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Technical Questions
    st.markdown('<div class="faq-category">Technical Questions</div>', unsafe_allow_html=True)

    with st.expander("Is there a limit to the code size I can analyze or execute?"):
        st.markdown("""
        <div class="faq-item">
            <div class="faq-answer">
            Yes, there are some limitations:
            <ul>
                <li>Code Analysis: Maximum of 2000 lines of code per request</li>
                <li>Code Execution: Maximum of 500 lines of code per execution</li>
                <li>Execution Time Limit: 15 seconds per run</li>
                <li>Memory Limit: 512MB per execution</li>
            </ul>
            These limits help ensure optimal performance and fair usage for all users.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("How secure is my code data?"):
        st.markdown("""
        <div class="faq-item">
            <div class="faq-answer">
            We take security seriously:
            <ul>
                <li>All code submissions are encrypted in transit using HTTPS</li>
                <li>Code execution happens in isolated, secure containers</li>
                <li>We don't store your code permanently</li>
                <li>Analysis history is only kept for the duration of your session</li>
                <li>No sensitive information is shared with third parties</li>
            </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Support and Troubleshooting
    st.markdown('<div class="faq-category">Support and Troubleshooting</div>', unsafe_allow_html=True)

    with st.expander("What should I do if I encounter an error?"):
        st.markdown("""
        <div class="faq-item">
            <div class="faq-answer">
            If you encounter an error:
            <ol>
                <li>Check if your code syntax is correct for the selected language</li>
                <li>Verify that you're within the size and resource limits</li>
                <li>Try refreshing the page and running the code again</li>
                <li>Clear your browser cache if issues persist</li>
                <li>Contact our support team at SHAClarifies@apsolutions.com if the problem continues</li>
            </ol>
            Common error messages are explained in our documentation.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Add contact information at the bottom
    st.markdown("""
    <div style="text-align: center; margin-top: 40px; padding: 20px;">
        <p>Still have questions? Contact us at <a href="mailto:SHAClarifies@apsolutions.com">SHAClarifies@apsolutions.com</a></p>
    </div>
    """, unsafe_allow_html=True)

# Custom footer
st.markdown(
    """
    <div class="custom-footer">
        © 2024 AP Solutions. All rights reserved. | SHA Clarifies
    </div>
    """,
    unsafe_allow_html=True
)

if __name__ == "__main__":
    st.sidebar.markdown("© 2024 AP Solutions")