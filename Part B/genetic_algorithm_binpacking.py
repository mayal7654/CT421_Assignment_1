import math
from numpy.random import randint, rand
from math import isclose

pop_num = 200
max_iterations = 300

# creating initial generation
def create_initial_gen(pop_num, optimal_bins, integer_list_num):
    new_gen = []
    for i in range(0, pop_num):
        integer_list = randint(1, optimal_bins+10, integer_list_num).tolist()
        new_gen.append(integer_list)
    return new_gen

# fitness function
# the closer the number of bins is to the optimal number of bins, the better the score
def binpacking_fitness(integer_list, integer_list_num, items_weight, total_weight_per_bin):
    new_bin = 0
    bin_weight = [0]
    # for each item, add its weight to the bin it is assigned to
    for i in range(0, integer_list_num):
        bin_number = integer_list[i]-1
        if (len(bin_weight) <= bin_number):
            i = len(bin_weight)
            while i < bin_number + 1:
                bin_weight.append(new_bin)
                i += 1
        bin_weight[bin_number] += items_weight[i]

        # if the bin is overfilled, add a new bin and add the item to it
        if bin_weight[bin_number] > total_weight_per_bin:
            new_bin_num = bin_number+1
            add_to_new_bin(new_bin, new_bin_num, items_weight, i, bin_weight)
            bin_weight[new_bin_num-1] -= items_weight[i]

            # while the new bin is overfilled, add a new bin and add the item to it
            while (bin_weight[new_bin_num] > total_weight_per_bin):
                bin_weight[new_bin_num] -= items_weight[i]
                new_bin_num += 1
                add_to_new_bin(new_bin, new_bin_num, items_weight, i, bin_weight)
    return len(bin_weight)

def add_to_new_bin(new_bin, new_bin_num, items_weight, i, bin_weight):
    if (len(bin_weight) == new_bin_num):
                bin_weight.append(new_bin)
    bin_weight[new_bin_num] += items_weight[i]

# selecting new generation - tournament selection
# returns best contender out of randomly selected bunch
def tournament(no_pop, pop, fitness, no_individ):
    candidate = randint(no_pop)
    for i in randint(0, no_pop, no_individ):
        if fitness[i] < fitness[candidate]:
            candidate = i
    return pop[candidate]

# one-point crossover function
def crossover(individ1, individ2, integer_list_num):
    child1, child2 = individ1, individ2
    if rand() < 0.8:
        crossover_point = randint(1, integer_list_num-2)
        child1 = individ1[:crossover_point] + individ2[crossover_point:]
        child2 = individ2[:crossover_point] + individ1[crossover_point:]
    return [child1, child2]

def standard_mutatation(integer_list, integer_list_num, optimal_bins):
    i = randint(0, integer_list_num)
    # about a 40% chance of changing a bin number (mutating)
    if rand() < 0.4:
        integer_list[i] = randint(1, optimal_bins)
    return integer_list

def check_fitness(scores, population, integer_list_num, file, items_weight, total_weight_per_bin):
    scores = []
    for i in range(0, pop_num):
        scores.append(binpacking_fitness(population[i], integer_list_num, items_weight, total_weight_per_bin))
    fitness_average = sum(scores)/pop_num
    file.write(str(fitness_average)+"\n")
    return scores

def algorithm(problem_num):
    items_weight = []
    weights = []
    items_instances = []
    textin = open("Part B/Datasets/Binpacking" +str(problem_num)+".txt", "r")
    num_weights = int(textin.readline())
    total_weight_per_bin = int(textin.readline())
    line = "in"
    while (line != ""):
        line = textin.readline()
        if (line != ""):
            item_weight, item_instance = line.split()
            weights.append(int(item_weight))
            items_weight.append(int(item_weight))
            items_instances.append(int(item_instance))
            i = int(item_instance)
            while (i > 1):
                items_weight.append(int(item_weight))
                i -= 1
    
    total_weight_to_pack = 0
    for i in range(len(weights)):
        total_weight_to_pack += items_weight[i]*items_instances[i]
    
    # optimal number of bins = total weight to pack / total weight per bin
    optimal_bins = math.ceil(total_weight_to_pack/total_weight_per_bin)

    # number of bits in bit string = number of items
    integer_list_num = sum(items_instances)
    
    # fitness_average = 0
    population = create_initial_gen(pop_num, optimal_bins, integer_list_num)
    iter = 0
    textout = open("Part B/Results/binpacking_fitness" +str(problem_num)+".txt", "w")
    #initial fitness average
    textout.write("Optimal Number of Bins: "+ str(optimal_bins)+"\n")
    scores = []
    scores = check_fitness(scores, population, integer_list_num, textout, items_weight, total_weight_per_bin)
    fitness_average = sum(scores)/pop_num

    while iter <= max_iterations  and (isclose(fitness_average, optimal_bins) != True):
        iter+=1
        # select fitter individuals for reproduction
        selected_fitter_individ = [tournament(pop_num, population, scores, 5) for _ in range(0, pop_num)]
        new_gen = []
        for i in range(0, pop_num-1, 2):
            # recombine between individuals
            individ1 = selected_fitter_individ[i]
            individ2 = selected_fitter_individ[i+1]
            # crossover individuals to make children
            children = crossover(individ1, individ2, integer_list_num)
            # mutate individuals
            new_gen.append(standard_mutatation(children[0], integer_list_num, optimal_bins))
            new_gen.append(standard_mutatation(children[1], integer_list_num, optimal_bins))
        
        # evaluate the fitness of the modified individuals
        scores = check_fitness(scores, new_gen, integer_list_num, textout, items_weight, total_weight_per_bin)
        fitness_average = sum(scores)/pop_num

        # generate a new population
        population = new_gen
    textout.close()
    textin.close()


for i in range(1, 6):
    algorithm(i)