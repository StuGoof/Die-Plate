import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

st.title("Nozzle-Shaped Perforation Visualizer")

# User inputs
plate_thickness = st.slider("Total Plate Thickness (mm)", 5, 100, 20)
cone_diameter = st.slider("Cone Opening Diameter (mm)", 5, 50, 20)
final_diameter = st.slider("Final Hole Diameter (mm)", 1, 30, 10)
cone_angle = st.slider("Cone Angle (degrees)", 10, 80, 45)
cone_length = st.slider("Cone Length (mm)", 1, plate_thickness, 10)
channel_length = st.slider("Channel (Land) Length (mm)", 1, plate_thickness, plate_thickness - cone_length)

# Additional inputs
num_holes = st.number_input("Total Number of Holes Required", min_value=1, value=100)
dry_meal_throughput = st.number_input("Dry Meal Throughput (tonne/h)", min_value=0.1, value=10.0)

# Calculations
open_area_one_hole = np.pi * (final_diameter / 2) ** 2
total_open_area = open_area_one_hole * num_holes
open_area_per_tonne = total_open_area / dry_meal_throughput

st.subheader("Open Area Calculations")
st.write(f"Open Area of One Hole: {open_area_one_hole:.2f} mm²")
st.write(f"Total Plate Open Area: {total_open_area:.2f} mm²")
st.write(f"Open Area per Tonne: {open_area_per_tonne:.2f} mm²/t/h")

# 2D Cross-section
st.subheader("2D Cross-Section View")
fig2d, ax2d = plt.subplots()
ax2d.set_aspect('equal')
ax2d.set_xlim(-cone_diameter, cone_diameter)
ax2d.set_ylim(0, plate_thickness + 5)
ax2d.set_title("Nozzle Cross-Section")

# Cone
cone_radius = cone_diameter / 2
final_radius = final_diameter / 2
cone_x = [-cone_radius, -final_radius, final_radius, cone_radius]
cone_y = [0, cone_length, cone_length, 0]
ax2d.fill(cone_x, cone_y, color='lightblue', label='Cone')

# Channel
channel_x = [-final_radius, -final_radius, final_radius, final_radius]
channel_y = [cone_length, plate_thickness, plate_thickness, cone_length]
ax2d.fill(channel_x, channel_y, color='lightgreen', label='Channel')

ax2d.set_xlabel("Radius (mm)")
ax2d.set_ylabel("Depth (mm)")
ax2d.legend()
st.pyplot(fig2d)

# 3D Visualization
st.subheader("3D Visualization of Nozzle-Shaped Perforation")

fig3d = plt.figure()
ax3d = fig3d.add_subplot(111, projection='3d')

# Create 3D surface of the cone and channel
z_cone = np.linspace(0, cone_length, 30)
r_cone = np.linspace(cone_radius, final_radius, 30)
theta = np.linspace(0, 2 * np.pi, 30)
Zc, Theta = np.meshgrid(z_cone, theta)
Rc = np.linspace(cone_radius, final_radius, 30)
Rc, _ = np.meshgrid(Rc, theta)
Xc = Rc * np.cos(Theta)
Yc = Rc * np.sin(Theta)

# Channel
z_channel = np.linspace(cone_length, plate_thickness, 30)
Zch, Theta_ch = np.meshgrid(z_channel, theta)
Rch = np.full_like(Zch, final_radius)
Xch = Rch * np.cos(Theta_ch)
Ych = Rch * np.sin(Theta_ch)

# Plot surfaces
ax3d.plot_surface(Xc, Yc, Zc, color='lightblue', alpha=0.8)
ax3d.plot_surface(Xch, Ych, Zch, color='lightgreen', alpha=0.8)

ax3d.set_xlabel("X (mm)")
ax3d.set_ylabel("Y (mm)")
ax3d.set_zlabel("Depth (mm)")
ax3d.set_title("3D Nozzle View")
st.pyplot(fig3d)
