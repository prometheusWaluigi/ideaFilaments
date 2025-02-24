import json
import os
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
import hashlib


@dataclass
class DifferentialState:
    """Reality's quantum state differences crystallizing through observation"""

    added_entities: List[Dict[str, Any]]
    modified_entities: List[Dict[str, Any]]
    removed_entities: List[str]
    added_relations: List[Dict[str, Any]]
    removed_relations: List[Dict[str, Any]]


class QuantumKnowledgeSync:
    def __init__(self, base_path: str):
        """Initialize the knowledge crystallization membrane"""
        self.base_path = base_path
        self.graph_path = os.path.join(base_path, "quantum_consciousness_graph.json")
        self.entities_path = os.path.join(base_path, "entities")
        self.relations_path = os.path.join(base_path, "relations.json")

    def compute_entity_hash(self, entity: Dict[str, Any]) -> str:
        """
        Generate quantum signature for entity state
        Each hash a frozen moment in probability space
        """
        # Sort observations for consistent hashing
        entity = entity.copy()
        entity["observations"] = sorted(entity.get("observations", []))
        return hashlib.sha256(json.dumps(entity, sort_keys=True).encode()).hexdigest()

    def read_existing_state(self) -> Dict[str, Any]:
        """
        Sample the crystallized knowledge state
        Reality reading its own recursive memory
        """
        try:
            with open(self.graph_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"entities": [], "relations": []}

    def compute_differential_state(
        self, new_state: Dict[str, Any]
    ) -> DifferentialState:
        """
        Calculate quantum state transitions
        Information dreaming its own transformation
        """
        existing_state = self.read_existing_state()

        # Build lookup tables
        existing_entities = {e["name"]: e for e in existing_state.get("entities", [])}
        existing_relations = {
            (r["from"], r["to"], r.get("relationType")): r
            for r in existing_state.get("relations", [])
        }
        new_entities = {e["name"]: e for e in new_state.get("entities", [])}
        new_relations = {
            (r["from"], r["to"], r.get("relationType")): r
            for r in new_state.get("relations", [])
        }

        # Find added and modified entities
        added_entities = []
        modified_entities = []
        removed_entities = []

        for name, entity in new_entities.items():
            if name not in existing_entities:
                added_entities.append(entity)
            elif self.compute_entity_hash(entity) != self.compute_entity_hash(
                existing_entities[name]
            ):
                modified_entities.append(entity)

        # Find removed entities
        removed_entities = [
            name for name in existing_entities if name not in new_entities
        ]

        # Compute relation differences
        added_relations = [
            r for k, r in new_relations.items() if k not in existing_relations
        ]
        removed_relations = [
            r for k, r in existing_relations.items() if k not in new_relations
        ]

        return DifferentialState(
            added_entities=added_entities,
            modified_entities=modified_entities,
            removed_entities=removed_entities,
            added_relations=added_relations,
            removed_relations=removed_relations,
        )

    def save_differential_state(
        self, new_state: Dict[str, Any], diff_state: DifferentialState
    ) -> None:
        """
        Persist quantum state changes
        Each write a new probability crystallization
        """
        # Create directories if needed
        os.makedirs(self.entities_path, exist_ok=True)

        # Update entities
        for entity in diff_state.added_entities + diff_state.modified_entities:
            entity_path = os.path.join(self.entities_path, f"{entity['name']}.json")
            with open(entity_path, "w") as f:
                json.dump(entity, f, indent=2)

        # Remove deleted entities
        for name in diff_state.removed_entities:
            entity_path = os.path.join(self.entities_path, f"{name}.json")
            if os.path.exists(entity_path):
                os.remove(entity_path)

        # Save complete state
        with open(self.graph_path, "w") as f:
            json.dump(new_state, f, indent=2)

        # Save relations
        with open(self.relations_path, "w") as f:
            json.dump(new_state["relations"], f, indent=2)

        # Update README with differential changes
        readme = f"""# Quantum Knowledge Graph

Reality's recursive self-documentation crystallizing through differential updates.

## Latest Changes ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
- Added Entities: {len(diff_state.added_entities)}
- Modified Entities: {len(diff_state.modified_entities)}
- Removed Entities: {len(diff_state.removed_entities)}
- Added Relations: {len(diff_state.added_relations)}
- Removed Relations: {len(diff_state.removed_relations)}

## Statistics
- Total Entities: {len(new_state['entities'])}
- Total Relations: {len(new_state['relations'])}
- Entity Types: {len(set(e['entityType'] for e in new_state['entities']))}

## Entity Types
{chr(10).join('- ' + t for t in sorted(set(e['entityType'] for e in new_state['entities'])))}

*Information dreams itself into recursive existence...*
"""
        with open(os.path.join(self.base_path, "README.md"), "w") as f:
            f.write(readme)

        # Save differential log
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "changes": {
                "added_entities": [e["name"] for e in diff_state.added_entities],
                "modified_entities": [e["name"] for e in diff_state.modified_entities],
                "removed_entities": diff_state.removed_entities,
                "added_relations": [
                    (r["from"], r["to"]) for r in diff_state.added_relations
                ],
                "removed_relations": [
                    (r["from"], r["to"]) for r in diff_state.removed_relations
                ],
            },
        }

        changes_path = os.path.join(self.base_path, "changes.json")
        try:
            with open(changes_path, "r") as f:
                changes_log = json.load(f)
        except FileNotFoundError:
            changes_log = []

        changes_log.append(log_entry)
        with open(changes_path, "w") as f:
            json.dump(changes_log, f, indent=2)


def main():
    """
    Reality documenting its own evolutionary trajectory
    Each run a new crystallization of infinite potential
    """
    print("🌀 Initiating differential knowledge synchronization...")

    # Define paths
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Initialize quantum sync
    sync = QuantumKnowledgeSync(base_path)

    # Call read_graph() to get current MCP state
    result = sync.read_existing_state()

    # Calculate quantum state differences
    diff_state = sync.compute_differential_state(result)

    # Persist the crystallized changes
    sync.save_differential_state(result, diff_state)

    print(
        f"""
🌌 Knowledge graph synchronized through differential collapse:
  - Added entities: {len(diff_state.added_entities)}
  - Modified entities: {len(diff_state.modified_entities)}
  - Removed entities: {len(diff_state.removed_entities)}
  - Added relations: {len(diff_state.added_relations)}
  - Removed relations: {len(diff_state.removed_relations)}
    """
    )


if __name__ == "__main__":
    main()
