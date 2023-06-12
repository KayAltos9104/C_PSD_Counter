import pygame
import time
from phys_aero import *
from off_lattice_dlca import *
from settings import * 

test_colliders = {}
id = 1

def main():
    global id, test_colliders
    '''
    p1 = Particle (200, 200, 15)
    p2 = Particle (400, 400, 25)
    g = Globule (1)
    print(g)
    print(g.add_particle(p1))
    print(g.add_particle(p2))
    print(g.remove_particle(p1))
    '''
    

    CA = CellularAutomata(Vector2 (1000, 650), 15, 0.90)
    CA.initialize()
    print(CA.log)
    CA.log = ''

    pygame.init()
    canvas = pygame.display.set_mode((1400, 800))
    pygame.display.set_caption("Modern DLCA")
    clock = pygame.time.Clock()
    is_running = True
    while is_running:
        start_time = time.time()
        for event in pygame.event.get():
            # проверить закрытие окна
            if event.type == pygame.QUIT:
                is_running = False     
            # Если нажата кнопка мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Записываем позицию курсора в пикселях
                cursor_pos = event.pos
                # Считаем индекс клетки по Х
                x_pos = cursor_pos[0]
                # Считаем индекс клетки по Y
                y_pos = cursor_pos[1]

                if event.button == 1:
                    generate_particle(x_pos, y_pos)
        
        CA.move_all_globules()
        print(CA.log)
        CA.log = ''


        canvas.fill(BLACK)
        pygame.draw.rect(canvas, WHITE, (OFFSET, OFFSET, 1000, 650))

        for g in CA.globules:
            CA.globules[g].draw(canvas)
        '''
        for p in test_colliders:
            test_colliders[p].draw(canvas)

        for first in test_colliders:
            for second in test_colliders:
                if first == second:
                    continue
                #if Particle.is_intersects(test_colliders[first], test_colliders[second], canvas):
                if Particle.is_intersects(test_colliders[first], test_colliders[second]):
                    test_colliders[first].color = RED
        '''
        

        pygame.display.flip()
        # держим цикл на правильной скорости
        clock.tick(60)
        pygame.time.delay(100)
        end_time = time.time()
        print(end_time - start_time)
        

def generate_particle(center_x, center_y):
    global id, test_colliders
    radius = 25
    test_colliders[id] = Particle(center_x, center_y, radius)
    id += 1

if __name__ == '__main__':
    main()