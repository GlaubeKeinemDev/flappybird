from Objects import *

# SCHWIERIGKEIT EINSTELLEN
# Erhöht die allgemeine Geschwindigkeit des Spiels
game_ticks = 120
# Vogel Anziehung nach unten (Wie viele Pixel pro Game tick nach unten)
bird_gravity = 1
# Definiert den Mindestabstand zwischen den Röhren in Pixeln
tube_min_distance = 250
# Definiert den Abstand zwischen untere Röhre und obere Röhre
tube_gap = 200
# SCHWIERIGKEIT-EINSTELLUNGEN ENDE



# Game width und height festlegen
width = 400
height = 600

# Pygame initialisieren, Höhe, Breite & Title setzen
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("FlappyHappy")

# Background image laden
background_image = pygame.image.load("assets/background.png").convert_alpha()

# Roll Animation (Boden) image laden, speed und start x wert definieren
roll_animation_image = pygame.image.load("assets/ground.png").convert_alpha()
roll_animation_speed = 4
roll_animation_x = 0

# Vogel initialisieren, Width, height, Gamewidth, Gameheight, gravity (pro tick wie viele pixel nach unten)
# und jumpheight definieren (bei jump x pixel nach oben)
bird = Bird(70, 50, width, height, bird_gravity, 10)

# Sprite Liste definieren und bird adden, seperate Liste mit allen Röhren
all_sprites = pygame.sprite.Group()
all_sprites.add(bird)
tubes = pygame.sprite.Group()
lastTube = None

# Restart Button/image laden
restart_image = pygame.transform.scale(pygame.image.load("assets/start-button.png").convert_alpha(), (200, 70))
restart_image_rect = restart_image.get_rect()
restart_image_rect.center = (width // 2, height // 2)

# Spielstadien definieren, pygame Clock getten
running = True
clock = pygame.time.Clock()
gamestate = GameState.PRE_GAME

# Score definieren (game width, abstand zwischen Zahlen) und allen Sprites (Entities) hinzufügen
score = Score(width, 10)
all_sprites.add(score)

# Genereller Gameloop
while running:
    try:
        # Game ticks limitieren
        clock.tick(game_ticks)

        # Tastatureingaben prüfen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if gamestate == GameState.PRE_GAME:
                        gamestate = GameState.RUNNING
                        bird.jump()
                    elif gamestate == GameState.RUNNING:
                        bird.jump()
                    elif gamestate == GameState.END:
                        gamestate = GameState.PRE_GAME
                        bird.reset()
                        score.reset()
                        lastTube = None
                        all_sprites = pygame.sprite.Group()
                        all_sprites.add(score)
                        all_sprites.add(bird)
                        tubes = pygame.sprite.Group()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_image_rect.collidepoint(event.pos):
                    gamestate = GameState.PRE_GAME
                    bird.reset()
                    score.reset()
                    lastTube = None
                    all_sprites = pygame.sprite.Group()
                    all_sprites.add(score)
                    all_sprites.add(bird)
                    tubes = pygame.sprite.Group()

        # Rollanimation am Boden anzeigen
        screen.blit(roll_animation_image, (0 - roll_animation_x, background_image.get_height()))
        screen.blit(roll_animation_image, (width - roll_animation_x, background_image.get_height()))
        # Background image anzeigen (Himmel)
        screen.blit(background_image, (0, 0))

        if gamestate == GameState.RUNNING:
            tube_x = width + random.randint(width, width + 300)

            if lastTube is not None:
                tube_x = lastTube.rect.x + random.randint(tube_min_distance, width)

            tube = Tube(tube_x, height, 3, tube_gap)
            tubes.add(tube)
            tubes.add(tube.get_upper_part())
            all_sprites.add(tube)
            all_sprites.add(tube.get_upper_part())
            lastTube = tube

            # Wenn Vogel mit Pipes kollidiert Spiel beenden
            if pygame.sprite.spritecollide(bird, tubes, False):
                gamestate = GameState.END

            # wenn Vogel am Boden angekommen Game beenden
            if bird.rect.y + bird.image.get_height() + bird.velocity >= background_image.get_height():
                gamestate = GameState.END

            # Scoring | Tube aus liste entfernen wenn bereits bepunktet, zusätzlich upper part da eigene Klasse entfernen
            for tube in tubes:
                if not(isinstance(tube, UpperTube)) and bird.rect.x > tube.rect.x:
                    tubes.remove(tube.upper_part)
                    tubes.remove(tube)
                    score.increase()

        # Roll animation (boden) anhalten bei end
        if gamestate != GameState.END:
            roll_animation_x += roll_animation_speed

            if roll_animation_x >= width:
                roll_animation_x = 0

        # Vogel bis zum Boden fliegen lassen bei End | Restart Button anzeigen
        if gamestate == GameState.END:
            if bird.rect.y + bird.image.get_height() + bird.velocity < background_image.get_height():
                bird.update()
            else:
                bottom_playzone_difference = background_image.get_height() - (bird.rect.y + bird.image.get_height())
                if bottom_playzone_difference > 0:
                    bird.fine_update(bottom_playzone_difference)

        # im Pregame Fluganimation machen, ingame nicht
        if gamestate == GameState.PRE_GAME:
            bird.pre_update()
        elif gamestate == GameState.RUNNING:
            all_sprites.update()

        # Score updaten - Score + Bird am ende der liste hinzufügen damit über tubes angezeigt.
        score.update()
        all_sprites.remove(bird)
        all_sprites.add(bird)
        all_sprites.remove(score)
        all_sprites.add(score)
        all_sprites.draw(screen)

        # Restart bild als letztes zeigen, da über allen Elementen
        if gamestate == GameState.END:
            screen.blit(restart_image, restart_image_rect)

        # Display aktualisieren - Inhalt anzeigen
        pygame.display.flip()
    except KeyboardInterrupt:
        running = False
        pygame.quit()

pygame.quit()
