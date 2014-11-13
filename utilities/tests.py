import unittest

import utilities.path


class PathTest(unittest.TestCase):

    def test_remove_dir(self):
        utilities.path.delete_folder('doesnotexistokay')