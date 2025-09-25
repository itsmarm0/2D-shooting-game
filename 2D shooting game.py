import pygame
import random
import time

# تنظیمات اولیه بازی
pygame.init()

# تنظیمات صفحه بازی
WIDTH, HEIGHT = 1149, 648
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Shooting Game")

# بارگذاری تصاویر
player_image = pygame.image.load('player.png').convert_alpha()
enemy_image = pygame.image.load('enemy.png').convert_alpha()
army_image = pygame.image.load('army.png').convert_alpha()
background_image = pygame.image.load('background.png').convert()

# بارگذاری تصاویر قلب و سکه
heart_image = pygame.image.load('heart.png').convert_alpha()
coin_image = pygame.image.load('coin.png').convert_alpha()

# تغییر اندازه تصاویر
player_image = pygame.transform.scale(player_image, (150, 150))  # اندازه بازیکن
enemy_image = pygame.transform.scale(enemy_image, (100, 100))    # اندازه دشمنان
army_image = pygame.transform.scale(army_image, (100, 100))

# تغییر اندازه تصاویر قلب و سکه
heart_image = pygame.transform.scale(heart_image, (40, 40))
coin_image = pygame.transform.scale(coin_image, (40, 40))

# بارگذاری صدای شلیک
shoot_sound = pygame.mixer.Sound('shoot.wav')

# رنگ‌ها
WHITE = (255, 255, 255)

# سرعت اولیه دشمنان
enemy_speed_increment = 0.1  # شروع با سرعت کم

# کلاس بازیکن
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image  # استفاده از تصویر بازیکن
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 150)
        self.speed = 5
        self.lives = 5  # تعداد جان‌های بازیکن
        self.velocity = 0  # سرعت فعلی بازیکن
        self.acceleration = 0.2  # شتاب حرکت بازیکن
        self.deceleration = 0.3  # توقف تدریجی

    def update(self):
        keys = pygame.key.get_pressed()
        
        # بهبود حرکت: شتاب و توقف تدریجی
        if keys[pygame.K_LEFT]:
            self.velocity -= self.acceleration
        elif keys[pygame.K_RIGHT]:
            self.velocity += self.acceleration
        else:
            if self.velocity > 0:
                self.velocity -= self.deceleration
            elif self.velocity < 0:
                self.velocity += self.deceleration
        # محدودیت سرعت
        self.velocity = max(-self.speed, min(self.speed, self.velocity))
        
        # حرکت بازیکن
        self.rect.x += self.velocity
        
        # جلوگیری از خروج از صفحه
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.velocity = 0

    def shoot(self):
        # پخش صدای شلیک دو بار
        shoot_sound.play()
        pygame.time.delay(100)  # تاخیر کوتاه بین پخش دو صدا
        shoot_sound.play()
        # ایجاد گلوله
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.add(bullet)
        all_sprites.add(bullet)
        
# کلاس دشمن
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image  # استفاده از تصویر دشمن
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.base_speed = random.uniform(0.2, 0.5)  # سرعت پایه دشمنان

    def update(self):
        self.rect.y += self.base_speed + enemy_speed_increment  # اعمال سرعت افزایشی به سرعت پایه
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.base_speed = random.uniform(0.2, 0.5)  # تنظیم سرعت پایه

# کلاس Army (افزایش جان بازیکن)
class Army(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = army_image  # استفاده از تصویر army
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.uniform(0.2, 0.7)  # سرعت Army بسیار آهسته‌تر از enemy

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            player.lives += 1  # اضافه کردن یک جان به بازیکن
            self.kill()  # حذف Army از بازی

# کلاس گلوله
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 255, 0))  # زرد برای گلوله
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -7
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# ایجاد گروه‌های اسپریت
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
armies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# تنظیمات دشمنان
ENEMY_SPAWN_TIME = 5000  # هر 1.5 ثانیه یک دشمن جدید اضافه شود
ARMY_SPAWN_TIME = 10000  # زمان تولید Army هر 10 ثانیه
last_enemy_spawn_time = pygame.time.get_ticks()
last_army_spawn_time = pygame.time.get_ticks()

# تعریف تعداد سکه‌ها
coins = 0

# تابع برای نمایش تعداد جان‌ها
font = pygame.font.SysFont(None, 36)
def draw_lives(surface, x, y, lives):
    # نمایش تصویر قلب
    surface.blit(heart_image, (x, y))
    # نمایش متن تعداد جان‌ها کنار قلب
    text = font.render(f' {lives}', True, WHITE)
    surface.blit(text, (x + 35, y))  # قرار دادن متن کنار تصویر قلب


# تابع برای نمایش تعداد سکه‌ها
def draw_coins(surface, x, y, coins):
    # نمایش تصویر سکه
    surface.blit(coin_image, (x, y))
    # نمایش متن تعداد سکه‌ها کنار سکه
    text = font.render(f' {coins}', True, WHITE)
    surface.blit(text, (x + 35, y))  # قرار دادن متن کنار تصویر سکه   


# حلقه اصلی بازی
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # بررسی فشردن کلید space برای شلیک
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        player.shoot()

    # افزایش یا کاهش سرعت دشمنان با کلیدهای + و -
    if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:  # کلید + برای افزایش سرعت
        enemy_speed_increment += 0.05
    if keys[pygame.K_MINUS]:  # کلید - برای کاهش سرعت
        enemy_speed_increment = max(0, enemy_speed_increment - 0.05)  # جلوگیری از منفی شدن سرعت

    # به‌روزرسانی اسپریت‌ها
    all_sprites.update()

    # تولید دشمنان با تاخیر
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn_time > ENEMY_SPAWN_TIME:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        last_enemy_spawn_time = current_time

    # تولید Army با تاخیر
    if current_time - last_army_spawn_time > ARMY_SPAWN_TIME:
        army = Army()
        all_sprites.add(army)
        armies.add(army)
        last_army_spawn_time = current_time

    # برخورد بین گلوله و دشمن
    hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
    if hits:
        coins += 100  # با کشتن هر دشمن 100 سکه اضافه می‌شود
    
    # برخورد دشمن با بازیکن
    hits = pygame.sprite.spritecollide(player, enemies, True)
    if hits:
        player.lives -= 1  # کاهش جان بازیکن
        if player.lives == 0:
            running = False  # پایان بازی وقتی جان تمام شود

    # رسم عناصر بازی
    screen.blit(background_image, (0, 0))  # رسم پس‌زمینه
    all_sprites.draw(screen)  # رسم همه اسپریت‌ها روی صفحه
    draw_lives(screen, 10, 10, player.lives)  # نمایش تعداد جان‌ها
    draw_coins(screen, 10, 50, coins)  # نمایش تعداد سکه‌ها

    pygame.display.flip()

    # تاخیر برای کاهش سرعت حلقه بازی
    pygame.time.delay(10)

pygame.quit()
