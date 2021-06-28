import pygame
from datetime import datetime
from gamemodule.utl.util import draw_text
import json
from _thread import start_new_thread
import tkinter
from tkinter import filedialog
from gamemodule.entity.playercharacter import PlayerCharacterEntity

pygame.init()

def now():

    return datetime.now()

dark_grey = (51, 51, 51)

class GridBlock(PlayerCharacterEntity):

    def __repr__(self):

        return f"""GridBlock[x:{self.x},y:{self.y},rgb:{self.c}]"""

    def __init__(self, size, x, y, unset=True, colour=dark_grey, margin=1, game=None):

        super().__init__(game, (x, y), size, colour)

        self.w, self.h, self.x, self.y = *size, x, y
        self.c = colour
        self.margin = margin
        self.unset = unset
        self.metadata = {}

    @property
    def rect(self):

        return pygame.rect.Rect(self.x, self.y, self.w, self.h)

    def draw(self, screen, x=None, y=None):

        if self.margin:

            pygame.draw.rect(screen, self.c, (self.x if x is None else x, self.y if y is None else y, self.w, self.h), self.margin)

        else:

            pygame.draw.rect(screen, self.c, (self.x if x is None else x, self.y if y is None else y, self.w, self.h))

        if 'displayname' in self.metadata:

            draw_text(screen, self.metadata['displayname'], (self.x + 2 if x is None else x + 2, self.y + (self.h/3)-1 if y is None else y + (self.h/3)-1), size=10, colour=(0, 0, 0))

    def copy(self):

        return GridBlock((self.w, self.h), self.x, self.y, self.unset, self.c, self.margin)

    def json(self):

        r, g, b = self.c

        return {'type': 'block', 'x': self.x, 'y': self.y, 'w': self.w, 'h': self.h, 'r': r, 'g': g, 'b': b, 'unset': self.unset, 'margin': self.margin if self.margin else False, 'metadata': self.metadata}

class Grid:

    def __getitem__(self, item):

        return self.gridblocks[item]

    def __init__(self, gnw, gnh, ww, wh, x, y):

        self.gnw, self.gnh, self.ww, self.wh = gnw, gnh, ww, wh
        self.x, self.y = x, y

        self.rows = int(self.wh / self.gnh)
        self.columns = int(self.ww / self.gnw)

        self.gridblocks = []

        [[self.gridblocks.append(GridBlock((self.gnw, self.gnh), (x*self.gnw)+self.x, (y*self.gnh)+self.y)) for x in range(self.columns)] for y in range(self.rows)]

    def draw(self, screen):

        for block in self.gridblocks:

            if block:

                block.draw(screen)

def export_grid(expgrid, filename):

    global latest_message

    gridblocks = []

    for block in expgrid.gridblocks:

        if block:

            gridblocks.append(block.json())

    open(filename, 'w').write(json.dumps({'grid': gridblocks, 'filetype': 'blockgridjson'}))

    latest_message = f'Finished save to file: {filename}'

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
grid = Grid(50, 50, screen.get_width() - 40, screen.get_height() - 100, 30, 10)
hotbar = Grid(50, 50, screen.get_width() - 40, 50, 30, screen.get_height() - 100)

# Player

hotbar[0].c = (255, 255, 255)
hotbar[0].margin = None
hotbar[0].metadata['displayname'] = hotbar[0].metadata['blocktype'] = 'playable'

hotbar[1].c = (255, 85, 255)
hotbar[1].margin = None
hotbar[1].metadata['displayname'] = hotbar[1].metadata['blocktype'] = 'portalin'

hotbar[2].c = (255, 85, 0)
hotbar[2].margin = None
hotbar[2].metadata['displayname'] = hotbar[2].metadata['blocktype'] = 'portalout'

mouse = pygame.mouse
mouse_block = None
latest_message = ''

while True:

    screen.fill((0, 0, 0))

    grid.draw(screen)
    hotbar.draw(screen)

    events = pygame.event.get()

    for event in events:

        if event.type == pygame.QUIT:

            quit()

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                quit()

            elif event.key == pygame.K_s and pygame.key.get_mods() * pygame.KMOD_CTRL:

                filename = f'gameexports/gridblocks_grid_{now().microsecond}_{now().second}_{now().minute}_{now().hour}_{now().day}_{now().month}_{now().year}.txt'

                latest_message = f'Starting save to file: {filename}'

                start_new_thread(export_grid, (grid, filename))

            elif event.key == pygame.K_o and pygame.key.get_mods() & pygame.KMOD_CTRL:

                filename = filedialog.askopenfilename()
                tkinter._default_root.destroy()  # Cheap way to get rid of window

                latest_message = f'Opening file: {filename}'

                try:

                    file = json.loads(open(filename, 'r').read())

                    if 'filetype' in file and 'grid' and file['filetype'] == 'blockgridjson':

                        grid.gridblocks = []

                        import_grid = file['grid']

                        imported_blocks = 0

                        for block in file['grid']:

                            imported_blocks += 1

                            latest_message = f'Loading imported assets: {imported_blocks}/{len(import_grid)}'

                            grid.gridblocks.append(
                                GridBlock(
                                (block['w'], block['h']),  # size: w,h
                                block['x'], block['y'],
                                block['unset'],
                                (block['r'], block['g'], block['b']), # colour: r,g,b
                                block['margin']))

                            screen.fill((0, 0, 0))

                            grid.draw(screen)
                            draw_text(screen, f'Latest message >> {latest_message}', (30, screen.get_height() - 30), 1,
                                      size=18)

                            pygame.display.update()

                    else:

                        latest_message = f'Json file must be a grid export'

                except json.JSONDecodeError:

                    latest_message = f'File open of: \'{filename}\' failed, not json'

                except FileNotFoundError:

                    latest_message = f'That file directory doesn\'t exist'

    if mouse.get_pressed()[0]:

        if pygame.key.get_mods() & pygame.KMOD_SHIFT:

            for i, gridblock in enumerate(grid.gridblocks):

                if gridblock and not mouse_block:

                    if gridblock.rect.collidepoint(mouse.get_pos()):

                        curr = grid.gridblocks[i]
                        grid.gridblocks[i] = GridBlock((curr.w, curr.h), curr.x, curr.y)
                        break

                elif mouse_block:

                    if gridblock.rect.collidepoint(mouse.get_pos()):

                        curr = grid.gridblocks[i]
                        mouse_block.x, mouse_block.y = curr.x, curr.y
                        grid.gridblocks[i] = mouse_block.copy()

        else:

            for i, gridblock in enumerate(hotbar.gridblocks):

                if gridblock and not mouse_block:

                    if gridblock.rect.collidepoint(mouse.get_pos()):

                        mouse_block = hotbar.gridblocks[i].copy()

                        break
    else:

        if mouse_block:

            for i, gridblock in enumerate(grid.gridblocks):

                if gridblock and mouse_block:

                    if gridblock.rect.collidepoint(mouse.get_pos()):

                        curr = grid.gridblocks[i]
                        mouse_block.x, mouse_block.y = curr.x, curr.y
                        grid.gridblocks[i] = mouse_block
                        mouse_block = None
                        break

            for i, gridblock in enumerate(hotbar.gridblocks):

                if gridblock and not mouse_block:

                    if gridblock.rect.collidepoint(mouse.get_pos()):

                        mouse_block = None
                        break

        pass

    if mouse_block:

        x, y = mouse.get_pos()
        x = x - mouse_block.w/2
        y = y - mouse_block.h/2

        mouse_block.draw(screen, x, y)

    draw_text(screen, f'Latest message >> {latest_message}', (30, screen.get_height() - 30), 1, size=18)

    pygame.display.update()

    clock.tick(60)