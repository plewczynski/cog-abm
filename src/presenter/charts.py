
import numpy as np
import matplotlib.pyplot as plt


def wykres(res, xlabel, ylabel):

	plt.ylabel(ylabel)
	plt.xlabel(xlabel)
	ax = np.array([x for x, _ in res])
	ay = np.array([y for _, y in res])
	
	plt.plot(ax, ay)
	plt.show()
	


def wykres3d(wyn, xlabel = 'alpha', ylabel = 'iteracja', zlabel = 'num of categ'):


	import pylab as p
	import mpl_toolkits.mplot3d.axes3d as p3
	

	x = np.outer(np.array([x for x, _ in wyn]), np.ones(len(wyn[0][1])))

	#y = np.outer(np.array([it for it, _, _ in wyn[0][1]]), np.ones(len(wyn)))
	y = np.outer(np.ones(len(wyn)), np.array([y for y, _ in wyn[0][1]]))

	tmpz = [[z for _, z in r] for _, r in wyn]

	z = np.array(tmpz)


	
	fig=p.figure()
	ax = p3.Axes3D(fig)
	
	#print "\n", np.ravel(x), "\n", np.ravel(y), "\n", np.ravel(z)
	
	#ax.plot_surface(x,y,z)
	ax.plot_wireframe(x,y,z)
	#ax.plot3D(np.ravel(x), np.ravel(y), np.ravel(z))
	
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.set_zlabel(zlabel)
	fig.add_axes(ax)
	
	p.show()
