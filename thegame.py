import pygame
import gamemodule
import _thread
import random

pygame.init()

startup_operations = gamemodule.Stack()
game_operations = gamemodule.Stack()
shutdown_operations = gamemodule.Stack()

game_entities = gamemodule.Stack()
game_events = gamemodule.Stack()
game_log = gamemodule.GameLog('PokaPoka')

ww, wh = 1000, 750
wd = (ww, wh)
screen = pygame.display.set_mode((ww, wh), pygame.FULLSCREEN)

mouse = gamemodule.Mouse()
clock = pygame.time.Clock()

healthgauge = gamemodule.Gauge(100, 0, 100, w=400, h=30, colour=(0, 255, 255), spawn=(screen.get_width() - 450, 10))
staminagauge = gamemodule.Gauge(100, 0, 100, w=400, h=30, colour=(255, 150, 255), spawn=(screen.get_width() - 450, 60))

#healthgauge2 = gamemodule.Gauge(100, 0, 100, w=400, h=30, colour=(255, 0, 0), spawn=(screen.get_width() - 450, 110))
#staminagauge2 = gamemodule.Gauge(100, 0, 100, w=400, h=30, colour=(210, 185, 25), spawn=(screen.get_width() - 450, 160))

game = gamemodule.Game(None, screen, game_operations, game_entities, game_events, shutdown_operations, startup_operations, game_log, mouse, clock)

player = gamemodule.Player(game, healthgauge, staminagauge)
player.character = gamemodule.PlayerCharacterEntity(game, (ww/2 + 100, wh - 100), (50, 50), (255, 255, 255))
game.player = player

#player2 = gamemodule.Player(game, healthgauge2, staminagauge2)
#player2.character = gamemodule.PlayerCharacter2Entity(game, (ww/2 - 100, wh - 100), (50, 50), (255, 255, 0))
#game.player2 = player2

game_entities.push(player.hotbar)
game.owh = game.wh - 50

for i in range(int(player.hotbar.amount)):

    if random.randint(1, 2) == 2:

        player.hotbar.slots[i] = gamemodule.PlayerCharacterEntity(game, (ww/2, wh/2), (50, 50), gamemodule.random_rgb())

    else:

        player.hotbar.slots[i] = gamemodule.NonCurrentPlayerCharacterEntity(game, (ww/2, wh/2), (50, 50), gamemodule.random_rgb())

game.conditions['hitboxes'] = False
game.conditions['gravity'] = True

entity_pickupable = (
    gamemodule.PlayerCharacterEntity, gamemodule.NonCurrentPlayerCharacterEntity,
    gamemodule.Enemy, gamemodule.PortalBlock)

def finish():

    for op in shutdown_operations:

        game_log.push(f'Running shutdown operation {op}')

        op.exec()

    game_log.push('Shutting down (2nd to last) final!')

    game_log.export(folder='gamelogs')

    quit()


def main_loop():

    #  game_log.push('Filled screen')
    #  No need to push to log?

    screen.fill((0, 0, 0))

@game_events.push
@gamemodule.GameOperation.s()
def key_events():

    keys = pygame.key.get_pressed()
    mods = pygame.key.get_mods()

    # Check key events in entities

    for entity in game_entities:

        for key, prop in entity.__dict__.items():

            if key.startswith('keypress_') and len(key) >= 9:

                if keys[pygame.key.key_code(key[9:])]:

                    prop()

    #  Left key

    if mouse.grabbed is None:

        if mouse.leftdown():

            for entity in game_entities:

                if (isinstance(entity, entity_pickupable)) and entity.collidepos(mouse.pos):

                    mouse.grabbed = entity

                    break

    else:

        if mouse.leftdown():

            mouse.grabbed.do_gravity = False
            mouse.grabbed.do_jump = False
            mouse.grabbed.change_pos(mouse.pos)

        else:

            # Check hotbar

            grabbed = mouse.grabbed

            c, x, y, w, h = player.hotbar.modular_traits()

            touched_hotbar = False

            for slot, val in player.hotbar.slots.items():

                r = pygame.Rect(((x + (w * slot)), y, w, h))

                if r.collidepoint(mouse.pos):

                    touched_hotbar = True

                    if player.hotbar.slots[slot] is None:

                        player.hotbar.slots[slot] = grabbed
                        game.mouse.grabbed = None

                        game_log.push(f'Item {grabbed} interacted with hotbar slot({slot}) --> added to inventory')
                        game_entities.remove(grabbed)

                        break

                    else:

                        curr = player.hotbar.slots[slot]
                        #  Need to handle overflow
                        player.hotbar.slots[slot] = grabbed

                        s = None

                        for k, v in player.hotbar.slots.copy().items():

                            if v is None:

                                s = k

                                break

                        if s is None:

                            # Handle having full hotbar

                            curr.change_pos(y=50, x=game.ww-int(game.ww*0.1))
                            game_entities.push(curr)
                            player.hotbar.slots[slot] = grabbed
                            game_entities.remove(grabbed)
                            game_log.push(f'Item {grabbed} interacted with hotbar slot({slot}) resulting in overflow --> Dropped item {curr}')

                            break

                        else:

                            player.hotbar.slots[k] = curr
                            game.mouse.grabbed = None

                            game_log.push(f'Item {grabbed} interacted with hotbar slot({slot}) --> added to inventory')
                            game_log.push(f'Overflow item {curr} interacted with hotbar slot({k}) --> added to inventory')

                            game_entities.remove(grabbed)

                            break

                    break


            if not touched_hotbar:

                mouse.grabbed.do_gravity = True
                mouse.grabbed.do_jump = True
                mouse.grabbed = None

    # Check general key events

    if keys[pygame.K_ESCAPE]:

        game_log.push('Attempted to QUIT @ Esc key')

        finish()

    # Binary and for mods

@game_events.push
@gamemodule.GameOperation.s()
def main_events():

    py_events = pygame.event.get()

    keys = pygame.key.get_pressed()
    mods = pygame.key.get_mods()

    for py_event in py_events:

        if py_event.type == pygame.QUIT:

            game_log.push('Attempted to QUIT')

            finish()

        if py_event.type == pygame.KEYDOWN:

            # If changing gravity

            if py_event.key == pygame.K_g and mods & pygame.KMOD_SHIFT and mods & pygame.KMOD_ALT:

                if game.get_condition('gravity'):

                    game.set_condition('gravity', False)

                    game_log.push('Toggled gravity --> False')

                else:

                    game.set_condition('gravity', True)

                    game_log.push('Toggled gravity --> True')

            elif py_event.key == pygame.K_h and mods & pygame.KMOD_SHIFT and mods & pygame.KMOD_ALT:

                if game.get_condition('hitboxes'):

                    game.set_condition('hitboxes', False)

                    game_log.push('Toggled hitboxes --> False')

                else:

                    game.set_condition('hitboxes', True)

                    game_log.push('Toggled hitboxes --> True')

            elif py_event.key == pygame.K_d and mods & pygame.KMOD_CTRL and mods & pygame.KMOD_ALT:

                if game.get_condition('developergui'):

                    game.set_condition('developergui', False)

                    game_log.push('Toggled developergui --> False')

                else:

                    game.set_condition('developergui', True)

                    game_log.push('Toggled developergui --> True')

def entities():

    for entity in game.entities.list:

        if isinstance(entity, (
                gamemodule.PlayerCharacterEntity, gamemodule.NonCurrentPlayerCharacterEntity,
                gamemodule.Hotbar,
                gamemodule.Enemy,
                gamemodule.PortalBlock)):

            entity.move()
            entity.frame()
            entity.draw(screen)

    for entity in game.entities.list:

        if type(entity) in (gamemodule.GasEntity, ):

            entity.frame()
            entity.draw(screen)

    for entity in game.entities.list:

        if game.get_condition('hitboxes'):

            entity.draw_hitbox(screen)

        elif game.get_condition('hitboxes_x'):

            pygame.draw.rect(screen, (0, 255, 0), (entity.rect), 2)

@game_operations.push
@gamemodule.GameOperation.s()
def justify_entities():

    for entity in game_entities:

        if ((-1 - entity.w) > entity.x > ww) or ((-1 - entity.h) > entity.y > wh):

            game_log.push(f'Removed entity {entity} @ entity position justification')

            game_entities.remove(entity)

# STARTING THE GAME HERE

game_log.push('Beginning game startup and startup-finish')

for op in startup_operations:

    op.exec()

game_loops = 0

game_entities.push(player.character)
#game_entities.push(player2.character)

#for i in range(5):

#    turret = gamemodule.InfernoTurret(game, (i * (50 * 7), game.wh-50), (50, 50), (210, 185, 25))
#    game.entities.push(turret)

turret = gamemodule.InfernoTurret(game, (game.ww/2, game.wh-50), (50, 50), (210, 185, 25))
game.entities.push(turret)

sentinel = gamemodule.SentinelTurret(game, (game.ww/2, game.wh/2), (50, 50), (210, 185, 25))
game.entities.push(sentinel)

portal1, portal2 = gamemodule.create_portal_pair(
    game,
    (game.ww/2-300, game.wh-50), (game.ww/2+300, game.wh-50),
    (50, 50), (50, 50),
    (255, 255, 0), (0, 255, 255))

game.entities.push(portal1)
game.entities.push(portal2)

# Main loop
while True:

    game_loops += 1

    main_loop()

    #  game_log.push(f'Beginning game loop {game_loops}')
    #  Events

    for event in game.events:

        event.exec()

    # Extra Loop Operations

    for operation in game.operations:

        operation.exec()

    for operation in game.player.operations:

        operation.exec()

    if game.get_condition('developergui'):

        # Game Conditions

        gamemodule.draw_text(screen, f'game.fps: {str(int(clock.get_fps()))}', (game.ww - 250, 200), bold=1, size=18)
        gamemodule.draw_text(screen, f'game.gravity: {game.get_condition("gravity")}', (game.ww - 250, 240), bold=1, size=18)
        gamemodule.draw_text(screen, f'game.entities: {len(game.entities.list)}', (game.ww - 250, 290), bold=1, size=18)
        gamemodule.draw_text(screen, f'game.events: {len(game.events.list)}', (game.ww - 250, 340), bold=1, size=18)
        #  gamemodule.draw_text(screen, f'game.log.latest: {game.log.__log__[-1]}', (0, game.wh + 10), bold=1, size=18)
        # ^ Game log in game

        # Player Conditions

        gamemodule.draw_text(screen, f'player.x: {player.character.x}, player.y: {player.character.y}', (game.ww - 250, 390), bold=1, size=18)
        gamemodule.draw_text(screen, f'player.grounded: {player.character.grounded}', (game.ww - 250, 440), bold=1, size=18)
        gamemodule.draw_text(screen, f'player.falling: {player.character.falling}', (game.ww - 250, 490), bold=1, size=18)

    if not game.get_condition('developergui') and game.get_condition('fps'):

        gamemodule.draw_text(screen, f'game.fps: {str(int(clock.get_fps()))}', (game.ww - 250, 200), bold=1, size=18)

    entities()

    player.healthgauge.refill()
    player.staminagauge.refill()
    player.healthgauge.draw(screen)
    player.staminagauge.draw(screen)

    # Player 2
    #player2.character.draw(screen)  # Make sure player is drawn

    #player2.healthgauge.refill()
    #player2.staminagauge.refill()
    #player2.healthgauge.draw(screen)
    #player2.staminagauge.draw(screen)

    pygame.display.update()
    clock.tick(60)
    #  game_log.push(f'Completed game loop {game_loops}')

finish()