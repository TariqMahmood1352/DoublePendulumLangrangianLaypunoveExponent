import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from scipy.integrate import solve_ivp

# ----------------------------
# Physical constants
# ----------------------------
g = 9.81
L1, L2 = 1.0, 1.0
m1, m2 = 1.0, 1.0

def equations(t, y):
    th1, w1, th2, w2 = y
    c, s = np.cos(th1-th2), np.sin(th1-th2)
    
    # Non-linear second-order ODEs reduced to first-order system
    dth1 = w1
    dw1 = (m2*g*np.sin(th2)*c - m2*s*(L1*w1**2*c + L2*w2**2) - (m1+m2)*g*np.sin(th1)) / (L1*(m1 + m2*s**2))
    dth2 = w2
    dw2 = ((m1+m2)*(L1*w1**2*s - g*np.sin(th2) + g*np.sin(th1)*c) + m2*L2*w2**2*s*c) / (L2*(m1 + m2*s**2))
    
    return [dth1, dw1, dth2, dw2]

# ----------------------------
# Time and Initial Conditions
# ----------------------------
t_span = (0, 15) # Increased time to see divergence
t_eval = np.linspace(*t_span, 1500)

# Two extremely close trajectories to calculate Lyapunov exponent
# IC: [theta1, omega1, theta2, omega2]
base_ic = [np.pi/2, 0, np.pi/2, 0]
perturbation = 1e-5
initial_conditions = [
    base_ic,
    [base_ic[0] + perturbation, 0, base_ic[2], 0],
    [np.pi, 0, np.pi/2, 0],   # Additional comparison pendulum
    [np.pi/3, 0, np.pi/2, 0]  # Additional comparison pendulum
]

solutions = [solve_ivp(equations, t_span, ic, t_eval=t_eval, method='RK45', rtol=1e-10)
             for ic in initial_conditions]

# ----------------------------
# Lyapunov Exponent Calculation
# ----------------------------
# We compare sol[0] and sol[1]
y0 = solutions[0].y # Reference
y1 = solutions[1].y # Perturbed

# Euclidean distance in 4D state space at each time point
dist = np.sqrt(np.sum((y1 - y0)**2, axis=0))
# Lyapunov over time: lambda = (1/t) * ln(dist/dist_initial)
# We handle t=0 to avoid division by zero
lyapunov_evolution = np.zeros_like(t_eval)
lyapunov_evolution[1:] = np.log(dist[1:] / perturbation) / t_eval[1:]

# ----------------------------
# Figure Setup
# ----------------------------
fig, ax = plt.subplots(figsize=(7, 7))
ax.set_xlim(-2.2, 2.2)
ax.set_ylim(-2.2, 2.2)
ax.set_aspect("equal")
ax.axis("off")

# UI Elements
time_text = ax.text(-2, 1.9, '', fontsize=10, color='black')
lyap_text = ax.text(-2, 1.7, '', fontsize=10, color='darkred', weight='bold')

colors = ["#0077BE", "#FF4500", "#32CD32", "#8A2BE2"]
rods = [ax.plot([], [], lw=2, color=c, solid_capstyle='round')[0] for c in colors]
bubbles = [ax.plot([], [], "o", color=c, markersize=8)[0] for c in colors]
trails = [ax.plot([], [], lw=1, color=c, alpha=0.5)[0] for c in colors]

path_x = [[] for _ in initial_conditions]
path_y = [[] for _ in initial_conditions]

# ----------------------------
# Animation
# ----------------------------
def animate(i):
    for k, sol in enumerate(solutions):
        th1, th2 = sol.y[0][i], sol.y[2][i]
        x1, y1 = L1*np.sin(th1), -L1*np.cos(th1)
        x2, y2 = x1 + L2*np.sin(th2), y1 - L2*np.cos(th2)

        rods[k].set_data([0, x1, x2], [0, y1, y2])
        bubbles[k].set_data([x2], [y2])
        
        path_x[k].append(x2)
        path_y[k].append(y2)
        trails[k].set_data(path_x[k], path_y[k])

    # Update Lyapunov info
    current_dist = dist[i]
    current_lyap = lyapunov_evolution[i]
    time_text.set_text(f"Time: {t_eval[i]:.2f}s")
    lyap_text.set_text(f"Lyapunov Exp: {current_lyap:.3f}\nSeparation: {current_dist:.2e}")

    return rods + bubbles + trails + [time_text, lyap_text]

ani = FuncAnimation(fig, animate, frames=len(t_eval), interval=20, blit=True)

# ----------------------------
# Save
# ----------------------------
print("Calculating and saving animation with Lyapunov metrics...")
writer = FFMpegWriter(fps=30, bitrate=2000)
ani.save("double_pendulum_lyapunov.mp4", writer=writer)
plt.close(fig)
print(f"Final Estimated Lyapunov Exponent: {lyapunov_evolution[-1]:.4f}")
