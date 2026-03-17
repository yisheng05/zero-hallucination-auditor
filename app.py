import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.getcwd())

from src.ontology.manager import OntologyManager
from src.memory.situation_model import SituationModel
from src.perception.tmr_parser import TMRParser
from src.deliberation.auditor import SymbolicAuditor
from src.action_specification.specifier import ActionSpecifier
from src.action_rendering.renderer import ActionRenderer
from src.perception.schema import CommunicationIntent

load_dotenv()

# Page config
st.set_page_config(page_title="Zero-Hallucination Audit Agent", page_icon="🛡️", layout="wide")

st.title("🛡️ Zero-Hallucination Trust & Safety Auditing Agent")
st.markdown("""
This agent uses a formal cognitive architecture (**TMR -> MMR -> GMR**) to audit AI systems against the **NIST AI Risk Management Framework**.
Decisions are made via symbolic logic over a knowledge graph, ensuring zero hallucination in compliance results.
""")

# Initialize Session State
if "situation_model" not in st.session_state:
    st.session_state.situation_model = SituationModel()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Components (Lazy Initialization)
@st.cache_resource
def get_components():
    ontology_path = "src/ontology/nist_rmf_v2.json"
    ontology_manager = OntologyManager(ontology_path)
    parser = TMRParser()
    auditor = SymbolicAuditor(ontology_manager)
    specifier = ActionSpecifier()
    renderer = ActionRenderer()
    return parser, auditor, specifier, renderer

parser, auditor, specifier, renderer = get_components()

# Sidebar: Situation Model Status
with st.sidebar:
    st.header("📊 Audit State (Situation Model)")
    if st.button("Reset Audit State"):
        st.session_state.situation_model.clear()
        st.session_state.messages = []
        st.rerun()
    
    st.subheader("System Info")
    st.write(f"**Target:** {st.session_state.situation_model.target_object or 'Not set'}")
    st.write(f"**Context:** {st.session_state.situation_model.context or 'Not set'}")
    
    st.subheader("Consolidated Preconditions")
    if st.session_state.situation_model.consolidated_statuses:
        for status in sorted(list(st.session_state.situation_model.consolidated_statuses)):
            st.success(f"✅ {status}")
    else:
        st.info("No preconditions identified yet.")

# Chat Interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Describe your system action or compliance status..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process through Cognitive Pipeline
    with st.spinner("Deliberating..."):
        # 1. Perception (Text -> TMR)
        parse_result = parser.parse(prompt)
        tmr = parse_result.frame
        
        # 2. Memory Update
        st.session_state.situation_model.update(tmr)
        
        # 3. Deliberation (MMR)
        mmr = auditor.deliberate(st.session_state.situation_model)
        
        # 4. Action Specification (GMR)
        gmr = specifier.specify(mmr)
        
        # 5. Action Rendering (Text)
        response_text = renderer.render(gmr)

    # Display agent response
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text)
        
        if gmr.intent == CommunicationIntent.REPORT:
            st.info("📢 This is a formal Audit Report based on verified preconditions.")
        else:
            st.warning("❓ More information is required to complete the NIST AI RMF audit.")

    st.rerun()
