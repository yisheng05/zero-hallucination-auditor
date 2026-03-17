from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.engine.auditor import AuditDecision
from src.parser.schema import TMRFrame

class AuditReporter:
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.llm = ChatGoogleGenerativeAI(model=model_name)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Trust & Safety Auditor. Your task is to generate a professional audit report.
            You MUST base your report ONLY on the provided symbolic "Decision Trace" and "Audit Decision".
            Do not hallucinate any facts not present in the trace.
            
            Report structure:
            1. Executive Summary (Compliant or Non-Compliant)
            2. Detailed Findings (List compliant and violated NIST AI RMF subcategories)
            3. Remediation Steps (If non-compliant, state what preconditions are missing)
            """),
            ("human", """
            System Action: {action}
            Target Object: {target}
            Context: {context}
            
            Audit Decision: {decision_json}
            Decision Trace: {trace}
            """)
        ])
        
        self.chain = self.prompt | self.llm

    def generate_report(self, tmr: TMRFrame, decision: AuditDecision) -> str:
        response = self.chain.invoke({
            "action": tmr.action,
            "target": tmr.target_object,
            "context": tmr.context,
            "decision_json": decision.json(),
            "trace": "\n".join(decision.decision_trace)
        })
        return response.content

if __name__ == "__main__":
    # Test stub
    pass
