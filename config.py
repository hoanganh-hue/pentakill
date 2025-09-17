import os
from typing import Optional


class Settings:
    # Base URL for thongtindoanhnghiep.co
    TTDN_BASE_URL: str = os.getenv("TTDN_BASE_URL", "https://thongtindoanhnghiep.co")

    # Caching TTLs (seconds)
    CATALOG_TTL_SECONDS: int = int(os.getenv("CATALOG_TTL_SECONDS", "86400"))  # 24h
    COMPANY_TTL_SECONDS: int = int(os.getenv("COMPANY_TTL_SECONDS", "21600"))  # 6h

    # Retry policy
    RETRY_MAX_ATTEMPTS: int = int(os.getenv("RETRY_MAX_ATTEMPTS", "3"))
    RETRY_INITIAL_DELAY_SECONDS: float = float(os.getenv("RETRY_INITIAL_DELAY_SECONDS", "1.0"))
    RETRY_BACKOFF_FACTOR: float = float(os.getenv("RETRY_BACKOFF_FACTOR", "2.0"))

    # API server
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))


settings = Settings()


