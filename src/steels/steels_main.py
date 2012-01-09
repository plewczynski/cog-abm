import sys
import logging
import cPickle
from time import localtime, strftime


def save_res(results, f_name = None):
	if f_name is None:
		f_name = strftime("experiment_%Y%m%d_%H_%M_%S.result", localtime())
	f = open(f_name, "w")
	cPickle.dump(results, f)
	f.close()


def load_params(pfile):
	if pfile is None:
		return default_params()
	
	from cog_abm.extras.parser import Parser
	return Parser().parse_simulation(pfile)
	

	
def default_params():
	from cog_abm.extras.color import get_1269Munsell_chips
	return {	'interaction_type': "DG", 
					'stimuli' : get_1269Munsell_chips(),  
					'num_agents': 10,
					'context_size' : 4,
					'num_iter' : 1000,
					'dump_freq':100, 
					'topology' : None, 
					'classifier' : None,
					'alpha' : 0.1, 
					'beta' : 1., 
					'sigma' : 10., 
					'inc_category_treshold' : 0.95
				}



if __name__ == "__main__":
	
	#import analyzer
	import optparse
	
	optp = optparse.OptionParser()
	
	optp.add_option('-v', '--verbose', dest='verbose', action='count',
			help="Increase verbosity (specify multiple times for more)")
			
	optp.add_option('-g', '--game', action="store", type="string", dest="game", 
			help="Which type of game agents play"
			, default="DG")
			
	optp.add_option('-f','--file', action="store", dest='file', type="string",
			help="output file with results")
	
	optp.add_option('-p','--params_file', action="store", dest='param_file', type="string",
			help="file with parameters")

	# Parse the arguments (defaults to parsing sys.argv).
	opts, args = optp.parse_args()
	

	log_level = logging.DEBUG # default logging.WARNING

	if opts.verbose == 1:
		log_level = logging.INFO
		
	elif opts.verbose >= 2:
		log_level = logging.DEBUG
	# Set up basic configuration, out to stderr with a reasonable default format.
	logging.basicConfig(level=log_level)

	#if opts.game not in ["DG","GG"]:
	#	optp.error("Wrong or no game specified. Allowed: DG, GG")
	
	sys.path.append('../')
	sys.path.append('')
	from steels.steels_experiment import *

	params = load_params(opts.param_file)
	
	#print params
	
	if opts.game is not None:
		params["interaction_type"]  == opts.game
			

	if params["interaction_type"] == "DG":
		#r = steels_basic_experiment_DG
		r = steels_basic_experiment_DG(**params)
	elif params["interaction_type"] == "GG":
		r = steels_basic_experiment_GG(**params)
		

	
	save_res((r, params), opts.file)
