from app.core.db import async_session_maker


class UnitOfWork:
    def __init__(self, session_factory: async_session_maker) -> None:
        self._session_factory = session_factory
        self.session = None
        self._cache = {}

    async def __aenter__(self) -> "UnitOfWork":
        self.session = self.session_maker()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self.session:
            if exc:
                await self.session.rollback()
            else:
                await self.session.commit()
            await self.session.close()

    def repo(self, repo_cls):
        if repo_cls not in self._cache:
            self._cache[repo_cls] = repo_cls(self.session)
        return self._cache[repo_cls]
