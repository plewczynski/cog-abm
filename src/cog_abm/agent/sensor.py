from ..extras.tools import abstract
from ..ML.diversity import new_sample_specified_attributes

class Sensor(object):
    """ Basic sensor.
    """
    
    def sense(self, item):
        abstract()


class SimpleSensor(Sensor):
    """ Just gives back what he got """
    
    def __init__(self, mask=None):
        self.mask = mask

    def sense(self, item):
        if self.mask is None:
            return item
        else:
            return new_sample_specified_attributes(item, self.mask)
