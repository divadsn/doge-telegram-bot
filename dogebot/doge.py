import random

from PIL import Image, ImageDraw, ImageFont

# https://www.webnots.com/vibgyor-rainbow-color-codes/
RAINBOW_COLORS = [
    (148, 0, 211),
    (75, 0, 130),
    (0, 0, 255),
    (0, 255, 0),
    (255, 255, 0),
    (255, 127, 0),
    (255, 0, 0)
]


class DogeImage(object):

    def __init__(self, image: Image, font: ImageFont):
        self.image = image
        self.font = font
        self.texts = []
        self.colors = RAINBOW_COLORS
        random.shuffle(self.colors)

    def add_phrase(self, modifier: str, word: str = ""):
        width, height = self.image.size
        text = f"{modifier}{' ' + word if word else ''}"
        color = self.colors[len(self.texts)]

        # Calculate maximum x and y for phrase
        max_x = width - self.font.getsize(text)[0]
        max_y = height - self.font.getsize(text)[1]

        x, y = random.randint(0, max_x), random.randint(0, max_y)
        draw_text = DogeText(text, color, self.font, x, y)
        num_attempts = 0

        while any(draw_text.intersects(txt) for txt in self.texts):
            draw_text.x = random.randint(0, max_x)
            draw_text.y = random.randint(0, max_y)

            num_attempts += 1

            # Cancel after 10 tries if we still haven't found
            if num_attempts > 10:
                break

        self.texts.append(draw_text)

    def save(self, output, format: str = "png"):
        for text in self.texts:
            text.draw(self.image)

        self.image.save(output, format)
        self.image.close()


class DogeText(object):

    def __init__(self, text, color, font, x=0, y=0):
        self.text = text
        self.color = color
        self.font = font
        self._x = x
        self._y = y
        self._box = (0, 0, 0, 0)
        self.update_box()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_x):
        self._x = new_x
        self.update_box()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new_y):
        self._y = new_y
        self.update_box()

    def update_box(self):
        self._box = (
            self.x,
            self.y,
            self.x + self.font.getsize(self.text)[0],
            self.y + self.font.getsize(self.text)[1]
        )

    def draw(self, image):
        canvas = ImageDraw.Draw(image)
        canvas.text((self.x, self.y), self.text, self.color, font=self.font)

    def intersects(self, other):
        return self.is_inside_text(other) or other.is_inside_text(self)

    def is_inside_text(self, other):
        self_corners = [
            (self._box[0], self._box[1]),
            (self._box[0], self._box[3]),
            (self._box[2], self._box[1]),
            (self._box[2], self._box[3])
        ]

        return any(other.point_inside(pnt) for pnt in self_corners)

    def point_inside(self, point):
        px, py = point
        return self._box[0] <= px <= self._box[2] and self._box[1] <= py <= self._box[3]
