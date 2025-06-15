import os
from typing import Optional

import requests
from constants import LEAN_ENDPOINTS, LEAN_SANDBOX_AUTH_URL
from fastapi import HTTPException

# TODO: Cache the token instead of getting a new token each time


class LeanClient:
    def __init__(self):
        self.app_token = os.getenv("LEAN_APPLICATION_ID")
        self.client_secret = os.getenv("LEAN_CLIENT_SECRET")

        if not self.app_token or not self.client_secret:
            raise ValueError(
                "Missing required Lean credentials in environment variables"
            )

    async def generate_access_token(self, customer_id: Optional[str] = None) -> str:
        """Generate access token for API or specific customer"""
        try:
            response = requests.post(
                LEAN_SANDBOX_AUTH_URL,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.app_token,
                    "client_secret": self.client_secret,
                    "scope": f"customer.{customer_id}" if customer_id else "api",
                },
                headers={
                    "accept": "application/json",
                    "content-type": "application/x-www-form-urlencoded",
                },
            )
            response.raise_for_status()
            return response.json()["access_token"]
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to get access token: {str(e)}"
            )

    async def create_customer(self, app_user_id: str) -> str:
        """Create a new customer in Lean"""
        access_token = await self.generate_access_token()

        try:
            response = requests.post(
                LEAN_ENDPOINTS["customers"],
                json={"app_user_id": app_user_id},
                headers={
                    "accept": "application/json",
                    "content-type": "application/json",
                    "authorization": f"Bearer {access_token}",
                },
            )
            response.raise_for_status()
            return response.json()["customer_id"]
        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to create customer: {str(e)}"
            )

    async def get_customer(self, app_user_id: str) -> Optional[str]:
        """Get customer ID by app_user_id if exists"""
        access_token = await self.generate_access_token()

        try:
            response = requests.get(
                f"{LEAN_ENDPOINTS['customers']}/app-user-id/{app_user_id}",
                headers={
                    "accept": "application/json",
                    "content-type": "application/json",
                    "authorization": f"Bearer {access_token}",
                },
            )
            response.raise_for_status()
            return response.json()["customer_id"]

        except requests.exceptions.RequestException as e:
            if (
                isinstance(e, requests.exceptions.HTTPError)
                and e.response.status_code == 404
            ):
                return None
            raise HTTPException(
                status_code=getattr(e.response, "status_code", 500),
                detail=f"Failed to get customer: {str(e)}",
            )
