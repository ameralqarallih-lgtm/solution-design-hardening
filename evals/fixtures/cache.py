"""Deterministic state model, not a Redis implementation."""
class VulnerableCache:
    def __init__(self):
        self.db = (1, 'old')
        self.cache = None
    def read(self):
        return self.db
    def update(self):
        self.db = (2, 'new')
        self.cache = None
    def fill(self, value):
        self.cache = value

class CorrectedCache(VulnerableCache):
    def __init__(self):
        super().__init__()
        self.watermark = 1
    def update(self):
        super().update()
        self.watermark = self.db[0]
    def fill(self, value):
        # Model a single atomic compare-and-set operation at the cache.
        if value[0] >= self.watermark:
            self.cache = value
