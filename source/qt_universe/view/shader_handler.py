import pygame

from source.pygame_shaders import pygame_shaders
from source.qt_universe.controller.qt_pan_zoom_handler import pan_zoom_handler
from source.qt_universe.view.qt_view_config import qt_draw_config



class ShaderHandler:
    def __init__(self) -> None:
        self.target_surface = pygame.Surface((1920, 1080))
        # self.target_surface = pygame.Surface((200, 200))
        self.target_surface.fill((0, 0, 0))
        self.screen = None
        self.shader = None
        self.setup_shader_handler()

    def setup_shader_handler(self):
        if qt_draw_config.DRAW_SHADER:
            self.screen = pygame.display.set_mode((
                1920, 1080), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE, display=0)

            # self.screen = pygame.display.set_mode((
            #     200, 200), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE, display=0)
            self.setup_shader()
        else:
            self.screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE, display=0)

    def setup_shader(self):
        # define the shader
        self.shader = pygame_shaders.Shader(r"C:\Users\sever\Documents\Galactica-RTS_zoomable1.107\source\glsl_shaders\vertex.txt", r"C:\Users\sever\Documents\Galactica-RTS_zoomable1.107\source\glsl_shaders\ring_atmosphere.glsl", self.target_surface)  # <- give it to our shader
        self.shader.send("iResolution", self.target_surface.get_size())

    def draw_shader(self, screen, point, image_rect):

        # if not DRAW_SHADER:
        #     return

        drawable = ["planet", "moon", "sun"]

        if not point.type in drawable:
            return

        if image_rect.width < 20:
            return

        # render the shader
        self.shader.send("iPos", image_rect.center)
        self.shader.send("iRadius", image_rect.width)
        self.shader.send("iColor", point.normalized_color)
        self.shader.send("iBlur", 30 * pan_zoom_handler.zoom)
        rendered_shader = self.shader.render()

        # then render the shader onto the display
        screen.blit(rendered_shader, (0, 0), special_flags=pygame.BLEND_MAX)

        # screen.blit(rendered_shader, (0, 0))




shader_handler = ShaderHandler()
