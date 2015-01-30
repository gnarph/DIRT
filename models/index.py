"""
Module for handling a directory of reports
"""

from models import match_set_factory
from utilities import path


class Index(object):
    """
    Class for handling a directory of output MatchSet json files
    """

    def __init__(self, out_dir):
        self.out_dir = out_dir

    def set_names_for_focus(self, doc_name):
        """
        Get the file names for the match sets corresponding
        to a focus document
        :param doc_name: name of a focus document, stripped of
                         extension
        :return: generator
        """
        files = path.iter_files_in(self.out_dir)
        for file_name in files:
            if doc_name in file_name:
                yield file_name

    def get_all_match_sets(self, focus_name):
        """
        Return a list of all match sets applying to the focus
        :param focus_name:
        :return:
        """
        file_names = self.set_names_for_focus(focus_name)
        all_sets = [match_set_factory.from_json(f) for f in file_names]
        for ms in all_sets:
            if focus_name not in ms.alpha_doc.file_name:
                ms.swap_alpha_beta()

        return all_sets

