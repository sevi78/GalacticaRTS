import pygame


class ImageHandler:

    def __init__(self, **kwargs):
        self.image = kwargs.get("image", None)
        self.image_raw = kwargs.get("image", None)
        self.rect = None
        self._image_name_small = kwargs.get("image_name_small")
        self.image_name_big = kwargs.get("image_name_big")


    def alignImageRect(self):
        self.rect.center = (self.screen_x + self.screen_width // 2, self.screen_y + self.screen_height // 2)
        # self.rect.center = (self.screen_x - self.screen_width / 2, self.screen_y - self.screen_height / 2)
        # self.rect.center = self.center#(self.screen_x - self.screen_width / 2, self.screen_y - self.screen_height / 2)

        if self.imageHAlign == 'left':
            self.rect.left = self.screen_x + self.margin - (self.radius_extension / 2)
        elif self.imageHAlign == 'right':
            self.rect.right = self.screen_x + self.screen_width - self.margin + (self.radius_extension / 2)

        if self.imageVAlign == 'top':
            self.rect.top = self.screen_y + self.margin - (self.radius_extension / 2)
        elif self.imageVAlign == 'bottom':
            self.rect.bottom = self.screen_y + self.screen_height - self.margin - (self.radius_extension / 2)

    def setImage(self, image):
        image = pygame.transform.scale(image, (self.get_screen_width(), self.get_screen_height()))
        self.image = image
        self.alignImageRect()

    def set_image_position(self):
        """
        sets the position of the image, based on the widgetbase recalculation of the coordinates, including pan_zoom
        """

        # self.rect = self.image.get_rect(center=self.center)
        self.rect = self.image.get_rect()
        self.rect.x = self.screen_x
        self.rect.y = self.screen_y
