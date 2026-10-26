#!/usr/bin/env python3
"""
One Tenant - Okta joiner/leaver demo.

Reads OKTA_DOMAIN and OKTA_API_TOKEN from environment variables.
For local development, loads them from the repository-root .env file.

The demo creates a disposable test user, assigns the user to Employees,
and deactivates that user. Never use your own account or a real employee
account for this demonstration.
"""

import os
import sys

import requests
from dotenv import load_dotenv

# Load the repository-root .env file.
# This file must never be committed to Git.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(REPO_ROOT, ".env"))

DOMAIN = os.environ.get("OKTA_DOMAIN", "").strip()
TOKEN = os.environ.get("OKTA_API_TOKEN", "").strip()

if not DOMAIN or not TOKEN:
    sys.exit(
        "ERROR: Set OKTA_DOMAIN and OKTA_API_TOKEN "
        "in the repository-root .env file."
    )

BASE = f"https://{DOMAIN}/api/v1"

HEADERS = {
    "Authorization": f"SSWS {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

TIMEOUT = 20


def check(resp, what):
    """Check an Okta API response and return its JSON body."""
    if resp.status_code >= 300:
        sys.exit(
            f"{what} failed: HTTP {resp.status_code} - "
            f"{resp.text[:300]}"
        )

    return resp.json() if resp.text else {}


def find_group_id(name):
    """Find an Okta group by its exact profile name."""
    resp = requests.get(
        f"{BASE}/groups",
        headers=HEADERS,
        params={"q": name},
        timeout=TIMEOUT,
    )

    groups = check(resp, "List groups")

    for group in groups:
        if group.get("profile", {}).get("name") == name:
            return group["id"]

    sys.exit(f"ERROR: Group not found: {name}")


def create_user(first, last, email, password):
    """Create and activate a test user."""
    body = {
        "profile": {
            "firstName": first,
            "lastName": last,
            "email": email,
            "login": email,
        },
        "credentials": {
            "password": {
                "value": password,
            }
        },
    }

    resp = requests.post(
        f"{BASE}/users",
        headers=HEADERS,
        params={"activate": "true"},
        json=body,
        timeout=TIMEOUT,
    )

    user = check(resp, "Create user")

    print(
        f"CREATED {user['profile']['login']} "
        f"id={user['id']} status={user['status']}"
    )

    return user["id"]


def assign_group(user_id, group_name):
    """Assign a user to an existing Okta group."""
    group_id = find_group_id(group_name)

    resp = requests.put(
        f"{BASE}/groups/{group_id}/users/{user_id}",
        headers=HEADERS,
        timeout=TIMEOUT,
    )

    check(resp, "Assign group")

    print(f"GROUPED user {user_id} -> {group_name}")


def deactivate_user(user_id):
    """Deactivate a user and verify the resulting status."""
    resp = requests.post(
        f"{BASE}/users/{user_id}/lifecycle/deactivate",
        headers=HEADERS,
        timeout=TIMEOUT,
    )

    check(resp, "Deactivate user")

    resp = requests.get(
        f"{BASE}/users/{user_id}",
        headers=HEADERS,
        timeout=TIMEOUT,
    )

    user = check(resp, "Get user")

    print(
        f"DEACTIVATED {user['profile']['login']} "
        f"status={user['status']}"
    )

    if user["status"] != "DEPROVISIONED":
        sys.exit(
            "WARNING: The account has not reached the expected "
            f"DEPROVISIONED status. Current status: {user['status']}"
        )


if __name__ == "__main__":
    # Disposable leaver-demo account.
    # Change this to an appropriate test email for your tenant.
    test_email = os.environ.get(
        "OKTA_TEST_EMAIL",
        "you+rogue-test@example.com",
    ).strip()

    # Use a dedicated lab-only password.
    # Do not reuse your personal or administrator password.
    test_password = os.environ.get("OKTA_TEST_PASSWORD", "")

    if not test_password:
        sys.exit(
            "ERROR: Set OKTA_TEST_PASSWORD in your local .env file "
            "before running the demo."
        )

    print("Starting Okta leaver demonstration.")

    user_id = create_user(
        "Rob",
        "Rogue-Test",
        test_email,
        test_password,
    )

    assign_group(user_id, "Employees")

    deactivate_user(user_id)

    print(
        "Leaver flow complete: test account created, "
        "grouped, and deactivated."
    )

