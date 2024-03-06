# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(generic genetic algorithm module)
"""
import random

class Individual:
    """Represents an Individual for a genetic algorithm"""

    def __init__(self, chromosome: list, fitness: float):
        """Initializes an Individual for a genetic algorithm

        Args:
            chromosome (list[]): a list representing the individual's
            chromosome
            fitness (float): the individual's fitness (the higher the value,
            the better the fitness)
        """
        self.chromosome = chromosome
        self.fitness = fitness

    def __lt__(self, other):
        """Implementation of the less_than comparator operator"""
        return self.fitness < other.fitness

    def __repr__(self):
        """Representation of the object for print calls"""
        return f'Indiv({self.fitness:.1f},{self.chromosome})'


class GAProblem:
    """Defines a Genetic algorithm problem to be solved by ga_solver"""

    def initiate_indiv(self):
        pass
    
    def calculate_fitness(self, new_chrom):
        pass

    def mutate(self, individual):
        pass

    def herit_second_parent(self, new_chrom, chr_parent2):
        pass

    def threshold(self, best_indiv, threshold_fitness):
        pass


class GASolver:
    def __init__(self, problem: GAProblem, selection_rate=0.5, mutation_rate=0.1):
        """Initializes an instance of a ga_solver for a given GAProblem

        Args:
            problem (GAProblem): GAProblem to be solved by this ga_solver
            selection_rate (float, optional): Selection rate between 0 and 1.0. Defaults to 0.5.
            mutation_rate (float, optional): mutation_rate between 0 and 1.0. Defaults to 0.1.
        """
        self._problem = problem
        self._selection_rate = selection_rate
        self._mutation_rate = mutation_rate
        self._population = []
        self.fitness_over_gen = []

    def reset_population(self, pop_size=50):
        """ Initialize the population with pop_size random Individuals and sort it"""

        for i in range(pop_size) : #Create pop_size random individuals
            new_chrom , new_fitness = self._problem.initiate_indiv()
            new_individual = Individual(new_chrom, new_fitness)
            self._population.append(new_individual)
        self.sort_population()

    def evolve_for_one_generation(self):
        """ Apply the process for one generation : 
            -	Sort the population (Descending order)
            -	Selection: Remove x% of population (less adapted)
            -   Reproduction: Recreate the same quantity by crossing the 
                surviving ones 
            -	Mutation: For each new Individual, mutate with probability 
                mutation_rate i.e., mutate it if a random value is below   
                mutation_rate
        """
        nb_of_reproduction = self.remove_less_adapted_population()
        self.reproduction_of_individual(nb_of_reproduction)
        self.sort_population()

    def mutate_individual(self, individual):
        """ Depending on the mutation rate, mutate a gene of the newly individual created
        
        Args: 
            individual (Individual): the individual to be mutate or not

        Returns:
            individual (Individual): the individual that has been mutate or not
        """
        mutation = random.random() 
        if mutation > self._mutation_rate: # Choose if we mutate or not
            individual = self._problem.mutate(individual)
        return individual

    def reproduction_of_individual(self, nb_to_reproduce):
        """ Create nb_to_reproduce indivudals from the crossing of surviving individuals
        
        Args: 
            nb_to_reproduce (int): number of individual to create
        """        
        for i in range(nb_to_reproduce):
            # Choose randomly the two chromosomes used as parents. We choose randomly to get diversity
            chr_parent1 = self._population[random.randint(0,len(self._population)-1)].chromosome
            chr_parent2 = self._population[random.randint(0,len(self._population)-1)].chromosome
            while chr_parent2 == chr_parent1 : # We want two differents chromosome, or the mix will not work correctly
                chr_parent2 = self._population[random.randint(0,len(self._population)-1)].chromosome
        
            limit_chr = random.randrange(0, len(chr_parent1)) # The limit that set the sizes of chromosome 1 and 2 to transmit to the children chromosome
            new_chrom = chr_parent1[0:limit_chr]
            new_chrom = self._problem.herit_second_parent(new_chrom, chr_parent2,limit_chr)
            new_fitness = self._problem.calculate_fitness(new_chrom)
            new_individual = Individual(new_chrom, new_fitness)
            mutate_individual = self.mutate_individual(new_individual) # Mutate or not the newly individual
            self._population.append(mutate_individual) # Add the individual to the population

    def remove_less_adapted_population(self):
        """ Remove the x% of population (less adapted) and return the size of population
        Returns:
            pop_size_to_generate (int): Number of individuals to create 
        """
        index_less_adapted = int(self._selection_rate * len(self._population)) # Choose the limit from where the individuals will be removed from the population
        pop_size_to_generate = len(self._population) - index_less_adapted 
        self._population = self._population[:index_less_adapted]
        return pop_size_to_generate

    def sort_population(self):
        """ Sort the population by its fitness score"""
        self._population.sort(reverse = True)

    def show_generation_summary(self):
        """ Print the fitness score for each generation realized """
        self.fitness_over_gen.append(self.get_best_individual().fitness)

    def get_best_individual(self):
        """ Return the best Individual of the population
        Returns:
            best_indiv (Individual): The individual from population who has the best fitness score """
        best_indiv = max(self._population, key=lambda x: x.fitness)
        return best_indiv

    def evolve_until(self, max_nb_of_generations=50, threshold_fitness=None):
        """ Launch the evolve_for_one_generation function until one of the two condition is achieved : 
            - Max nb of generation is achieved
            - The fitness of the best Individual is greater than or equal to
              threshold_fitness
        
        Arguments: 
            max_nb_of_generations (int, optional): Maximum number of generation before we stop evolving
            threshold_fitness (int, optional): The limit of the fitness score to obtain.  
        """
        nb_of_gen = 1
        best_indiv = self.get_best_individual()
        superiortovalue = self._problem.threshold(best_indiv, threshold_fitness)
        while (nb_of_gen < max_nb_of_generations) and superiortovalue==False:
            nb_of_gen += 1 
            self.show_generation_summary()
            self.evolve_for_one_generation()
            best_indiv = self.get_best_individual()
            superiortovalue = self._problem.threshold(best_indiv, threshold_fitness)
            
