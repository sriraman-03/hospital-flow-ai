"""Environment-configured demo authentication for Hospital Flow AI."""
import hmac
import os
from dotenv import load_dotenv

load_dotenv()

ROLE_ACCOUNTS = {
    "Admin": {
        "username": os.getenv("HF_ADMIN_USERNAME", ""),
        "password": os.getenv("HF_ADMIN_PASSWORD", ""),
    },
    "Hospital Operations Manager": {
        "username": os.getenv("HF_MANAGER_USERNAME", ""),
        "password": os.getenv("HF_MANAGER_PASSWORD", ""),
    },
    "Clinical Staff": {
        "username": os.getenv("HF_CLINICAL_USERNAME", ""),
        "password": os.getenv("HF_CLINICAL_PASSWORD", ""),
    },
}

ROLE_PAGES = {
    "Admin": [
        "Dashboard", "Register Patient", "Patient Queue", "Resource Management",
        "Bed Allocation", "Department Routing", "Discharge & Transfers",
        "Notifications", "Agent Workflow", "About Project",
    ],
    "Hospital Operations Manager": [
        "Dashboard", "Register Patient", "Patient Queue", "Resource Management",
        "Bed Allocation", "Department Routing", "Discharge & Transfers",
        "Notifications", "Agent Workflow", "About Project",
    ],
    "Clinical Staff": [
        "Dashboard", "Register Patient", "Patient Queue", "Bed Allocation",
        "Department Routing", "Discharge & Transfers", "About Project",
    ],
}


def authenticate(username: str, password: str):
    """Return the matched role, or None when credentials do not match."""
    username = username.strip()
    for role, credentials in ROLE_ACCOUNTS.items():
        configured_user = credentials["username"]
        configured_password = credentials["password"]
        if not configured_user or not configured_password:
            continue
        if hmac.compare_digest(username, configured_user) and hmac.compare_digest(
            password, configured_password
        ):
            return role
    return None


def has_configured_accounts() -> bool:
    return all(account["username"] and account["password"] for account in ROLE_ACCOUNTS.values())
