import tkinter as tk
import pygame
import math
import threading
import numpy as np
from PIL import Image, ImageTk
import settings

global rot_speed
rot_speed = 0.0

# Initialize Pygame and set up display
def pygame_setup(canvas):
    pygame.init()
    width, height = 75, 75
    screen = pygame.Surface((width, height), pygame.SRCALPHA, 32)

    # Cube vertices and edges
    vertices = [
        [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
        [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1],
    ]
    edges = [
        (0, 1), (0, 2), (0, 4), (1, 3), (1, 5),
        (2, 3), (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7),
    ]

    angle_x = 45 * (math.pi / 180)
    angle_y = 0
    angle_z = 45 * (math.pi / 180)
    clock = pygame.time.Clock()


    def mupdate():
        nonlocal angle_y
        
        screen.fill(settings.backgroundOptions[settings._colorscheme_index])
        angle_y += rot_speed

        # Project vertices and draw edges
        projected_vertices = []
        for vertex in vertices:
            x, y, z = vertex

            x_rotated_z = x * math.cos(angle_z) - y * math.sin(angle_z)
            y_rotated_z = x * math.sin(angle_z) + y * math.cos(angle_z)
            z_rotated_z = z  # No rotation around Z

            # Apply X rotation
            y_rotated_x = y_rotated_z * math.cos(angle_x) - z_rotated_z * math.sin(angle_x)
            z_rotated_x = y_rotated_z * math.sin(angle_x) + z_rotated_z * math.cos(angle_x)
            x_rotated_x = x_rotated_z  # No rotation around X

            # Now apply Y rotation
            x_final = (x_rotated_x * math.cos(angle_y)) + (z_rotated_x * math.sin(angle_y))
            y_final = y_rotated_x
            z_final = (-x_rotated_x * math.sin(angle_y)) + (z_rotated_x * math.cos(angle_y))

            fov = 130
            distance = 6.7
            factor = fov / (distance + z_final)
            x_projected = int(x_final * factor + width // 2)
            y_projected = int(-y_final * factor + height // 2)

            projected_vertices.append((x_projected, y_projected))

        # Draw the cube edges
        for start, end in edges:
            pygame.draw.line(screen, settings.fontColorOptions[settings._colorscheme_index], projected_vertices[start], projected_vertices[end])

        # Convert Pygame surface to a format suitable for Tkinter using Pillow
        pygame_image = pygame.surfarray.array3d(screen)
        pygame_image = np.rot90(pygame_image)
        pygame_image = np.flipud(pygame_image)
        tk_image = ImageTk.PhotoImage(image=Image.fromarray(pygame_image))

        # Update Tkinter canvas with Pygame surface
        canvas.create_image(0, 0, image=tk_image, anchor=tk.NW)
        canvas.image = tk_image

        clock.tick(60)
        canvas.after(16, mupdate)
    mupdate()


