#import math
from simple_classif import *
from ..extras.tools import *
#MLPY classifiers:
import numpy as np
import mlpy

class SimpleMlpyClassifier(SimpleClassifier):
    """A base class for a single MlPy classifier.
    """

    def train(self, vals, etiq):
        """Retrains the classifier using the passed - values and the etiquettes.
        """
        temp_cl = self.create_classifier()
        arr = np.array(vals)
        etiq = np.array(etiq)
        temp_cl.compute(arr, etiq)
        self.classifier = temp_cl

    def create_classifier(self):
        """function of creating a classifier.
        """
        abstract()

    def reaction(self, data):
        """Returns the reaction of this single classifer for the data.
        """
        abstract()


#general types of mlpy wrappers:
class SimpleMlpyIntClassifier(SimpleMlpyClassifier):
    """A base class for a single BINARY MlPy classifier, wrapping the mlpy library function.
    """
    def reaction(self,  data):
        """Returns the reaction of this single classifer for the data.
        """
        xtr = np.array(data)
        return self.classifier.predict(xtr)

class SimpleMlpyRealClassifier(SimpleMlpyClassifier):
    """A base class for a single REAL MlPy classifier, wrapping the mlpy library function.
    """
    def reaction(self,  data):
        """Returns the reaction of this single classifer for the data.
        """
        xtr = np.array(data)
        self.classifier.predict(xtr)
        return self.classifier.realpred

#specific instances of wrappers of classifiers from MLPY:
class SimpleFdaRealClassifier(SimpleMlpyRealClassifier):
    """Single FDA classifier
    """
    def create_classifier(self):
        """Creates an Fda classifier
        """
        return mlpy.Fda(1)

class SimpleSvmRealClassifier(SimpleMlpyRealClassifier):
    """Single SVM classifier
    """
    def create_classifier(self):
        """Creates an Fda classifier
        """
        return mlpy.Svm('linear', 0.05, 1.0, 0.01, 0.01, 2000, 0.5, 1.0, 1.0, True)

class SimpleKnnIntClassifier(SimpleMlpyIntClassifier):
    """Single KNN classifier..
    """
    def create_classifier(self):
        """Creates an Fda classifier
        """
        return mlpy.Knn(1)
