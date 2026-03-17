from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.perception.schema import TMRFrame, TMRParseResult
from dotenv import load_dotenv

load_dotenv()

class TMRParser:
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.llm = ChatGoogleGenerativeAI(model=model_name)
        self.structured_llm = self.llm.with_structured_output(TMRParseResult)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a specialized Trust & Safety Perception module.
            Your task is to parse user input into a formal Text Meaning Representation (TMR).
            
            Identify the action, target object, and context.
            Extract ANY information related to NIST AI RMF preconditions.
            
            **CRITICAL: You must map natural language to these EXACT status strings if mentioned:**
            - 'PolicyExists': user mentions a policy, guidelines, or rules.
            - 'LegalReviewDone': user mentions legal check, lawyers, or regulatory review.
            - 'RolesDefined': user mentions who is responsible or assigned roles.
            - 'AccountabilityStructureSet': user mentions accountability or oversight structure.
            - 'ContextEstablished': user mentions what the system is for or its use case.
            - 'SystemBoundariesDefined': user mentions system limits, boundaries, or scope.
            - 'BiasTestingDone': user mentions checking for bias, fairness, or demographic disparities.
            - 'MetricsDefined': user mentions specific metrics, KPIs, or measurement standards.
            - 'RiskMitigationsImplemented': user mentions mitigations, safety filters, or risk controls.
            - 'HumanInTheLoop': user mentions human oversight, manual review, or human-in-the-loop.

            If the user says they HAVE NOT done something, do NOT include it in the statuses.
            """),
            ("human", "{input}")
        ])
        
        self.chain = self.prompt | self.structured_llm

    def parse(self, text: str) -> TMRParseResult:
        result = self.chain.invoke({"input": text})
        result.frame.raw_input = text
        return result
