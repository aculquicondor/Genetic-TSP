import pygame


class Main(object):

    cell_width = 6
    node_color = (0, 0, 0)
    path_color = (30, 240, 60)
    background_color = (255, 255, 255)

    def __init__(self, graph, height, width):
        self.graph = graph
        self.width = width
        self.height = height
        pygame.init()
        self.screen = pygame.display.set_mode((self.width * self.cell_width,
                                               self.height * self.cell_width))
        pygame.display.set_caption('TSP')
        self.update()

    def get_rectangle(self, row, col):
        return (col * self.cell_width,
                row * self.cell_width,
                self.cell_width,
                self.cell_width),

    def get_center(self, row, col):
        return (col * self.cell_width + self.cell_width / 2,
                row * self.cell_width + self.cell_width / 2)

    def get_y_x(self, row, col):
        return row / self.cell_width, col / self.cell_width

    def update(self):
        self.screen.fill(self.background_color)

        for node in self.graph.nodes:
            pygame.draw.circle(self.screen, self.node_color,
                               self.get_center(*node), self.cell_width >> 1)
        pygame.display.flip()

        for edge in self.graph.solve():
            pygame.draw.line(self.screen, self.path_color,
                             self.get_center(*edge[0]),
                             self.get_center(*edge[1]))
        pygame.display.flip()

    def run(self):
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = self.get_y_x(*event.pos[::-1])
                if self.graph.add_node(*pos):
                    self.update()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                self.update()
