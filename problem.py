from sys import *
import random, os, operator, math

if version_info.major == 3:
	import configparser
else:
	import ConfigParser as configparser

class Representation:
	def get_weight(self, problem):
		return sum([problem.item_weights[problem.items[i]]
			for i in range(problem.total_items) if self.ks[i] == 1])

	def get_ratio(self, item, problem):
		return problem.item_values[problem.items[item]] \
			/ problem.item_weights[problem.items[item]]

	def repair(self, problem):
		feno = [[i, problem.items[i], self.get_ratio(i, problem)]
			for i in range(problem.total_items) if self.ks[i] == 1]

		feno.sort(key=operator.itemgetter(2))
		it, weight = 0, self.get_weight(problem)

		while(weight > problem.W):
			pos, item = feno[it][0], feno[it][1]
			weight -= problem.item_weights[item]
			self.ks[pos] = 0
			it += 1

	def isvalid(self, problem):
		return self.get_weight(problem) <= problem.W

	def evaluate(self, problem):
		weight = value = time = 0.0

		for i in range(problem.num_cities):
			city = self.tsp[i]

			for j in range(problem.bounds[city][0], problem.bounds[city][1]):
				if self.ks[j] == 1:
					item = problem.items[j]
					value += problem.item_values[item]
					weight += problem.item_weights[item]

			vc = problem.vmax - weight * (problem.vmax - problem.vmin) / problem.W
			time += problem.dists[city][self.tsp[(i+1) % problem.num_cities]] / vc

		self.score = value - problem.R * time

	def nearest_neighbor(self, problem):
		path = [random.randint(0, problem.num_cities - 1)]
		city_inpath = [0 for _ in range(problem.num_cities)]
		city_inpath[path[0]] = 1

		for i in range(1, problem.num_cities):
			dist = float("inf")

			for j in range(problem.num_cities):
				if not city_inpath[j] and problem.dists[path[i-1]][j] < dist:
					dist = problem.dists[path[i-1]][j]
					next_city = j

			path.append(next_city)
			city_inpath[next_city] = 1

		return path

	def greedy_knapsack(self, problem):
		plan = [0 for _ in range(problem.total_items)]
		feno = [[i, problem.items[i], self.get_ratio(i, problem)]
			for i in range(problem.total_items)]

		feno.sort(key=operator.itemgetter(2), reverse=True)

		weight = it = 0
		while(weight < problem.W and it < problem.total_items):
			pos, item = feno[it][0], feno[it][1]
			if weight + problem.item_weights[item] <= problem.W:
				weight += problem.item_weights[item]
				plan[pos] = 1

			it += 1

		return plan

	def heuristic_indiv(self, problem):
		self.ks  = self.greedy_knapsack(problem)
		self.tsp = self.nearest_neighbor(problem)

	def random_indiv(self, problem):
		self.ks  = [random.randint(0,1) for _ in range(problem.total_items)]
		self.tsp = random.sample(range(problem.num_cities), problem.num_cities)
		self.repair(problem)

	def __init__(self, problem):
		if problem != None:
			self.heuristic_indiv(problem);

class Problem:
	def read_conf(self, conf):
		if not os.path.isfile(conf):
			print('ttp: invalid conf file')
			exit(-1)

		parser = configparser.ConfigParser()
		parser.read(conf)

		self.generations = int(parser.get('configs', 'generations'))
		self.population_size = int(parser.get('configs', 'population_size'))
		self.crossover_prob = float(parser.get('configs', 'crossover_prob'))
		self.mutation_prob = float(parser.get('configs', 'mutation_prob'))
		self.elite_size = float(parser.get('configs', 'elite_size'))
		self.tournament_size = int(parser.get('configs', 'tournament_size'))

	def read_input1(self):
		self.num_cities = int(stdin.readline().rstrip())
		num_items  = int(stdin.readline().rstrip())
		self.W = float(stdin.readline().rstrip())
		self.vmax = float(stdin.readline().rstrip())
		self.vmin = float(stdin.readline().rstrip())
		self.R = float(stdin.readline().rstrip())

		self.dists = []
		for i in range(self.num_cities):
			distances = [float(n) for n in stdin.readline().rstrip().split()]
			self.dists.append(distances)

		self.item_weights = [float(n) for n in stdin.readline().rstrip().split()]
		self.item_values = [float(n) for n in stdin.readline().rstrip().split()]

		item_locations = []
		for i in range(num_items):
			locations = [int(n) for n in stdin.readline().rstrip().split()]
			item_locations.append(locations)

		self.total_items = sum(map(sum, item_locations))
		self.items = []
		self.bounds = []

		total = 0
		for i in range(self.num_cities):
			self.bounds.append([total, 0])
			for j in range(num_items):
				if item_locations[j][i] == 1:
					total += 1
					self.bounds[i][1] = total
					self.items.append(j)

	def read_input2(self):
		stdin.readline(), stdin.readline()

		self.num_cities = int(stdin.readline().split('\t')[1])
		self.total_items = int(stdin.readline().split('\t')[1])
		self.W = float(stdin.readline().split('\t')[1])
		self.vmin = float(stdin.readline().split('\t')[1])
		self.vmax = float(stdin.readline().split('\t')[1])
		self.R = float(stdin.readline().split('\t')[1])

		stdin.readline(), stdin.readline()
		cities = []

		for i in range(self.num_cities):
			tmp = stdin.readline().split()
			cities.append([int(tmp[0]), int(tmp[1])])

		self.dists = [[0.0 for _ in range(self.num_cities)] for _ in range(self.num_cities)]
		for i in range(self.num_cities):
			for j in range(self.num_cities):
				if i != j:
					self.dists[i][j] = math.sqrt((cities[i][0] - cities[j][0])**2
						+ (cities[i][1] - cities[j][1])**2)

		stdin.readline()
		itemset = set()
		all_items = []
		self.bounds = [[0, 0] for _ in range(self.num_cities)]

		for i in range(self.total_items):
			tmp = stdin.readline().split()
			all_items.append([(float(tmp[1]), float(tmp[2])), int(tmp[3])])
			itemset.add((float(tmp[1]), float(tmp[2])))
			self.bounds[int(tmp[3])-1][1] += 1

		itemset = list(itemset)

		self.item_weights = [w for (v,w) in itemset]
		self.item_values = [v for (v,w) in itemset]

		for i in range(1, self.num_cities):
			self.bounds[i][0] = self.bounds[i-1][1]
			self.bounds[i][1] += self.bounds[i-1][1]

		self.items = []
		for i in range(self.num_cities):
			for j in range(self.total_items):
				if(all_items[j][1] - 1 == i):
					self.items.append(itemset.index(all_items[j][0]))

	def __init__(self, args):
		self._nodes = 0
		self.best_cromo = None
		self.best_score = -float("inf")

		self.debug = args[0]
		self.read_conf(args[1])

		if int(args[2]) == 1:
			self.read_input1()
		elif int(args[2]) == 2:
			self.read_input2()
		else:
			print('ttp: invalid test case type')
			exit(-1)