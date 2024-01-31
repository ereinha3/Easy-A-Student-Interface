"""
Unit Tests for Web Scraper Module
2024-01-20
by ajps

Test name matching
"""

# resolve importing project Python files
import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, project_root)

# resolve finding filenames in tests dir
tests_dir = os.path.abspath(os.path.dirname(__file__))
cur_dir = os.getcwd()
if tests_dir != cur_dir:
    os.chdir(tests_dir)
    print("Please run unit tests from tests dir")
    print(f"Changed working dir: {os.getcwd()}")

# import modules
import unittest
import scrapedNames
import gradeDataNames
# FIXME change to data access module once name-matching logic is moved over
import nameMatch as nameMatch

expand_prints = False

class TestAbnormalNames(unittest.TestCase):
    """
    Test for abnormal names in sample data.
    These are provided to improve name matching by analyzing sample data.
    These tests do not test program logic and will always pass.
    """

    def test_empty_names_gradedata(self):
        """
        Check for empty string names in gradedata sample.
        """
        names = gradeDataNames.gradedata_names_sample
        empty_names = {}
        for i in range(len(names)):
            if names[i] == "":
                empty_names[i] = names[i]
        # print test results
        if len(empty_names.keys()) > 0:
            if not expand_prints:
               empty_names = len(empty_names)
            print(f"gradedata empty names: {empty_names}")
        else:
            print("No empty names in gradedata sample")

    def test_non_alphabetic_names_gradedata(self):
        """
        Check for names without alphabetic characters in gradedata sample.
        """
        names = gradeDataNames.gradedata_names_sample
        non_alpha_names = {}
        for i in range(len(names)):
            for char in names[i]:
                if char.isalpha():
                    break
                non_alpha_names[i] = names[i]
        # print test results
        if len(non_alpha_names.keys()) > 0:
            if not expand_prints:
                non_alpha_names = len(non_alpha_names)
            print(f"gradedata non-alphabetic names: {non_alpha_names}")
        else:
            print("No non-alphabetic names in gradedata sample")

    def test_no_last_name_gradedata(self):
        """
        Check for names with no last name or which only provide last initial in gradedata sample.
        """
        names = gradeDataNames.gradedata_names_sample
        no_last_names = {}
        for i in range(len(names)):
            last_name = names[i].split(",")[0]
            # remove period commonly added to initials
            last_name = "".join(char for char in last_name if char.isalpha())
            if len(last_name) <= 1:
                no_last_names[i] = names[i]
        # print test results
        if len(no_last_names) > 0:
            if not expand_prints:
                no_last_names = len(no_last_names)
            print(f"gradedata no last names: {no_last_names}")
        else:
            print("No missing last names in gradedata sample")

    def test_double_last_name_gradedata(self):
        """
        Check for double last names separated by space in gradedata sample.
        """
        names = gradeDataNames.gradedata_names_sample
        double_last_names = {}
        for i in range(len(names)):
            last_name = names[i].split(",")[0]
            # remove period commonly added to initials
            if " " in last_name:
                double_last_names[i] = names[i]
        # print test results
        if len(double_last_names) > 0:
            if not expand_prints:
                double_last_names = len(double_last_names)
            print(f"gradedata double last names: {double_last_names}")
        else:
            print("No double last names in gradedata sample")

    def test_hyphenated_last_name_gradedata(self):
        """
        Check for double last names separated by hyphen in gradedata sample.
        """
        names = gradeDataNames.gradedata_names_sample
        hyphen_last_names = {}
        for i in range(len(names)):
            last_name = names[i].split(",")[0]
            # remove period commonly added to initials
            if "-" in last_name:
                hyphen_last_names[i] = names[i]
        # print test results
        if len(hyphen_last_names) > 0:
            if not expand_prints:
                hyphen_last_names = len(hyphen_last_names)
            print(f"gradedata hyphenated last names: {hyphen_last_names}")
        else:
            print("No hyphenated last names in gradedata sample")

    def test_wordy_names_scraped(self):
        """
        Check for names with more than 3 words (or initials) in scraped names sample.
        Hyphenated names treated as one word.
        """
        names = scrapedNames.scraped_names_sample
        wordy_names = {}
        for i in range(len(names)):
            name_list = names[i].split(" ")
            if len(name_list) >= 4:
                wordy_names[i] = names[i]
        # print test results
        if len(wordy_names) > 0:
            if not expand_prints:
                wordy_names = len(wordy_names)
            print(f"scraped wordy names: {wordy_names}")
        else:
            print("No wordy names in scraped sample")

class TestNameMatch(unittest.TestCase):
    """
    Test for the efficacy of the functions dedicated to matching names
    """

    def test_match_simple(self):
        """
        Test the full name matching process with an example name from gradedata sample.
        There is only one logical match in the scraped names sample.
        """
        example_name = "Johnson, Eric Allen"
        # create dict from scraped names sample
        names_dict = nameMatch.scraped_names_to_dict(scrapedNames.scraped_names_sample)
        # try to match name
        result = nameMatch.match_name(example_name, names_dict)
        self.assertEqual(["Eric A. Johnson"], result)


    def test_match_similar_names(self):
        """
        Test the full name matching process with an example name.
        A contrived scraped names list is given with multiple matching last names.
        """
        example_name = "Doe, Jon A."
        # create dict from this list of contrived names
        scraped_names = ["Jon A. Doe", "John B. Doe", "John C. Smith"]
        names_dict = nameMatch.scraped_names_to_dict(scraped_names)
        # try to match name
        result = nameMatch.match_name(example_name, names_dict)
        self.assertEqual(["Jon A. Doe"], result)

    def test_match_wordy_last_name(self):
        """
        Test the full name matching process with an example name.
        The example name has 3 last names.
        """
        example_name = "Chioma Tufayl Regin, Jocelyn Rigantona"
        # create dict from this list of contrived names
        scraped_names = ["Jocelyn Rigantona China Tufayl Regin",
                         "Jocelyn Rigantona Chioma Tulip Regin",
                         "Jocelyn Rigantona Chioma Tufayl Regent",
                         "Jocelyn Rigantona Chioma Tufayl Regin"]
        names_dict = nameMatch.scraped_names_to_dict(scraped_names)
        # try to match name
        result = nameMatch.match_name(example_name, names_dict)
        self.assertEqual(["Jocelyn Rigantona Chioma Tufayl Regin"], result)

    def test_match_wordy_given_name(self):
        """
        Test the full name matchcing process with an exmaple name.
        The example name has 3 given names, including one initial.
        The example scraped names will sometimes use initials or extra given names.
        """
        example_name = "Sargon, Jeanne Ita A. Kenina"
        # creat a dict from this list of contrived names
        scraped_names = ["Jeanne Ita Anatu Kenina Sargon",
                         "J. Ita Anatu Kenina Sargon", # first initial
                         "Jeanne Ita Anatu Kenina Neva Sargon", # extra given name
                         "Jeanne Ita Antas K. Sargon", # middle initial
                         "Joanna Ita Anatu Kenina Sargon", # wrong
                         "Jeanne Ita Anatu Keller Sargon"] # wrong
        names_dict = nameMatch.scraped_names_to_dict(scraped_names)
        # try to match name
        result = nameMatch.match_name(example_name, names_dict)
        expected = ["Jeanne Ita Anatu Kenina Sargon",
                    "J. Ita Anatu Kenina Sargon",
                    "Jeanne Ita Anatu Kenina Neva Sargon",
                    "Jeanne Ita Antas K. Sargon"]
        self.assertEqual(expected, result)


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "expand":
        # enable expanding information for sample name tests
        expand_prints = True if "expand" in sys.argv else False
        sys.argv.pop(1)

    unittest.main()
else:
    print("Importing unit tests is not recommended (unless using iPython interactive shell)")