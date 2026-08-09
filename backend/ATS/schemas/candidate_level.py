from enum import Enum

class CandidateLevel(str, Enum):
    FRESHER = "fresher"
    EARLY_CAREER = "early_career"
    EXPERIENCED = "experienced"
    SENIOR = "senior"