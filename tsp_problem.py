# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(GA solving TSP example)
"""
from ga_solver import GAProblem
import cities
import random

class TSProblem(GAProblem):
    """Implementation of GAProblem for the traveling salesperson problem"""
    def initiate_indiv(self):
        """
        Create a new a new chromosome and compute its fitness score. 
        To do so, it gets all the possible cities and shuffle them to store inside a chromosome. 
        The fitness is calculated with the negative of the total lenght between each city
        Return the chromosome and the fitness
        """
        chromosome = cities.default_road(city_dict)
        random.shuffle(chromosome) 
        fitness = - cities.road_length(city_dict, chromosome)
        return (chromosome, fitness)
        return super().initiate_indiv(chromosome,fitness)
    
    def calculate_fitness(self, new_chrom):
        """
        Compute the fitness score  and return it of the chromosome given as input.
        """
        fitness = - cities.road_length(city_dict, new_chrom)      
        return (fitness)
        return super().calculate_fitness(new_chrom)
    
    def mutate(self, individual):
        """
        Take as input an individual, a chromosome with its fitness score and mutate it.
        To do so choose randomly 2 different chromosome and interchange their position
        Return the mutate individual.
        """
        idx = range(len(individual.chromosome))
        i1, i2 = random.sample(idx, 2)
        individual.chromosome[i1], individual.chromosome[i2] = individual.chromosome[i2], individual.chromosome[i1]
        individual.fitness=- cities.road_length(city_dict, individual.chromosome)
        return (individual)
        return super().mutate(individual)
    
    def herit_second_parent(self, new_chrom, chr_parent2,limit_chr):
        """
        Take as input the new chromosome, the second parent and a limit.
        Complete the second part of the new chromosome using the second parent gene.
        If a gene of the second parent is already in the chromosome pass to the next one. 
        Complete the chromosome if its length is too short with the cities not already in the chromosome.
        Return the full new chromosome.
        """
        for i in range(limit_chr, len(city_dict)-1):
            if chr_parent2[i] not in new_chrom:
                new_chrom.append(chr_parent2[i])
        if len(new_chrom)!=len(city_dict):
            for city in cities.default_road(city_dict):
                if city not in new_chrom:
                    new_chrom.append(city)        
        return (new_chrom)
        return super().herit_second_parent(new_chrom, chr_parent2)
    
    def threshold(self, best_indiv, threshold_fitness):
        """
        There is no succeed threshold in this problem
        Return false
        """
        return (False)


if __name__ == '__main__':

    from ga_solver import GASolver

    city_dict = cities.load_cities("cities.txt")
    problem = TSProblem()
    solver = GASolver(problem)
    solver.reset_population()
    solver.evolve_until()
    cities.draw_cities(city_dict, solver.get_best_individual().chromosome)
