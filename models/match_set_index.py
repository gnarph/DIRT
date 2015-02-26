"""
Module for handling a directory of reports
"""
import re

from models import match_set_factory
from utilities import path
from utilities import file_ops

FILE_NAME_REGEX = r'^(?P<alpha>.+)__(?P<beta>.+)__CMP\.json$'


class MatchSetIndex(object):
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

    def get_all_file_names(self):
        """
        Get all files names in the index
        :return: list of MatchSet json file names
        """
        regex = re.compile(FILE_NAME_REGEX)
        names = set()
        files = path.iter_files_in(self.out_dir)
        for full_path in files:
            file_name = file_ops.get_file_name_only(full_path)
            match = regex.search(file_name)
            alpha_name = match.group('alpha')
            beta_name = match.group('beta')
            names.add(alpha_name)
            names.add(beta_name)
        return names

    def get_all_matched_documents(self, focus_name):
        """
        Get a list of all documents matched in the index with the
        focus document
        :param focus_name: name of the focus document
        :return: list of Documents matched with focus
        """
        all_match_sets = self.get_all_match_sets(focus_name)
        docs = set()
        for ms in all_match_sets:
            if focus_name not in ms.alpha_doc.file_name:
                docs.add(ms.alpha_doc)
            else:
                docs.add(ms.beta_doc)
        return docs

    def get_matched_document_count(self, focus_name):
        """
        Get number of matched documents
        :return: int number of matched documents
        """
        set_names = self.set_names_for_focus(focus_name)
        return len(list(set_names))

