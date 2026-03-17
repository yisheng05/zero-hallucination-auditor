from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.perception.schema import GenerationMeaningRepresentation, CommunicationIntent

class ActionRenderer:
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.llm = ChatGoogleGenerativeAI(model=model_name)
        
        self.report_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Trust & Safety Action Renderer. 
            Translate the Generation Meaning Representation (GMR) into a professional audit report.
            Base your output ONLY on the GMR's content_payload.
            """),
            ("human", "Render this Audit Report: {payload}")
        ])

        self.request_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Trust & Safety Action Renderer.
            The audit is currently 'Unactionable' due to missing information.
            Your task is to politely ask the user for the missing preconditions listed in the GMR.
            Explain WHY these are needed for a NIST AI RMF audit.
            """),
            ("human", "Render this Info Request: {payload}")
        ])

    def render(self, gmr: GenerationMeaningRepresentation) -> str:
        if gmr.intent == CommunicationIntent.REPORT:
            chain = self.report_prompt | self.llm
            response = chain.invoke({"payload": str(gmr.content_payload)})
            return response.content
        elif gmr.intent == CommunicationIntent.REQUEST_INFO:
            chain = self.request_prompt | self.llm
            response = chain.invoke({"payload": str(gmr.content_payload)})
            return response.content
        else:
            return "Unexpected Communication Intent."
