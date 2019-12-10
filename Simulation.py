import random , sys
from Person import Person
from Virus import Virus
from FileWriter import FileWriter

class Simulation:
  
    def __init__(self, initial_vaccinated, initial_infected, initial_healthy, virus, resultsfilename):
        '''Set up the initial simulation values'''

        self.virus = virus 
        self.initial_infected = initial_infected 
        self.initial_healthy = initial_healthy
        self.initial_vaccinated = initial_vaccinated

        self.population = []

        self.population_size = initial_infected + initial_healthy + initial_vaccinated


        self.total_dead = 0
        self.total_vaccinated = initial_vaccinated

        self.file_writer = FileWriter(resultsfilename)


    def create_population(self):
        '''Creates the population (a list of Person objects) consisting of initial infected people, initial healthy non-vaccinated people, and 
        initial healthy vaccinated people. Adds them to the population list'''

        for i in range(self.initial_infected):
        	person = Person(False, virus)
        	self.population.append(person)

        for i in range(self.initial_healthy):
            person = Person(False, None)
            self.population.append(person)

        for i in range(self.initial_vaccinated):
            person = Person(True, None)
            self.population.append(person)
        	
    def print_population(self):
        '''Prints out every person in the population and their current attributes'''
        for i in self.population:
            print('alive: ', i.is_alive, 'vaccinated: ', i.is_vaccinated, 'infection:', i.infection)

    def get_infected(self):
        '''Gets all the infected people from the population and returns them as a list'''
        infected_population = []
        for i in self.population:
            if (i.infection is not None):
                infected_population.append(i)
        return(infected_population)
        #TODO: finish this method


    def simulation_should_continue(self):
        '''Determines whether the simulation should continue.
        If everyone in the population is dead then return False, the simulation should not continue
        If everyone in the population is vaccinated return False
        If there are no more infected people left and everyone is either vaccinated or dead return False
        In all other cases return True'''
        infected_ppl = int()
        alive_ppl = int()
        vacc_ppl = int()
        dead_ppl = int()
        for i in self.population:
            if(i.is_vaccinated):
                vacc_ppl += 1
            if(i.infection is not None):
                infected_ppl += 1
            if(i.is_alive == True):
                alive_ppl += 1
            else:
                dead_ppl += 1

        self.total_vaccinated = vacc_ppl
        if(alive_ppl < 1 or dead_ppl == len(self.population)):
            self.should_continue = False
        if(len(self.population) == vacc_ppl + dead_ppl):
            self.should_continue = False

    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        
        self.create_population()
        random.shuffle(self.population)

        self.print_population()
        
        time_step_counter = 0
        self.should_continue = True

        self.file_writer.init_file(self.virus, self.population_size, self.initial_vaccinated, self.initial_healthy, self.initial_infected)
        
        #keep looping until the simulation ends
        while self.should_continue == True:
            self.simulation_should_continue()
            print(self.total_dead, self.total_vaccinated)
            #save the current infected
            old_infected = self.get_infected()
            self.time_step(old_infected)
            #time step will create newly infected people, just determine the survivial of the previous infected people
            self.determine_survival(old_infected)
            time_step_counter += 1

        print(f'The simulation has ended after {time_step_counter} turns.')
        self.file_writer.write_results(time_step_counter, self.total_dead, self.total_vaccinated)

    def determine_survival(self, infected):
        '''Check if the current infected people survive their infection
        Call the did_survive_infection() method
        if it returns false then the person is no longer alive, does not have an infection and one is added to total dead
        if it returns true then the person no longer has an infection and is vaccinated, one is added to total vaccinated'''
        for infect in infected:
            if(infect.did_survive_infection()):
                self.total_vaccinated += 1
                infect.infection = None
            else:
                self.total_dead += 1
                infect.is_alive = False
                infect.infection = None

        #TODO: finish this method
            


    def time_step(self, infected):
        ''' For every infected person interact with a random person from the population 10 times'''

        for infected_person in infected:

            for i in range(10):
                index = random.randint(0, len(self.population) - 1)
                sick_dude = self.population[index]
                if (sick_dude != infected_person):
                    self.interaction(infected_person, sick_dude)
                #TODO: get a random index for the population list
                #TODO: using the random index get a random person from the population
                #TODO: call interaction() with the current infected person and the random person

    def interaction(self, infected, random_person):
        '''If the infected person is the same object as the random_person return and do nothing
        if the random person is not alive return and do nothing
        if the random person is vaccinated return and do nothing
        if the random person is not vaccinated:
            generate a random float between 0 and 1
            if the random float is less then the infected person's virus reproduction number then the random person is infected
            othersie the random person is vaccinated and one is added to the total vaccinated'''

        if(random_person.is_alive == False or random_person.is_vaccinated == True):
            return
        else:
            if(random_person.is_vaccinated == False):
                num = float(random.randint(0, 100)/100)
                if (num < self.virus.reproduction_num):
                    random_person.infection = self.virus
                else: 
                    random_person.is_vaccinated == True
            return
        #TODO: finish this method
        


        


if __name__ == "__main__":

    #Set up the initial simulations values
    virus_name = "Coffee addiction"
    reproduction_num = 0.8
    mortality_num = .1

    initial_healthy = 100
    initial_vaccinated = 0

    initial_infected = 5

    virus = Virus(virus_name, reproduction_num, mortality_num)

    simulation = Simulation(initial_vaccinated, initial_infected, initial_healthy, virus, "results.txt")

    #run the simulation
    simulation.run()
