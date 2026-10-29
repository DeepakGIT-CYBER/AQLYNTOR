from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

# Role-Based Permissions Matrix for Multi-Tenant Agent Fleets
ROLES_PERMISSIONS = {
    "admin": ["read", "write", "execute", "manage_policies", "deploy"],
    "agent_executor": ["read", "execute"],
    "auditor": ["read"]
}

def verify_roles(required_role: str):
    def role_dependency(credentials: HTTPAuthorizationCredentials = Security(security)):
        token = credentials.credentials
        # Dynamic token-to-role mapping for multi-tenant simulation
        token_role_map = {
            "aqlyntor-secret-token-999": "admin",
            "agent-token-123": "agent_executor",
            "auditor-token-456": "auditor"
        }
        
        user_role = token_role_map.get(token)
        if not user_role:
            raise HTTPException(status_code=403, detail="[RBAC SECURITY] Invalid or unrecognized token.")
            
        if required_role not in ROLES_PERMISSIONS.get(user_role, []):
            raise HTTPException(status_code=403, detail=f"[RBAC SECURITY] Permission denied. Role '{user_role}' lacks '{required_role}' privileges.")
            
        return user_role
    return role_dependency