import unittest

from .evaluation import Params, evaluation_function

class TestEvaluationFunction(unittest.TestCase):
    """
    Tests the source-pair matcher against three short-answer questions:
    sugar (default sources), plant oils, and starch.

    Read the docs on how to use unittest here:
    https://docs.python.org/3/library/unittest.html
    """

    # Question 1: Comparing Types of Natural Sugars (default sources)
    # Table: Honey/Milk/Sugarcane/Apple - correct pair is Honey & Apple.

    def test_sugar_correct(self):
        result = evaluation_function("Honey and Apple", "Honey and Apple", Params()).to_dict()
        self.assertTrue(result.get("is_correct"))

    def test_sugar_correct_order_independent(self):
        result = evaluation_function("Apple, Honey", "Honey and Apple", Params()).to_dict()
        self.assertTrue(result.get("is_correct"))

    def test_sugar_wrong_pair(self):
        result = evaluation_function("Milk and Sugarcane", "Honey and Apple", Params()).to_dict()
        self.assertFalse(result.get("is_correct"))

    def test_sugar_incomplete(self):
        result = evaluation_function("Honey", "Honey and Apple", Params()).to_dict()
        self.assertFalse(result.get("is_correct"))

    def test_sugar_extra_wrong_name(self):
        result = evaluation_function("Honey, Apple, and Milk", "Honey and Apple", Params()).to_dict()
        self.assertFalse(result.get("is_correct"))

    # Question 2: Comparing Types of Plant Oils
    # Table: Olive/Coconut/Sunflower/Avocado - correct pair is Olive & Avocado.

    def test_oils_correct(self):
        params = Params(sources=["olive", "coconut", "sunflower", "avocado"])
        result = evaluation_function("Olive and Avocado", "Olive and Avocado", params).to_dict()
        self.assertTrue(result.get("is_correct"))

    def test_oils_wrong_pair(self):
        params = Params(sources=["olive", "coconut", "sunflower", "avocado"])
        result = evaluation_function("Coconut and Sunflower", "Olive and Avocado", params).to_dict()
        self.assertFalse(result.get("is_correct"))

    # Question 3: Comparing Types of Starch
    # Table: Potato/Rice/Corn/Wheat - correct pair is Corn & Wheat.

    def test_starch_correct(self):
        params = Params(sources=["potato", "rice", "corn", "wheat"])
        result = evaluation_function("Corn and Wheat", "Corn and Wheat", params).to_dict()
        self.assertTrue(result.get("is_correct"))

    def test_starch_wrong_pair(self):
        params = Params(sources=["potato", "rice", "corn", "wheat"])
        result = evaluation_function("Potato and Rice", "Corn and Wheat", params).to_dict()
        self.assertFalse(result.get("is_correct"))

    def test_feedback_present_when_incorrect(self):
        result = evaluation_function("not relevant at all", "Honey and Apple", Params()).to_dict()
        self.assertFalse(result.get("is_correct"))
        self.assertTrue(result.get("feedback"))
