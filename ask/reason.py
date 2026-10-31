"""OWL-RL closure over an asserted C5 RDF graph."""

from __future__ import annotations

import owlrl
from rdflib import Graph


def close(graph: Graph) -> Graph:
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(graph)
    return graph
