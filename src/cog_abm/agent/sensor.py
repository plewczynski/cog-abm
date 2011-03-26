from cog_abm.stimuli.perception import SimplePerception

class Sensor(object):
    """ Basic sensor.
    """
    pass

class SimpleSensor(Sensor):
	""" Just gives back what he got """
	
	def sense(self, object):
		return SimplePerception(object.content)
