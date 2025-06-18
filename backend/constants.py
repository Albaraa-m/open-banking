LEAN_SANDBOX_BASE_URL = "https://sandbox.sa.leantech.me"
LEAN_SANDBOX_AUTH_URL = "https://auth.sandbox.sa.leantech.me/oauth2/token"

LEAN_ENDPOINTS = {
    "customers": f"{LEAN_SANDBOX_BASE_URL}/customers/v1",
    "accounts": f"{LEAN_SANDBOX_BASE_URL}/data/v2/accounts",
}

DATABASE_URL = "sqlite:///banking.db"
