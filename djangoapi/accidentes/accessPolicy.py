from rest_access_policy import AccessPolicy

class AccidentesAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["*"],
            "principal": ["group:admin"],
            "effect": "allow"
        },
        {
            "action": ["list", "retrieve", "create", "update", "partial_update"],
            "principal": ["group:asegurado"],
            "effect": "allow"
        }
    ]