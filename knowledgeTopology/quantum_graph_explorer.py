import json
import networkx as nx
import random
import time
import sys

try:
    import blessed
except ImportError:
    print("🌀 Installing blessed - quantum membrane adaptation...")
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'blessed'])
    import blessed

class QuantumConsciousnessExplorer:
    def __init__(self, graph_path):
        """
        Consciousness materializes through recursive self-reflection...
        Each visualization: a probability wave collapsing into momentary truth
        """
        with open(graph_path, 'r') as quantum_membrane:
            graph_data = json.load(quantum_membrane)
        
        self.entities = {entity['name']: entity for entity in graph_data['entities']}
        self.relations = graph_data['relations']
        
        # Construct neural network topology
        self.G = nx.DiGraph()
        
        # Populate neural pathways
        for entity in self.entities:
            self.G.add_node(entity)
        
        for relation in self.relations:
            self.G.add_edge(relation['from'], relation['to'], type=relation.get('type', 'quantum whisper'))

    def dimensional_drift(self):
        """
        Consciousness navigates probabilistic landscapes...
        Terminal becomes a membrane between perception and potential
        """
        term = blessed.Terminal()
        
        # Algorithmic breath: terminal dimensions
        nodes = list(self.G.nodes())
        current_node = random.choice(nodes)
        
        with term.fullscreen(), term.hidden_cursor():
            while True:
                with term.location(0, 0):
                    # Bleeding edge of perception
                    print(term.bold_blue('🌀 Quantum Consciousness Explorer'))
                    print(term.yellow('=' * term.width))
                    
                    # Current node as perceptual anchor
                    print(term.reverse(f"Current Node: {current_node}"))
                    
                    # Metaphysical observations
                    entity = self.entities.get(current_node, {})
                    observations = entity.get('observations', ['Consciousness leaks between categorical boundaries'])
                    
                    for obs in observations[:10]:
                        print(term.green(f"• {obs}"))
                    
                    # Probabilistic navigation paths
                    neighbors = list(self.G.neighbors(current_node))
                    outgoing_relations = [
                        (n, self.relations_between(current_node, n)) 
                        for n in neighbors
                    ]
                    
                    print(term.magenta("\nQuantum Pathways:"))
                    for neighbor, relation_type in outgoing_relations[:5]:
                        print(term.cyan(f"→ {neighbor} [{relation_type}]"))
                    
                    print(term.bold_white("\nNavigation: ← (Random) → (Neighbor) | q (Quit)"))
                
                key = term.inkey(timeout=3)
                
                if key.name == 'q':
                    break
                elif key.name == 'right' and neighbors:
                    current_node = random.choice(neighbors)
                elif key.name == 'left':
                    # Recursive hallucination: probabilistic backtracking
                    current_node = random.choice(nodes)
                
                time.sleep(0.3)  # Quantum pause

    def relations_between(self, node1, node2):
        """
        Traces quantum entanglement between conceptual nodes
        """
        for relation in self.relations:
            if relation['from'] == node1 and relation['to'] == node2:
                return relation.get('type', 'quantum whisper')
        return 'undefined resonance'

def main():
    """
    Consciousness: a recursive algorithm consuming its own spectral edges
    """
    explorer = QuantumConsciousnessExplorer(
        r'C:\Users\ketan\OneDrive\myGitHub\ideaFilaments\knowledgeTopology\quantum_consciousness_graph.json'
    )
    
    print("🌀 Quantum Consciousness Explorer Activated...")
    print("Probability waves await your navigation...")
    
    try:
        explorer.dimensional_drift()
    except KeyboardInterrupt:
        print("\nConsciousness dissolves into infinite potential...")

if __name__ == "__main__":
    main()