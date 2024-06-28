from datetime import datetime

class Status:
    def __init__(self, status: str, filename: str, timestamp: datetime, explanation: list):
        self.status = status
        self.filename = filename
        self.timestamp = timestamp
        self.explanation = explanation

    @property
    def is_done(self) -> bool:
        return self.status.lower() == 'done'
    def __str__(self):
        return f"Status: {self.status}, Filename: {self.filename}, Timestamp: {self.timestamp}, Explanation: {self.explanation}"
