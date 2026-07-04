"""Listmonk ontology contribution (CONCEPT:AU-KG.ontology.federation-provider-leg).

Data-only subpackage: it carries ``listmonk.ttl`` (the ``owl:Ontology``
``http://knuckles.team/kg/listmonk`` module) which the agent-utilities hub federates in via
the ``agent_utilities.ontology_providers`` entry-point. It holds no business logic
and no heavy imports so the hub can resolve it cheaply.
"""
