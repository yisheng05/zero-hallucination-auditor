# Zero-Hallucination Trust & Safety Auditing Agent (V2)

An advanced compliance-checking agent for heavily regulated domains (like finance or healthcare). It utilizes a formal cognitive architecture and a stateful situation model to perform verifiable, non-hallucinatory safety audits against the NIST AI Risk Management Framework (AI RMF).

## 🧠 Cognitive Architecture
The agent follows a multi-stage cognitive pipeline to ensure that all decisions are grounded in symbolic logic and that the LLM is only used for perception and rendering:

1.  **Perception Interpretation (TMR)**: Parses natural language system actions into a formal **Text Meaning Representation**.
2.  **Situation Model (Memory)**: Persists and consolidates audit state across multiple interactions.
3.  **Symbolic Deliberation (MMR)**: Reasons over the Knowledge Graph to produce a **Mental Meaning Representation**, identifying compliance gaps and trustworthiness impacts.
4.  **Action Specification (GMR)**: Evaluates "Actionability" and specifies a **Generation Meaning Representation** (either a final `REPORT` or a `REQUEST_INFO` event).
5.  **Action Rendering**: Translates the structured GMR into fluent, professional, and verifiable text.

## ✨ Key Features
- **Deepened NIST AI RMF Ontology**: Maps actions to all four core functions (GOVERN, MAP, MEASURE, MANAGE) and assesses impacts on the 7 Trustworthiness Characteristics.
- **Semantic Expansions**: Automatically maps informal language (e.g., "checked for leaks") to formal framework criteria.
- **Mixed-Initiative Dialog**: Autonomously asks clarifying questions if required preconditions are missing, rather than generating an incomplete report.
- **Verifiable Audit Traces**: The core compliance logic is executed via graph-based symbolic checks, preventing LLM hallucinations in the decision-making process.

## 📂 Project Structure
- `src/ontology/`: Machine-readable NIST AI RMF (V2), Trustworthiness Characteristics, and `OntologyManager`.
- `src/memory/`: `SituationModel` for tracking the state of the audit across turns.
- `src/perception/`: `TMRParser` and semantic schemas for Text Meaning Representation.
- `src/deliberation/`: `SymbolicAuditor` that performs graph-based logic checks (TMR -> MMR).
- `src/action_specification/`: `ActionSpecifier` for determining communication intent (MMR -> GMR).
- `src/action_rendering/`: `ActionRenderer` to translate GMR into human-readable text.
- `main.py`: Interactive CLI entry point.

## 🛠 Setup
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure API Key**:
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key
   ```

## 🚀 Usage
Run the interactive auditor:
```bash
export PYTHONPATH=$PYTHONPATH:.
python zero-hallucination-auditor/main.py
```
**Example Session:**
- `User:` "We are deploying a new medical diagnosis model."
- `Agent:` (Identifies missing context and asks for system boundaries/policy.)
- `User:` "We have established system boundaries and completed bias testing."
- `Agent:` (Updates memory and continues the audit or requests remaining info.)

## 🧪 Testing
Run unit tests for the symbolic deliberation engine:
```bash
pytest zero-hallucination-auditor/tests/
```
