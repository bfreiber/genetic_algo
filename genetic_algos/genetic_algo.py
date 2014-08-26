from random import randint, random
from operator import add

#Create an individual member of the population
def individual(length, min, max):
	return [randint(min,max) for x in xrange(length)]

#Creates a population of individuals
def population(count, length, min, max):
	return [individual(length, min, max) for x in xrange(count)]

#Analyzes fitness of a given individual - a fitness score of 0 is perfect
def fitness(individual, target):
	#Sum an individual
	fit_sum = reduce(add, individual, 0)
	return abs(target-fit_sum)

#Analyzes the average individual fitness of a given population
def grade(population, target):
	#Analyze the fitness level of each individual
	individual_fitnesses = []
	for individual in population:
		individual_fitnesses.append(fitness(individual, target))
	#Average them
	return sum(individual_fitnesses)/(len(population) * 1.0)

#Transform (map) one generation of a population to the next generation of the same population
#retain = % of best individuals creating next generation
#random_select = % (random_select/1.0) to randomly add back in - e.g., 0.05 = 5%
#mutate = % (mutate/1.0) to randomly mutate - e.g., 0.01 = 1%
def evolve(population, target, retain=0.2, random_select=0.05, mutate=0.01):
	#Grade each individual and return an array [[grade1,[individual1]],...]
	graded = [(fitness(x, target), x) for x in population]
	#Rank-order individuals and then cut off the grades
	graded = [x[1] for x in sorted(graded)]
	#Retain top n% as parents
	retain_length = int(len(graded)*retain)
	parents = graded[:retain_length]

	#Randomly add other individuals to promote genetic diversity
	for individual in graded[retain_length:]:
		if random_select > random():
			parents.append(individual)

	#Mutate a small portion of the population - to avoid getting stuck at local maxima
	for individual in parents:
		if mutate > random():
			#Not ideal, but function's parameters don't reveal the max/min values possible for a given attribute of a given individual
			pos_to_mutate = randint(0, len(individual)-1)
			individual[pos_to_mutate] = randint(min(individual), max(individual))

	#Create children from parents
	parents_length = len(parents)
	desired_length = len(population) - parents_length
	children = []
	while len(children) < desired_length:
		male = randint(0, parents_length-1)
		female = randint(0, parents_length-1)
		if male != female:
			male = parents[male]
			female = parents[female]
			half = len(male)/2
			child = male[:half] + female[half:]
			children.append(child)

	parents.extend(children)
	return parents

#Test conditions
target = 371
population_count = 100
individual_length = 5
individual_min = 0
individual_max = 100
test_population = population(population_count, individual_length, individual_min, individual_max)
fitness_history = []
for i in xrange(100):
	fitness_history.append(grade(test_population, target))
	test_population = evolve(test_population, target)
print fitness_history