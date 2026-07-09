"""
Test script for CareerPath Application Tracker.

These tests check the Application class, priority score,
missing skills, dictionary conversion, and JSON save/load.
"""

import os
import tempfile
import unittest
from datetime import date, timedelta

import main


class TestApplicationTracker(unittest.TestCase):
    """Tests for the CareerPath Application Tracker."""

    def test_priority_score_with_matching_skills(self):
        """Tests that priority score calculates correctly."""

        deadline = date.today() + timedelta(days=5)

        application = main.Application(
            "Test Company",
            "Data Analyst",
            deadline,
            "Applied",
            ["python", "sql", "excel"],
            ["python", "sql"],
            4,
            "Test notes"
        )

        self.assertEqual(application.calculate_priority_score(), 80)

    def test_missing_skills(self):
        """Tests that missing skills are identified correctly."""

        deadline = date.today() + timedelta(days=20)

        application = main.Application(
            "Test Company",
            "GIS Intern",
            deadline,
            "Interested",
            ["python", "sql", "arcgis"],
            ["python"],
            3,
            "Need to learn ArcGIS"
        )

        self.assertEqual(application.get_missing_skills(), ["sql", "arcgis"])

    def test_application_to_dict(self):
        """Tests that an Application object converts into a dictionary."""

        deadline = date(2026, 7, 31)

        application = main.Application(
            "The Home Depot",
            "Data Analyst",
            deadline,
            "Applied",
            ["python", "sql"],
            ["python"],
            4,
            "Requires SQL experience"
        )

        application_dict = application.to_dict()

        self.assertEqual(application_dict["company"], "The Home Depot")
        self.assertEqual(application_dict["role"], "Data Analyst")
        self.assertEqual(application_dict["deadline"], "2026-07-31")
        self.assertEqual(application_dict["status"], "Applied")
        self.assertEqual(application_dict["required_skills"], ["python", "sql"])
        self.assertEqual(application_dict["user_skills"], ["python"])
        self.assertEqual(application_dict["interest_level"], 4)
        self.assertEqual(application_dict["notes"], "Requires SQL experience")

    def test_save_and_load_applications(self):
        """Tests that applications can be saved and loaded from JSON."""

        original_data_file = main.DATA_FILE

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            main.DATA_FILE = temp_file.name

        deadline = date(2026, 7, 31)

        application = main.Application(
            "Test Company",
            "Software Intern",
            deadline,
            "Interviewing",
            ["python", "git"],
            ["python"],
            5,
            "Practice technical questions"
        )

        applications = [application]

        main.save_applications(applications)
        loaded_applications = main.load_applications()

        self.assertEqual(len(loaded_applications), 1)
        self.assertEqual(loaded_applications[0].company, "Test Company")
        self.assertEqual(loaded_applications[0].role, "Software Intern")
        self.assertEqual(loaded_applications[0].deadline, deadline)
        self.assertEqual(loaded_applications[0].status, "Interviewing")
        self.assertEqual(loaded_applications[0].required_skills, ["python", "git"])
        self.assertEqual(loaded_applications[0].user_skills, ["python"])
        self.assertEqual(loaded_applications[0].interest_level, 5)
        self.assertEqual(loaded_applications[0].notes, "Practice technical questions")

        main.DATA_FILE = original_data_file
        os.remove(temp_file.name)


if __name__ == "__main__":
    unittest.main()