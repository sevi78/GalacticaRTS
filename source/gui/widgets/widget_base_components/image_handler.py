import copy

from source.multimedia_library.images import outline_image, scale_image_cached, rounded_surface
#
#
# class ImageHandler:
#     """
#     the image handler class used by the widget base
#     """
#     def __init__(self, **kwargs):
#         self.image = kwargs.get("image", None)
#         self.image_raw = kwargs.get("image_raw", copy.copy(self.image))
#         self.outline_thickness = kwargs.get("outline_thickness", 0)
#         self.outline_threshold = kwargs.get("outline_threshold", 0)
#         self.corner_radius = kwargs.get('corner_radius', 3)
#         if self.image:
#             # Create a rounded version of the scaled image if corner_radius is greater than 0
#             if self.corner_radius > 0:
#                 self.image = rounded_surface(self.image, self.corner_radius)
#                 # self.image_raw = rounded_surface(self.image_raw, self.corner_radius)
#
#             self.set_image_outline()
#         self.rect = None
#         self._image_name_small = kwargs.get("image_name_small")
#         self.image_name_big = kwargs.get("image_name_big")
#         self.image_alpha = kwargs.get("image_alpha", None)
#         if self.image_alpha:
#             self.image.set_alpha(self.image_alpha)
#
#     def set_image_outline(self):
#         self.image_outline = outline_image(copy.copy(self.image), self.frame_color, self.outline_threshold, self.outline_thickness)
#
#     def align_image_rect(self):
#         self.rect.center = (self.screen_x + self.screen_width // 2, self.screen_y + self.screen_height // 2)
#
#         if self.image_h_align == 'left':
#             self.rect.left = self.screen_x + self.margin - (self.radius_extension / 2)
#         elif self.image_h_align == 'right':
#             self.rect.right = self.screen_x + self.screen_width - self.margin + (self.radius_extension / 2)
#
#         if self.image_v_align == 'top':
#             self.rect.top = self.screen_y + self.margin - (self.radius_extension / 2)
#         elif self.image_v_align == 'bottom':
#             self.rect.bottom = self.screen_y + self.screen_height - self.margin - (self.radius_extension / 2)
#
#     def set_image(self, image):
#         image = scale_image_cached(image, (self.get_screen_width(), self.get_screen_height()))
#         if self.image_alpha:
#             image.set_alpha(self.image_alpha)
#         self.image = image
#         self.align_image_rect()
#         self.set_image_outline()
#
#     def set_image_position(self):
#         """
#         sets the position of the image, based on the widgetbase recalculation of the coordinates, including pan_zoom
#         """
#         # self.rect = self.image.get_rect(center=self.center)
#         self.rect = self.image.get_rect()
#         self.rect.x = self.screen_x
#         self.rect.y = self.screen_y
class ImageHandler:
    """
    The image handler class used by the widget base.
    """

    def __init__(self, **kwargs):
        self.image = kwargs.get("image", None)
        self.image_raw = kwargs.get("image_raw", copy.copy(self.image))
        self.outline_thickness = kwargs.get("outline_thickness", 0)
        self.outline_threshold = kwargs.get("outline_threshold", 0)
        self.corner_radius = kwargs.get('corner_radius', 3)

        if self.image:
            # Create a rounded version of the image if corner_radius is greater than 0
            if self.corner_radius > 0:
                self.image = rounded_surface(self.image, self.corner_radius)
                # self.image_raw = rounded_surface(self.image_raw, self.corner_radius) if self.image_raw else None

            self.set_image_outline()

        self.rect = None
        self._image_name_small = kwargs.get("image_name_small")
        self.image_name_big = kwargs.get("image_name_big")
        self.image_alpha = kwargs.get("image_alpha", None)

        if self.image_alpha:
            self.image.set_alpha(self.image_alpha)

    def set_image_outline(self):
        """Sets the outline of the image based on specified parameters."""
        self.image_outline = outline_image(copy.copy(self.image),
                self.frame_color,
                self.outline_threshold,
                self.outline_thickness)

    def align_image_rect(self):
        """Aligns the image rectangle based on horizontal and vertical alignment settings."""
        self.rect.center = (self.screen_x + self.screen_width // 2,
                            self.screen_y + self.screen_height // 2)

        if self.image_h_align == 'left':
            self.rect.left = self.screen_x + self.margin - (self.radius_extension / 2)
        elif self.image_h_align == 'right':
            self.rect.right = self.screen_x + self.screen_width - self.margin + (self.radius_extension / 2)

        if self.image_v_align == 'top':
            self.rect.top = self.screen_y + self.margin - (self.radius_extension / 2)
        elif self.image_v_align == 'bottom':
            self.rect.bottom = self.screen_y + self.screen_height - self.margin - (self.radius_extension / 2)

    def set_image(self, image):
        """Sets a new image for the handler and applies rounding if necessary."""
        # Scale and round the new image
        image = scale_image_cached(image, (self.get_screen_width(),
                                           self.get_screen_height()))

        if self.corner_radius > 0:
            image = rounded_surface(image, self.corner_radius)

        if self.image_alpha:
            image.set_alpha(self.image_alpha)

        # Update the image and align its rectangle
        self.image = image
        self.align_image_rect()
        self.set_image_outline()

    def set_image_position(self):
        """
        Sets the position of the image based on recalculated coordinates,
        including pan and zoom adjustments.
        """
        # Set rectangle for positioning
        self.rect = self.image.get_rect()
        self.rect.x = self.screen_x
        self.rect.y = self.screen_y
