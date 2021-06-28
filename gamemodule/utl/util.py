import random, datetime, pygame
from gamemodule.utl.datastructure import stack
import re

def now():

    return datetime.datetime.now()


def validate_rgb(d):

    if not 0 <= d <= 255:

        raise ValueError(f'Expected valid rgb value modifier, instead got {d}')

def random_rgb():

    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def floor_all(*numbers):

    return tuple([int(number) for number in numbers])


def floor(number):

    return int(number)


class GameLog:

    def __init__(self, name):

        self.__log__ = []

        self.__log_name__ = name

        self.__file_name__ = f"""{self.__log_name__}_{now().microsecond}_{now().second}_{now().minute}_{now().hour}_{now().day}_{now().month}_{now().year}.log"""

    @property
    def name(self):

        return self.__log_name__

    @property
    def filename(self):

        return self.__file_name__

    def export(self, name: str = None, folder: str =''):

        self.push(f'Exported game log as {self.filename if name is None else name}')

        open(folder + '/' + (self.filename if name is None else name), 'w').write(
            '\n'.join(self.__log__)
        )

    def push(self, text, display=True):

        log = f"""[{self.__log_name__} @ {now().microsecond}ms/{now().second}s/{now().minute}m/{now().hour}h, {now().day}d/{now().month}mo/{now().year}y] --> {text}"""

        self.__log__.append(log)

        if display:

            print(log)

# Draw text

def draw_text(surface, text='Hello World', pos=(10, 10), bold=1, colour=(0, 255, 0), size=24, font='Trebuchet MS'):

    font = pygame.font.SysFont(font, size)
    t = font.render(text, bold, colour)
    surface.blit(t, pos)

class Game:

    def __init__(
            self, player, screen: pygame.Surface,
            operations: stack, entities: stack, events: stack, shutdown: stack, startup: stack,
            log: GameLog, mouse, clock: pygame.time.Clock,
            player2=None, player3=None, player4=None, player5=None, player6=None, player7=None, player8=None
    ):

        self.player = player
        self.player2, self.player3, self.player4, self.player5, self.player6, self.player7, self.player8 = player2, player3, player4, player5, player6, player7, player8
        self.screen: pygame.Surface = screen
        self.operations: stack = operations
        self.entities: stack = entities
        self.events: stack = events
        self.shutdown: stack = shutdown
        self.startup: stack = startup
        self.log: GameLog = log
        self.mouse = mouse
        self.clock = clock
        self.conditions = {}

        self.oww = None
        self.owh = None

    def get_condition(self, con):

        return self.conditions[con] if con in self.conditions else None

    def set_condition(self, con, val):

        self.conditions[con] = val

        return val

    @property
    def window(self):

        return pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()

    @property
    def ww(self):

        return self.window[0] if not self.oww else self.oww

    @property
    def wh(self):

        return self.window[1] if not self.owh else self.owh


    def collide_entity(self, entity):

        results = []

        for e in self.entities:

            if e is not entity:

                results.append(pygame.Rect(*e.rect).colliderect(entity.rect))

        return True in results


def get_digit(number, n):

    if number - 10 ** n == 0:

        return 0

    elif number - 10 ** n < 0:

        return int(get_digit(-number, n))

    return number // 10 ** n % 10

def is_positive(x): return (x ** 2) >= 0

def is_negative(x): return not is_positive(x)

def get_travel_vector(pointa, pointb):

    ax, ay, bx, by = *pointa, *pointb

    rx, ry = ax - bx, ay - by

    return rx // 70, ry // 70