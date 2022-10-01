from painter import Painter
import pygame as pg
from pygame import font, display, event, mouse
from sys import exit
from pygame_textinput import TextInputVisualizer 
from os import makedirs, listdir
from os.path import exists as exists_path, join as join_path
from torchvision.transforms import ToPILImage
to_img_transform = ToPILImage()

class ImageGenerator(Painter):
    def __init__(self):
        super().__init__()
        font.init()
        self.text_font = font.SysFont("comicsans", 40)
        display.set_caption("Image generator")
        self.input = TextInputVisualizer(font_color=(255, 0, 0), cursor_color=(255, 0, 0))
        self.cur_dir = 'created_images'
        self.count = 0

    def change_dir(self):
        self.cur_dir = join_path('created_images', self.input.value)
        if not exists_path(self.cur_dir):
            makedirs(self.cur_dir)

        images = listdir(self.cur_dir)
        self.count = len(images)

    def save_img(self):
        filename = f'{self.count}.png'
        path = join_path(self.cur_dir, filename)
        image = to_img_transform(self.grid)
        image.save(path)
        self.count += 1

    def draw_stuff(self):
        super().draw_stuff()
        self.screen.blit(self.input.surface, (10, 10))

        text = self.text_font.render(f'{self.count}', False, (255, 0, 0))
        self.screen.blit(text, (self.size[0] - 30, 10))

    def start(self):
        while True:
            self.draw_stuff()
            events = event.get()
            
            self.input.update(events)

            for e in events:
                match e.type:
                    case pg.QUIT: exit()
                    case pg.MOUSEBUTTONDOWN:
                        match e.button:
                            case 2:
                                self.save_img()
                                self.clear_canvas()
                            case 3: self.clear_canvas()
                    case pg.KEYDOWN:
                        match e.key:
                            case pg.K_RETURN: 
                                self.change_dir()
                    case pg.MOUSEMOTION:
                        left_mouse_button_pressed = mouse.get_pressed()[0]
                        if left_mouse_button_pressed:
                            pos = mouse.get_pos()
                            self.paint(pos)

            display.update()
            self.clock.tick(self.fps)

if __name__ == '__main__':
    my_image_generator = ImageGenerator()
    my_image_generator.start()