from .api import Methods
from .api.session import Session


class Marzban(Methods):
    def __init__(self, session: Session) -> None:
        if isinstance(session.token, dict):
            super().__init__(session)
        else:
            raise Exception("Session Is Not Started Yet")
