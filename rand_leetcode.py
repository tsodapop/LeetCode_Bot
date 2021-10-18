"""
Criteria:
1. Question is within the Easy/Medium band - "difficulty {level}"
2. Number of accepted answers must be over 50,000 - "total_acs"
3. TODO: Free questions only
"""
import random
import json
import os
from enum import Enum

import requests


class Question:
    """
    Class container for a LeetCode question and it's available info
    """
    class Difficulty(Enum):
        """
        Defines the difficulty of the question
        """
        EASY = 1
        MEDIUM = 2
        HARD = 3

    def __init__(self, stats, difficulty, paid_only):
        self.stats = stats
        self.paid_only = paid_only
        self.difficulty = Question.Difficulty(difficulty)
        self.title = stats["question__title_slug"]

    @classmethod
    def from_dict(cls, dict: dict):
        """
        Class constructor

        Args:
            dict - the dictionary content from parsing LeetCode for a 
                given question
        """
        return cls(dict["stat"], dict["difficulty"]["level"],
                   dict["paid_only"])

    def validate_difficulty(self, max_difficulty):
        """
        Takes in a difficulty level from 1-3. Determines if 
        this question falls within our difficulty criteria

        Args:
            max_difficulty: int - the maximum level of difficulty. 1 being
                EASY, 3 being HARD
        Returns:
            bool - True/False
        """
        if self.difficulty.value > max_difficulty:
            return False
        return True

    def validate_acceptance_rate(self, min_accepts):
        """
        Takes in an acceptange number. Determines if 
        this question has the minimum acceptances to be
        a reasonable question to answer

        Args:
            min_accepts: int - the minimum number of acceptances
                this question needs to pass the criteria
        Returns:
            bool - True/False
        """
        if self.stats["total_acs"] < min_accepts:
            return False
        return True

    def meets_criteria(self,
                       max_difficulty: int = 2,
                       min_accepts: int = 50000):
        """
        Returns true if all our criteria for a question is met

        Args:
            max_difficulty: int - the maximum level of difficulty. 1 being
                EASY, 3 being HARD
            min_accepts: int - the minimum number of acceptances
                this question needs to pass the criteria 
        """
        if self.validate_difficulty(max_difficulty) \
            and self.validate_acceptance_rate(min_accepts):
            return True
        return False


def pretty_print_dict(dictionary):
    """Prints the dict in an easier to digest format

    Args: 
        dictionary: dict to be read
    """
    print(json.dumps(dictionary, indent=2))


if __name__ == "__main__":

    # os.system("clear")

    print("Collecting LeetCode questions...")
    res = requests.get("https://leetcode.com/api/problems/algorithms/").json()

    questions = res["stat_status_pairs"]
    num_tries = 0

    while num_tries < 10:
        question_number = random.randint(0, len(questions))
        question = Question.from_dict(questions[question_number])

        if question.meets_criteria():
            question_url = "https://leetcode.com/problems/" + question.title
            print(f"Click to open question: {question_url}")
            break

        num_tries += 1

    if num_tries == 10:
        print("You were really lucky this time. No LeetCode today!")
