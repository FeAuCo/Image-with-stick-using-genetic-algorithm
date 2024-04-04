import random
import numpy as np
from img_preprocessing import preprocess_image, bresenham_line
from visualize import visualize

POPULATION_SIZE = 180  # размер популяции
GENERATIONS = 1001  # количество поколений
path = "circle.jpeg"
IMAGE = preprocess_image(path)
DRAFT = preprocess_image(path)


def update_fitness(population):
    for individ in population:
        individ.fitness = get_fitness(individ)


def draw_population(population):
    for individ in population:
        for pixel in individ.pixels:
            DRAFT[pixel[0]][pixel[1]] = 150


def reset_draft():
    global DRAFT
    DRAFT = preprocess_image(path)


# посчитать значение подходимости (fitness) для конкретного отрезка (особи)
def get_fitness(stick):
    current_value = 0
    for pixel in stick.pixels:
        if IMAGE[pixel[0], pixel[1]] == 0:
            current_value += 5
        # elif DRAFT[pixel[0], pixel[1]] == 150:
        #     current_value -=2
        else:
            current_value -= 5
    return current_value  # считаете количество пересечений ваших палок и черных пикселей на данной картинке


class Individ:
    def __init__(self, l, angle, x, y):
        # параметры, которые нужно менять
        self.l = l
        self.angle = angle  # degrees
        self.middle_x = x
        self.middle_y = y

        # свойства, которые нельзя менять
        angle_rad = np.radians(angle)
        y0 = int(self.middle_y + np.cos(angle_rad) * l / 2)
        x0 = int(self.middle_x + np.sin(angle_rad) * l / 2)
        y1 = int(self.middle_y - np.cos(angle_rad) * l / 2)
        x1 = int(self.middle_x - np.sin(angle_rad) * l / 2)
        self.pixels = bresenham_line(x0, y0, x1, y1)
        self.fitness = get_fitness(self)


def create_individ():
    # Здесь код для создания одного индивида в популяции
    # каждый индивид - [длина палки, наклон палки, x_середины, y_середины]
    l = random.randint(1, 5)  # длина палки от 5 до 40 пикселей #34
    angle = random.randint(0, 359)  # наклон в градусах
    x = random.randint(10, 231)
    y = random.randint(10, 231)
    stick = Individ(l, angle, x, y)
    return stick


# создаем всю популяцию
def create_population(size):  # size = POPULATION_SIZE
    population = []
    for item in range(size):
        population.append(create_individ())
    return population.copy()


def selection(population):
    # выбор 25% самых лучших индивидов из популяции
    sorted_population = sorted(population, key=lambda x: x.fitness, reverse=True)
    return sorted_population[:POPULATION_SIZE // 4]


def crossover(individ1, individ2):
    l = individ1.l
    angle = individ1.angle
    middle_x = individ1.middle_x
    middle_y = individ1.middle_y
    probability = random.random()
    if probability < 0.1:
        l = individ2.l
    elif probability < 0.2:
        angle = individ2.angle
    elif probability < 0.3:
        middle_x = individ2.middle_x
    elif probability < 0.4:
        middle_y = individ2.middle_y
    elif probability < 0.5:
        middle_x = individ2.middle_x
        middle_y = individ2.middle_y
    elif probability < 0.6:
        l = individ2.l
        angle = individ2.angle
    elif probability < 0.7:
        l = individ2.l
        middle_x = individ2.middle_x
    elif probability < 0.8:
        l = individ2.l
        middle_y = individ2.middle_y
    elif probability < 0.9:
        angle = individ2.angle
        middle_x = individ2.middle_x
    else:
        angle = individ2.angle
        middle_y = individ2.middle_y
    new_individ = Individ(l, angle, middle_x, middle_y)
    return new_individ


def mutation(individ):
    l = individ.l
    angle = individ.angle
    middle_x = individ.middle_x
    middle_y = individ.middle_y
    probability = random.random()
    if probability < 0.1:
        l = random.randint(1, 5)
    elif probability < 0.2:
        angle = random.randint(0, 359)
    elif probability < 0.3:
        middle_x = random.randint(25, 231)
    elif probability < 0.4:
        middle_y = random.randint(25, 231)
    elif probability < 0.5:
        middle_x = random.randint(25, 231)
        middle_y = random.randint(25, 231)
    elif probability < 0.6:
        l = random.randint(1, 5)
        angle = random.randint(0, 359)
    elif probability < 0.7:
        l = random.randint(1, 5)
        middle_x = random.randint(25, 231)
    elif probability < 0.8:
        l = random.randint(1, 5)
        middle_y = random.randint(25, 231)
    elif probability < 0.9:
        angle = random.randint(0, 359)
        middle_x = random.randint(25, 231)
    else:
        angle = random.randint(0, 359)
        middle_y = random.randint(25, 231)
    new_individ = Individ(l, angle, middle_x, middle_y)
    return new_individ


def main():
    population = create_population(POPULATION_SIZE)
    for generation in range(GENERATIONS):
        # update_fitness(population)
        best_individs = selection(population)  # селекция
        crossovered = [crossover(random.choice(best_individs), random.choice(best_individs)) for _ in
                       range(POPULATION_SIZE // 4)]  # тут несколько строк кода,
        # чтобы сделать скрещивание между лучшими особями
        # и создать 25% популяции скрещиванием
        mutated = [mutation(random.choice(best_individs)) for _ in
                   range(POPULATION_SIZE // 4)]  # тут несколько строк кода,
        # чтобы сделать мутации лучшим
        # и создать 25% популяции мутацией
        population = best_individs + crossovered + mutated + create_population(
            POPULATION_SIZE // 4)  # размер популяции всегда фиксированный
        # reset_draft()
        # draw_population(population)
        population = sorted(population, key=lambda x: x.fitness, reverse=True)
        print(f'generation {generation}, fitness: {sum([x.fitness for x in population])}')

    visualize(IMAGE.shape, population, image=None) # IMAGE.copy()


if __name__ == '__main__':
    main()
