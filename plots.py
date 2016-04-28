from matplotlib import pyplot as plt
import sys

def plot_bests(data_file):
	with open(data_file) as f:
		content = f.readlines()
	f.close()

	best_list = []
	avg_list = []

	for i in range(0, len(content), 2):
		best_list.append(content[i].replace('\n', '').split(' '))
		avg_list.append(content[i + 1].replace('\n', '').split(' '))

	bestest = [0 for i in range(len(best_list[0]))]
	avgs = [0 for i in range(len(best_list[0]))]

	for i in range(len(best_list[0])):
		for k in range(len(best_list)):
			bestest[i] += float(best_list[k][i])
			avgs[i] += float(avg_list[k][i])

	bestest = [k / len(best_list) for k in bestest]
	avgs = [k / len(best_list) for k in avgs]

	plt.ylabel('Fitness')
	plt.xlabel('Generation')
	plt.title('Evolution of Fitness over Generations')

	p2 = plt.plot(bestest, 'r', label = 'Best over all over generations')
	p3 = plt.plot(avgs, 'g', label = 'Average best over generations')

	plt.legend(loc='best')
	plt.show()

if __name__ == '__main__':
	plot_bests(sys.argv[1])
