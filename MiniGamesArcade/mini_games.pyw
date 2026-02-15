import pygame
import sys
import random
import math
import colorsys

# ─── Constants ───────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 900, 700
FPS = 60
CREATOR = "Kotan123"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 50, 50)
GREEN = (50, 200, 50)
BLUE = (50, 100, 220)
YELLOW = (240, 220, 40)
ORANGE = (240, 150, 30)
PURPLE = (150, 50, 200)
CYAN = (50, 200, 220)
DARK_GRAY = (40, 40, 50)
LIGHT_GRAY = (180, 180, 190)
DARK_BG = (12, 12, 22)
NEON_GREEN = (0, 255, 100)
NEON_BLUE = (0, 150, 255)
NEON_PINK = (255, 50, 150)
GOLD = (255, 215, 0)
DARK_RED = (140, 20, 20)
TEAL = (0, 180, 180)
LIME = (180, 255, 0)
SKY_BLUE = (100, 180, 255)

# ─── Theme System ────────────────────────────────────────────────────────────
THEMES = {
    "Neon": {
        "bg": (12, 12, 22),
        "accent1": (0, 150, 255),
        "accent2": (255, 50, 150),
        "gold": (255, 215, 0),
        "panel": (20, 20, 35),
        "text": (255, 255, 255),
        "name_color": (0, 150, 255),
    },
    "Ocean": {
        "bg": (5, 15, 35),
        "accent1": (0, 200, 200),
        "accent2": (50, 120, 220),
        "gold": (100, 220, 255),
        "panel": (10, 25, 50),
        "text": (200, 230, 255),
        "name_color": (0, 200, 200),
    },
    "Sunset": {
        "bg": (25, 10, 18),
        "accent1": (255, 120, 50),
        "accent2": (220, 50, 100),
        "gold": (255, 200, 60),
        "panel": (35, 15, 25),
        "text": (255, 220, 200),
        "name_color": (255, 120, 50),
    },
    "Matrix": {
        "bg": (2, 5, 2),
        "accent1": (0, 220, 0),
        "accent2": (0, 160, 0),
        "gold": (100, 255, 100),
        "panel": (5, 15, 5),
        "text": (0, 255, 80),
        "name_color": (0, 220, 0),
    },
}
theme = dict(THEMES["Neon"])
theme_name = "Neon"


def set_theme(name):
    global theme, theme_name
    theme_name = name
    theme.update(THEMES[name])


# ─── Particle System ────────────────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, color, vx=None, vy=None, life=None, size=None, gravity=0, fade=True, glow=False):
        self.x = x
        self.y = y
        self.color = color
        self.vx = vx if vx is not None else random.uniform(-3, 3)
        self.vy = vy if vy is not None else random.uniform(-5, -1)
        self.life = life if life is not None else random.randint(20, 50)
        self.max_life = self.life
        self.size = size if size is not None else random.randint(2, 5)
        self.gravity = gravity
        self.fade = fade
        self.glow = glow

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.life -= 1

    def draw(self, surface):
        if self.life <= 0:
            return
        alpha = self.life / self.max_life if self.fade else 1
        r = min(255, int(self.color[0] * alpha))
        g = min(255, int(self.color[1] * alpha))
        b = min(255, int(self.color[2] * alpha))
        sz = max(1, int(self.size * alpha))
        if self.glow and sz > 2:
            glow_surf = pygame.Surface((sz * 4, sz * 4), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (r, g, b, int(60 * alpha)), (sz * 2, sz * 2), sz * 2)
            surface.blit(glow_surf, (int(self.x - sz * 2), int(self.y - sz * 2)))
        pygame.draw.circle(surface, (r, g, b), (int(self.x), int(self.y)), sz)

    @property
    def alive(self):
        return self.life > 0


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, x, y, color, count=10, **kwargs):
        for _ in range(count):
            self.particles.append(Particle(x, y, color, **kwargs))

    def explosion(self, x, y, color, count=30):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 6)
            self.particles.append(Particle(
                x, y, color,
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                life=random.randint(15, 40),
                size=random.randint(2, 5),
                gravity=0.05,
                glow=True
            ))

    def sparkle(self, x, y, color, count=5):
        for _ in range(count):
            self.particles.append(Particle(
                x + random.randint(-20, 20), y + random.randint(-20, 20),
                color, vx=random.uniform(-0.5, 0.5), vy=random.uniform(-1, 0),
                life=random.randint(10, 25), size=random.randint(1, 3), glow=True
            ))

    def update(self):
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.alive]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)


# ─── Helpers ─────────────────────────────────────────────────────────────────
def draw_text(surface, text, size, color, x, y, center=True, font_name=None):
    font = pygame.font.SysFont(font_name or "consolas", size, bold=True)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(rendered, rect)
    return rect


def draw_text_shadow(surface, text, size, color, x, y, shadow_color=(0, 0, 0)):
    draw_text(surface, text, size, shadow_color, x + 2, y + 2)
    return draw_text(surface, text, size, color, x, y)


def draw_rounded_bar(surface, x, y, w, h, fill_ratio, bg_color, fill_color, border_color=None):
    """Draw a rounded progress/health bar."""
    pygame.draw.rect(surface, bg_color, (x, y, w, h), border_radius=h // 2)
    fill_w = max(h, int(w * max(0, min(1, fill_ratio))))
    if fill_ratio > 0:
        pygame.draw.rect(surface, fill_color, (x, y, fill_w, h), border_radius=h // 2)
    if border_color:
        pygame.draw.rect(surface, border_color, (x, y, w, h), 2, border_radius=h // 2)


def draw_panel(surface, rect, bg_color=(20, 20, 35), border_color=None, alpha=200, radius=18):
    """Draw a semi-transparent rounded panel."""
    panel = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    pygame.draw.rect(panel, (*bg_color, alpha), (0, 0, rect[2], rect[3]), border_radius=radius)
    if border_color:
        pygame.draw.rect(panel, (*border_color, 180), (0, 0, rect[2], rect[3]), 2, border_radius=radius)
    surface.blit(panel, (rect[0], rect[1]))


def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                return True
        pygame.time.wait(50)


def screen_transition(screen, direction="in", color=BLACK, speed=15):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.fill(color)
    if direction == "in":
        for alpha in range(255, -1, -speed):
            overlay.set_alpha(max(0, alpha))
            screen.blit(overlay, (0, 0))
            pygame.display.flip()
            pygame.time.wait(10)
    else:
        for alpha in range(0, 256, speed):
            overlay.set_alpha(min(255, alpha))
            screen.blit(overlay, (0, 0))
            pygame.display.flip()
            pygame.time.wait(10)


def game_over_screen(screen, score, particles):
    """Animated game over with rounded overlay panel."""
    particles.explosion(WIDTH // 2, HEIGHT // 2 - 60, RED, 40)
    for _ in range(30):
        particles.update()
        screen.fill(theme["bg"])
        particles.draw(screen)
        draw_panel(screen, (WIDTH // 2 - 200, HEIGHT // 2 - 100, 400, 200), (40, 10, 10), RED)
        draw_text_shadow(screen, "GAME OVER", 60, RED, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text_shadow(screen, f"Score: {score}", 36, GOLD, WIDTH // 2, HEIGHT // 2 + 10)
        draw_text(screen, "Press any key (ESC = menu)", 20, LIGHT_GRAY, WIDTH // 2, HEIGHT // 2 + 60)
        pygame.display.flip()
        pygame.time.wait(16)
    return wait_for_key()


def win_screen(screen, msg, score, particles):
    for i in range(5):
        particles.explosion(
            random.randint(100, WIDTH - 100),
            random.randint(100, HEIGHT - 100),
            random.choice([GOLD, NEON_GREEN, CYAN, NEON_PINK]),
            20
        )
    for _ in range(40):
        particles.update()
        screen.fill(theme["bg"])
        particles.draw(screen)
        draw_panel(screen, (WIDTH // 2 - 220, HEIGHT // 2 - 100, 440, 200), (10, 30, 10), NEON_GREEN)
        draw_text_shadow(screen, msg, 60, NEON_GREEN, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text_shadow(screen, f"Score: {score}", 36, GOLD, WIDTH // 2, HEIGHT // 2 + 10)
        draw_text(screen, "Press any key (ESC = menu)", 20, LIGHT_GRAY, WIDTH // 2, HEIGHT // 2 + 60)
        pygame.display.flip()
        pygame.time.wait(16)
    return wait_for_key()


def draw_stars(surface, stars, scroll=0):
    for sx, sy, sz in stars:
        brightness = int(100 + sz * 50)
        y = (sy + scroll * sz * 0.5) % HEIGHT
        pygame.draw.circle(surface, (brightness, brightness, brightness + 20), (int(sx), int(y)), max(1, int(sz)))


def rainbow_color(offset=0):
    t = (pygame.time.get_ticks() / 1000 + offset) % 1.0
    r, g, b = colorsys.hsv_to_rgb(t, 0.9, 1.0)
    return (int(r * 255), int(g * 255), int(b * 255))


def draw_hud(surface, text, y=22):
    """Draw HUD text with rounded background bar."""
    font = pygame.font.SysFont("consolas", 22, bold=True)
    rendered = font.render(text, True, theme["text"])
    tw = rendered.get_width()
    draw_panel(surface, (WIDTH // 2 - tw // 2 - 16, y - 14, tw + 32, 28), theme["panel"], None, 160, 14)
    rect = rendered.get_rect(center=(WIDTH // 2, y))
    surface.blit(rendered, rect)


def draw_controls_hint(surface, text, timer):
    """Draw fading control hint panel in bottom-right corner."""
    if timer <= 0:
        return
    alpha = min(200, timer * 3)
    font = pygame.font.SysFont("consolas", 15, bold=True)
    txt = font.render(text, True, theme["text"])
    tw = txt.get_width()
    px, py = WIDTH - tw - 36, HEIGHT - 38
    panel = pygame.Surface((tw + 24, 26), pygame.SRCALPHA)
    pygame.draw.rect(panel, (*theme["panel"], alpha), (0, 0, tw + 24, 26), border_radius=10)
    surface.blit(panel, (px, py))
    txt.set_alpha(alpha)
    surface.blit(txt, (px + 12, py + 4))


# ─── Background stars (shared) ──────────────────────────────────────────────
BG_STARS = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(0.5, 2.5)) for _ in range(120)]


# ═══════════════════════════════════════════════════════════════════════════════
#  1. PONG
# ═══════════════════════════════════════════════════════════════════════════════
def run_pong(screen):
    clock = pygame.time.Clock()
    ps = ParticleSystem()
    pw, ph = 14, 90
    player_y = HEIGHT // 2 - ph // 2
    ai_y = HEIGHT // 2 - ph // 2
    ball_x, ball_y = float(WIDTH // 2), float(HEIGHT // 2)
    base_speed = 5.0
    bvx, bvy = base_speed, 3.0
    p_score, a_score = 0, 0
    ai_speed = 4.5
    trail = []
    max_score = 12
    ctrl_timer = 3 * FPS

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player_y = max(0, player_y - 7)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player_y = min(HEIGHT - ph, player_y + 7)

        ai_center = ai_y + ph // 2
        if ball_y < ai_center - 15:
            ai_y = max(0, ai_y - ai_speed)
        elif ball_y > ai_center + 15:
            ai_y = min(HEIGHT - ph, ai_y + ai_speed)

        trail.append((int(ball_x), int(ball_y)))
        if len(trail) > 15:
            trail.pop(0)

        ball_x += bvx
        ball_y += bvy

        if ball_y <= 5 or ball_y >= HEIGHT - 5:
            bvy = -bvy
            ps.sparkle(ball_x, ball_y, CYAN, 3)

        if ball_x <= 35 + pw and player_y <= ball_y <= player_y + ph and bvx < 0:
            bvx = -bvx * 1.02
            offset = (ball_y - (player_y + ph / 2)) / (ph / 2)
            bvy = offset * 6
            ps.explosion(ball_x, ball_y, NEON_BLUE, 15)
        if ball_x >= WIDTH - 35 - pw and ai_y <= ball_y <= ai_y + ph and bvx > 0:
            bvx = -bvx * 1.02
            offset = (ball_y - (ai_y + ph / 2)) / (ph / 2)
            bvy = offset * 6
            ps.explosion(ball_x, ball_y, NEON_PINK, 15)

        if ball_x < 0:
            a_score += 1
            total = p_score + a_score
            base_speed = 5.0 + total * 0.3
            ai_speed = 4.5 + total * 0.15
            ps.explosion(30, ball_y, RED, 25)
            ball_x, ball_y = float(WIDTH // 2), float(HEIGHT // 2)
            bvx = base_speed
            bvy = random.choice([-3.0, 3.0])
            trail.clear()
        elif ball_x > WIDTH:
            p_score += 1
            total = p_score + a_score
            base_speed = 5.0 + total * 0.3
            ai_speed = 4.5 + total * 0.15
            ps.explosion(WIDTH - 30, ball_y, NEON_GREEN, 25)
            ball_x, ball_y = float(WIDTH // 2), float(HEIGHT // 2)
            bvx = -base_speed
            bvy = random.choice([-3.0, 3.0])
            trail.clear()

        # Score limit
        if p_score >= max_score:
            if not win_screen(screen, "YOU WIN!", p_score, ps):
                return
            p_score = a_score = 0
            base_speed = 5.0
            ai_speed = 4.5
            ball_x, ball_y = float(WIDTH // 2), float(HEIGHT // 2)
            bvx, bvy = base_speed, 3.0
            trail.clear()
            continue
        if a_score >= max_score:
            if not game_over_screen(screen, p_score, ps):
                return
            p_score = a_score = 0
            base_speed = 5.0
            ai_speed = 4.5
            ball_x, ball_y = float(WIDTH // 2), float(HEIGHT // 2)
            bvx, bvy = base_speed, 3.0
            trail.clear()
            continue

        bvx = max(-15, min(15, bvx))
        ctrl_timer = max(0, ctrl_timer - 1)

        ps.update()
        screen.fill(theme["bg"])
        draw_stars(screen, BG_STARS)

        for y in range(0, HEIGHT, 24):
            pygame.draw.rect(screen, (40, 40, 50), (WIDTH // 2 - 1, y, 2, 12))

        for i, (tx, ty) in enumerate(trail):
            alpha = int((i / len(trail)) * 150) if trail else 0
            sz = max(1, int((i / max(1, len(trail))) * 6))
            s = pygame.Surface((sz * 2, sz * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 255, 255, alpha), (sz, sz), sz)
            screen.blit(s, (tx - sz, ty - sz))

        glow_p = pygame.Surface((pw + 20, ph + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow_p, (*NEON_BLUE, 40), (0, 0, pw + 20, ph + 20), border_radius=8)
        screen.blit(glow_p, (25, player_y - 10))
        pygame.draw.rect(screen, NEON_BLUE, (35, player_y, pw, ph), border_radius=6)

        glow_a = pygame.Surface((pw + 20, ph + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow_a, (*NEON_PINK, 40), (0, 0, pw + 20, ph + 20), border_radius=8)
        screen.blit(glow_a, (WIDTH - 35 - pw - 10, ai_y - 10))
        pygame.draw.rect(screen, NEON_PINK, (WIDTH - 35 - pw, ai_y, pw, ph), border_radius=6)

        glow_b = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(glow_b, (255, 255, 255, 60), (15, 15), 15)
        screen.blit(glow_b, (int(ball_x) - 15, int(ball_y) - 15))
        pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), 8)

        ps.draw(screen)
        draw_text_shadow(screen, str(p_score), 56, NEON_BLUE, WIDTH // 2 - 70, 45)
        draw_text_shadow(screen, str(a_score), 56, NEON_PINK, WIDTH // 2 + 70, 45)
        draw_text(screen, f"First to {max_score}", 16, LIGHT_GRAY, WIDTH // 2, 80)
        draw_hud(screen, "PONG", HEIGHT - 22)
        draw_controls_hint(screen, "W/S or Up/Down", ctrl_timer)
        pygame.display.flip()
        clock.tick(FPS)


# ═══════════════════════════════════════════════════════════════════════════════
#  2. FLAPPY BIRD  (FIX: replaced per-pixel pipe gradient with solid rects)
# ═══════════════════════════════════════════════════════════════════════════════
def run_flappy(screen):
    clock = pygame.time.Clock()
    ps = ParticleSystem()
    ctrl_timer = 3 * FPS
    bird_x = 140
    bird_y = float(HEIGHT // 2)
    bird_vel = 0.0
    gravity = 0.45
    flap_power = -7.5
    bird_r = 18
    pipe_w = 65
    gap = 170
    pipe_speed = 3
    pipes = []
    score = 0
    frame = 0
    game_started = False
    cloud_x = [random.randint(0, WIDTH) for _ in range(6)]
    cloud_y = [random.randint(30, 150) for _ in range(6)]

    def spawn_pipe():
        top = random.randint(70, HEIGHT - gap - 70)
        pipes.append([float(WIDTH), top])

    spawn_pipe()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_SPACE:
                    bird_vel = flap_power
                    game_started = True
                    ps.emit(bird_x - 10, bird_y + 10, YELLOW, 5,
                            vx=random.uniform(-2, 0), vy=random.uniform(1, 3),
                            life=15, size=2, gravity=0.1)

        if game_started:
            bird_vel += gravity
            bird_y += bird_vel

            for p in pipes:
                p[0] -= pipe_speed

            if pipes and pipes[0][0] + pipe_w < 0:
                pipes.pop(0)
                score += 1
                ps.sparkle(bird_x, bird_y, GOLD, 8)

            frame += 1
            if frame % 85 == 0:
                spawn_pipe()

            dead = bird_y - bird_r < 0 or bird_y + bird_r > HEIGHT
            for px, ptop in pipes:
                if bird_x + bird_r > px and bird_x - bird_r < px + pipe_w:
                    if bird_y - bird_r < ptop or bird_y + bird_r > ptop + gap:
                        dead = True

            if dead:
                ps.explosion(bird_x, bird_y, ORANGE, 40)
                if not game_over_screen(screen, score, ps):
                    return
                bird_y = float(HEIGHT // 2)
                bird_vel = 0.0
                pipes.clear()
                spawn_pipe()
                score = 0
                frame = 0
                game_started = False
                continue

        # Draw sky gradient (horizontal lines are fine, one per row)
        for y_line in range(0, HEIGHT, 3):
            t = y_line / HEIGHT
            r = int(25 + 15 * t)
            g = int(25 + 30 * t)
            b_val = int(60 + 30 * (1 - t))
            pygame.draw.line(screen, (r, g, b_val), (0, y_line), (WIDTH, y_line))
            if y_line + 1 < HEIGHT:
                pygame.draw.line(screen, (r, g, b_val), (0, y_line + 1), (WIDTH, y_line + 1))
            if y_line + 2 < HEIGHT:
                pygame.draw.line(screen, (r, g, b_val), (0, y_line + 2), (WIDTH, y_line + 2))

        # Clouds
        for i in range(len(cloud_x)):
            cloud_x[i] -= 0.3
            if cloud_x[i] < -80:
                cloud_x[i] = WIDTH + 40
            cx, cy = int(cloud_x[i]), cloud_y[i]
            s = pygame.Surface((80, 30), pygame.SRCALPHA)
            pygame.draw.ellipse(s, (255, 255, 255, 25), (0, 8, 80, 22))
            pygame.draw.ellipse(s, (255, 255, 255, 30), (15, 0, 50, 30))
            screen.blit(s, (cx, cy))

        pygame.draw.rect(screen, (50, 100, 30), (0, HEIGHT - 5, WIDTH, 5))

        # FIX: Pipes drawn as solid rects with highlight strip (no per-pixel lines)
        for px, ptop in pipes:
            # Top pipe body
            pipe_color = (40, 160, 40)
            pipe_dark = (30, 120, 30)
            pipe_light = (60, 200, 60)
            pygame.draw.rect(screen, pipe_color, (int(px), 0, pipe_w, int(ptop)), border_radius=0)
            pygame.draw.rect(screen, pipe_light, (int(px) + 4, 0, 8, int(ptop)))
            pygame.draw.rect(screen, pipe_dark, (int(px) + pipe_w - 8, 0, 8, int(ptop)))
            # Bottom pipe body
            bot_top = int(ptop + gap)
            pygame.draw.rect(screen, pipe_color, (int(px), bot_top, pipe_w, HEIGHT - bot_top), border_radius=0)
            pygame.draw.rect(screen, pipe_light, (int(px) + 4, bot_top, 8, HEIGHT - bot_top))
            pygame.draw.rect(screen, pipe_dark, (int(px) + pipe_w - 8, bot_top, 8, HEIGHT - bot_top))
            # Pipe caps
            pygame.draw.rect(screen, (40, 170, 40), (int(px) - 4, int(ptop) - 12, pipe_w + 8, 16), border_radius=6)
            pygame.draw.rect(screen, (40, 170, 40), (int(px) - 4, int(ptop + gap), pipe_w + 8, 16), border_radius=6)

        # Bird
        wing_y = math.sin(pygame.time.get_ticks() * 0.015) * 4
        pygame.draw.circle(screen, YELLOW, (int(bird_x), int(bird_y)), bird_r)
        pygame.draw.circle(screen, (255, 240, 100), (int(bird_x - 3), int(bird_y - 3)), bird_r - 4)
        pygame.draw.ellipse(screen, ORANGE, (int(bird_x - 14), int(bird_y + wing_y), 16, 10))
        pygame.draw.circle(screen, WHITE, (int(bird_x + 8), int(bird_y - 5)), 6)
        pygame.draw.circle(screen, BLACK, (int(bird_x + 10), int(bird_y - 5)), 3)
        pygame.draw.polygon(screen, ORANGE, [
            (bird_x + bird_r - 2, bird_y + 1),
            (bird_x + bird_r + 12, bird_y - 2),
            (bird_x + bird_r + 12, bird_y + 5),
        ])

        ps.update()
        ps.draw(screen)

        draw_text_shadow(screen, str(score), 56, WHITE, WIDTH // 2, 55)
        if not game_started:
            draw_panel(screen, (WIDTH // 2 - 180, HEIGHT // 2 + 75, 360, 45), (20, 20, 40), None, 180, 12)
            draw_text_shadow(screen, "Press SPACE to flap!", 28, WHITE, WIDTH // 2, HEIGHT // 2 + 97)
        ctrl_timer = max(0, ctrl_timer - 1)
        draw_controls_hint(screen, "SPACE to flap", ctrl_timer)
        pygame.display.flip()
        clock.tick(FPS)


# ═══════════════════════════════════════════════════════════════════════════════
#  3. BREAKOUT  (FIX: minimum horizontal velocity so ball doesn't go straight up)
# ═══════════════════════════════════════════════════════════════════════════════
def run_breakout(screen):
    clock = pygame.time.Clock()
    ps = ParticleSystem()
    ctrl_timer = 3 * FPS
    paddle_w, paddle_h = 110, 14
    paddle_x = WIDTH // 2 - paddle_w // 2
    paddle_y = HEIGHT - 45
    ball_x, ball_y = float(WIDTH // 2), float(HEIGHT // 2 + 50)
    bvx, bvy = 4.0, -4.0
    ball_r = 7
    score = 0

    brick_rows = 7
    brick_cols = 11
    brick_w = (WIDTH - 20) // brick_cols - 4
    brick_h = 24
    row_colors = [RED, ORANGE, YELLOW, GREEN, CYAN, NEON_BLUE, PURPLE]

    def make_bricks():
        bricks = []
        for row in range(brick_rows):
            for col in range(brick_cols):
                bx = col * (brick_w + 4) + 12
                by = row * (brick_h + 4) + 60
                bricks.append((pygame.Rect(bx, by, brick_w, brick_h), row))
        return bricks

    bricks = make_bricks()

    def reset():
        nonlocal paddle_x, ball_x, ball_y, bvx, bvy, score, bricks
        paddle_x = WIDTH // 2 - paddle_w // 2
        ball_x, ball_y = float(WIDTH // 2), float(HEIGHT // 2 + 50)
        bvx, bvy = 4.0, -4.0
        score = 0
        bricks = make_bricks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            paddle_x = max(0, paddle_x - 8)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            paddle_x = min(WIDTH - paddle_w, paddle_x + 8)

        ball_x += bvx
        ball_y += bvy

        if ball_x - ball_r <= 0 or ball_x + ball_r >= WIDTH:
            bvx = -bvx
        if ball_y - ball_r <= 0:
            bvy = -bvy

        paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_w, paddle_h)
        if bvy > 0 and paddle_rect.collidepoint(ball_x, ball_y + ball_r):
            bvy = -abs(bvy)
            offset = (ball_x - (paddle_x + paddle_w / 2)) / (paddle_w / 2)
            bvx = offset * 5.5
            # FIX: ensure minimum horizontal velocity
            if abs(bvx) < 1.5:
                bvx = 1.5 if bvx >= 0 else -1.5
            ps.sparkle(ball_x, paddle_y, CYAN, 6)

        ball_rect = pygame.Rect(ball_x - ball_r, ball_y - ball_r, ball_r * 2, ball_r * 2)
        for brick_data in bricks[:]:
            brick, row = brick_data
            if ball_rect.colliderect(brick):
                bricks.remove(brick_data)
                bvy = -bvy
                score += (brick_rows - row) * 10
                c = row_colors[row % len(row_colors)]
                ps.explosion(brick.centerx, brick.centery, c, 12)
                break

        if ball_y > HEIGHT + 20:
            if not game_over_screen(screen, score, ps):
                return
            reset()
            continue

        if not bricks:
            if not win_screen(screen, "YOU WIN!", score, ps):
                return
            reset()
            continue

        screen.fill(theme["bg"])
        draw_stars(screen, BG_STARS)

        for brick, row in bricks:
            c = row_colors[row % len(row_colors)]
            pygame.draw.rect(screen, c, brick, border_radius=6)
            highlight = pygame.Rect(brick.x + 2, brick.y + 2, brick.width - 4, brick.height // 2 - 2)
            hl_color = tuple(min(255, v + 50) for v in c)
            s = pygame.Surface((highlight.width, highlight.height), pygame.SRCALPHA)
            pygame.draw.rect(s, (*hl_color, 60), s.get_rect(), border_radius=4)
            screen.blit(s, highlight.topleft)

        glow = pygame.Surface((paddle_w + 20, paddle_h + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow, (*CYAN, 30), (0, 0, paddle_w + 20, paddle_h + 20), border_radius=10)
        screen.blit(glow, (paddle_x - 10, paddle_y - 10))
        pygame.draw.rect(screen, WHITE, paddle_rect, border_radius=7)

        gb = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(gb, (*NEON_PINK, 50), (12, 12), 12)
        screen.blit(gb, (int(ball_x) - 12, int(ball_y) - 12))
        pygame.draw.circle(screen, NEON_PINK, (int(ball_x), int(ball_y)), ball_r)

        ps.update()
        ps.draw(screen)
        draw_hud(screen, f"BREAKOUT  Score: {score}")
        ctrl_timer = max(0, ctrl_timer - 1)
        draw_controls_hint(screen, "A/D or Left/Right", ctrl_timer)
        pygame.display.flip()
        clock.tick(FPS)


# ═══════════════════════════════════════════════════════════════════════════════
#  4. SPACE INVADERS  (FIX: store row color per enemy instead of using index)
# ═══════════════════════════════════════════════════════════════════════════════
def run_invaders(screen):
    clock = pygame.time.Clock()
    ps = ParticleSystem()
    ctrl_timer = 3 * FPS

    player_x = float(WIDTH // 2)
    player_y = HEIGHT - 55
    player_speed = 5.5
    bullets = []
    bullet_speed = 8

    enemy_rows, enemy_cols = 5, 9
    enemy_w, enemy_h = 38, 30
    enemy_pad = 12
    colors_e = [NEON_GREEN, LIME, GREEN, TEAL, CYAN]

    def make_enemies():
        enemies = []
        for row in range(enemy_rows):
            for col in range(enemy_cols):
                ex = col * (enemy_w + enemy_pad) + 60
                ey = row * (enemy_h + enemy_pad) + 55
                # FIX: store the row color with each enemy
                ec = colors_e[row % len(colors_e)]
                enemies.append({"rect": pygame.Rect(ex, ey, enemy_w, enemy_h), "color": ec})
        return enemies

    enemies = make_enemies()
    enemy_dx = 2
    enemy_bullets = []
    score = 0
    shoot_cd = 0
    star_scroll = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x = max(25, player_x - player_speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x = min(WIDTH - 25, player_x + player_speed)
        if keys[pygame.K_SPACE] and shoot_cd <= 0:
            bullets.append([player_x, float(player_y - 18)])
            shoot_cd = 12

        shoot_cd -= 1
        star_scroll += 0.5

        bullets = [[bx, by - bullet_speed] for bx, by in bullets if by > 0]
        enemy_bullets = [[bx, by + 5] for bx, by in enemy_bullets if by < HEIGHT]

        move_down = False
        for e in enemies:
            er = e["rect"]
            if er.x + enemy_dx < 5 or er.x + er.width + enemy_dx > WIDTH - 5:
                move_down = True
                break
        if move_down:
            enemy_dx = -enemy_dx
            for e in enemies:
                e["rect"].y += 18
        for e in enemies:
            e["rect"].x += enemy_dx

        if enemies and random.random() < 0.025:
            shooter = random.choice(enemies)
            enemy_bullets.append([float(shooter["rect"].centerx), float(shooter["rect"].bottom)])

        for bullet in bullets[:]:
            br = pygame.Rect(bullet[0] - 3, bullet[1] - 8, 6, 16)
            for enemy in enemies[:]:
                if br.colliderect(enemy["rect"]):
                    ps.explosion(enemy["rect"].centerx, enemy["rect"].centery, NEON_GREEN, 20)
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    score += 25
                    break

        player_rect = pygame.Rect(player_x - 20, player_y - 14, 40, 28)
        hit = False
        for eb in enemy_bullets:
            if player_rect.collidepoint(eb[0], eb[1]):
                hit = True
        for e in enemies:
            if e["rect"].bottom >= player_y - 10:
                hit = True

        if hit:
            ps.explosion(player_x, player_y, CYAN, 50)
            if not game_over_screen(screen, score, ps):
                return
            player_x = float(WIDTH // 2)
            bullets.clear()
            enemy_bullets.clear()
            enemies = make_enemies()
            enemy_dx = 2
            score = 0
            continue

        if not enemies:
            if not win_screen(screen, "WAVE CLEARED!", score, ps):
                return
            enemies = make_enemies()
            enemy_dx = 2
            bullets.clear()
            enemy_bullets.clear()
            continue

        screen.fill(theme["bg"])
        draw_stars(screen, BG_STARS, star_scroll)

        pygame.draw.polygon(screen, CYAN, [
            (player_x, player_y - 18), (player_x - 8, player_y - 5),
            (player_x - 22, player_y + 12), (player_x + 22, player_y + 12),
            (player_x + 8, player_y - 5),
        ])
        pygame.draw.polygon(screen, (100, 220, 255), [
            (player_x, player_y - 12), (player_x - 5, player_y),
            (player_x + 5, player_y),
        ])
        eg = pygame.Surface((16, 10), pygame.SRCALPHA)
        pygame.draw.ellipse(eg, (*ORANGE, 150), eg.get_rect())
        screen.blit(eg, (int(player_x) - 8, player_y + 10))

        t = pygame.time.get_ticks()
        for i, e in enumerate(enemies):
            wobble = math.sin(t * 0.005 + i * 0.3) * 2
            er = e["rect"]
            draw_r = pygame.Rect(er.x, er.y + wobble, er.width, er.height)
            ec = e["color"]
            pygame.draw.rect(screen, ec, draw_r, border_radius=8)
            eye_y = draw_r.y + draw_r.height // 2 - 2
            pygame.draw.circle(screen, WHITE, (draw_r.x + 10, int(eye_y)), 5)
            pygame.draw.circle(screen, WHITE, (draw_r.x + draw_r.width - 10, int(eye_y)), 5)
            pygame.draw.circle(screen, BLACK, (draw_r.x + 11, int(eye_y)), 2)
            pygame.draw.circle(screen, BLACK, (draw_r.x + draw_r.width - 9, int(eye_y)), 2)

        for bx, by in bullets:
            glow_s = pygame.Surface((10, 20), pygame.SRCALPHA)
            pygame.draw.rect(glow_s, (*YELLOW, 80), (0, 0, 10, 20), border_radius=4)
            screen.blit(glow_s, (int(bx) - 5, int(by) - 10))
            pygame.draw.rect(screen, YELLOW, (int(bx) - 2, int(by) - 8, 4, 16), border_radius=2)
        for bx, by in enemy_bullets:
            pygame.draw.rect(screen, RED, (int(bx) - 2, int(by) - 5, 4, 10), border_radius=2)

        ps.update()
        ps.draw(screen)
        draw_hud(screen, f"SPACE INVADERS  Score: {score}")
        ctrl_timer = max(0, ctrl_timer - 1)
        draw_controls_hint(screen, "A/D + SPACE shoot", ctrl_timer)
        pygame.display.flip()
        clock.tick(FPS)


# ═══════════════════════════════════════════════════════════════════════════════
#  5. ASTEROIDS
# ═══════════════════════════════════════════════════════════════════════════════
def run_asteroids(screen):
    clock = pygame.time.Clock()
    ps = ParticleSystem()
    ctrl_timer = 3 * FPS

    ship_x, ship_y = float(WIDTH // 2), float(HEIGHT // 2)
    ship_angle = 0.0
    ship_vx, ship_vy = 0.0, 0.0
    bullets = []
    asteroids_list = []
    score = 0
    shoot_cd = 0

    def spawn_asteroid(size=3, x=None, y=None):
        if x is None:
            side = random.randint(0, 3)
            if side == 0: x, y = random.randint(0, WIDTH), 0
            elif side == 1: x, y = WIDTH, random.randint(0, HEIGHT)
            elif side == 2: x, y = random.randint(0, WIDTH), HEIGHT
            else: x, y = 0, random.randint(0, HEIGHT)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 3)
        radius = size * 14
        verts = []
        num_pts = random.randint(7, 12)
        for i in range(num_pts):
            a = (i / num_pts) * 2 * math.pi
            r = radius * random.uniform(0.7, 1.0)
            verts.append((a, r))
        return {"x": float(x), "y": float(y), "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed, "r": radius, "size": size, "verts": verts,
                "rot": random.uniform(-2, 2)}

    for _ in range(5):
        asteroids_list.append(spawn_asteroid())

    rot_accum = 0.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            ship_angle += 4.5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ship_angle -= 4.5
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            rad = math.radians(ship_angle)
            ship_vx += math.sin(rad) * -0.18
            ship_vy += math.cos(rad) * -0.18
            ta = math.radians(ship_angle + 180)
            ttx = ship_x + math.sin(ta) * -16
            tty = ship_y + math.cos(ta) * -16
            ps.emit(ttx, tty, ORANGE, 2, vx=math.sin(ta) * -2 + random.uniform(-1, 1),
                    vy=math.cos(ta) * -2 + random.uniform(-1, 1), life=12, size=3, gravity=0)
        if keys[pygame.K_SPACE] and shoot_cd <= 0:
            rad = math.radians(ship_angle)
            bullets.append([ship_x, ship_y, math.sin(rad) * -9, math.cos(rad) * -9, 55])
            shoot_cd = 8

        shoot_cd -= 1
        ship_x = (ship_x + ship_vx) % WIDTH
        ship_y = (ship_y + ship_vy) % HEIGHT
        ship_vx *= 0.99
        ship_vy *= 0.99

        new_bullets = []
        for b in bullets:
            b[0] += b[2]
            b[1] += b[3]
            b[4] -= 1
            if b[4] > 0 and -10 <= b[0] <= WIDTH + 10 and -10 <= b[1] <= HEIGHT + 10:
                new_bullets.append(b)
        bullets = new_bullets

        for a in asteroids_list:
            a["x"] = (a["x"] + a["vx"]) % WIDTH
            a["y"] = (a["y"] + a["vy"]) % HEIGHT

        for b in bullets[:]:
            for a in asteroids_list[:]:
                dist = math.hypot(b[0] - a["x"], b[1] - a["y"])
                if dist < a["r"]:
                    if b in bullets:
                        bullets.remove(b)
                    asteroids_list.remove(a)
                    score += (4 - a["size"]) * 50
                    ps.explosion(a["x"], a["y"], LIGHT_GRAY, 20)
                    if a["size"] > 1:
                        for _ in range(2):
                            asteroids_list.append(spawn_asteroid(a["size"] - 1, a["x"], a["y"]))
                    break

        hit = False
        for a in asteroids_list:
            if math.hypot(ship_x - a["x"], ship_y - a["y"]) < a["r"] + 14:
                hit = True

        if hit:
            ps.explosion(ship_x, ship_y, CYAN, 50)
            if not game_over_screen(screen, score, ps):
                return
            ship_x, ship_y = float(WIDTH // 2), float(HEIGHT // 2)
            ship_vx = ship_vy = 0.0
            ship_angle = 0.0
            bullets.clear()
            asteroids_list.clear()
            for _ in range(5):
                asteroids_list.append(spawn_asteroid())
            score = 0
            continue

        if not asteroids_list:
            for _ in range(5 + score // 400):
                asteroids_list.append(spawn_asteroid())

        screen.fill(theme["bg"])
        draw_stars(screen, BG_STARS)

        pts = []
        for angle_off, dist in [(0, 22), (140, 18), (180, 9), (220, 18)]:
            a = math.radians(ship_angle + angle_off)
            pts.append((ship_x + math.sin(a) * -dist, ship_y + math.cos(a) * -dist))
        pygame.draw.polygon(screen, CYAN, pts)
        pygame.draw.polygon(screen, WHITE, pts, 2)

        rot_accum += 0.02
        for a in asteroids_list:
            rot = rot_accum * a["rot"]
            pts = []
            for va, vr in a["verts"]:
                angle = va + rot
                apx = a["x"] + math.cos(angle) * vr
                apy = a["y"] + math.sin(angle) * vr
                pts.append((apx, apy))
            pygame.draw.polygon(screen, (160, 160, 170), pts, 2)

        for b in bullets:
            pygame.draw.circle(screen, YELLOW, (int(b[0]), int(b[1])), 3)
            gbul = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(gbul, (*YELLOW, 60), (5, 5), 5)
            screen.blit(gbul, (int(b[0]) - 5, int(b[1]) - 5))

        ps.update()
        ps.draw(screen)
        draw_hud(screen, f"ASTEROIDS  Score: {score}")
        ctrl_timer = max(0, ctrl_timer - 1)
        draw_controls_hint(screen, "A/D turn  W gas  SPACE shoot", ctrl_timer)
        pygame.display.flip()
        clock.tick(FPS)


# ═══════════════════════════════════════════════════════════════════════════════
#  6. MEMORY MATCH  (FIX: smaller cards so they fit on screen)
# ═══════════════════════════════════════════════════════════════════════════════
def run_memory(screen):
    clock = pygame.time.Clock()
    ps = ParticleSystem()
    ctrl_timer = 3 * FPS
    rows, cols = 4, 6
    total = rows * cols
    card_w, card_h = 90, 100
    pad = 10
    grid_w = cols * (card_w + pad) - pad
    grid_h = rows * (card_h + pad) - pad
    offset_x = (WIDTH - grid_w) // 2
    offset_y = (HEIGHT - grid_h) // 2 + 20

    symbols = list(range(total // 2)) * 2
    random.shuffle(symbols)

    sym_colors = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN, NEON_PINK, NEON_GREEN, NEON_BLUE, GOLD, LIME]
    revealed = [True] * total  # start revealed for preview
    matched = [False] * total
    selected = []
    wait_timer = 0
    moves = 0
    pairs_found = 0
    preview_timer = 10 * FPS  # 10 seconds to memorize

    def draw_symbol(surf, sym, cx, cy):
        c = sym_colors[sym % len(sym_colors)]
        shapes = sym % 6
        if shapes == 0:
            pygame.draw.circle(surf, c, (cx, cy), 22)
            pygame.draw.circle(surf, tuple(min(255, v + 60) for v in c), (cx - 5, cy - 5), 8)
        elif shapes == 1:
            pygame.draw.rect(surf, c, (cx - 18, cy - 18, 36, 36), border_radius=6)
        elif shapes == 2:
            pts = [(cx, cy - 22), (cx - 20, cy + 14), (cx + 20, cy + 14)]
            pygame.draw.polygon(surf, c, pts)
        elif shapes == 3:
            pts = [(cx, cy - 22), (cx + 22, cy), (cx, cy + 22), (cx - 22, cy)]
            pygame.draw.polygon(surf, c, pts)
        elif shapes == 4:
            inner_r, outer_r = 10, 22
            pts = []
            for i in range(10):
                a = math.radians(i * 36 - 90)
                r = outer_r if i % 2 == 0 else inner_r
                pts.append((cx + int(r * math.cos(a)), cy + int(r * math.sin(a))))
            pygame.draw.polygon(surf, c, pts)
        else:
            pts = []
            for i in range(6):
                a = math.radians(i * 60)
                pts.append((cx + int(20 * math.cos(a)), cy + int(20 * math.sin(a))))
            pygame.draw.polygon(surf, c, pts)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and wait_timer <= 0 and preview_timer <= 0:
                mx, my = event.pos
                for i in range(total):
                    row = i // cols
                    col = i % cols
                    cx = offset_x + col * (card_w + pad)
                    cy = offset_y + row * (card_h + pad)
                    if cx <= mx <= cx + card_w and cy <= my <= cy + card_h:
                        if not revealed[i] and not matched[i] and len(selected) < 2:
                            revealed[i] = True
                            selected.append(i)
                            if len(selected) == 2:
                                moves += 1
                                if symbols[selected[0]] == symbols[selected[1]]:
                                    matched[selected[0]] = True
                                    matched[selected[1]] = True
                                    pairs_found += 1
                                    for s_idx in selected:
                                        sr = s_idx // cols
                                        sc = s_idx % cols
                                        spx = offset_x + sc * (card_w + pad) + card_w // 2
                                        spy = offset_y + sr * (card_h + pad) + card_h // 2
                                        ps.sparkle(spx, spy, GOLD, 10)
                                    selected = []
                                else:
                                    wait_timer = 45

        # Preview countdown
        if preview_timer > 0:
            preview_timer -= 1
            if preview_timer == 0:
                revealed = [False] * total

        if wait_timer > 0:
            wait_timer -= 1
            if wait_timer == 0:
                for idx in selected:
                    revealed[idx] = False
                selected = []

        screen.fill(theme["bg"])
        draw_stars(screen, BG_STARS)

        for i in range(total):
            row = i // cols
            col = i % cols
            cx = offset_x + col * (card_w + pad)
            cy = offset_y + row * (card_h + pad)
            rect = pygame.Rect(cx, cy, card_w, card_h)

            if matched[i]:
                pygame.draw.rect(screen, (25, 55, 25), rect, border_radius=12)
                glow = pygame.Surface((card_w + 8, card_h + 8), pygame.SRCALPHA)
                pygame.draw.rect(glow, (*NEON_GREEN, 25), (0, 0, card_w + 8, card_h + 8), border_radius=14)
                screen.blit(glow, (cx - 4, cy - 4))
                draw_symbol(screen, symbols[i], cx + card_w // 2, cy + card_h // 2 - 6)
            elif revealed[i]:
                pygame.draw.rect(screen, (45, 45, 65), rect, border_radius=12)
                pygame.draw.rect(screen, WHITE, rect, 2, border_radius=12)
                draw_symbol(screen, symbols[i], cx + card_w // 2, cy + card_h // 2 - 6)
            else:
                pygame.draw.rect(screen, (40, 60, 140), rect, border_radius=12)
                pygame.draw.rect(screen, (60, 90, 180), rect, 2, border_radius=12)
                ccx, ccy = cx + card_w // 2, cy + card_h // 2
                pygame.draw.polygon(screen, (50, 75, 160), [
                    (ccx, ccy - 16), (ccx + 12, ccy), (ccx, ccy + 16), (ccx - 12, ccy)
                ])
                draw_text(screen, "?", 34, (80, 120, 220), ccx, ccy)

        ps.update()
        ps.draw(screen)

        if preview_timer > 0:
            secs_left = preview_timer // FPS + 1
            draw_panel(screen, (WIDTH // 2 - 160, HEIGHT // 2 - 30, 320, 60), (20, 20, 50), NEON_BLUE, 220, 16)
            draw_text_shadow(screen, f"MEMORIZE!  {secs_left}s", 32, NEON_BLUE, WIDTH // 2, HEIGHT // 2)
            bar_w = 280
            bar_ratio = preview_timer / (10 * FPS)
            draw_rounded_bar(screen, WIDTH // 2 - bar_w // 2, HEIGHT // 2 + 22, bar_w, 10, bar_ratio, (30, 30, 50), NEON_BLUE)

        draw_hud(screen, f"MEMORY MATCH   Moves: {moves}   Pairs: {pairs_found}/{total // 2}")
        ctrl_timer = max(0, ctrl_timer - 1)
        draw_controls_hint(screen, "Mouse click", ctrl_timer)

        if pairs_found == total // 2:
            if not win_screen(screen, "YOU WIN!", moves, ps):
                return
            random.shuffle(symbols)
            revealed = [True] * total
            matched = [False] * total
            selected = []
            moves = 0
            pairs_found = 0
            wait_timer = 0
            preview_timer = 10 * FPS
            continue

        pygame.display.flip()
        clock.tick(FPS)


# ═══════════════════════════════════════════════════════════════════════════════
#  7. DODGE MASTER  (FIX: gentler difficulty curve)
# ═══════════════════════════════════════════════════════════════════════════════
def run_dodge(screen):
    clock = pygame.time.Clock()
    ps = ParticleSystem()
    ctrl_timer = 3 * FPS

    px, py = float(WIDTH // 2), float(HEIGHT - 80)
    speed = 5
    enemies = []
    score = 0
    spawn_timer = 0
    difficulty = 1.0
    trail = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            px = max(15, px - speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            px = min(WIDTH - 15, px + speed)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            py = max(15, py - speed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            py = min(HEIGHT - 15, py + speed)

        trail.append((int(px), int(py)))
        if len(trail) > 20:
            trail.pop(0)

        score += 1
        # FIX: gentler difficulty curve
        difficulty = 1.0 + score / 1500

        spawn_timer += 1
        if spawn_timer >= max(18, int(40 / difficulty)):
            spawn_timer = 0
            side = random.randint(0, 3)
            if side == 0:
                ex, ey = random.randint(0, WIDTH), -20
                evx, evy = random.uniform(-1, 1), random.uniform(2, 3.5) * difficulty
            elif side == 1:
                ex, ey = WIDTH + 20, random.randint(0, HEIGHT)
                evx, evy = random.uniform(-3.5, -2) * difficulty, random.uniform(-1, 1)
            elif side == 2:
                ex, ey = random.randint(0, WIDTH), HEIGHT + 20
                evx, evy = random.uniform(-1, 1), random.uniform(-3.5, -2) * difficulty
            else:
                ex, ey = -20, random.randint(0, HEIGHT)
                evx, evy = random.uniform(2, 3.5) * difficulty, random.uniform(-1, 1)
            size = random.randint(8, 18)
            c = random.choice([RED, ORANGE, NEON_PINK, PURPLE])
            enemies.append([float(ex), float(ey), evx, evy, size, c])

        new_enemies = []
        for e in enemies:
            e[0] += e[2]
            e[1] += e[3]
            if -50 < e[0] < WIDTH + 50 and -50 < e[1] < HEIGHT + 50:
                new_enemies.append(e)
        enemies = new_enemies

        hit = False
        for e in enemies:
            if math.hypot(px - e[0], py - e[1]) < 12 + e[4]:
                hit = True

        if hit:
            ps.explosion(px, py, NEON_GREEN, 60)
            if not game_over_screen(screen, score, ps):
                return
            px, py = float(WIDTH // 2), float(HEIGHT - 80)
            enemies.clear()
            score = 0
            difficulty = 1.0
            spawn_timer = 0
            trail.clear()
            continue

        screen.fill(theme["bg"])
        draw_stars(screen, BG_STARS)

        for i, (tx, ty) in enumerate(trail):
            alpha = int((i / len(trail)) * 100) if trail else 0
            sz = max(1, int((i / max(1, len(trail))) * 10))
            s = pygame.Surface((sz * 2, sz * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*NEON_GREEN, alpha), (sz, sz), sz)
            screen.blit(s, (tx - sz, ty - sz))

        glow = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*NEON_GREEN, 40), (20, 20), 20)
        screen.blit(glow, (int(px) - 20, int(py) - 20))
        pygame.draw.circle(screen, NEON_GREEN, (int(px), int(py)), 12)
        pygame.draw.circle(screen, WHITE, (int(px), int(py)), 6)

        for e in enemies:
            glow_e = pygame.Surface((e[4] * 3, e[4] * 3), pygame.SRCALPHA)
            pygame.draw.circle(glow_e, (*e[5], 30), (e[4] * 3 // 2, e[4] * 3 // 2), e[4] * 3 // 2)
            screen.blit(glow_e, (int(e[0]) - e[4] * 3 // 2, int(e[1]) - e[4] * 3 // 2))
            pygame.draw.circle(screen, e[5], (int(e[0]), int(e[1])), e[4])

        ps.update()
        ps.draw(screen)
        draw_hud(screen, f"DODGE MASTER  Score: {score}")
        ctrl_timer = max(0, ctrl_timer - 1)
        draw_controls_hint(screen, "WASD or Arrows", ctrl_timer)
        pygame.display.flip()
        clock.tick(FPS)


# ═══════════════════════════════════════════════════════════════════════════════
#  8. COLOR CATCH  (FIX: larger target indicator + colored basket border)
# ═══════════════════════════════════════════════════════════════════════════════
def run_color_catch(screen):
    clock = pygame.time.Clock()
    ps = ParticleSystem()
    ctrl_timer = 3 * FPS

    basket_x = float(WIDTH // 2)
    basket_w = 80
    basket_y = HEIGHT - 50
    speed = 7
    score = 0
    lives = 5

    target_color = random.choice([RED, GREEN, BLUE, YELLOW, PURPLE, CYAN])
    orbs = []
    spawn_cd = 0

    all_colors = [RED, GREEN, BLUE, YELLOW, PURPLE, CYAN, ORANGE, NEON_PINK]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            basket_x = max(basket_w // 2, basket_x - speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            basket_x = min(WIDTH - basket_w // 2, basket_x + speed)

        spawn_cd += 1
        if spawn_cd >= 25:
            spawn_cd = 0
            c = random.choice(all_colors)
            ox = random.randint(30, WIDTH - 30)
            orbs.append([float(ox), -15.0, random.uniform(2, 4), c, random.randint(10, 16)])

        new_orbs = []
        for o in orbs:
            o[1] += o[2]
            if o[1] >= basket_y - 10 and abs(o[0] - basket_x) < basket_w // 2 + o[4]:
                if o[3] == target_color:
                    score += 50
                    ps.sparkle(o[0], basket_y, GOLD, 10)
                    if score % 200 == 0:
                        target_color = random.choice(all_colors)
                else:
                    lives -= 1
                    ps.explosion(o[0], basket_y, RED, 10)
                continue
            if o[1] > HEIGHT + 20:
                if o[3] == target_color:
                    lives -= 1
                continue
            new_orbs.append(o)
        orbs = new_orbs

        if lives <= 0:
            if not game_over_screen(screen, score, ps):
                return
            basket_x = float(WIDTH // 2)
            score = 0
            lives = 5
            orbs.clear()
            target_color = random.choice(all_colors)
            continue

        screen.fill(theme["bg"])
        draw_stars(screen, BG_STARS)

        # FIX: larger target indicator with panel
        draw_panel(screen, (WIDTH // 2 - 120, 8, 240, 70), (20, 20, 40), target_color, 200, 16)
        draw_text(screen, "CATCH:", 20, WHITE, WIDTH // 2 - 30, 28)
        pygame.draw.circle(screen, target_color, (WIDTH // 2 + 40, 28), 14)
        glow_t = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(glow_t, (*target_color, 60), (20, 20), 20)
        screen.blit(glow_t, (WIDTH // 2 + 20, 8))
        # Lives display
        for i in range(lives):
            pygame.draw.circle(screen, RED, (WIDTH // 2 - 40 + i * 22, 58), 7)
            pygame.draw.circle(screen, (255, 100, 100), (WIDTH // 2 - 42 + i * 22, 56), 3)

        for o in orbs:
            glow_o = pygame.Surface((o[4] * 3, o[4] * 3), pygame.SRCALPHA)
            pygame.draw.circle(glow_o, (*o[3], 40), (o[4] * 3 // 2, o[4] * 3 // 2), o[4] * 3 // 2)
            screen.blit(glow_o, (int(o[0]) - o[4] * 3 // 2, int(o[1]) - o[4] * 3 // 2))
            pygame.draw.circle(screen, o[3], (int(o[0]), int(o[1])), o[4])

        # FIX: basket with colored border matching target
        bx = int(basket_x)
        pygame.draw.rect(screen, WHITE, (bx - basket_w // 2, basket_y, basket_w, 16), border_radius=8)
        pygame.draw.rect(screen, target_color, (bx - basket_w // 2, basket_y, basket_w, 16), 3, border_radius=8)
        pygame.draw.rect(screen, target_color, (bx - basket_w // 2 + 4, basket_y + 3, basket_w - 8, 10), border_radius=5)
        pygame.draw.line(screen, LIGHT_GRAY, (bx - basket_w // 2, basket_y), (bx - basket_w // 2 + 5, basket_y - 15), 2)
        pygame.draw.line(screen, LIGHT_GRAY, (bx + basket_w // 2, basket_y), (bx + basket_w // 2 - 5, basket_y - 15), 2)

        ps.update()
        ps.draw(screen)
        draw_text_shadow(screen, f"Score: {score}", 28, GOLD, WIDTH // 2, HEIGHT - 20)
        ctrl_timer = max(0, ctrl_timer - 1)
        draw_controls_hint(screen, "A/D or Left/Right", ctrl_timer)
        pygame.display.flip()
        clock.tick(FPS)


# ═══════════════════════════════════════════════════════════════════════════════
#  9. METEOR STORM
# ═══════════════════════════════════════════════════════════════════════════════
def run_meteor(screen):
    clock = pygame.time.Clock()
    ps = ParticleSystem()
    ctrl_timer = 3 * FPS

    ship_x = float(WIDTH // 2)
    ship_y = float(HEIGHT - 70)
    speed = 5
    bullets = []
    meteors = []
    score = 0
    shoot_cd = 0
    powerups = []
    rapid_fire = 0
    star_scroll = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            ship_x = max(20, ship_x - speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            ship_x = min(WIDTH - 20, ship_x + speed)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            ship_y = max(HEIGHT // 2, ship_y - speed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            ship_y = min(HEIGHT - 30, ship_y + speed)

        fire_rate = 4 if rapid_fire > 0 else 10
        if keys[pygame.K_SPACE] and shoot_cd <= 0:
            bullets.append([ship_x, ship_y - 20, 0, -10])
            if rapid_fire > 0:
                bullets.append([ship_x - 10, ship_y - 15, -1, -9])
                bullets.append([ship_x + 10, ship_y - 15, 1, -9])
            shoot_cd = fire_rate

        shoot_cd -= 1
        if rapid_fire > 0:
            rapid_fire -= 1
        star_scroll += 2

        if random.random() < 0.04 + score / 5000:
            mx = random.randint(20, WIDTH - 20)
            sz = random.randint(12, 30)
            mvy = random.uniform(2, 5 + score / 1000)
            mvx = random.uniform(-1, 1)
            meteors.append([float(mx), -30.0, mvx, mvy, sz, random.uniform(-3, 3)])

        if random.random() < 0.003:
            powerups.append([float(random.randint(50, WIDTH - 50)), -20.0, 2.0])

        bullets = [[b[0] + b[2], b[1] + b[3], b[2], b[3]] for b in bullets if b[1] > -10]
        meteors_new = []
        for m in meteors:
            m[0] += m[2]
            m[1] += m[3]
            if m[1] < HEIGHT + 40:
                meteors_new.append(m)
        meteors = meteors_new

        pups_new = []
        for p in powerups:
            p[1] += p[2]
            if p[1] < HEIGHT + 20:
                if math.hypot(ship_x - p[0], ship_y - p[1]) < 25:
                    rapid_fire = 300
                    ps.explosion(p[0], p[1], GOLD, 15)
                else:
                    pups_new.append(p)
        powerups = pups_new

        for b in bullets[:]:
            for m in meteors[:]:
                if math.hypot(b[0] - m[0], b[1] - m[1]) < m[4] + 4:
                    ps.explosion(m[0], m[1], ORANGE, 15)
                    if b in bullets:
                        bullets.remove(b)
                    meteors.remove(m)
                    score += 30
                    break

        hit = False
        for m in meteors:
            if math.hypot(ship_x - m[0], ship_y - m[1]) < m[4] + 15:
                hit = True

        if hit:
            ps.explosion(ship_x, ship_y, CYAN, 60)
            if not game_over_screen(screen, score, ps):
                return
            ship_x, ship_y = float(WIDTH // 2), float(HEIGHT - 70)
            bullets.clear()
            meteors.clear()
            powerups.clear()
            score = 0
            rapid_fire = 0
            continue

        screen.fill((8, 8, 18))
        draw_stars(screen, BG_STARS, star_scroll)

        pygame.draw.polygon(screen, CYAN, [
            (ship_x, ship_y - 20), (ship_x - 18, ship_y + 12),
            (ship_x - 6, ship_y + 6), (ship_x + 6, ship_y + 6),
            (ship_x + 18, ship_y + 12)
        ])
        pygame.draw.polygon(screen, (150, 230, 255), [
            (ship_x, ship_y - 14), (ship_x - 6, ship_y + 4), (ship_x + 6, ship_y + 4)
        ])
        eg = pygame.Surface((20, 12), pygame.SRCALPHA)
        flicker = random.randint(100, 200)
        pygame.draw.ellipse(eg, (255, flicker, 0, 180), eg.get_rect())
        screen.blit(eg, (int(ship_x) - 10, int(ship_y) + 10))

        if rapid_fire > 0:
            rf_glow = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(rf_glow, (*GOLD, 30), (25, 25), 25)
            screen.blit(rf_glow, (int(ship_x) - 25, int(ship_y) - 25))

        for m in meteors:
            ps.emit(m[0], m[1] - m[4] * 0.5, ORANGE, 1,
                    vx=random.uniform(-0.5, 0.5), vy=-1, life=8, size=random.randint(2, 4), gravity=0)
            color_m = (180 + random.randint(0, 50), 80 + random.randint(0, 40), 30)
            pygame.draw.circle(screen, color_m, (int(m[0]), int(m[1])), m[4])
            pygame.draw.circle(screen, (220, 160, 60), (int(m[0]), int(m[1])), m[4], 2)

        for b in bullets:
            pygame.draw.rect(screen, NEON_GREEN, (int(b[0]) - 2, int(b[1]) - 5, 4, 10), border_radius=2)

        for p in powerups:
            t = pygame.time.get_ticks()
            glow_p = pygame.Surface((30, 30), pygame.SRCALPHA)
            pulse = int(abs(math.sin(t * 0.005)) * 60) + 40
            pygame.draw.circle(glow_p, (*GOLD, pulse), (15, 15), 15)
            screen.blit(glow_p, (int(p[0]) - 15, int(p[1]) - 15))
            pygame.draw.circle(screen, GOLD, (int(p[0]), int(p[1])), 8)
            draw_text(screen, "R", 12, BLACK, int(p[0]), int(p[1]))

        ps.update()
        ps.draw(screen)
        draw_hud(screen, f"METEOR STORM  Score: {score}")
        if rapid_fire > 0:
            draw_text(screen, f"RAPID FIRE: {rapid_fire // 60 + 1}s", 18, GOLD, WIDTH // 2, 50)
        ctrl_timer = max(0, ctrl_timer - 1)
        draw_controls_hint(screen, "WASD + SPACE shoot", ctrl_timer)
        pygame.display.flip()
        clock.tick(FPS)


# ═══════════════════════════════════════════════════════════════════════════════
#  10. PLATFORM JUMPER  (FIX: world-space coords, camera only for drawing)
# ═══════════════════════════════════════════════════════════════════════════════
def run_platformer(screen):
    clock = pygame.time.Clock()
    ps = ParticleSystem()
    ctrl_timer = 3 * FPS

    player_w, player_h = 24, 32
    px = float(WIDTH // 2)
    py_w = float(HEIGHT - 100)
    pvx, pvy = 0.0, 0.0
    gravity = 0.5
    jump_power = -10
    on_ground = False
    jumps_left = 2  # double jump
    max_jumps = 2
    score = 0

    # Easier platforms: wider (80-140), spacing 70px
    platforms = [(WIDTH // 2 - 60, HEIGHT - 40, 120, 12)]
    for i in range(60):
        pw = random.randint(80, 140)
        px_plat = random.randint(20, WIDTH - pw - 20)
        py_plat = HEIGHT - 40 - (i + 1) * 70
        platforms.append((px_plat, py_plat, pw, 12))

    camera_y = 0.0
    highest_y = py_w

    coins = []
    for plat in platforms[1:]:
        if random.random() < 0.5:
            coins.append([plat[0] + plat[2] // 2, plat[1] - 25, False])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if (event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP) and jumps_left > 0:
                    pvy = jump_power
                    jumps_left -= 1
                    on_ground = False
                    # Different particles for 2nd jump
                    p_color = CYAN if jumps_left == 0 else WHITE
                    ps.emit(px, py_w + camera_y + player_h, p_color, 5,
                            vx=random.uniform(-2, 2), vy=random.uniform(1, 3),
                            life=10, size=2, gravity=0.1)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            pvx = max(-6, pvx - 0.8)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            pvx = min(6, pvx + 0.8)
        else:
            pvx *= 0.85

        pvy += gravity
        px += pvx
        py_w += pvy

        if px < 0:
            px = 0
        if px > WIDTH - player_w:
            px = WIDTH - player_w

        # Collision in world space
        on_ground = False
        for plat in platforms:
            plat_x, plat_y, plat_w, plat_h = plat
            if (pvy >= 0 and
                px + player_w > plat_x and px < plat_x + plat_w and
                py_w + player_h >= plat_y and py_w + player_h <= plat_y + plat_h + 8):
                py_w = plat_y - player_h
                pvy = 0
                on_ground = True
                jumps_left = max_jumps  # reset double jump

        if py_w < highest_y:
            highest_y = py_w
            score = max(score, int((HEIGHT - 100 - highest_y) // 10))

        # Camera follows player (smooth)
        target_cam = -(py_w - HEIGHT // 3)
        camera_y += (target_cam - camera_y) * 0.1

        # Collect coins (world space)
        for coin in coins:
            if not coin[2]:
                if math.hypot(px + player_w // 2 - coin[0], py_w + player_h // 2 - coin[1]) < 25:
                    coin[2] = True
                    score += 50
                    ps.sparkle(coin[0], coin[1] + camera_y, GOLD, 10)

        # Death check — forgiving threshold
        if py_w > highest_y + HEIGHT + 400:
            if not game_over_screen(screen, score, ps):
                return
            px = float(WIDTH // 2)
            py_w = float(HEIGHT - 100)
            pvx, pvy = 0.0, 0.0
            camera_y = 0.0
            highest_y = py_w
            score = 0
            jumps_left = max_jumps
            for c in coins:
                c[2] = False
            continue

        screen.fill((15, 15, 30))

        # Draw platforms (apply camera for drawing only)
        for plat in platforms:
            plat_x, plat_y, plat_w, plat_h = plat
            sy = plat_y + camera_y
            if -20 < sy < HEIGHT + 20:
                pygame.draw.rect(screen, (60, 140, 60), (plat_x, int(sy), plat_w, plat_h), border_radius=6)
                pygame.draw.rect(screen, (80, 180, 80), (plat_x, int(sy), plat_w, plat_h), 2, border_radius=6)
                for gx in range(plat_x + 5, plat_x + plat_w - 5, 8):
                    gh = random.randint(4, 8)
                    pygame.draw.line(screen, (50, 180, 50), (gx, int(sy)), (gx + random.randint(-3, 3), int(sy) - gh), 1)

        # Draw coins (apply camera)
        for coin in coins:
            if not coin[2]:
                cy_screen = coin[1] + camera_y
                if -20 < cy_screen < HEIGHT + 20:
                    t = pygame.time.get_ticks()
                    bob = math.sin(t * 0.005 + coin[0]) * 3
                    pygame.draw.circle(screen, GOLD, (int(coin[0]), int(cy_screen + bob)), 8)
                    pygame.draw.circle(screen, YELLOW, (int(coin[0]) - 2, int(cy_screen + bob) - 2), 3)

        # Draw player (apply camera for drawing)
        draw_py = py_w + camera_y
        pygame.draw.rect(screen, NEON_BLUE, (int(px), int(draw_py), player_w, player_h), border_radius=6)
        pygame.draw.circle(screen, WHITE, (int(px) + 8, int(draw_py) + 10), 5)
        pygame.draw.circle(screen, WHITE, (int(px) + 18, int(draw_py) + 10), 5)
        eye_dir = 1 if pvx > 0.5 else (-1 if pvx < -0.5 else 0)
        pygame.draw.circle(screen, BLACK, (int(px) + 9 + eye_dir, int(draw_py) + 10), 2)
        pygame.draw.circle(screen, BLACK, (int(px) + 19 + eye_dir, int(draw_py) + 10), 2)
        pygame.draw.arc(screen, BLACK, (int(px) + 7, int(draw_py) + 16, 12, 8), 3.14, 6.28, 2)

        ps.update()
        ps.draw(screen)
        draw_hud(screen, f"PLATFORM JUMPER  Score: {score}")
        # Double jump indicator
        for ji in range(max_jumps):
            jc = NEON_GREEN if ji < jumps_left else (50, 50, 60)
            pygame.draw.circle(screen, jc, (30 + ji * 20, 50), 6)
        ctrl_timer = max(0, ctrl_timer - 1)
        draw_controls_hint(screen, "A/D + SPACE (x2 jump)", ctrl_timer)
        pygame.display.flip()
        clock.tick(FPS)


# ═══════════════════════════════════════════════════════════════════════════════
#  11. TANK BATTLE  (FIX: enemy bullet direction matches facing)
# ═══════════════════════════════════════════════════════════════════════════════
def run_tank(screen):
    clock = pygame.time.Clock()
    ps = ParticleSystem()
    ctrl_timer = 3 * FPS

    tx, ty = float(WIDTH // 2), float(HEIGHT // 2)
    t_angle = 0.0
    t_speed = 0.0
    turret_angle = 0.0
    bullets = []
    enemies = []
    score = 0
    shoot_cd = 0
    max_hp = 5
    player_hp = max_hp
    invincible = 0  # frames of invincibility after taking damage

    def spawn_enemies(count):
        for _ in range(count):
            ex = random.choice([random.randint(20, 100), random.randint(WIDTH - 100, WIDTH - 20)])
            ey = random.choice([random.randint(20, 100), random.randint(HEIGHT - 100, HEIGHT - 20)])
            enemies.append({"x": float(ex), "y": float(ey), "angle": random.uniform(0, 360),
                            "speed": random.uniform(0.5, 1.5), "cd": random.randint(60, 120),
                            "bullets": [], "hp": 3})

    spawn_enemies(5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            t_angle += 3
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            t_angle -= 3
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            t_speed = min(3, t_speed + 0.2)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            t_speed = max(-2, t_speed - 0.2)
        else:
            t_speed *= 0.95

        mx, my = pygame.mouse.get_pos()
        turret_angle = math.degrees(math.atan2(mx - tx, -(my - ty)))

        if (keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]) and shoot_cd <= 0:
            rad = math.radians(turret_angle)
            bvx = math.sin(rad) * 8
            bvy = -math.cos(rad) * 8
            bullets.append([tx, ty, bvx, bvy, 80])
            shoot_cd = 15

        shoot_cd -= 1
        rad = math.radians(t_angle)
        tx += math.sin(rad) * -t_speed
        ty += math.cos(rad) * -t_speed
        tx = max(20, min(WIDTH - 20, tx))
        ty = max(20, min(HEIGHT - 20, ty))

        new_b = []
        for b in bullets:
            b[0] += b[2]
            b[1] += b[3]
            b[4] -= 1
            if b[4] > 0 and 0 <= b[0] <= WIDTH and 0 <= b[1] <= HEIGHT:
                new_b.append(b)
        bullets = new_b

        for e in enemies:
            a_to_player = math.degrees(math.atan2(tx - e["x"], -(ty - e["y"])))
            diff = (a_to_player - e["angle"] + 180) % 360 - 180
            e["angle"] += max(-2, min(2, diff))
            rad_e = math.radians(e["angle"])
            e["x"] += math.sin(rad_e) * -e["speed"]
            e["y"] += math.cos(rad_e) * -e["speed"]
            e["x"] = max(20, min(WIDTH - 20, e["x"]))
            e["y"] = max(20, min(HEIGHT - 20, e["y"]))

            e["cd"] -= 1
            if e["cd"] <= 0:
                e["cd"] = random.randint(60, 120)
                # FIX: shoot toward player, not in facing direction
                aim_rad = math.atan2(tx - e["x"], -(ty - e["y"]))
                ebvx = math.sin(aim_rad) * 5
                ebvy = -math.cos(aim_rad) * 5
                e["bullets"].append([e["x"], e["y"], ebvx, ebvy, 60])

            new_eb = []
            for eb in e["bullets"]:
                eb[0] += eb[2]
                eb[1] += eb[3]
                eb[4] -= 1
                if eb[4] > 0:
                    new_eb.append(eb)
            e["bullets"] = new_eb

        for b in bullets[:]:
            for e in enemies[:]:
                if math.hypot(b[0] - e["x"], b[1] - e["y"]) < 22:
                    e["hp"] -= 1
                    ps.sparkle(b[0], b[1], YELLOW, 5)
                    if b in bullets:
                        bullets.remove(b)
                    if e["hp"] <= 0:
                        ps.explosion(e["x"], e["y"], ORANGE, 30)
                        enemies.remove(e)
                        score += 100
                    break

        if invincible > 0:
            invincible -= 1

        if invincible == 0:
            hit = False
            for e in enemies:
                for eb in e["bullets"][:]:
                    if math.hypot(eb[0] - tx, eb[1] - ty) < 18:
                        hit = True
                        e["bullets"].remove(eb)
                        break
                if math.hypot(e["x"] - tx, e["y"] - ty) < 30:
                    hit = True
            if hit:
                player_hp -= 1
                ps.explosion(tx, ty, RED, 20)
                invincible = 60  # 1 second of invincibility

        if player_hp <= 0:
            ps.explosion(tx, ty, CYAN, 60)
            if not game_over_screen(screen, score, ps):
                return
            tx, ty = float(WIDTH // 2), float(HEIGHT // 2)
            t_angle = 0.0
            t_speed = 0.0
            bullets.clear()
            enemies.clear()
            spawn_enemies(5)
            score = 0
            player_hp = max_hp
            invincible = 0
            continue

        if not enemies:
            score += 200
            spawn_enemies(5 + score // 500)

        screen.fill((25, 30, 20))
        for gx in range(0, WIDTH, 40):
            pygame.draw.line(screen, (35, 40, 30), (gx, 0), (gx, HEIGHT))
        for gy in range(0, HEIGHT, 40):
            pygame.draw.line(screen, (35, 40, 30), (0, gy), (WIDTH, gy))

        # Player tank (blinks when invincible)
        show_tank = invincible == 0 or (invincible // 4) % 2 == 0
        if show_tank:
            body_pts = []
            for ax, ay in [(-14, -18), (14, -18), (14, 18), (-14, 18)]:
                rx = ax * math.cos(math.radians(-t_angle)) - ay * math.sin(math.radians(-t_angle))
                ry = ax * math.sin(math.radians(-t_angle)) + ay * math.cos(math.radians(-t_angle))
                body_pts.append((tx + rx, ty + ry))
            pygame.draw.polygon(screen, (60, 130, 60), body_pts)
            pygame.draw.polygon(screen, (80, 180, 80), body_pts, 2)

            trad = math.radians(turret_angle)
            t_end_x = tx + math.sin(trad) * 24
            t_end_y = ty - math.cos(trad) * 24
            pygame.draw.line(screen, (100, 200, 100), (int(tx), int(ty)), (int(t_end_x), int(t_end_y)), 5)
            pygame.draw.circle(screen, (80, 160, 80), (int(tx), int(ty)), 8)

        for e in enemies:
            ebody = []
            for ax, ay in [(-12, -16), (12, -16), (12, 16), (-12, 16)]:
                rx = ax * math.cos(math.radians(-e["angle"])) - ay * math.sin(math.radians(-e["angle"]))
                ry = ax * math.sin(math.radians(-e["angle"])) + ay * math.cos(math.radians(-e["angle"]))
                ebody.append((e["x"] + rx, e["y"] + ry))
            pygame.draw.polygon(screen, DARK_RED, ebody)
            pygame.draw.polygon(screen, RED, ebody, 2)
            erad = math.radians(e["angle"])
            e_end_x = e["x"] + math.sin(erad) * -20
            e_end_y = e["y"] + math.cos(erad) * -20
            pygame.draw.line(screen, RED, (int(e["x"]), int(e["y"])), (int(e_end_x), int(e_end_y)), 4)
            pygame.draw.circle(screen, DARK_RED, (int(e["x"]), int(e["y"])), 6)
            # HP pips
            for i in range(e["hp"]):
                pygame.draw.rect(screen, RED, (int(e["x"]) - 12 + i * 9, int(e["y"]) - 24, 7, 4), border_radius=2)

            for eb in e["bullets"]:
                pygame.draw.circle(screen, RED, (int(eb[0]), int(eb[1])), 3)

        for b in bullets:
            pygame.draw.circle(screen, NEON_GREEN, (int(b[0]), int(b[1])), 4)
            gbul = pygame.Surface((14, 14), pygame.SRCALPHA)
            pygame.draw.circle(gbul, (*NEON_GREEN, 50), (7, 7), 7)
            screen.blit(gbul, (int(b[0]) - 7, int(b[1]) - 7))

        ps.update()
        ps.draw(screen)
        draw_hud(screen, f"TANK BATTLE  Score: {score}")
        ctrl_timer = max(0, ctrl_timer - 1)
        draw_controls_hint(screen, "WASD + Mouse aim + Click", ctrl_timer)
        # Player HP bar
        hp_bar_w = 160
        draw_panel(screen, (20, 46, hp_bar_w + 70, 24), (15, 15, 25), None, 160, 12)
        draw_text(screen, "HP", 16, WHITE, 40, 58)
        hp_color = NEON_GREEN if player_hp > 2 else (YELLOW if player_hp > 1 else RED)
        draw_rounded_bar(screen, 56, 52, hp_bar_w, 12, player_hp / max_hp, (30, 30, 40), hp_color, (60, 60, 70))
        pygame.display.flip()
        clock.tick(FPS)


# ═══════════════════════════════════════════════════════════════════════════════
#  12. RHYTHM TAP  (FIX: added lives system + game over)
# ═══════════════════════════════════════════════════════════════════════════════
def run_rhythm(screen):
    clock = pygame.time.Clock()
    ps = ParticleSystem()
    ctrl_timer = 3 * FPS

    lanes = 4
    lane_w = 100
    total_w = lanes * lane_w
    start_x = (WIDTH - total_w) // 2
    hit_y = HEIGHT - 80
    lane_colors = [RED, BLUE, GREEN, YELLOW]
    lane_keys = [pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k]
    key_labels = ["D", "F", "J", "K"]

    notes = []
    score = 0
    combo = 0
    max_combo = 0
    spawn_timer = 0
    note_speed = 4
    miss_flash = 0
    lives = 10  # FIX: added lives

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                for i, k in enumerate(lane_keys):
                    if event.key == k:
                        closest = None
                        closest_dist = 999
                        for n in notes:
                            if n[0] == i and not n[2]:
                                dist = abs(n[1] - hit_y)
                                if dist < closest_dist:
                                    closest = n
                                    closest_dist = dist
                        if closest and closest_dist < 40:
                            closest[2] = True
                            if closest_dist < 15:
                                score += 100
                                ps.sparkle(start_x + i * lane_w + lane_w // 2, hit_y, GOLD, 8)
                            elif closest_dist < 30:
                                score += 50
                                ps.sparkle(start_x + i * lane_w + lane_w // 2, hit_y, WHITE, 5)
                            else:
                                score += 25
                            combo += 1
                            max_combo = max(max_combo, combo)
                        else:
                            combo = 0
                            miss_flash = 10
                            lives -= 1  # FIX: lose a life on wrong tap

        spawn_timer += 1
        if spawn_timer >= max(15, 35 - score // 500):
            spawn_timer = 0
            lane = random.randint(0, lanes - 1)
            notes.append([lane, -20.0, False])

        new_notes = []
        for n in notes:
            n[1] += note_speed
            if n[1] > HEIGHT + 20:
                if not n[2]:
                    combo = 0
                    miss_flash = 10
                    lives -= 1  # FIX: lose a life on missed note
            elif n[1] <= HEIGHT + 20:
                new_notes.append(n)
        notes = new_notes

        # FIX: game over when lives run out
        if lives <= 0:
            if not game_over_screen(screen, score, ps):
                return
            notes.clear()
            score = 0
            combo = 0
            max_combo = 0
            spawn_timer = 0
            lives = 10
            miss_flash = 0
            continue

        if miss_flash > 0:
            miss_flash -= 1

        screen.fill((15, 10, 25))

        for i in range(lanes):
            lx = start_x + i * lane_w
            s = pygame.Surface((lane_w, HEIGHT), pygame.SRCALPHA)
            s.fill((30, 30, 50, 100) if i % 2 == 0 else (25, 25, 45, 100))
            screen.blit(s, (lx, 0))
            pygame.draw.line(screen, (50, 50, 70), (lx, 0), (lx, HEIGHT), 1)

        if miss_flash > 0:
            pygame.draw.rect(screen, (100, 20, 20), (start_x, hit_y - 3, total_w, 6), border_radius=3)
        else:
            pygame.draw.rect(screen, (80, 80, 100), (start_x, hit_y - 2, total_w, 4), border_radius=2)

        for i in range(lanes):
            lx = start_x + i * lane_w + lane_w // 2
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[lane_keys[i]]:
                glow = pygame.Surface((lane_w, 30), pygame.SRCALPHA)
                pygame.draw.rect(glow, (*lane_colors[i], 60), (0, 0, lane_w, 30), border_radius=8)
                screen.blit(glow, (start_x + i * lane_w, hit_y - 15))
            pygame.draw.circle(screen, lane_colors[i], (lx, hit_y), 18, 3)
            draw_text(screen, key_labels[i], 20, lane_colors[i], lx, hit_y)

        for n in notes:
            if not n[2]:
                lx = start_x + n[0] * lane_w + lane_w // 2
                c = lane_colors[n[0]]
                glow_n = pygame.Surface((lane_w - 10, 30), pygame.SRCALPHA)
                pygame.draw.rect(glow_n, (*c, 40), (0, 0, lane_w - 10, 30), border_radius=10)
                screen.blit(glow_n, (start_x + n[0] * lane_w + 5, int(n[1]) - 15))
                pygame.draw.rect(screen, c, (start_x + n[0] * lane_w + 10, int(n[1]) - 10, lane_w - 20, 20), border_radius=8)

        ps.update()
        ps.draw(screen)

        draw_hud(screen, f"Score: {score}   Lives: {lives}")
        if combo > 2:
            c = rainbow_color(0)
            draw_text_shadow(screen, f"COMBO x{combo}", 32, c, WIDTH // 2, 60)
        draw_text(screen, f"Best Combo: {max_combo}", 18, LIGHT_GRAY, WIDTH // 2, HEIGHT - 20)
        ctrl_timer = max(0, ctrl_timer - 1)
        draw_controls_hint(screen, "D F J K", ctrl_timer)
        pygame.display.flip()
        clock.tick(FPS)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN MENU  (FIX: centered title using font measurement)
# ═══════════════════════════════════════════════════════════════════════════════
GAMES = [
    ("Pong", NEON_BLUE, run_pong),
    ("Flappy Bird", YELLOW, run_flappy),
    ("Breakout", NEON_PINK, run_breakout),
    ("Space Invaders", CYAN, run_invaders),
    ("Asteroids", LIGHT_GRAY, run_asteroids),
    ("Memory Match", PURPLE, run_memory),
    ("Dodge Master", NEON_GREEN, run_dodge),
    ("Color Catch", GOLD, run_color_catch),
    ("Meteor Storm", ORANGE, run_meteor),
    ("Platform Jump", SKY_BLUE, run_platformer),
    ("Tank Battle", GREEN, run_tank),
    ("Rhythm Tap", NEON_PINK, run_rhythm),
]


def draw_game_icon(screen, name, cx, cy, color):
    if name == "Pong":
        pygame.draw.rect(screen, color, (cx - 22, cy - 12, 5, 24), border_radius=2)
        pygame.draw.rect(screen, color, (cx + 17, cy - 12, 5, 24), border_radius=2)
        pygame.draw.circle(screen, WHITE, (cx, cy), 4)
    elif name == "Flappy Bird":
        pygame.draw.circle(screen, YELLOW, (cx, cy), 12)
        pygame.draw.circle(screen, WHITE, (cx + 5, cy - 4), 4)
        pygame.draw.circle(screen, BLACK, (cx + 6, cy - 4), 2)
        pygame.draw.polygon(screen, ORANGE, [(cx + 12, cy), (cx + 22, cy - 2), (cx + 22, cy + 4)])
    elif name == "Breakout":
        for i in range(3):
            c = [RED, ORANGE, YELLOW][i]
            pygame.draw.rect(screen, c, (cx - 24, cy - 15 + i * 9, 48, 7), border_radius=3)
        pygame.draw.circle(screen, WHITE, (cx, cy + 12), 4)
    elif name == "Space Invaders":
        pygame.draw.polygon(screen, color, [(cx, cy - 15), (cx - 15, cy + 10), (cx + 15, cy + 10)])
        pygame.draw.rect(screen, NEON_GREEN, (cx - 10, cy - 25, 8, 8), border_radius=3)
        pygame.draw.rect(screen, NEON_GREEN, (cx + 2, cy - 25, 8, 8), border_radius=3)
    elif name == "Asteroids":
        pygame.draw.polygon(screen, color, [(cx, cy - 14), (cx - 10, cy + 10), (cx + 10, cy + 10)], 2)
        pygame.draw.circle(screen, LIGHT_GRAY, (cx + 18, cy - 8), 6, 1)
        pygame.draw.circle(screen, LIGHT_GRAY, (cx - 16, cy + 8), 8, 1)
    elif name == "Memory Match":
        pygame.draw.rect(screen, color, (cx - 16, cy - 14, 14, 18), border_radius=4)
        pygame.draw.rect(screen, CYAN, (cx + 2, cy - 14, 14, 18), border_radius=4)
        draw_text(screen, "?", 14, WHITE, cx - 9, cy - 5)
        draw_text(screen, "?", 14, WHITE, cx + 9, cy - 5)
    elif name == "Dodge Master":
        pygame.draw.circle(screen, color, (cx, cy), 8)
        for i in range(4):
            angle = math.radians(i * 90 + 45)
            ex = cx + int(18 * math.cos(angle))
            ey = cy + int(18 * math.sin(angle))
            pygame.draw.circle(screen, RED, (ex, ey), 4)
    elif name == "Color Catch":
        pygame.draw.rect(screen, WHITE, (cx - 15, cy + 5, 30, 8), border_radius=4)
        for i, c in enumerate([RED, BLUE, GREEN]):
            pygame.draw.circle(screen, c, (cx - 12 + i * 12, cy - 10), 5)
    elif name == "Meteor Storm":
        pygame.draw.polygon(screen, CYAN, [(cx, cy - 12), (cx - 10, cy + 8), (cx + 10, cy + 8)])
        pygame.draw.circle(screen, ORANGE, (cx + 14, cy - 8), 7, 2)
        pygame.draw.circle(screen, ORANGE, (cx - 12, cy - 14), 5, 2)
    elif name == "Platform Jump":
        pygame.draw.rect(screen, color, (cx - 6, cy - 10, 12, 16), border_radius=4)
        pygame.draw.rect(screen, GREEN, (cx - 20, cy + 8, 40, 6), border_radius=3)
        pygame.draw.rect(screen, GREEN, (cx - 8, cy - 18, 30, 6), border_radius=3)
    elif name == "Tank Battle":
        pygame.draw.rect(screen, color, (cx - 12, cy - 8, 24, 16), border_radius=4)
        pygame.draw.line(screen, color, (cx, cy), (cx + 20, cy - 10), 3)
        pygame.draw.circle(screen, color, (cx, cy), 5)
    elif name == "Rhythm Tap":
        for i in range(4):
            c = [RED, BLUE, GREEN, YELLOW][i]
            pygame.draw.circle(screen, c, (cx - 18 + i * 12, cy + 8), 5)
        pygame.draw.rect(screen, color, (cx - 8, cy - 14, 6, 16), border_radius=3)
        pygame.draw.rect(screen, color, (cx + 2, cy - 10, 6, 12), border_radius=3)


def intro_screen(screen):
    clock = pygame.time.Clock()
    ps = ParticleSystem()
    start_time = pygame.time.get_ticks()
    duration = 3000

    while pygame.time.get_ticks() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

        t = (pygame.time.get_ticks() - start_time) / duration
        screen.fill(theme["bg"])

        if random.random() < 0.3:
            ps.sparkle(random.randint(0, WIDTH), random.randint(0, HEIGHT), rainbow_color(random.random()), 2)

        ps.update()
        ps.draw(screen)

        alpha = min(255, int(t * 3 * 255))
        logo_surf = pygame.Surface((WIDTH, 200), pygame.SRCALPHA)

        if t > 0.15:
            font_big = pygame.font.SysFont("consolas", 72, bold=True)
            title_text = font_big.render("MINI GAMES", True, (*NEON_BLUE, alpha))
            logo_surf.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))

        if t > 0.35:
            font_med = pygame.font.SysFont("consolas", 56, bold=True)
            arcade_text = font_med.render("ARCADE", True, (*NEON_PINK, alpha))
            logo_surf.blit(arcade_text, (WIDTH // 2 - arcade_text.get_width() // 2, 95))

        screen.blit(logo_surf, (0, HEIGHT // 2 - 150))

        if t > 0.55:
            alpha2 = min(255, int((t - 0.55) * 4 * 255))
            creator_surf = pygame.Surface((400, 50), pygame.SRCALPHA)
            font_cr = pygame.font.SysFont("consolas", 28, bold=True)
            by_text = font_cr.render(f"by {CREATOR}", True, (*GOLD, alpha2))
            creator_surf.blit(by_text, (200 - by_text.get_width() // 2, 10))
            screen.blit(creator_surf, (WIDTH // 2 - 200, HEIGHT // 2 + 30))

        if t > 0.75:
            pulse = int(abs(math.sin(pygame.time.get_ticks() * 0.005)) * 100) + 100
            draw_text(screen, "Press any key to start", 22, (pulse, pulse, pulse), WIDTH // 2, HEIGHT - 60)

        line_progress = min(1.0, t * 2)
        lw = int(WIDTH * 0.6 * line_progress)
        pygame.draw.line(screen, NEON_BLUE, (WIDTH // 2 - lw // 2, HEIGHT // 2 - 68), (WIDTH // 2 + lw // 2, HEIGHT // 2 - 68), 2)
        pygame.draw.line(screen, NEON_PINK, (WIDTH // 2 - lw // 2, HEIGHT // 2 + 75), (WIDTH // 2 + lw // 2, HEIGHT // 2 + 75), 2)

        pygame.display.flip()
        clock.tick(FPS)


def main_menu(screen):
    clock = pygame.time.Clock()
    ps = ParticleSystem()

    btn_w, btn_h = 180, 115
    cols = 4
    pad = 16
    grid_w = cols * btn_w + (cols - 1) * pad
    start_x = (WIDTH - grid_w) // 2
    start_y = 150

    buttons = []
    for i, (name, color, func) in enumerate(GAMES):
        row = i // cols
        col = i % cols
        x = start_x + col * (btn_w + pad)
        y = start_y + row * (btn_h + pad)
        buttons.append((pygame.Rect(x, y, btn_w, btn_h), name, color, func))

    hover_scales = [0.0] * len(buttons)

    # Theme selector pills
    theme_names = list(THEMES.keys())
    theme_pill_w, theme_pill_h = 80, 30
    theme_gap = 12
    total_tw = len(theme_names) * theme_pill_w + (len(theme_names) - 1) * theme_gap
    theme_start_x = (WIDTH - total_tw) // 2
    theme_y = 555
    theme_pills = []
    for i, tn in enumerate(theme_names):
        tx = theme_start_x + i * (theme_pill_w + theme_gap)
        theme_pills.append((pygame.Rect(tx, theme_y, theme_pill_w, theme_pill_h), tn))
    theme_hover = [0.0] * len(theme_pills)

    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, name, color, func in buttons:
                    if rect.collidepoint(mx, my):
                        screen_transition(screen, "out", speed=20)
                        func(screen)
                        screen_transition(screen, "in", speed=20)
                for pill_rect, tn in theme_pills:
                    if pill_rect.collidepoint(mx, my):
                        set_theme(tn)

        screen.fill(theme["bg"])
        draw_stars(screen, BG_STARS)

        if random.random() < 0.1:
            ps.particles.append(Particle(
                random.randint(0, WIDTH), HEIGHT + 10,
                rainbow_color(random.random()),
                vx=random.uniform(-0.5, 0.5), vy=random.uniform(-2, -0.5),
                life=random.randint(40, 80), size=random.randint(1, 3), glow=True
            ))

        ps.update()

        # FIX: title centered using font measurement instead of manual char positioning
        title = "MINI GAMES ARCADE"
        t = pygame.time.get_ticks()
        font_title = pygame.font.SysFont("consolas", 48, bold=True)
        title_w = font_title.size(title)[0]
        char_w = title_w / len(title)
        title_start_x = WIDTH // 2 - title_w // 2

        for i, ch in enumerate(title):
            wave = math.sin(t * 0.003 + i * 0.35) * 8
            c = rainbow_color(i * 0.06)
            cx = int(title_start_x + i * char_w + char_w // 2)
            draw_text(screen, ch, 48, (0, 0, 0), cx + 2, 52 + wave)
            draw_text(screen, ch, 48, c, cx, 50 + wave)

        draw_panel(screen, (WIDTH // 2 - 180, 88, 360, 28), theme["panel"], None, 150, 14)
        draw_text(screen, "Click a game to play  |  ESC to quit", 16, theme["text"], WIDTH // 2, 102)

        for idx, (rect, name, color, func) in enumerate(buttons):
            hovered = rect.collidepoint(mx, my)
            if hovered:
                hover_scales[idx] = min(1.0, hover_scales[idx] + 0.1)
            else:
                hover_scales[idx] = max(0.0, hover_scales[idx] - 0.1)

            hs = hover_scales[idx]
            expand = int(hs * 4)
            draw_rect = rect.inflate(expand * 2, expand * 2)

            bg_alpha = int(40 + hs * 40)
            bg_surf = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(bg_surf, (50, 50, 70, bg_alpha + 50), (0, 0, draw_rect.width, draw_rect.height), border_radius=16)
            screen.blit(bg_surf, draw_rect.topleft)

            border_c = tuple(int(c * (0.4 + hs * 0.6)) for c in color)
            pygame.draw.rect(screen, border_c, draw_rect, 2, border_radius=16)

            if hs > 0:
                glow = pygame.Surface((draw_rect.width + 16, draw_rect.height + 16), pygame.SRCALPHA)
                pygame.draw.rect(glow, (*color, int(20 * hs)), (0, 0, glow.get_width(), glow.get_height()), border_radius=20)
                screen.blit(glow, (draw_rect.x - 8, draw_rect.y - 8))

            draw_game_icon(screen, name, draw_rect.centerx, draw_rect.centery - 18, color)
            text_color = WHITE if hs > 0.3 else LIGHT_GRAY
            draw_text(screen, name, 16, text_color, draw_rect.centerx, draw_rect.bottom - 22)

        ps.draw(screen)

        # ── Theme selector ──
        draw_text(screen, "THEME", 13, (100, 100, 120), WIDTH // 2, theme_y - 12)
        for idx_t, (pill_rect, tn) in enumerate(theme_pills):
            hovered_t = pill_rect.collidepoint(mx, my)
            if hovered_t:
                theme_hover[idx_t] = min(1.0, theme_hover[idx_t] + 0.12)
            else:
                theme_hover[idx_t] = max(0.0, theme_hover[idx_t] - 0.08)
            th = theme_hover[idx_t]
            is_active = (tn == theme_name)

            pill_s = pygame.Surface((pill_rect.width, pill_rect.height), pygame.SRCALPHA)
            tc = THEMES[tn]
            if is_active:
                pygame.draw.rect(pill_s, (*tc["accent1"], 180), (0, 0, pill_rect.width, pill_rect.height), border_radius=15)
            else:
                pygame.draw.rect(pill_s, (*tc["panel"], int(120 + th * 60)), (0, 0, pill_rect.width, pill_rect.height), border_radius=15)
                pygame.draw.rect(pill_s, (*tc["accent1"], int(80 + th * 80)), (0, 0, pill_rect.width, pill_rect.height), 2, border_radius=15)
            screen.blit(pill_s, pill_rect.topleft)

            txt_c = WHITE if is_active else tuple(int(c * (0.6 + th * 0.4)) for c in tc["accent1"])
            draw_text(screen, tn, 14, txt_c, pill_rect.centerx, pill_rect.centery)

            # small color preview dots
            dot_y = pill_rect.bottom + 6
            for di, dk in enumerate(["accent1", "accent2", "gold"]):
                dx = pill_rect.centerx - 10 + di * 10
                pygame.draw.circle(screen, tc[dk], (dx, dot_y), 3)

        draw_panel(screen, (WIDTH // 2 - 130, HEIGHT - 48, 260, 32), theme["panel"], None, 140, 12)
        draw_text(screen, f"Created by {CREATOR}", 18, theme["gold"], WIDTH // 2, HEIGHT - 32)

        pygame.display.flip()
        clock.tick(FPS)


# ═══════════════════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════
def make_window_icon():
    """Generate a 32x32 window icon with a neon gamepad."""
    ico = pygame.Surface((32, 32), pygame.SRCALPHA)
    ico.fill((0, 0, 0, 0))
    # Background
    pygame.draw.rect(ico, (14, 14, 28), (0, 0, 32, 32), border_radius=6)
    pygame.draw.rect(ico, (0, 120, 255, 140), (0, 0, 32, 32), 1, border_radius=6)
    # Controller body
    pygame.draw.rect(ico, (35, 35, 65), (6, 12, 20, 11), border_radius=4)
    # Grips
    pygame.draw.circle(ico, (40, 40, 72), (8, 22), 4)
    pygame.draw.circle(ico, (40, 40, 72), (24, 22), 4)
    # D-pad (left) - blue
    pygame.draw.rect(ico, (0, 150, 255), (9, 15, 5, 1))
    pygame.draw.rect(ico, (0, 150, 255), (11, 13, 1, 5))
    # Buttons (right) - colored
    pygame.draw.circle(ico, (255, 50, 150), (22, 14), 2)  # pink
    pygame.draw.circle(ico, (0, 255, 100), (25, 17), 2)    # green
    pygame.draw.circle(ico, (255, 215, 0), (19, 17), 2)    # gold
    pygame.draw.circle(ico, (0, 150, 255), (22, 20), 2)    # blue
    # Stars
    for pos in [(5, 4), (16, 3), (27, 5), (10, 7), (23, 6)]:
        ico.set_at(pos, (255, 255, 255, 200))
    return ico

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_icon(make_window_icon())
    pygame.display.set_caption(f"Mini Games Arcade - by {CREATOR}")
    intro_screen(screen)
    main_menu(screen)
