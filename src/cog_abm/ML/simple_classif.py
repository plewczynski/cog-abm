from ..extras.tools import *

class SimpleClassifier(object):
    """A base class for a single classifier. This class should be a base for each wrapper of an ML library function.
    """
    def __init__(self):
        """
        """
        self.classifier = self.create_classifier()

    def train(self, vals, etiq):
        """Retrains the classifier using the passed - values and the etiquettes.
        """
        abstract()

    def create_classifier(self):
        """function of creating a classifier.
        """
        abstract()

    def reaction(self, data):
        """Returns the reaction of this single classifer for the data.
        """
        abstract()
