

import sys
import logging
import cPickle
import math

from itertools import imap
from time import time

sys.path.append('../')

from cog_abm.extras.tools import get_progressbar



def compose(fun_out, fun_in):
	def composition(*args, **kwargs):
		return fun_out(fun_in(*args, **kwargs))
	
	return composition



def avg(lista):
	return [math.fsum(lista)/len(lista)]


def wmin(lista):
	return [min(lista)]


def wmax(lista):
	return [max(lista)]



cc_computed = {}

def count_categ(agents, params, it):

	global cc_computed
	try:
		stimuli = params['environments']['global'].stimuli
	except:
		stimuli = params['STIMULI']
	
	def pom(a):
		Z = {}
		for s in stimuli:
			Z[a.sense_and_classify(s)]=1
		return len(Z)
	
	tmpr = cc_computed.get(it, None)
	if tmpr is None:
		tmpr = [pom(a) for a in agents]
		cc_computed[it] = tmpr
	
	return tmpr
	


from metrics import *

#def avg_cc(agents, params, it):
#	return [float(sum(count_categ(agents, params, it))) / len(agents)]



fun_map = {
		'cc':count_categ, 
		'it': lambda ag, par, it : [it], 
		'DSA': lambda ag, par, it: map(DS_A, ag), 
		'DS': lambda ag, par, it: [DS(ag, it)], 
		'CSA': lambda ag, par, it: map(CS_A, ag), 
		'CS': lambda ag, par, it: [CS(ag, it)], 
		'cv': lambda ag, par, it:[cv(ag, it)]
		}



pref_fun_map = {
		'avg':avg, 
		'min':wmin, 
		'max':wmax
		}



def gen_res(results, params, funs):
	start_time = time()
	logging.info("Calculating stats...")

	pb = get_progressbar()	
	retv = [[x for f in funs for x in f(agents, params, it)]
					for it, agents in pb(results)]

	logging.info("Calculating stats finished. Total time: "+str(time()-start_time))
	return retv


def main():

	import optparse
	
	usage = "%prog [-c] [-v] -f FILE statistic1 statistic2 ...\n"+\
			"where statistic in {"+";".join(fun_map.keys())+"}"
	optp = optparse.OptionParser(usage = usage)
	
	optp.add_option('-v', '--verbose', dest='verbose', action='count',
			help="increase verbosity (specify multiple times for more)")
	
	optp.add_option('-c','--chart', action="store_true", dest='chart',
			help="specifies output to be a chart")
	
	optp.add_option('-f','--file', action="store", dest='file', type="string",
			help="input file with results. THIS OPTION IS NECESSARY!")
	
	optp.add_option('--xlabel', action="store", dest='xlabel', type="string",
			help="Label of x-axis")
	
	optp.add_option('--ylabel', action="store", dest='ylabel', type="string",
			help="Label of y-axis")
	

	opts, args = optp.parse_args()
	
	if len(args) == 0:
		optp.error("No argument given!")

	
	if opts.file is None or opts.file == "":
		optp.error("No or wrong file specified (option -f)")
	
	if opts.chart == True and len(args)<2:
		optp.error("Can't draw a chart with one dimension data")



	log_level = logging.INFO #logging.DEBUG # default logging.WARNING


	if opts.verbose == 1:
		log_level = logging.INFO
		
	elif opts.verbose >= 2:
		log_level = logging.DEBUG

	
	# Set up basic configuration, out to stderr with a reasonable default format.
	logging.basicConfig(level=log_level)
	
	f = open(opts.file)
	res, params = cPickle.load(f)
	f.close()
	
	funcs = []
	for arg in args:
		ind = arg.find("_")
		fun = None
		if  ind != -1:
			p_fun = pref_fun_map.get(arg[0:ind])
			
			m_fun = fun_map.get(arg[ind+1:len(arg)])

			if p_fun is not None and m_fun is not None:
				fun = compose(p_fun, m_fun)


		if fun is None:
			fun = fun_map.get(arg, None)
			
		if fun is not None:
			funcs.append(fun)
		else:
			logging.warning("Unrecognized option %s - ignoring", arg)

	wyn = gen_res(res, params, funcs)
	
	if opts.chart is not None:
		from presenter.charts import wykres
		data = []
		#print wyn
		map(lambda x: data.append((x[0], x[1:])), wyn)
		wykres(data, opts.xlabel, opts.ylabel)
		
	else:
		for r in wyn:
			print "\t".join(imap(str, r))




if __name__ == "__main__":
	main()
