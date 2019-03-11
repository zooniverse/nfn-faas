import os
import urllib.parse as urlparse

class ClassificationParser(object):
    '''A classification parser'''

    def __init__(self, classification):
        self.classification = classification
        self.created_at = self.classification['created_at']
        self.params = {k: v[0] for k, v in urlparse.parse_qs(os.getenv("Http_Query")).items()}
        self.subject_metadata = {k.lower():v for k,v in self.classification['subject']['metadata'].items()}
        self.metadata = {k.lower():v for k,v in self.classification['metadata'].items()}
        self.tasks = self.classification['annotations']
        self.properties = {}

    def get_basic(self, label):
        if label in self.subject_metadata:
           return self.subject_metadata[label]
        elif label in self.params:
            task = self.params[label]
            if self.params[label] in self.tasks:
                value = self.tasks[task]
                return value[0]['value']
            else:
                return None
        else:
            return None