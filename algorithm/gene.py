import numpy as np
import random as rd
import math
from tqdm import tqdm
# Implementar algoritmo genetico

COORDS_CONTAINER = {
  '0': [-1, 1],
  '1': [0, 1],
  '2': [1, 1],
  '3': [-1, 0],
  '4': [0, 0],
  '5': [1, 0],
  '6': [-1, -1],
  '7': [0, -1],
  '8': [1, -1],
}

class GeneticAlgorithm():
  population = []
  evaluations = []

  def __init__(self, population_size = 100, number_of_generations = 100, gene_number = 18, mutation_rate = 0.05, crossover_rate = 0.8):
    self.population_size = population_size
    self.number_of_generations = number_of_generations
    self.mutation_rate = mutation_rate
    self.crossover_rate = crossover_rate
    self.gene_number = gene_number
    self.generate_population()

  def generate_chromosome(self):
    result = np.random.randint(0, 100, self.gene_number).tolist()
    return result

  def generate_population(self):
    self.population = []
    for i in range(self.population_size):
      self.population.append(self.generate_chromosome())
  
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
        chromo[i] = rd.randint(0, 100)

  def generate_fitness(self):
    self.evaluations = []
    for chromo in self.population:      
      self.evaluations.append(
          self.objective_function(chromo)
      )

  def rearrange_chromo_by_priority(self, chromo):
    new_chromo = chromo[:]
    positions = range(18)
    
    dtype = [('priority', int), ('position', int)]
    array_from_np = np.array(list(zip(new_chromo, positions)), dtype=dtype)
    result = np.sort(array_from_np, order='priority')[::-1]
    result = [x[-1] for x in result]
    return result
  
  def position_of_container_in_ship(self, a_position):
    normalized_position = a_position % 9
    row = normalized_position // 3
    column = normalized_position % 3
    return [row, column]
  
  def multiply_vector_by_number(self, a_vector, a_number):
    new_vector = np.array(a_vector) * a_number
    return list(new_vector)
  
  def calculate_cm(self, a_matrix):
    result = [0,0]
    for i in range(9):
      row, column = self.position_of_container_in_ship(i)
      number_of_container = a_matrix[row, column]
      pos = COORDS_CONTAINER[str(i)][:]
      current_coords = self.multiply_vector_by_number(pos, number_of_container)
      result = np.sum([result, current_coords], axis=0).tolist()
    return result
  
  def magnitude(self, vector):
    return math.sqrt(sum(pow(element, 2) for element in vector))

  def objective_function(self, chromo):
    current_cm = [0,0]
    total_displacement = 0
    
    rearranged_chromo = self.rearrange_chromo_by_priority(chromo)
    
    ship = np.matrix([[0,0,0], [0,0,0], [0,0,0]])
    
    for current_position in rearranged_chromo:
      row, column = self.position_of_container_in_ship(current_position)
      ship[row, column] += 1
      if (ship[row, column] > 2):
        return 100000
      
      temp_cm = self.calculate_cm(ship)
      current_cm = [
        current_cm[0] - temp_cm[0],
        current_cm[1] - temp_cm[1],
      ]
      total_displacement += self.magnitude(current_cm)
            
    return total_displacement

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
    ag.generate_fitness()
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
        ag.generate_fitness()

        current_best_chromo = min(list(zip(ag.population,ag.evaluations)),key=lambda x: x[-1])
        best_chromos.append(ag.rearrange_chromo_by_priority(current_best_chromo[0]))
    
    print(current_best_chromo)
    return best_chromos[-1]
  
if __name__ == "__main__":
  result = get_best_chromo()
  print(result)