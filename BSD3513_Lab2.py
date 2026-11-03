import random
import streamlit as st
import matplotlib.pyplot as plt

# Parameters
POPULATION_SIZE = 300
CHROMOSOME_LENGTH = 80
TARGET_ONES = 50
GENERATIONS = 50

# Generate chromosome
def create_chromosome():
    return [random.randint(0, 1) for _ in range(80)]

# Fitness function
def fitness(chromosome):
    return 80 - abs(sum(chromosome) - TARGET_ONES)

# Selection
def select_parent(population):
    candidates = random.sample(population, 5)
    return max(candidates, key=fitness)

# Crossover
def crossover(parent1, parent2):
    point = random.randint(1, 79)
    return parent1[:point] + parent2[point:]

# Mutation
def mutate(chromosome):
    child = chromosome[:]

    for i in range(80):
        if random.random() < 1/80:
            child[i] = 1 - child[i]

    return child

# Genetic Algorithm
def genetic_algorithm():
    population = [
        create_chromosome()
        for _ in range(POPULATION_SIZE)
    ]

    best_history = []
    average_history = []

    for generation in range(GENERATIONS + 1):

        best = max(population, key=fitness)

        best_history.append(fitness(best))

        average = sum(
            fitness(c) for c in population
        ) / POPULATION_SIZE

        average_history.append(average)

        if generation == GENERATIONS:
            break

        ranked = sorted(
            population,
            key=fitness,
            reverse=True
        )

        new_population = [
            ranked[0][:],
            ranked[1][:]
        ]

        while len(new_population) < POPULATION_SIZE:

            p1 = select_parent(population)
            p2 = select_parent(population)

            child = crossover(p1, p2)
            child = mutate(child)

            new_population.append(child)

        population = new_population

    best = max(population, key=fitness)

    return best, best_history, average_history


# Streamlit Application
st.title("Genetic Algorithm")
st.write("Binary Pattern Optimization")

st.subheader("Algorithm Parameters")

st.write("Population Size:", POPULATION_SIZE)
st.write("Chromosome Length:", CHROMOSOME_LENGTH)
st.write("Target Ones:", TARGET_ONES)
st.write("Maximum Fitness:", 80)
st.write("Generations:", GENERATIONS)

if st.button("Run Genetic Algorithm"):

    best, best_history, average_history = genetic_algorithm()

    st.subheader("Best Chromosome")

    st.code("".join(map(str, best)))

    st.write("Number of Ones:", sum(best))
    st.write("Fitness Score:", fitness(best))

    if sum(best) == TARGET_ONES:
        st.success("Target achieved!")
    else:
        st.warning("Try running the algorithm again.")

    # Graph
    st.subheader("Fitness Performance")

    fig, ax = plt.subplots()

    ax.plot(best_history, label="Best Fitness")
    ax.plot(average_history, label="Average Fitness")

    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    ax.set_title("Genetic Algorithm Progress")

    ax.legend()
    ax.grid()

    st.pyplot(fig)
