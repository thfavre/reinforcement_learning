import pygame

def draw_text(surface, text, pos, font, color=(222,222,222), centerx=False, centery=False):
	rendered_text = font.render(text, True, color)
	rect = rendered_text.get_rect()
	if centerx:
		rect.centerx = pos[0]
	else:
		rect.x = pos[0]
	if centery:
		rect.centery = pos[1]
	else:
		rect.y = pos[1]
	surface.blit(rendered_text, rect)

