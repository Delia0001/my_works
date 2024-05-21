import pygame
import colorsys


def get_color(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


class LorenzAttractor:
    def __init__(self, x0, y0, z0, sigma, beta, ro):
        self.x = x0
        self.y = y0
        self.z = z0
        self.sigma = sigma
        self.beta = beta
        self.ro = ro

    def update(self, d_t):
        dx = (self.sigma * (self.y - self.x)) * d_t
        dy = (self.x * (self.ro - self.z) - self.y) * d_t
        dz = (self.x * self.y - self.beta * self.z) * d_t

        self.x += dx
        self.y += dy
        self.z += dz

        points.append((int(self.x * scale) + width // 2, int(self.y * scale) + height // 2))


pygame.init()
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
surface = pygame.Surface((width, height))
pygame.display.set_caption("Lorenz Attractor")
clock = pygame.time.Clock()

fps = 60
scale = 10
dt = 0.01
hue = 0
lorenz = LorenzAttractor(1, 2, 0.1, 10, 8 / 3, 28)
running = True
points = []

font_size = 25
font = pygame.font.SysFont("serif", font_size)

text = "Нажмите клавиши 'Вверх' - для увеличения параметра 'ro', 'Вниз' - для уменьшения параметра 'ro', 'Вправо' - для увеличения параметра 'beta', \
    'Влево' - для уменьшения параметра 'beta', '+' - для увеличения параметра 'sigma' или '-' - для уменьшения параметра 'sigma'"

image_width = 400
image_x, image_y = 250, 150


def draw_text(sfc, tx, x, y, clr, ft):
    words = tx.split()
    lines = []
    current_line = words[0]

    for word in words[1:]:
        if ft.size(current_line + ' ' + word)[0] < image_width:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word

    lines.append(current_line)

    for i, line in enumerate(lines):
        text_surface = ft.render(line, True, clr)
        sfc.blit(text_surface, (x, y + i * font_size))


while running:
    surface.fill((0, 0, 0))
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                lorenz.ro += 0.5
            elif event.key == pygame.K_DOWN:
                lorenz.ro -= 0.5
            elif event.key == pygame.K_LEFT:
                lorenz.beta -= 0.5
            elif event.key == pygame.K_RIGHT:
                lorenz.beta += 0.5
            elif event.key == pygame.K_KP_PLUS:
                lorenz.sigma += 0.5
            elif event.key == pygame.K_KP_MINUS:
                lorenz.sigma -= 0.5

    lorenz.update(dt)

    if hue > 1:
        hue = 0
    color = get_color(hue, 1, 1)

    if len(points) >= 2:
        pygame.draw.lines(surface, color, False, points)
        hue += 0.006

    draw_text(surface, text, image_x, image_y, (255, 255, 255), font)
    screen.blit(surface, (0, 0))
    pygame.display.flip()

pygame.quit()
