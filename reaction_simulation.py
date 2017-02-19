#Reaction Simulation code for EE 5393 HW 1
#Author: Owen Hoffend

import math
import random
from functools import reduce

def k_choose_n(k, n):
		return math.factorial(k) / (math.factorial(n) * math.factorial(k - n))

def reaction_probs(reactant_descs, counts, k_values): #Returns the probability of a reaction happening
	#Reactant desc: tuple containing: ((r1 coefficient, r1 index), (r2 coefficient, r2 index), ..., (rn coefficient, rn index), k_value)
	#index gives the molecule type, while coefficient gives the number of molecules requied.
	alphas = []
	for index, desc in enumerate(reactant_descs):
		if can_fire(desc, counts):
			alphas.append(k_values[index] * reduce(lambda x, y: x * y, [k_choose_n(counts[desc[index][1]], desc[index][0]) for index in range(len(desc))]))
		else:
			alphas.append(0)
	if sum(alphas) == 0:
		return 'end'
	return [alphas[i] / sum(alphas) for i in range(len(alphas))]

def p1_probs(counts): #For testing purposes: using the probability equations given in the problem. Should be equivalent to reaction_probs!
	x1, x2, x3 = counts[0], counts[1], counts[2]
	denominator = (0.5 * x1 * (x1 - 1) * x2) + (x1 * x3 * (x3 - 1)) + (3 * x2 * x3)
	p1 = (0.5 * x1 * (x1 - 1) * x2) / denominator
	p2 = (x1 * x3 * (x3 - 1)) / denominator
	p3 = (3 * x2 * x3) / denominator
	return [p1, p2, p3]

def can_fire(reactant_descs, counts): #Determines if a reaction can actually physically happen given the number of remaining molecules in the systen and the given reaction's chemical equation.
	can_fire_ = True
	if type(reactant_descs) == tuple:
		for reactant in reactant_descs:
			if counts[reactant[1]] < reactant[0]:
				can_fire_ = False
	else:
		if counts[reactant_descs[1]] < reactant_descs[0]:
			can_fire_ = False
	return can_fire_

def stochastic_sim(init_counts, reaction_descs, iterations, halt_on_low_reactants=False):
	#Reaction descs: ((reactant_descs), (product_descs), (k_values))
	reactant_descs = [desc[0] for desc in reaction_descs]
	product_descs = [desc[1] for desc in reaction_descs]
	k_values = [desc[2] for desc in reaction_descs]
	counts = list(init_counts)

	for iteration in range(iterations):
		#if(0 in counts): break
		#print("Molecule counts for iteration %s: %s" % (iteration, counts))
		#probs = p1_probs(counts)
		probs = reaction_probs(reactant_descs, counts, k_values) #Probs should actually be a list containing the reaction index for the reaction as well as the probability of it ocurring
		#print("Reaction probs for iteration %s: %s" % (iteration, probs))
		if probs == 'end' or halt_on_low_reactants and False in [can_fire(desc, counts) for desc in reactant_descs]:
			break

		prob_sum = 0
		rand = random.uniform(0,1)
		#Does probs need to be sorted?
		for index, pb in enumerate(probs): #Generate a list of thresholded probabilities. For example: for probs 1/5, 2/5, 2/5, these would be: 1/5, 3/5, 5/5. Selection of a real number between 0 and 1 gives precisely one of the reactions
			prob_sum += pb
			if rand <= prob_sum:
				fired_reaction_index = index
				break

		#print("Reaction of index %s fired" % fired_reaction_index)
		fired_reactants = reactant_descs[fired_reaction_index]
		fired_products = product_descs[fired_reaction_index]
		for reactant in fired_reactants:
			counts[reactant[1]] -= reactant[0]

		if type(fired_products[0]) == tuple:
			for product in fired_products:
				counts[product[1]] += product[0]
		else:
			counts[fired_products[1]] += fired_products[0]
	return counts

def analyze_outcome(init_counts, reaction_descs, trial_count, iteration_count, halt_on_low_reactants):
	if trial_count * len(init_counts) < 1000000:
		all_outcomes = [stochastic_sim(init_counts, reaction_descs, iteration_count, halt_on_low_reactants) for _ in range(trial_count)]

		C1_prob = len(list(filter(lambda x: x > 7, list(zip(*all_outcomes))[0]))) / trial_count
		C2_prob = len(list(filter(lambda x: x >= 8, list(zip(*all_outcomes))[1]))) / trial_count
		C3_prob = len(list(filter(lambda x: x < 3, list(zip(*all_outcomes))[2]))) / trial_count

		print("C1_prob: %s" % C1_prob)
		print("C2_prob: %s" % C2_prob)
		print("C3_prob: %s" % C3_prob)
	else:
		print("Careful, that operation might use a lot of memory")

#Reactions for problem 1:
r1 = (((2,0), (1,1)),(4, 2), 1)
r2 = (((1,0), (2,2)),(3, 1), 2)
r3 = (((1,1), (1,2)),(2, 0), 3)
p1_descs = [r1, r2, r3]
p1_counts = [5, 5, 5]
#print(stochastic_sim(p1_counts, p1_descs, 1000))
analyze_outcome(p1_counts, p1_descs, 10000, 1000, True)

#Trial Results:
#Organic simulation:
#1000 trials at 10 reactions per trial:
#C1: 0.16, C2: 0.32, C3: 0.32

#1000 trials at 100 reactions per trial:
#C1: 0.258, C2: 1.0, C3: 0.007

#1000 trials at 1000 reactions per trial:
#C1: 0.949, C2: 1.0, C3: 0.007

#Halting simulation at first
#10000 Trials:
#C1: 0.191, C2: 0.78, C3: 0.541
