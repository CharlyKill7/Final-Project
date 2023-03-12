import pygame

pygame.init()
pygame.display.set_caption("Luna")

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_rect = screen.get_rect()

luna_image = pygame.image.load(r"img/luna.png")
luna_small = pygame.transform.scale(luna_image, (int(1*screen.get_width()/12), int(1*screen.get_width()/12)))
luna_small_rect = luna_small.get_rect()
luna_small_rect.bottomright = screen_rect.bottomright

screen.fill((0, 0, 0))
screen.blit(luna_small, luna_small_rect)
pygame.display.update()

pygame.time.delay(5000)  # tiempo de espera en milisegundos (5 segundos en este caso)
pygame.quit()
