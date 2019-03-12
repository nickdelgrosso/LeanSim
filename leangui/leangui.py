import pygame
import random

pygame.init()

screenx = 1200
screeny = 600

win = pygame.display.set_mode((screenx, screeny))

pygame.display.set_caption("Production Line Simulation")

clock = pygame.time.Clock()


class Product(object):
    def __init__(self, name, x, y, width, height):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 1
        self.color = (255, 0, 0)
        self.seconds = 0
        self.leadtime = 0
        self.path = 0
        self.destinationx = 0
        self.destinationy = 0

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

    def move(self):
        if self.path >= wscount-1:
            self.x += self.vel
        elif self.x - self.destinationx != 0 or self.y - self.destinationy != 0:
            if self.x > self.destinationx:
                self.x -= self.vel
            if self.x < self.destinationx:
                self.x += self.vel
            if self.y > self.destinationy:
                self.y -= self.vel
            if self.y < self.destinationy:
                self.y += self.vel

    def wait(self):
        self.vel = 0

    def count_and_finish(self):
        global count
        count += 1


class Workstation(object):
    def __init__(self, name, x, y, width, height):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.cycletime = random.randrange(1, 8)
        self.color = (0, 255, 0)
        self.seconds = 0
        self.idletime = 0
        self.working = False
        self.complete = False

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

    def do_work(self):
        self.working = True
        self.seconds += clock.get_time() / 1000
        if self.seconds >= self.cycletime:
            self.complete = True
            self.seconds = 0
            self.working = False


def redraw_screen():
    win.fill((0, 0, 0))
    for workstation in workstations:
        workstation.draw(win)
        win.blit(pygame.font.SysFont('None', round(workstation.height)).render(workstation.name + ' ' + str(round(workstation.cycletime - workstation.seconds, 2)), 0, (255, 255, 255)), (workstation.x, workstation.y - round(workstation.height) + 5))
        win.blit(pygame.font.SysFont('None', round(workstation.height)).render('Idle ' + str(round(workstation.idletime, 2)), 0, (255, 255, 255)),(workstation.x, workstation.y - round(2 * workstation.height) + 5))
    for product in products:
        product.draw(win)
    win.blit(pygame.font.SysFont('None', 50).render('count ' + str(count), 0, (255, 255, 255)), (5, 5))
    pygame.display.update()


pnumber = 0
count = 0
wscount = 5
batch = 50
products = []
workstations = []

for i in range(1, wscount + 1):
    workstations.append(Workstation("WS" + str(i), round((screenx // (wscount + 1) * i), - 1), round(((screeny // 2) - (.195 * screenx) / wscount)), round((.195 * screenx) // wscount), round((.195 * screenx) // wscount)))

for i in range(0, batch):
    pnumber += 1
    products.append(Product("P" + str(pnumber), 0, round(screeny // 2), round(((.195 * screenx) // wscount) - 10), round(((.195 * screenx) // wscount) - 10)))

run = True
while run:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

#   keys = pygame.key.get_pressed()

    for workstation in workstations:
        if workstation.working is False:
            workstation.idletime += clock.get_time() / 1000

    for product in products:
        product.leadtime += clock.get_time() / 1000
        product.destinationx = round(workstations[product.path].x)
        product.destinationy = round(workstations[product.path].y)
        if product.x >= 0 and product.x + product.width + 10 <= screenx:
            if products.index(product) != 0:
                if product.x >= products[products.index(product) - 1].x - product.width - 10:
                    product.wait()
                elif product.x == workstations[product.path].x:
                    product.wait()
                    workstations[product.path].do_work()
                    if workstations[product.path].complete:
                        product.vel = 10
                        workstations[product.path].complete = False
                        if product.path < wscount - 1:
                            product.path += 1
                        product.move()
                else:
                    product.vel = 10
                    product.move()
            else:
                if product.x == workstations[product.path].x:
                    product.wait()
                    workstations[product.path].do_work()
                    if workstations[product.path].complete:
                        product.vel = 10
                        workstations[product.path].complete = False
                        if product.path < wscount - 1:
                            product.path += 1
                        product.move()
                else:
                    product.vel = 10
                    product.move()
        else:
            print("lead time of product " + str(count + 1) + ' ' + str(round(product.leadtime, 2)))
            products.pop(products.index(product))
            product.count_and_finish()
            if len(products) is 0:
                for workstation in workstations:
                    print(workstation.name + "  " + str(round(workstation.idletime, 2)))

    redraw_screen()

pygame.quit()
