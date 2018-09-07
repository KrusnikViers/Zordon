_stored_engine = None


class ScopedEngine:
    def __init__(self, engine):
        self.old_value = _stored_engine
        self.engine = engine

    def __enter__(self):
        global _stored_engine
        _stored_engine = self.engine

    def __exit__(self, exc_type, exc_val, exc_tb):
        global _stored_engine
        _stored_engine = self.old_value


def get_scoped_engine():
    return _stored_engine
