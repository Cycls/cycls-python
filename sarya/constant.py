from .settings import settings

if settings.Environment == "development":
    SARYA_URL = "http://localhost:8000/"
else:
    SARYA_URL = "https://api.sarya.com/"