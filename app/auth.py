import os
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN", "harvey-secret-token")

api_key_header = APIKeyHeader(name="X-API-Token", auto_error=False)


def verify_token(token: str = Security(api_key_header)):
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API token. Pass it as header: X-API-Token",
        )
    if token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API token.",
        )
    return token
```

Save the file.

This means every API request to Harvey's mock HRMS will need this header:
```
X-API-Token: harvey-secret-token-2026