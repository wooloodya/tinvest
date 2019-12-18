from .constants import PRODUCTION


class BaseClient:
    def __init__(self, token, session=None):
        super().__init__()
        if not token:
            raise ValueError("Token cannot be empty")
        self._api: str = PRODUCTION
        self._token: str = token
        self._session = session

    @property
    def headers(self):
        return {
            "accept": "application/json",
            "Authorization": f"Bearer {self._token}",
        }
