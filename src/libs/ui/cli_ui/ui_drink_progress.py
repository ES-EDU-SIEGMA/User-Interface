from __future__ import annotations


class Progress:
    """__return_value:= {
            "cmd": "progress",
            "data": <progress-percentage>
    }"""

    def __init__(self):
        pass

    def activate(self, __progress_percentage: int) -> dict:
        self.__drink_progress(__progress_percentage)
        return {"cmd": "progress", "data": __progress_percentage}

    @staticmethod
    def __drink_progress(__progress_percentage: int):
        if __progress_percentage == -1:
            print("drink took to long. aborting progress measurements.\n")
        else:
            print(f"Progress {__progress_percentage}%")
