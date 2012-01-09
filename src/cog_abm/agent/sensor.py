from ..extras.tools import abstract

class Sensor(object):
    """ Basic sensor.
    """
    
    def sense(self, item):
        abstract()


class SimpleSensor(Sensor):
	""" Just gives back what he got """
	
	def sense(self, item):
		return item


