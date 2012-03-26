"""
Module providing classifiers from orange library
"""

import orange, orngSVM, orngEnsemble
import core
from itertools import izip

orange_learners_modules = [orange, orngSVM, orngEnsemble]
#useful methods

def create_numeric_variable(sid, meta):
    return orange.FloatVariable(sid)

def create_nominal_variable(sid, meta):
    return orange.EnumVariable(sid, values=[str(e) for e in meta.symbols])

orange_variable_map = {
                core.NumericAttribute.ID: create_numeric_variable,
                core.NominalAttribute.ID: create_nominal_variable
                }

def create_basic_variables(meta):
    return [orange_variable_map[m.ID]("atr"+str(i), m) 
                for i,m in enumerate(meta)]


def create_domain_with_cls(meta, cls_meta):
    l = create_basic_variables(meta)
    l.append(create_nominal_variable("classAttr",cls_meta))
    return orange.Domain(l, True)
    


def _basic_convert_sample(domain, sample):
    return [orange.Value(dv, v) for dv, v in 
                    izip(domain, sample.get_values())]


def convert_sample(domain, sample):
    tmp = _basic_convert_sample(domain, sample)
    return orange.Example(domain, tmp+[None])
#this should work if cls is in domain


def convert_sample_with_cls(domain, sample):
    tmp = _basic_convert_sample(domain, sample)
    return orange.Example(domain, tmp + [domain.classVar(sample.get_cls())])
    

def get_orange_classifier_class(name, module=None):
    if module is None:
        for module in orange_learners_modules:
            try:
                classifier_class = getattr(module, name)
                return classifier_class
            except AttributeError:
                pass
        return None
    else:
        module = __import__(module)
        # TODO i think that this won't work if module contains dot
        return getattr(module, name)



class OrangeClassifier(core.Classifier):
    
    
    def __init__(self, name, *args, **kargs):
        self.classifier_class = get_orange_classifier_class(name,
                                        module=kargs.get('module', None))
        if self.classifier_class is None:
            raise ValueError("No %s learner in orange libs", name)
        self.classifier_args = args
        self.classifier_kargs = kargs
        self.classifier = self.classifier_class(*args, **kargs)
        self.domain_with_cls = None
        
    
    def _extract_value(self, cls):
        return cls.value
    
    def classify(self, sample):
        if self.domain_with_cls is None:
            return None
        s = convert_sample(self.domain_with_cls, sample)
        return self._extract_value(self.classifier(s))
    
    
    # TODO: I think that parent method should be fine 
#    def clone(self):
#        return None  

    def classify_pval(self, sample):
        if self.domain_with_cls is None:
            return None
        s = convert_sample(self.domain_with_cls, sample)
        v, p = self.classifier(s, orange.GetBoth)
        return (self._extract_value(v), p[v])

    def class_probabilities(self, sample):
        if self.domain_with_cls is None:
            return None
        s = convert_sample(self.domain_with_cls, sample)
        probs = self.classifier(s, orange.GetProbabilities)
        d = dict(probs.items())
        return d
    
        
    def train(self, samples):
        """
        Trains classifier with given samples.
        
        We recreate domain, because new class could be added
        """
        if not samples:
            self.domain_with_cls = None
            return
        meta = samples[0].meta
        cls_meta = samples[0].cls_meta
        self.domain_with_cls = create_domain_with_cls(meta, cls_meta)
        et = orange.ExampleTable(self.domain_with_cls)
        et.extend([convert_sample_with_cls(self.domain_with_cls, s) 
                                for s in samples])
        self.classifier = self.classifier_class(*self.classifier_args,\
                                                **self.classifier_kargs)
        self.classifier = self.classifier(et)

#        self.classifier = self.classifier_class(et, *self.classifier_args,\
#                                                **self.classifier_kargs)

