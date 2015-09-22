from gui import Main
from ia import Graph


def main(height, width):
    game = Main(Graph(), height, width)
    game.run()

if __name__ == '__main__':
    main(120, 200)
