import maze_visual
import maze_samples
import random
import math





'''
NOTE: I renamed the maze.py file that was given, because there were some conflicts when importing it
Since I used 'maze' as a parameter name in several of my functions and attributes, I thought it would
be best to make this minor change. Apologies for any inconvienience

Thank you

'''




# --------------- Monte Carlo Selection ---------------- #
def SetWeightsForMonteCarloSelection(fitness_scores):
    '''
    Monte Carlo Selection that given
    Opted to not use in GA class
    '''
    
    normalized_values = [int(v/sum(fitness_scores)*100+.5) for v in fitness_scores]
    accum = 0
    selection_weights = []
    for w in normalized_values:
        accum += w
        selection_weights.append(accum)
    return selection_weights

def MonteCarloSelection(selection_weights):
    selection = random.randint(0,selection_weights[-1])
    for i,w in enumerate(selection_weights):
        if selection <= w:
            return i


# -------------------------------  Genetic Algorithm Class ------------------------------------ # 
class Ga:
    def __init__(self,maze, maze_length, population = 10, generations = 100):
        '''Initialize with maze, maze length, default population and generations '''
        self.maze = maze
        self.maze_length = maze_length
        self.population = [Individual(maze_length) for individual in range(population)]
        self.generations = generations
        self.selection_weights = [] 
        self.offspring = []
        self.evolved = 0
        
    
    def __str__(self):
        return "The Genertic Algorithm ran for {0} genertations with a population size of {1}".format(self.evolved, len(self.population))
    
    
    def cross_breed(self, set_weight):
        '''Creates a new generation '''
        for idx in range(len(self.population) // 2):
            parent_one = MonteCarloSelection(set_weight)
            parent_two = MonteCarloSelection(set_weight) # set_weight uses 'SetWeightsFor...' function. The parameter is defined in __main__
            break_point = random.randint(1,self.maze_length -1)
            child_one = Individual(self.maze_length)  # Instantiate children and alter string using parent selection
            child_two = Individual(self.maze_length)
            child_one.string = self.population[parent_one].string[0:break_point] + self.population[parent_two].string[break_point:self.maze_length]
            child_two.string = self.population[parent_two].string[0:break_point] + self.population[parent_one].string[break_point:self.maze_length]
    
            
            self.offspring.append(child_one)
            self.offspring.append(child_two)
        
        self.evolved += 1     
        return self.offspring
      
        
    def fitness_scores(self):
        '''
        Returns list of all fitness scores in population
        To be used in Monte Carlo Selection
        '''
        
        return [individual.fitness(self.maze) for individual in self.population] 

            
# ------------- Helper Functions to get starting positions and cheese position ------------- #
def row_start(maze):
    ''' Function to get starting row position of maze'''
    row_pos = 0
    for row in range(len(maze)):
        if 'M' in maze[row]:
            row_pos = row
            
    return row_pos


def col_start(maze):
    '''Function to return starting column position of maze'''
    row = row_start(maze)
    for col in range(len(maze[row])):
        if maze[row][col] == 'M':
            return col

def cheese_row(maze):
    '''Function to return starting row position of cheese '''
    for row in range(len(maze)):
        if 'C' in maze[row]:
            return int(row)

def cheese_col(maze):
    '''Function to return starting column position of cheese '''
    cheese_r = cheese_row(maze)
    for col in range(len(maze[cheese_r])):
        if maze[cheese_r][col] == 'C':
            return int(col)

def edge_maze(maze,row_pos,col_pos,move):
    return((row_pos != len(maze) -1 and move == 'U') or     # To check if on edge.
           (row_pos != 0 and move == 'D') or                # Used in combination with 'check_blockage()'
           (col_pos != len(maze[0]) -1 and move == 'R') or  # As to not get indexing error
           (col_pos != 0 and move == 'L'))



def check_blockage(maze,row_pos,col_pos):
    return (maze[row_pos + 1][col_pos] == 'x' or      # Return True if any move leads to a block
            maze[row_pos - 1][col_pos] == 'x' or      # If True, blocked is incremented by 1 and thus overall fitness score falls
            maze[row_pos][col_pos + 1] == 'x' or
            maze[row_pos][col_pos - 1] == 'x')



# ---------------------------   Individual Class   -------------------------------------- # 
class Individual:

    def __init__(self,maze_length):
        '''Randomly initialize a solution for the maze using the four possible moves '''
        self.string = ''
        self.maze_length = maze_length
        for el in range(maze_length):
            self.string = self.string + random.choice(['U','D','R','L'])
        self.fitness_score = 0
    

    
    def __str__(self):
        return "The Individual has a fitness of {0}".format(self.fitness_score)
    
    
    def fitness(self,maze):
        '''
        Fitness points given based on open moves, distance relative to cheese (closer the more points)
        Points are DEDUCTED if move leads to a blockage
        '''


        # Determine Maze starting position and cheese position
        self.row_pos = row_start(maze)
        self.col_pos = col_start(maze)
        self.cheese_r = cheese_row(maze)
        self.cheese_c = cheese_col(maze)
        blocked = 0
        open_space = 0      # Points for going into open spaces
        no_back_forth = 0   # Giving points for not going back and forth e.g DUDU...
        self.cheese_distance = 0
        moves = ['U','D','L','R']
        
        for move in range(len(self.string) -1):
            if edge_maze(maze, self.row_pos, self.col_pos,move):
                if check_blocakge(maze, self.row_pos,self.col_pos):
                    blocked +=1                                     # If a move leads to being on the edge and a potential move that
                                                                    # will be of the maze or 'x', deduct a pointblocked +=1
 
            if self.string[move + 1] != self.string[move]: # UU or DD or LL... can work! 
                '''Simple if statement to check if moving back or forth'''
                if (self.string[move] in moves[0:2] and self.string[move + 1] in moves[2:4]):
                    no_back_forth +=1
            

            if self.row_pos != len(maze) -1:  # These if checks are to make sure the move is valid
                if self.string[move] == 'U':  # E.g If row position is last row, going UP ('U') would lead to error
                    self.row_pos += 1         # Otherwise, move a row forward. Same logic applies for 'D', 'R', 'L'
                    open_space += 1

        
            if self.row_pos != 0:
                if self.string[move] == 'D':
                    self.row_pos -= 1
                    open_space += 1
            
            if self.col_pos != len(maze[0]) - 1:
                if self.string[move] == 'R':       # If the col_pos is end of row, going Right ('R') would lead to error
                    self.col_pos +=1               # Otherwise, move col_pos by 1
                    open_space +=1
            
            if self.col_pos != 0:
                if self.string[move] == 'L':
                        self.col_pos -= 1
                        open_space += 1
        
        
        self.fitness_score = open_space  + no_back_forth - blocked 
        self.cheese_distance = int(math.sqrt((self.cheese_c - self.col_pos)**2 + (self.cheese_r - self.row_pos)**2))

        
        for point in range(self.maze_length, self.cheese_distance, -1):
            self.fitness_score += 1     # Add a point the closer you are to the cheese
        
        if self.fitness_score < 0:
            self.fitness_score = -1     # In the rare case we get a very unfit solution
            
        if maze[self.row_pos][self.col_pos] == 'C':
            self.fitness_score += len(self.string) # If cheese found, points equivalent to length of string
      
        return self.fitness_score


    def mutate(self):
        if random.uniform(0.0 , 1.0) <= 0.60:     # Setting Mutation rate to 0.60         
            lwr_bound = random.randint(1,self.maze_length)
            upr_bound = random.randint(lwr_bound, self.maze_length)
            subset_individual = list(self.string[lwr_bound:upr_bound]) # Take a subset of the individual and scramble it
            random.shuffle(subset_individual)                          # using the random.shuffle method
            self.string = self.string[0:lwr_bound] + ''.join(subset_individual) + self.string[upr_bound: self.maze_length]
    
        return self.string
    
    
    def get_row(self):
        return self.row_pos        # Getters to determine position incase individual is on cheese
                                   # and thus break out of loop in __main__()
    def get_col(self):
        return self.col_pos

    def get_fitness(self):
        return self.fitness_score

    def get_distance(self):
        return self.cheese_distance 


# -----------------  Main Function ------------------ #
def main():
    '''
    ALGORITHM WORKS FOR BOTH 0 AND 1
    '''
    test_case = 0
    string_length = maze_samples.string_length[test_case]

    start_ga = Ga(maze_samples.maze[test_case],
                  maze_length = string_length,
                  population = 1000,
                  generations = 1000)

    while start_ga.evolved < start_ga.generations:
        for individual in start_ga.population:
            individual.fitness(maze_samples.maze[test_case])

            # ------------------ We can visualize it as well ------------ #
            # M = maze_visual.Maze(maze_samples.maze[test_case])
            #M.Visualize()
            #M.RunMaze(individual.string)
            #M.RunMaze('R')
            #M.ResetMouse()
            print(individual)
            if maze_samples.maze[test_case][individual.get_row()][individual.get_col()] == 'C':
                print('Cheese Found!!:' , '\n', 'At Generation: ', start_ga.evolved )
                quit()
        
        set_weight = SetWeightsForMonteCarloSelection(start_ga.fitness_scores())
        start_ga.cross_breed(set_weight)
        print("This is generation", start_ga.evolved)
    
    
        for child in start_ga.offspring:
            child.mutate()
            child.fitness(maze_samples.maze[test_case])
            print("This child has a fitness of: ", child.get_fitness())

    
        for idx in range(len(start_ga.population)):
            start_ga.population[idx] = start_ga.offspring[idx]
    
        start_ga.offspring = []

    

        for ind in start_ga.population:
            if ind.get_fitness() == max(start_ga.fitness_scores()):
                print("The best fit has a score of: ", ind.get_fitness(), "\n", "Final Position: ", ind.get_row(),ind.get_col(), '\n',
                  "Distance from cheese: ", ind.get_distance())

 


if __name__=='__main__' :
  main()













