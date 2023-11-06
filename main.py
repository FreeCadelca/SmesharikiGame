import pygame
import moviepy.editor

pygame.init()
video = moviepy.editor.VideoFileClip("source\\preview.mp4")
video.preview()
pygame.quit()