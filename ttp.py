from __future__ import print_function

import cProfile

from sys import *
from problem import *
from random import *

def gen_population(problem):
	return [Representation(problem) for _ in range(problem.population_size)]

def fitness(indiv, problem):
	return indiv.evaluate(problem)

def eval_population(population, problem):
	for i in range(problem.population_size):
		population[i].score = fitness(population[i], problem)

# tournament selection
def select_parents(population, problem):
	parents = [Representation(None) for _ in range(problem.population_size)]

	for i in range(problem.population_size):
		points = sample(range(problem.population_size), problem.tournament_size)
		subset = [[population[pos].score, pos] for pos in points]
		pos = max(subset, key=lambda p: p[0])[1]

		parents[i].ks, parents[i].tsp = population[pos].ks[:], population[pos].tsp[:]

	return parents

# knapsack crossver
def two_point(cromo1, cromo2, problem):
	if random() < problem.crossover_prob:
		return

	points = sample(range(problem.total_items), 2)
	pos1, pos2 = min(points), max(points)

	child1 = cromo1.ks[:pos1] + cromo2.ks[pos1:pos2] + cromo1.ks[pos2:]
	child2 = cromo2.ks[:pos1] + cromo1.ks[pos1:pos2] + cromo2.ks[pos2:]
	cromo1.ks, cromo2.ks = child1, child2

# tsp crossver
def pmx(cromo1, cromo2, problem):
	if random() < problem.crossover_prob:
		return

	points = sample(range(problem.num_cities), 2)
	beg, end = min(points), max(points)

	child1, child2 = cromo1.tsp[:], cromo2.tsp[:]
	child1[beg:end+1] = cromo2.tsp[beg:end+1]
	child2[beg:end+1] = cromo1.tsp[beg:end+1]

	for parent, child in zip([cromo1.tsp, cromo2.tsp], [child1, child2]):
		for i in range(beg, end+1):
			if parent[i] not in child[beg:end+1]:
				spot = i
				while beg <= spot <= end:
					spot = parent.index(child[spot])
				child[spot] = parent[i]

	cromo1.tsp, cromo2.tsp = child1, child2

def apply_mutation(cromo, problem):
	# knapsack - xor mutation
	for i in range(problem.total_items):
		if random() < problem.mutation_prob:
			cromo.ks[i] ^= 1

	# tsp - swap mutation
	if random() < problem.mutation_prob:
		pos1, pos2 = sample(range(problem.num_cities), 2)
		cromo.tsp[pos1], cromo.tsp[pos2] = cromo.tsp[pos2], cromo.tsp[pos1]

def apply_variation(parents, problem):
	for i in range(0, problem.population_size, 2):
		two_point(parents[i], parents[i+1], problem)
		pmx(parents[i], parents[i+1], problem)

	for i in range(problem.population_size):
		apply_mutation(parents[i], problem)
		parents[i].repair(problem)

	return parents

def select_survivors(population, offsprings, problem):
	population.sort(key=lambda i: i.score, reverse=True)
	offsprings.sort(key=lambda i: i.score, reverse=True)

	comp = int(problem.population_size * problem.elite_size)
	return population[:comp] + offsprings[:problem.population_size - comp]

def update_fittest(population, problem):
	new_best = False

	for i in range(problem.population_size):
		score = population[i].evaluate(problem)

		if not population[i].isvalid(problem):
			problem._nodes += 1
		if score > problem.best_score:
			problem.best_score = score
			problem.best_cromo = [population[i].tsp[:], population[i].ks[:]]
			new_best = True

	return new_best

def print_status(generation, problem, new_best):
	if not problem.debug:
		return
	if generation > 1:
		stdout.write("\r" if not new_best else "\n")

	stdout.write("info generation " + str(generation) + " ")
	stdout.write("bestscore " + str(problem.best_score) + " ")
	stdout.write("invalid nodes " + str(problem._nodes))
	stdout.write("\n" if generation == problem.generations else "")
	stdout.flush()

def print_solution(problem):
	print("info bestscore " + str(problem.best_score))
	if not problem.debug:
		return

	print('\ntour\tplan')
	tour, plan = problem.best_cromo[0], problem.best_cromo[1]

	for i in range(problem.num_cities):
		print(tour[i]+1, end='\t')

		for j in range(problem.bounds[tour[i]][0], problem.bounds[tour[i]][1]):
			if plan[j] == 1:
				print(problem.items[j]+1, end=' ')

		print('')

	print("\n" if '--prof' in argv else "")

def sea(problem):
	population = gen_population(problem)
	eval_population(population, problem)

	for i in range(problem.generations):
		parents = select_parents(population, problem)
		offsprings = apply_variation(parents, problem)

		eval_population(offsprings, problem)
		population = select_survivors(population, offsprings, problem)
		new_best = update_fittest(population, problem)

		print_status(i+1, problem, new_best)

	print_solution(problem)

def parse_args():
	if '--help' in argv:
		print('usage: ttp [OPTION...] [FILE...]')
		print('  --help    display this help and exit')
		print('  --prof    enable profiling')
		print('  --debug   enable debugging')
		print('  --seed S  use S as a seed for the random number generator')
		print('  --conf F  use F as a config file (mandatory)')
		print('  --type T  use T as the type of the test case (mandatory)')
		print('            valid test case types are 1 and 2\n')
	elif '--conf' not in argv or argv.index('--conf')+1 == len(argv):
		print('ttp: missing or invalid option --conf')
		print('Try \'ttp --help\' for more information.\n')
	elif '--type' not in argv or argv.index('--type')+1 == len(argv):
		print('ttp: missing or invalid option --type')
		print('Try \'ttp --help\' for more information.\n')
	elif '--seed' in argv and argv.index('--seed')+1 == len(argv):
		print('ttp: missing argument in --seed')
		print('Try \'ttp --help\' for more information.\n')
	else:
		return ['--debug' in argv, argv[argv.index('--conf')+1], argv[argv.index('--type')+1]]

	exit(-1)

def main():
	problem = Problem(parse_args())

	if '--prof' in argv:
		cProfile.runctx('sea(problem)', {'sea':sea}, {'problem':problem}, sort=1)
	else:
		sea(problem)

main()
