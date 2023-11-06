import time
from os.path import join

from code.resources import resource_path
from settings import *
from snake import Snake
from apple import Apple


class Main:
    def __init__(self):
        # general
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('PySnake')

        # game objects
        self.bg_rects = [pygame.Rect((col + int(row % 2 == 0)) * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                         for col in range(0, COLS, 2) for row in range(ROWS)]
        self.snake = Snake()
        self.apple = Apple(self.snake)

        # timer
        self.update_event = pygame.event.custom_type()
        pygame.time.set_timer(self.update_event, 200)
        self.game_active = False
        self.last_input_time = 0
        self.input_delay = 0.05

        # audio
        # self.crunch_sound = pygame.mixer.Sound(join('..', 'audio', 'crunch.wav'))
        # self.bg_music = pygame.mixer.Sound(join('..', 'audio', 'Arcade.ogg'))

        crunch_path = resource_path(join('audio', 'crunch.wav'))
        self.crunch_sound = pygame.mixer.Sound(crunch_path)
        bg_music_path = resource_path(join('audio', 'Arcade.ogg'))
        self.bg_music = pygame.mixer.Sound(bg_music_path)

        self.bg_music.set_volume(0.5)

        # score counter
        self.score = 0

    def draw_bg(self):
        self.display_surface.fill(GREY)
        for rect in self.bg_rects:
            pygame.draw.rect(self.display_surface, LIGHT_GREY, rect)

    def input(self):
        current_time = time.time()
        if current_time - self.last_input_time > self.input_delay:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.snake.direction = pygame.Vector2(1, 0) if self.snake.direction.x != -1 else self.snake.direction
            if keys[pygame.K_LEFT]:
                self.snake.direction = pygame.Vector2(-1, 0) if self.snake.direction.x != 1 else self.snake.direction
            if keys[pygame.K_UP]:
                self.snake.direction = pygame.Vector2(0, -1) if self.snake.direction.y != 1 else self.snake.direction
            if keys[pygame.K_DOWN]:
                self.snake.direction = pygame.Vector2(0, 1) if self.snake.direction.y != -1 else self.snake.direction
            self.last_input_time = current_time

    def collision(self):
        if self.snake.body[0] == self.apple.pos:
            self.snake.has_eaten = True
            self.apple.set_pos()
            self.crunch_sound.play()
            self.score += 1  # Увеличиваем счетчик

        if self.snake.body[0] in self.snake.body[1:] or \
                not 0 <= self.snake.body[0].x < COLS or \
                not 0 <= self.snake.body[0].y < ROWS:
            self.bg_music.stop()
            self.display_final_score()
            waiting_for_key = True
            while waiting_for_key:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        waiting_for_key = False
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
            self.snake.reset()
            self.game_active = False
            self.score = 0

    def display_final_score(self):
        self.display_surface.fill(GREY)
        font = pygame.font.Font(None, 36)
        text_surf = font.render(f'Score: {self.score}', True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        bg_rect = text_rect.inflate(20, 20)
        pygame.draw.rect(self.display_surface, (0, 0, 0), bg_rect)
        self.display_surface.blit(text_surf, text_rect)
        pygame.display.update()

    def draw_shadow(self):
        shadow_surf = pygame.Surface((self.display_surface.get_size()))
        shadow_surf.fill((0, 255, 0))
        shadow_surf.set_colorkey((0, 255, 0))
        # surf
        shadow_surf.blit(self.apple.scaled_surf, self.apple.scaled_rect.topleft + SHADOW_SIZE)
        for surf, rect in self.snake.draw_data:
            shadow_surf.blit(surf, rect.topleft + SHADOW_SIZE)

        mask = pygame.mask.from_surface(shadow_surf)
        mask.invert()
        shadow_surf = mask.to_surface()
        shadow_surf.set_colorkey((255, 255, 255))
        shadow_surf.set_alpha(SHADOW_OPACITY)

        self.display_surface.blit(shadow_surf, (0, 0))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == self.update_event and self.game_active:
                    self.snake.update()

                if event.type == pygame.KEYDOWN and not self.game_active:
                    self.game_active = True
                    self.bg_music.play(-1)

            # updates
            self.input()
            self.collision()

            # drawing
            self.draw_bg()
            self.draw_shadow()
            self.snake.draw()
            self.apple.draw()
            pygame.display.update()


if __name__ == '__main__':
    main = Main()
    main.run()
