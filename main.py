import sys
import os
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.getcwd())

from src.ontology.manager import OntologyManager
from src.memory.situation_model import SituationModel
from src.perception.tmr_parser import TMRParser
from src.deliberation.auditor import SymbolicAuditor
from src.action_specification.specifier import ActionSpecifier
from src.action_rendering.renderer import ActionRenderer

load_dotenv()

def main():
    print("\n=== [Zero-Hallucination Trust & Safety Auditing Agent V2] ===")
    print("This agent uses a cognitive pipeline (TMR -> MMR -> GMR) and the NIST AI RMF.")
    print("Type 'exit' or 'quit' to end session. Type 'clear' to reset audit state.\n")

    # 1. Initialize Components
    ontology_path = "zero-hallucination-auditor/src/ontology/nist_rmf_v2.json"
    ontology_manager = OntologyManager(ontology_path)
    situation_model = SituationModel()
    
    parser = TMRParser()
    auditor = SymbolicAuditor(ontology_manager)
    specifier = ActionSpecifier()
    renderer = ActionRenderer()

    while True:
        try:
            user_input = input("User Action/Log: ").strip()
            if user_input.lower() in ['exit', 'quit']:
                break
            if user_input.lower() == 'clear':
                situation_model.clear()
                print("[System] Audit state reset.\n")
                continue
            if not user_input:
                continue

            # Perception (Text -> TMR)
            parse_result = parser.parse(user_input)
            tmr = parse_result.frame
            
            # Memory (Update Situation Model)
            situation_model.update(tmr)
            
            # Deliberation (Memory -> MMR)
            mmr = auditor.deliberate(situation_model)
            
            # Action Specification (MMR -> GMR)
            gmr = specifier.specify(mmr)
            
            # Action Rendering (GMR -> Text)
            response = renderer.render(gmr)
            
            print(f"\n--- [Agent Response] ---")
            print(response)
            print(f"--- [Intent: {gmr.intent}] ---\n")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
