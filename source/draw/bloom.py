# import pygame, cv2, numpy
#
# def Bloom1(canvas: pygame.Surface):
#     size = canvas.get_size()
#     newCanvas = pygame.Surface(size, pygame.SRCALPHA)
#     newCanvas.set_colorkey((0,0,0))
#
#     canvas_rgb = pygame.surfarray.array3d(canvas)
#     canvas_alpha = pygame.surfarray.array_alpha(canvas).reshape((*canvas_rgb.shape[0:2], 1))
#     canvas_rgba = numpy.concatenate((canvas_rgb, canvas_alpha), 2)
#
#     cv2.GaussianBlur(canvas_rgba, ksize=(9, 9), sigmaX=10, sigmaY=10, dst=canvas_rgba)
#     cv2.blur(canvas_rgba, ksize=(9, 9), dst=canvas_rgba)
#
#     newCanvas.blit(pygame.image.frombuffer(canvas_rgba.transpose((1, 0, 2)).copy(order='C'), size, 'RGBA'), (0,0))
#     return newCanvas
#
# def Bloom2(canvas: pygame.Surface):
#     size = canvas.get_size()
#     newCanvas = pygame.Surface(size, pygame.SRCALPHA)
#     newCanvas.set_colorkey((0,0,0))
#
#     canvas_color = pygame.surfarray.array2d(canvas)
#     canvas_rgba = canvas_color.view(dtype=numpy.uint8).reshape((*canvas_color.shape, 4))
#
#     cv2.GaussianBlur(canvas_rgba, ksize=(9, 9), sigmaX=10, sigmaY=10, dst=canvas_rgba)
#     cv2.blur(canvas_rgba, ksize=(9, 9), dst=canvas_rgba)
#
#     pygame.surfarray.blit_array(newCanvas, canvas_color)
#     return newCanvas
#
# pygame.init()
# window = pygame.display.set_mode((550, 300))
# clock = pygame.time.Clock()
#
# font = pygame.font.SysFont(None, 90)
# text = font.render("Bloom", True, 0)
#
# surface = pygame.Surface((250, 250))
# surface.fill(0)
# pygame.draw.circle(surface, (255, 255, 255), surface.get_rect().center, 100)
# surface.blit(text, text.get_rect(center = surface.get_rect().center))
# surface.set_colorkey(0)
# surface = surface.convert_alpha()
# surface1 = Bloom1(surface)
# surface2 = Bloom1(surface)
#
# run = True
# while run:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#
#     window.fill((64, 64, 64))
#     window.blit(surface1, surface1.get_rect(center = (150, 150)), special_flags = pygame.BLEND_PREMULTIPLIED)
#     window.blit(surface2, surface2.get_rect(center = (400, 150)), special_flags = pygame.BLEND_PREMULTIPLIED)
#     pygame.display.flip()
#     clock.tick(60)
#
# pygame.quit()
# exit()

