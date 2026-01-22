class ConversationMemory:
    def __init__(self):
        self.store = {}

    def get(self, session_id):
        return self.store.get(session_id, [])

    def add(self, session_id, q, a):
        if session_id not in self.store:
            self.store[session_id] = []
        self.store[session_id].append({"q": q, "a": a})
