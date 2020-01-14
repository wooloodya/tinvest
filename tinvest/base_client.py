from typing import Generic, Optional, TypeVar

from .constants import PRODUCTION

T = TypeVar('T')


class BaseClient(Generic[T]):
    def __init__(self, token: str, *, session: Optional[T] = None):
        if not token:
            raise ValueError('Token cannot be empty')
        self._base_url: str = PRODUCTION
        self._token: str = token
        self._session = session

    @property
    def session(self) -> T:
        if self._session:
            return self._session
        raise AttributeError


__all__ = ('BaseClient',)
