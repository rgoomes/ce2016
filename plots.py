from matplotlib import pyplot as plt
import sys

def plot_bests(data_file):
	with open(data_file) as f:
		content = f.readlines()
	f.close()

	bests = content[0].replace('\n', '').split(' ')
	bestest = content[1].replace('\n', '').split(' ')
	avgs = content[2].replace('\n', '').split(' ')

	for i in range(len(bests)):
		bests[i] = float(bests[i])
		bestest[i] = float(bestest[i])
		avgs[i] = float(avgs[i])

	plt.ylabel('Fitness')
	plt.xlabel('Generation')
	plt.title('Evolution of Fitness over Generations')

	p1 = plt.plot(bests, 'b-o', label = 'Generation Best')
	p2 = plt.plot(bestest, 'r-o', label = 'Best Over All')
	p3 = plt.plot(avgs, 'g-s', label = 'Generation Average')

	plt.legend(loc='best')
	plt.show()

if __name__ == '__main__':
	plot_bests(sys.argv[1])