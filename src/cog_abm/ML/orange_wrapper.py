"""
Module providing classifiers from orange library
"""

import orange, orngTree


class OrangeClassifier(object):
    
    
    def __init__(self, name, *args, **kargs):
        self.classifier_class = getattr(orange, name)
        self.classifier_args = args
        self.classifier_kargs = kargs
        self.classifier = self.classifier_class(*args, **kargs)
        self.domain_with_cls = None
        self.domain = None
        
    
    def classify(self, stimulus):
        st = self._convert_sample(stimulus)
        return self.classifier(st)
    
    
    def clone(self):
        return None  # TODO 

    
    def train(self, samples):
        """
        Trains classifier with given samples.
        samples is iterable of pairs (s,c) where:
        s - sample
        c - class ID
        
        We recreate domain, because new class could be added
        """
        l = [orange.FloatVariable("atr"+str(i)) for i in xrange(len(samples[0][0]))]
        classes = set([c for _,c in samples])
        classattr = orange.EnumVariable("classAttr", values=[str(e) for e in classes])
        l.append(classattr)

        self.domain_with_cls = orange.Domain(l, True)
        l = [self._convert_sample_with_cls(s, c) for s, c in samples]
        et = orange.ExampleTable(self.domain_with_cls)
        et.extend(l)
        self.classifier = self.classifier_class(et, *self.classifier_args, \
                                                **self.classifier_kargs)

    
    def _convert_sample(self, sample):
        tmp = sample+[None]
        return orange.Example(self.domain_with_cls, tmp)
    
    
    def _convert_sample_with_cls(self, sample, cls):
        tmp = sample+[self.domain_with_cls.classVar(str(cls))]
        return orange.Example(self.domain_with_cls, tmp)
    
    