"""
Serves out the frequently used common UI elements by rendering them
"""
import pygame

from config import Colors
import pygame.gfxdraw as draw

canvas = None
default_font = 'BreeSerif-Regular.ttf'


def set_screen(screen):
    global canvas
    canvas = screen


def draw_line(line_position, line_size, color=Colors.red, thick=2):
    """Draw a line"""
    pygame.draw.line(canvas, color, line_position, (line_position[0] + line_size, line_position[1]), thick)


def draw_text(text, position, color=Colors.white, size=18, font_name=default_font):
    """Draw a configured text element to a specific place"""
    text_font = pygame.font.Font(f'./font/{font_name}', size)
    rendered_text = text_font.render(text, False, color)
    canvas.blit(rendered_text, position)


def draw_panel(position, size, border_color, background):
    x, y, w, h = position[0], position[1], size[0], size[1]
    pygame.draw.rect(canvas, border_color, (x, y, w, h), 2)
    draw.box(canvas, [x + 2, y + 2, w - 3, h - 3], background)


def draw_progress_bar(position, size, level, values, colors=(Colors.dark_grey, Colors.grey, Colors.green)):
    """
    Draw a progress bar with the specified parameters
    Show the progress of how fulfilled the actual level
    :param position: where to render (x, y coordinate of top-left position)
    :param size: of the bar (width, height)
    :param level: Actual level
    :param values: actual and maximum value (base of percentage)
    :param colors: colors of the elements (border, panel, font)
    """
    # Panel-border
    draw_panel(position, size, colors[0], colors[1])
    fill = int(size[0] * (values[0] / values[1]))
    x, y, w, h = position[0]+3, position[1]+3, fill, size[1]-6
    draw_panel((x, y), (w, h), colors[2], colors[2])

    draw_text(f'Level: {level}', (position[0] + int(size[0]/3), position[1]+10), size=21)