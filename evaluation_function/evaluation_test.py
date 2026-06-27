import unittest

from .evaluation import Params, evaluation_function

class TestEvaluationFunction(unittest.TestCase):
    """
    Tests the claim/evidence/reasoning (CER) rubric against the six sample
    student responses to the "Comparing Types of Natural Sugars" question.

    Read the docs on how to use unittest here:
    https://docs.python.org/3/library/unittest.html
    """

    def _is_correct(self, response: str) -> bool:
        result = evaluation_function(response, "", Params()).to_dict()
        return result.get("is_correct")

    def test_student_a_missing_evidence_and_reasoning(self):
        response = (
            "Well the one that has the similar sugar is honey and apple because there "
            "only 1 percent from each other. Honey and apple, because there like 1 sugar "
            "away from each other. And milk and sugar are 6 percent of sugar away from "
            "each other."
        )
        self.assertFalse(self._is_correct(response))

    def test_student_b_wrong_claim(self):
        response = (
            "My conclusion is that none have the same sugar and two of them have the "
            "same melting point and they all have the same solubility in water. "
            "Differences are density also sugar can and milk are different in melting "
            "point from honey and apple. Honey and apple have the same melting point. "
            "All of them (honey,milk,sugar cane, apple) have the same solubility in "
            "water. They all have a different density. Milk's and sugar cane's melting "
            "point are different from honey's and apple's melting point."
        )
        self.assertFalse(self._is_correct(response))

    def test_student_c_no_claim(self):
        response = (
            "A lot of foods have the same sugar but some foods have a decent amount of "
            "sugar the differences is that sugar can be in anything the simularites is "
            "that they have foods that are the same with sugar."
        )
        self.assertFalse(self._is_correct(response))

    def test_student_d_missing_reasoning(self):
        response = (
            "What i can conclude from the pattern is that the apple and honey sugar are "
            "almost the most because they have the same melting point and they almost "
            "have the amount of density. The similarities or differences i would look to "
            "tell weather they have the same sugar is the Density and the melting point."
        )
        self.assertFalse(self._is_correct(response))

    def test_student_e_fully_correct(self):
        response = (
            "I can draw a conclusion that the sugar of the sources from both the honey "
            "and the apple are the same because their characteristic properties are "
            "either the same or very, very similar. For example, the density of the "
            "honey is 1.69 g/cm cubed, and the apple's density is 1.70g/cm cubed, so the "
            "difference between both the densities is only 0.01g/cm cubed. Additionally, "
            "their are both soluble and have the melting points, which is 103 degrees "
            "Celsius. In order to tell whether or not any of the foods contained the "
            "same sugar, I would look to see if the density and melting point were the "
            "same. I would make sure that the characteristic properties between the "
            "sugar from the multiple sources were the same because the properties are "
            "what make up a substance."
        )
        self.assertTrue(self._is_correct(response))

    def test_student_f_fully_correct(self):
        response = (
            "Claim: honey and apple have the same sugar. evidence: the density (1.69 "
            "and 1/70 g/cm3) and melting point are the same (103 C). Reasoning: unique "
            "substances that have unique characteristic properties."
        )
        self.assertTrue(self._is_correct(response))

    def test_feedback_present_when_incorrect(self):
        result = evaluation_function("not relevant at all", "", Params()).to_dict()
        self.assertFalse(result.get("is_correct"))
        self.assertTrue(result.get("feedback"))
