import json
import networkx as nx
from pathlib import Path
from typing import List, Dict, Optional

class OntologyManager:
    def __init__(self, ontology_path: str):
        self.ontology_path = Path(ontology_path)
        self.graph = nx.DiGraph()
        self.semantic_expansions: Dict[str, str] = {}
        self.trustworthiness_characteristics: List[str] = []
        self.load_ontology()

    def load_ontology(self):
        with open(self.ontology_path, 'r') as f:
            data = json.load(f)
        
        # Load functions and subcategories
        for function in data.get('functions', []):
            func_id = function['id']
            self.graph.add_node(func_id, type='function')
            
            for category in function.get('categories', []):
                cat_id = category['id']
                self.graph.add_node(cat_id, type='category')
                self.graph.add_edge(func_id, cat_id)
                
                for subcategory in category.get('subcategories', []):
                    sub_id = subcategory['id']
                    self.graph.add_node(
                        sub_id, 
                        type='subcategory', 
                        title=subcategory.get('title', ''),
                        preconditions=subcategory.get('preconditions', []),
                        trustworthiness_impact=subcategory.get('trustworthiness_impact', [])
                    )
                    self.graph.add_edge(cat_id, sub_id)
        
        # Load expansions and characteristics if they exist (V2)
        self.semantic_expansions = data.get('semantic_expansions', {})
        self.trustworthiness_characteristics = data.get('trustworthiness_characteristics', [])

    def get_preconditions(self, sub_id: str) -> List[str]:
        if self.graph.has_node(sub_id):
            return self.graph.nodes[sub_id].get('preconditions', [])
        return []

    def get_trustworthiness_impact(self, sub_id: str) -> List[str]:
        if self.graph.has_node(sub_id):
            return self.graph.nodes[sub_id].get('trustworthiness_impact', [])
        return []

    def get_all_subcategories(self) -> List[str]:
        return [n for n, d in self.graph.nodes(data=True) if d.get('type') == 'subcategory']

    def expand_term(self, term: str) -> Optional[str]:
        """Maps an informal term to a formal subcategory ID or characteristic."""
        return self.semantic_expansions.get(term.lower())

if __name__ == "__main__":
    manager = OntologyManager("zero-hallucination-auditor/src/ontology/nist_rmf_v2.json")
    print(f"Subcategories: {len(manager.get_all_subcategories())}")
    print(f"Expansion for 'system limits': {manager.expand_term('system limits')}")
