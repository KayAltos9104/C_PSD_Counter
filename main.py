import pygame
from phys_aero import *

test_colliders = {}
id = 1

def main():
    global id, test_colliders

    

    pygame.init()
    canvas = pygame.display.set_mode((1200, 720))
    pygame.display.set_caption("Modern DLCA")
    clock = pygame.time.Clock()
    is_running = True
    while is_running:
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
        
        canvas.fill((255,255,255))
        for p in test_colliders:
            test_colliders[p].draw(canvas)

        for first in test_colliders:
            for second in test_colliders:
                if first == second:
                    continue
                if Particle.is_intersects(test_colliders[first], test_colliders[second], canvas):
                    test_colliders[first].color = (255, 0, 0)

        

        pygame.display.flip()
        # держим цикл на правильной скорости
        clock.tick(60)
        pygame.time.delay(50)

def generate_particle(center_x, center_y):
    global id, test_colliders
    radius = 25
    test_colliders[id] = Particle(center_x, center_y, radius)
    id += 1

if __name__ == '__main__':
    main()