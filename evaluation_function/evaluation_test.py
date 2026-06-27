import unittest

from .evaluation import Params, evaluation_function

class TestEvaluationFunction(unittest.TestCase):
    """
    Tests the LLM-based grader against the "Comparing Types of Natural
    Sugars" question. These tests call the OpenRouter API, so
    OPENROUTER_API_KEY must be set in the environment.

    Read the docs on how to use unittest here:
    https://docs.python.org/3/library/unittest.html
    """

    _QUESTION = "Which of the sources (Honey, Milk, Sugarcane, Apple) has the same type of sugar? Why?"
    _ANSWER = (
        "Apple and honey have the same type of sugar, as they share the same "
        "density and melting point."
    )

    def _params(self, feedback_prompt=""):
        return Params(
            model="openai/gpt-4o-mini",
            question=self._QUESTION,
            main_prompt="You are a science teacher grading a student's short-answer response.",
            default_prompt=(
                "The question was: {{question}} The correct answer is: {{answer}}. "
                "Respond with exactly 'true' if the student's response is correct, "
                "or 'false' otherwise."
            ),
            feedback_prompt=feedback_prompt,
        )

    def test_correct_response(self):
        result = evaluation_function(
            "Honey and apple, because they have the same density and melting point.",
            self._ANSWER,
            self._params(),
        ).to_dict()
        self.assertTrue(result.get("is_correct"))

    def test_incorrect_response(self):
        result = evaluation_function(
            "Milk and sugarcane have the same sugar.",
            self._ANSWER,
            self._params(),
        ).to_dict()
        self.assertFalse(result.get("is_correct"))

    def test_combined_feedback_branch(self):
        params = self._params(
            feedback_prompt="Explain in one sentence why the response is correct or incorrect."
        )
        result = evaluation_function(
            "Honey and apple, because they have the same density and melting point.",
            self._ANSWER,
            params,
        ).to_dict()
        self.assertTrue(result.get("is_correct"))
        self.assertTrue(result.get("feedback"))
