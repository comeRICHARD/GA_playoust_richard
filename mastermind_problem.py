# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(GA solving Mastermind example)
"""
from ga_solver import GAProblem , Individual
import mastermind as mm
import random


class MastermindProblem(GAProblem):
    """Implementation of GAProblem for the mastermind problem"""
    
    def initiate_indiv(self):
        """
        Create a new a new chromosome by getting a random combination of colours and compute its fitness score.
        Returns :
            chromosome (list[]): a list representing the individual's chromosome generated
            fitness (float): the individual's fitness depending of its chromosome (the higher, the better the fitness) 
        """
        chromosome = match.generate_random_guess()
        fitness = match.rate_guess(chromosome)
        return chromosome, fitness
        return super().initiate_indiv()
    
    def calculate_fitness(self, new_chrom):
        """
        Compute the fitness score  and return it of the chromosome given as input.

        Args : 
            new_chrom : chromosome that has been created
        
        Returns :
            new_fitness : fitness score of the created chromosome
        """
        new_fitness = match.rate_guess(new_chrom)
        return new_fitness
        return super().calculate_fitness()
    
    def mutate(self, individual):
        """
        Take as input an individual, a chromosome with its fitness score and mutate it. 
        To mutate, the function get all the possibles genes (colors), choose randomly one of them and replace randomly one of its gene with the mutate one
        Return the mutate individual.
        """
        valid_colors = mm.get_possible_colors() # Choose a valid gene to increment into the chromosome
        new_gene = random.choice(valid_colors)
        random_pos = random.randrange(0, len(individual.chromosome)) 
        # Modify the chromosome and the fitness score of the individual
        individual.chromosome= individual.chromosome[0:random_pos] + [new_gene] + individual.chromosome[random_pos+1:]
        individual.fitness=match.rate_guess(individual.chromosome)
        return(individual)
        return super().mutate(individual)
    
    def herit_second_parent(self, new_chrom, chr_parent2,limit_chr):
        """
        Take as input the new chromosome, the second parent and a limit.
        Complete the second part of the new chromosome using the second parent genes.
        Return the full new chromosome.
        """
        new_chrom = new_chrom + chr_parent2[limit_chr:]
        return new_chrom
        return super().herit_second_parent()
    
    def threshold(self, best_indiv, threshold_fitness):
        """
        Compare the best result to the treshold choosen.
        Return True if the best result is higher or equal to the treshold.
        """
        if best_indiv.fitness < threshold_fitness :
            superiortovalue = False
        else : 
            superiortovalue = True
        return superiortovalue
        return super().threshold()

if __name__ == '__main__':

    from ga_solver import GASolver

    match = mm.MastermindMatch(secret_size=6)
    problem = MastermindProblem()
    solver = GASolver(problem)

    solver.reset_population()
    solver.evolve_until(threshold_fitness=match.max_score())

    print(
        f"Best guess {solver.get_best_individual()}")
    print(
        f"Problem solved? {match.is_correct(solver.get_best_individual().chromosome)}")
