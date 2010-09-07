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


def load_params(file):
	return default_params()

	
def default_params():
	from cog_abm.stimuli.stimulus import SimpleStimulus
	from cog_abm.extras.color import get_1269Munsell_chips
	return {'stimuli' : [SimpleStimulus(c) for c in get_1269Munsell_chips()],  
					'context_size' : 4,
					'num_agents': 10,
					'num_iter' : 1000,
					'inc_category_treshold' : 0.90,
					'topology' : None, 
					'classifier' : None,
					'alpha' : 0.1, 
					'beta' : 1., 
					'sigma' : 4.
				}



if __name__ == "__main__":
	
	import analyzer
	import optparse
	
	optp = optparse.OptionParser()
	
	optp.add_option('-v', '--verbose', dest='verbose', action='count',
			help="Increase verbosity (specify multiple times for more)")
			
	optp.add_option('-g', '--game', action="store", type="string", dest="game", 
			help="Which type of game agents play", default="DG")
			
	optp.add_option('-f','--file', action="store", dest='file', type="string",
			help="output file with results")

	# Parse the arguments (defaults to parsing sys.argv).
	opts, args = optp.parse_args()
	
	# Here would be a good place to check what came in on the command line and
	# call optp.error("Useful message") to exit if all it not well.

	log_level = logging.DEBUG # default logging.WARNING

	if opts.verbose == 1:
		log_level = logging.INFO
		
	elif opts.verbose >= 2:
		log_level = logging.DEBUG
	# Set up basic configuration, out to stderr with a reasonable default format.
	logging.basicConfig(level=log_level)

	if opts.game not in ["DG","GG"]:
		optp.error("Wrong or no game specified. Allowed: DG, GG")
	
	sys.path.append("../")
	from cog_abm.stimuli.stimulus import SimpleStimulus
	from cog_abm.extras.color import *
	#from presenter.charts import *
	from steels.steels_experiment import *
	
	#stimuli = default_stimuli()
	#stimuli = Color.get_1296Munsell_chips()
	#stimuli = [SimpleStimulus(Color(z*9, (i-4)*10, 10*(j-4))) for i in xrange(11) for j in xrange(11) for z in xrange(11)]

	params = load_params(None)
				
	if opts.game == "DG":
		r = steels_basic_experiment_DG(**params)
	elif opts.game == "GG":
		r = steels_basic_experiment_GG(**params)
		

	
	save_res((r, params), opts.file)
#		r = steels_basic_experiment_GG(**arg)
#		r = steels_basic_experiment_GG(num_agents = 2, 
#					alpha = alpha, stimuli = stimuli, context_size=4, inc_category_treshold = 0.80, num_iter = 100)

		

	
#	res = []
#	from time import time
#	start_time = time()
#	logging.info("Counting category start...")
#	res = [(alpha, [(it, analyzer.count_categ(agents, stimuli)) for it, agents in listt])\
#                                           	for alpha, listt in wyn]
#	logging.info("Counting category finish. Total time: "+str(time()-start_time))
#
#	
#	#analyzer.wykres3d(wyn)
#	
#	#jesli teraz damy:
#	#analyzer.wykres(res[0][1], "num of iter","num of categ")
#	# to otrzymamy wkres ilosci kategori dla wszystkich graczy
#	
#	#srednia ilosc kategori:
#	res = [(alpha, [(it, float(sum(categ_num))/len(categ_num)) for it, categ_num in list]) for alpha, list in res]
#	analyzer.wykres(res[0][1], "num of iter","num of categ")
	
	#analyzer.wykres3d(res)
