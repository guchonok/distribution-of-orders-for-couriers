from enum import Enum


class StatusOrder(str, Enum):
    in_progress = "in_progress"
    completed = "completed"
