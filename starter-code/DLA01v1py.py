import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numpy.linalg import norm

""" 
    randomStep([x,y])

Returns a random step from the current position, [x,y]. The step is 1 step to the left or right, or up or down."""
def randomStep(pos):
    steps = np.array([[-1,0],[1,0],[0,-1],[0,1]])
    return pos + steps[np.random.randint(0, 4)]

"""
    walkerStart(rstart)

Returns a random starting position for a walker. The starting position is a distance rstart from the origin, at a random angle.
"""
def walkerStart(rstart, rad):
    theta = 2 * np.pi * np.random.rand()
    return np.round(rstart * np.array([np.cos(theta), np.sin(theta)])).astype(int) + np.array([rad, rad])

"""
    clusterCheck(position,cluster,radius)

Checks if the position is part of the cluster (if it is inside the box).
"""
def clusterCheck(position, cluster, radius):
    if not (np.any(position < 0) or np.any(position >= 2*radius+1)) and cluster[position[0], position[1]] > 0:
        return True
    return False

rad = 200 # Smaller than 50 will give poor statistics, bigger than 200 takes too long to run (depending on your computer)
rstart = 2  
clust = np.zeros((2*rad+1, 2*rad+1), dtype=int)
clust[rad, rad] = 1
done = False
count = 0
while not done: # keep starting walkers until the cluster touches the boundary
    pos = walkerStart(rstart, rad)
    while True: # keep stepping until the walker wanders off or sticks to the cluster
        newpos = randomStep(pos) # take a random step
        #print("New position: ", newpos)
        if norm(newpos - np.array([rad, rad])) > 1.5*rstart: # if the walker wanders off, start a new walker 
            break
        # If the walker is inside the box and touches the cluster, stick it to the cluster
        if clusterCheck(newpos, clust, rad):
            count += 1
            clust[pos[0], pos[1]] = count # keep track of the order so that we can make an animation later
            # Extend the starting radius, if necessary
            rstart = max(rstart, int(np.ceil(norm(newpos - np.array([rad, rad])))) + 2)
            if count % 1000 == 0: # Just so we know it's still running
                print("Count: ", count)
            # If the cluster touches any boundary, the simulation is done
            if np.any(pos == np.array([0, 0])) or np.any(pos == np.array([2*rad, 2*rad])):
                done = True
            break
        pos = newpos
    if done: # Cluster touches the boundary
        break
    
# plt.imshow(clust, aspect='equal', origin='lower', extent=[0, 2*rad, 0, 2*rad], cmap='gray')
# plt.axis('off')
# plt.show()

# Get cluster points, coordinates of nonzero values in clust
cp = np.nonzero(clust)
x_cp = cp[0]
y_cp = cp[1]

# Create scatter plot (adjust markersize depending on the radius of the cluster, `rad`)
plt.figure()
plt.scatter(x_cp, y_cp, s=1, c='black', edgecolors='none')
plt.axis('equal')
plt.xlim(0, 2*rad)
plt.ylim(0, 2*rad)
plt.axis('off')
plt.show()

# Get distances from the center of the cluster
dists = np.array([norm(np.array([cp[0][i], cp[1][i]]) - np.array([rad, rad])) for i in range(len(cp[0]))])

# compute m(r) and plot on log scale. Like Fig. 7.20 in "Random Systems" Chap. 7 of Giordano
xr = np.arange(10, int(np.round(rad/2)) + 1) # Skip the first few points which have larger jitter due to the discrete lattice
mr = np.array([np.sum(dists < r) for r in xr])
plt.figure()
plt.loglog(xr, mr, 'o', markersize=2, markeredgewidth=0)
plt.xlabel("Radius")
plt.ylabel("Number of particles")
plt.title("Number of particles vs. Radius")
plt.show()

# Fit a line to the log of the data
A = np.column_stack([np.ones(len(xr)), np.log10(xr)])
b = np.log10(mr)
x = np.linalg.lstsq(A, b, rcond=None)[0] # Solve the linear system to find the slope and intercept
plt.figure()
plt.scatter(np.log10(xr), np.log10(mr), s=2, edgecolors='none', label="Data")
plt.plot(np.log10(xr), x[1]*np.log10(xr) + x[0], linewidth=2, label="Fit")
plt.xlabel("Radius")
plt.ylabel("Number of particles")
plt.title("Number of particles vs. Radius")
plt.legend()
plt.text(np.log10(xr)[-1]*0.9, np.log10(mr)[-1]*0.8, f"Slope: {round(x[1], 3)}", fontsize=10, ha='left')
plt.show()

# Animate the growth of the cluster, just for fun 
lcp = np.max(clust) # last cluster point
fs = max(1, lcp // 200) # frame step. // is the integer division operator
frames = list(range(1, lcp+1, fs)) + [lcp] + [lcp]*30  # Repeat last frame 30 times to give the animation a "pause" at the end

fig, ax = plt.subplots()
ax.set_xlim(0, 2*rad)
ax.set_ylim(0, 2*rad)
ax.set_aspect('equal')
ax.axis('off')

def animate(frame):
    ax.clear()
    ax.set_xlim(0, 2*rad)
    ax.set_ylim(0, 2*rad)
    ax.set_aspect('equal')
    ax.axis('off')
    
    mask = (clust > 0) & (clust <= frame) # mask to get all cluster points in the current frame
    cp_frame = np.nonzero(mask) # get the cluster point coordinates in the current frame
    x_frame = cp_frame[0]
    y_frame = cp_frame[1]
    colors_frame = clust[cp_frame[0], cp_frame[1]]
    
    scatter = ax.scatter(x_frame, y_frame, 
            s=0.8,  # Adjust this depending on the radius of the cluster, `rad`
            c=colors_frame,
            edgecolors='none',
            cmap='viridis',
            vmin=1,
            vmax=lcp)
    ax.set_title(f"DLA Cluster Growth (n = {frame})")
    return scatter,

anim = animation.FuncAnimation(fig, animate, frames=frames, interval=1000/15, blit=False, repeat=True)
anim.save("pysrc/DLA_cluster_growth.gif", writer='pillow', fps=15, dpi=300)
plt.close()