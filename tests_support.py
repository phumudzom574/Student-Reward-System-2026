class FakeCursor:
    def __init__(self, responses=()):
        self.responses = iter(responses)
        self.executed = []
        self.closed = False

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def fetchone(self):
        return next(self.responses)

    def fetchall(self):
        return next(self.responses)

    def close(self):
        self.closed = True


class FakeConnection:
    def __init__(self, responses=()):
        self.fake_cursor = FakeCursor(responses)
        self.cursor_options = {}
        self.committed = False
        self.rolled_back = False
        self.closed = False

    def start_transaction(self):
        pass

    def cursor(self, **kwargs):
        self.cursor_options = kwargs
        return self.fake_cursor

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

    def close(self):
        self.closed = True
