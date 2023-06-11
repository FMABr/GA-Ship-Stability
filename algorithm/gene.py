import numpy as np
import random as rd
from tqdm import tqdm
# Implementar algoritmo genetico

class GeneticAlgorithm():
  population_size = 50
  number_of_generations = 100
  mutation_rate = 0.5
  crossover_rate = 0.95
  gene_number = 18
  population = []
  evaluations = []

  def __init__(self, population_size = 50, number_of_generations = 100, gene_number = 18, mutation_rate = 0.5, crossover_rate = 0.8):
    self.population_size = population_size
    self.number_of_generations = number_of_generations
    self.mutation_rate = mutation_rate
    self.crossover_rate = crossover_rate
    self.gene_number = gene_number
    self.generate_population()

  def generate_gene(self):
    result = np.random.randint(0, self.gene_number - 1, self.gene_number).tolist()
    return result

  def generate_population(self):
    self.population = []
    for i in range(self.population_size):
      self.population.append(self.generate_gene())
  
  def crossover(self, m_chromo, d_chromo):
    if (rd.random() < self.crossover_rate):
      split_point = rd.randint(1, self.gene_number - 1)
      child_1 = m_chromo[split_point:] + d_chromo[:split_point]
      child_2 = d_chromo[split_point:] + m_chromo[:split_point]
    else:
      child_1 = m_chromo[:]
      child_2 = d_chromo[:]
    return (child_1, child_2)

  def mutation(self, chromo):
    for i in range(len(chromo)):
      if (rd.random() < self.mutation_rate):
        chromo[i] = rd.randint(0, self.gene_number - 1)

  def generate_evaluations(self):
    self.evaluations = []
    for chromo in self.population:
      chromo_repeats = 0
      for i in range(self.gene_number):
        if (chromo.count(i) > 1):
          chromo_repeats += 1
      
      if (chromo_repeats):
        self.evaluations.append(1000 * chromo_repeats)
        continue
      
      self.evaluations.append(
          self.objective_function(chromo)
      )

  def objective_function(self, chromo):
    result = rd.random()
    return result

  def select_chromo(self):
    index_chromo_1 = rd.randint(0, self.population_size - 1)
    index_chromo_2 = rd.randint(0, self.population_size - 1)

    while index_chromo_2 == index_chromo_1:
      index_chromo_2 = rd.randint(0, self.population_size - 1)

    if (self.evaluations[index_chromo_1] > self.evaluations[index_chromo_2]):
      return self.population[index_chromo_1]
    
    return self.population[index_chromo_2]


def get_best_chromo():
    best_chromos = []

    ag = GeneticAlgorithm()
    ag.generate_evaluations()
    for _ in tqdm(range(ag.number_of_generations), total = ag.number_of_generations):
        new_population = []
        while len(new_population) < ag.population_size:
            d_chromo = ag.select_chromo()
            m_chromo = ag.select_chromo()

            new_chromo_1, new_chromo_2 = ag.crossover(m_chromo, d_chromo)

            ag.mutation(new_chromo_1)
            ag.mutation(new_chromo_2)

            new_population.append(new_chromo_1)
            new_population.append(new_chromo_2)
        ag.population = new_population[:]
        ag.generate_evaluations()

        current_best_chromo = min(list(zip(ag.population,ag.evaluations)),key=lambda x: x[-1])
        best_chromos.append(current_best_chromo)
    
    return best_chromos[-1]