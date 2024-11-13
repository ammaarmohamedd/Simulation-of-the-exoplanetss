import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
G = 6.67430e-11  # Gravitational constant, m^3 kg^-1 s^-2
M_star = 1.989e30  # Mass of the star (e.g., Sun), kg

# Simulation parameters
time_step = 24 * 3600  # 1 day in seconds
total_time = 365 * time_step  # Simulate for 1 year

# Define an exoplanet class
class Exoplanet:
    def __init__(self, mass, distance, velocity, name="Planet"):
        self.mass = mass
        self.position = np.array([distance, 0.0])  # Start at a distance from the star on the x-axis
        self.velocity = np.array([0.0, velocity])  # Initial velocity perpendicular to radius
        self.name = name

    def update_position(self, force, time_step):
        # Update velocity based on force (F = ma, so a = F/m)
        acceleration = force / self.mass
        self.velocity += acceleration * time_step
        # Update position based on velocity
        self.position += self.velocity * time_step

    def gravitational_force(self, star_position):
        # Calculate the gravitational force exerted by the star
        r_vector = self.position - star_position
        r_magnitude = np.linalg.norm(r_vector)
        force_magnitude = G * self.mass * M_star / r_magnitude**2
        force_direction = -r_vector / r_magnitude  # Direction towards the star
        return force_magnitude * force_direction

# Create a star and planets (example system)
star_position = np.array([0.0, 0.0])

# Define planets (e.g., mass in kg, distance in meters, and velocity in m/s)
planets = [
    Exoplanet(3.285e23, 5.79e10, 47400, "Mercury-like"),  # close, fast orbit
    Exoplanet(4.867e24, 1.08e11, 35000, "Venus-like"),
    Exoplanet(5.972e24, 1.496e11, 29800, "Earth-like"),
    Exoplanet(6.39e23, 2.279e11, 24100, "Mars-like")
]

# Set up the plot
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(-3e11, 3e11)
ax.set_ylim(-3e11, 3e11)

# Plot the star
star_plot, = ax.plot(0, 0, 'yo', markersize=12, label="Star (e.g., Sun)")

# Plot the planets
planet_plots = [ax.plot([], [], 'o', label=planet.name)[0] for planet in planets]
planet_trails = [ax.plot([], [], '-', alpha=0.5)[0] for _ in planets]
planet_paths = [[] for _ in planets]

# Update function for animation
def update(frame):
    for i, planet in enumerate(planets):
        # Calculate the force on each planet from the star
        force = planet.gravitational_force(star_position)
        
        # Update planet's position
        planet.update_position(force, time_step)
        
        # Update plot data
        planet_plots[i].set_data([planet.position[0]], [planet.position[1]])  # Wrapping position in lists
        
        # Store planet position in path
        planet_paths[i].append(planet.position.copy())
        
        # Update trail for each planet (last 100 points)
        trail_x, trail_y = zip(*planet_paths[i][-100:])
        planet_trails[i].set_data(trail_x, trail_y)
    
    return planet_plots + planet_trails

# Animation
ani = FuncAnimation(fig, update, frames=int(total_time / time_step), interval=20, blit=False)

# Add legend and show plot
plt.legend(loc="upper right")
plt.show()
