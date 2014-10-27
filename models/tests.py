import unittest

from models.document import Document


class DocumentTest(unittest.TestCase):
    file_name = 'this_is_a_file.txt'
    meta = {'title': 'test yeah',
            'author': 'gord'
           }
    body = 'In id tristique orci. Aenean.'

    def test_clone(self):
        doc = Document(file_name=self.file_name,
                       body=self.body,
                       metadata=self.meta)
        doc_cloned = doc.clone()
        self.assertEqual(doc_cloned.file_name, doc.file_name)
        self.assertEqual(doc_cloned.metadata, doc.metadata)
        self.assertEqual(doc_cloned.body, doc.body)
        self.assertEqual(doc, doc_cloned)

        doc_cloned.file_name = 'nope'
        self.assertNotEqual(doc, doc_cloned)

        doc_cloned.file_name = doc.file_name
        doc_cloned.metadata = None
        self.assertNotEqual(doc, doc_cloned)

        doc_cloned.metadata = doc.metadata
        doc_cloned.body = ''
        self.assertNotEqual(doc, doc_cloned)
