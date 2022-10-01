import torch
from painter import Painter
import pygame as pg
from pygame import font, display, event, mouse
from sys import exit
from torchvision.datasets import ImageFolder

device = 'cuda'

class ImagePredictor(Painter):
    def __init__(self):
        super().__init__()
        font.init()
        self.text_font = font.SysFont("comicsans", 30)
        display.set_caption("Image predictor")

        self.model = torch.load('model.pth')
        self.model.eval()

        self.labels = ImageFolder(root='sorted_images/train').class_to_idx
        self.inverted_labels = {value: index for index, value in self.labels.items()}

    def format_with_labels(self, output):
        result = {}
        for i in range(0, len(self.inverted_labels)):
            result[self.inverted_labels[i]] = output[0, i].item()
        return torch.max(output, dim=1)[0].item(), result

    def draw_stuff(self):
        super().draw_stuff()
        data = self.grid.view(1, 1, self.grid_size[0], self.grid_size[1]).to(device).float()
        output = self.model(data)
        max, predictions = self.format_with_labels(output)
        for prediction_index, (dictionary_index, value) in enumerate(predictions.items()):
          val = round(value * 100, 2)
          text = self.text_font.render(f'{dictionary_index}: {val}%', False, (255, 0, 0) if value == max else (255, 255, 255))
          self.screen.blit(text, (10, 10 + prediction_index * 24))

    def start(self):
        while True:
            self.draw_stuff()
            events = event.get()
            
            for e in events:
                match e.type:
                    case pg.QUIT: exit()
                    case pg.MOUSEBUTTONDOWN:
                        match e.button:
                            case 3: self.clear_canvas()
                    case pg.MOUSEMOTION:
                        left_mouse_button_pressed = mouse.get_pressed()[0]
                        if left_mouse_button_pressed:
                            pos = mouse.get_pos()
                            self.paint(pos)

            display.update()
            self.clock.tick(self.fps)

if __name__ == '__main__':
    my_image_predictor = ImagePredictor()
    my_image_predictor.start()