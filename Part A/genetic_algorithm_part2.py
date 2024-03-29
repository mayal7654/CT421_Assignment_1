from numpy.random import randint, rand
from math import isclose

bit_string_num = 30
target_string = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
max_iterations = 100

# creating initial generation
def create_initial_gen():
    new_gen = []
    for i in range(0, 100):
        bit_string = randint(0, 2, bit_string_num).tolist()
        new_gen.append(bit_string)
    return new_gen

# fitness function
# sum of each correct placement = score
def target_string_fitness(bit_string):
    correct_pos = 0
    for i in range(0, bit_string_num):
        if bit_string[i] == target_string[i]:
            correct_pos += 1 
    return correct_pos

# selecting new generation - tournament selection
# returns best contender out of randomly selected bunch
def tournament(no_pop, pop, fitness, no_individ):
    candidate = randint(no_pop)
    for i in randint(0, no_pop, no_individ):
        if fitness[i] > fitness[candidate]:
            candidate = i
    return pop[candidate]

# one-point crossover function
def crossover(individ1, individ2):
    crossover_point = randint(1, bit_string_num-2)
    child1 = individ1[:crossover_point] + individ2[crossover_point:]
    child2 = individ2[:crossover_point] + individ1[crossover_point:]
    return [child1, child2]

# switches bits with a low probability
def standard_mutatation(bit_string):
    i = randint(0, bit_string_num)
    # about a 1% chance of flipping the bit
    if rand() < 0.01:
        bit_string[i] = 1 - bit_string[i]
    return bit_string

def check_fitness(scores, population, file, iter):
    scores = []
    for i in range(0, 100):
        scores.append(target_string_fitness(population[i]))
    fitness_average = sum(scores)/100
    file.write(str(fitness_average)+"\n")
    return scores

def algorithm():
    fitness_average = 0
    population = create_initial_gen()
    iter = 0
    txt = open("Part A/part2_fitness_average.txt", "w")
    
    #initial fitness average
    scores = []
    scores = check_fitness(scores, population, txt, iter)
    fitness_average = sum(scores)/100

    while iter <= max_iterations and (isclose(fitness_average, 30.00) != True):
        iter+=1
        #select fitter individuals for reproduction
        selected_fitter_individ = [tournament(100, population, scores, 5) for _ in range(0, 100)]
        new_gen = []
        for i in range(0, 99, 2):
            # recombine between individuals
            individ1 = selected_fitter_individ[i]
            individ2 = selected_fitter_individ[i+1]
            # crossover individuals to make children
            children = crossover(individ1, individ2)
            # mutate individuals
            new_gen.append(standard_mutatation(children[0]))
            new_gen.append(standard_mutatation(children[1]))
        
        # evaluate the fitness of the modified individuals
        scores = check_fitness(scores, new_gen, txt, iter)
        # generate a new population
        population = new_gen
        fitness_average = sum(scores)/100
    txt.close()

algorithm()