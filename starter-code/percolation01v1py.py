import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, to_hex
import matplotlib.cm as cm
import time

# Code for part (a)
# This is a really naive implementation of percolation. It works but it relies on an inefficient approach that scales as O(L^2) in the number of sites, L. It doesn't do anything clever to relabel sites when clusters merge.
"""
    percCheck(clust)

Checks if the cluster percolates. Returns true if the cluster percolates, false otherwise. Assumes that sites that are positive (>0) are part of the cluster. Percolation happens when *one* cluster touches all four sides of the simulation cell.
"""
def percCheck(clust):
    s1 = set(clust[0, :][clust[0, :] > 0])  # Top row (first row in 0-indexed)
    s2 = set(clust[-1, :][clust[-1, :] > 0])  # Bottom row
    s3 = set(clust[:, 0][clust[:, 0] > 0])  # Left column
    s4 = set(clust[:, -1][clust[:, -1] > 0])  # Right column
    # Check if any cluster appears on all four boundaries
    all_boundaries = s1 & s2 & s3 & s4
    return len(all_boundaries) > 0

""" 
    percolate(L)

Models percolation on a square lattice of size LxL by occupying sites in a random order, one at a time, until a percolating cluster is formed. Returns an array containing the values of each site in the simulation cell, the x,y coordinates of the final site that caused percolation, and the fraction of sites occupied.
"""
def percolate(L):
    clust = np.zeros((L, L), dtype=int)
    list_sites = np.random.permutation(L * L) + 1  # 1-indexed like Julia
    percSite = [0, 0]  # initialize this variable so that it is defined outside the loop
    p = 0  # fraction of sites occupied
    
    for clab, site in enumerate(list_sites, start=1):  # loop through the list of sites in random order
        x = ((site - 1) % L) + 1  # Convert to 1-indexed coordinates
        y = ((site - 1) // L) + 1
        # Convert to 0-indexed for numpy arrays
        x_idx = x - 1
        y_idx = y - 1
        clust[x_idx, y_idx] = clab
        
        # check if neighboring sites are already occupied. Relabel them if so.
        if x > 1 and clust[x_idx - 1, y_idx] > 0:
            clust[clust == clust[x_idx - 1, y_idx]] = clab
        if x < L and clust[x_idx + 1, y_idx] > 0:
            clust[clust == clust[x_idx + 1, y_idx]] = clab
        if y > 1 and clust[x_idx, y_idx - 1] > 0:
            clust[clust == clust[x_idx, y_idx - 1]] = clab
        if y < L and clust[x_idx, y_idx + 1] > 0:
            clust[clust == clust[x_idx, y_idx + 1]] = clab
        
        if percCheck(clust):
            percSite = [x, y]  # coordinates of the percolating site (1-indexed)
            p = clab / (L * L)  # fraction of sites occupied
            break
    
    return clust, percSite, p

# Run the percolation simulation and visualize the clusters
L = 50
clust, percSite, p = percolate(L)

# Visualize all the different clusters with different colors
plt.figure(figsize=(10, 10))
plt.imshow(clust, aspect='equal', origin='lower', cmap='Paired', 
           vmin=0, vmax=np.max(clust))
plt.colorbar()
plt.axis('off')
plt.title(f'Percolation Clusters (p = {p:.4f})')
plt.tight_layout()
plt.show()

# Color the non-percolating sites gray, the percolating cluster yellow, and the final connecting site red
perc_label = clust[percSite[0]-1, percSite[1]-1]  # Convert to 0-indexed
clust_colored = np.zeros_like(clust)
clust_colored[(clust > 0) & (clust < perc_label)] = 1  # Gray for non-percolating
clust_colored[clust == perc_label] = 2  # Light yellow for percolating cluster
clust_colored[percSite[0]-1, percSite[1]-1] = 3  # Red for final connecting site

plt.figure(figsize=(10, 10))
cmap = ListedColormap(['black', 'gray', 'lightyellow', 'red'])
plt.imshow(clust_colored, aspect='equal', origin='lower', cmap=cmap, vmin=0, vmax=3)
plt.axis('off')
plt.title(f'Percolation Visualization (p = {p:.4f})')
plt.tight_layout()
plt.show()

## Code for part (b)
# Animated version that stops when percolation occurs
"""
    percolate_animated(L)

An animated version of the percolation simulation that stops when percolation occurs. Returns the labeled cluster, the coordinates of the percolating site, and the fraction of sites occupied. It creates an animation of the percolation process, showing the cluster at each step.
"""
def percolate_animated(L, save_file="percolation_animation.mp4", fps=60):
    clust = np.zeros((L, L), dtype=int)
    list_sites = np.random.permutation(L * L) + 1
    percSite = [0, 0]
    p = 0
    max_clab = 0
    
    frames = []
    percolated = False
    
    for clab, site in enumerate(list_sites, start=1):
        x = ((site - 1) % L) + 1
        y = ((site - 1) // L) + 1
        x_idx = x - 1
        y_idx = y - 1
        clust[x_idx, y_idx] = clab
        
        # check if neighboring sites are already occupied. Relabel them if so.
        if x > 1 and clust[x_idx - 1, y_idx] > 0:
            clust[clust == clust[x_idx - 1, y_idx]] = clab
        if x < L and clust[x_idx + 1, y_idx] > 0:
            clust[clust == clust[x_idx + 1, y_idx]] = clab
        if y > 1 and clust[x_idx, y_idx - 1] > 0:
            clust[clust == clust[x_idx, y_idx - 1]] = clab
        if y < L and clust[x_idx, y_idx + 1] > 0:
            clust[clust == clust[x_idx, y_idx + 1]] = clab
        
        # Create frame every 3 steps (equivalent to "every 3" in Julia)
        if clab % 3 == 0:
            fig, ax = plt.subplots(figsize=(5.12, 5.12))
            im = ax.imshow(clust, aspect='equal', origin='lower', cmap='tab10', 
                          vmin=0, vmax=clab)
            ax.set_title(f'Step: {clab} / {L*L}, p = {clab/(L*L):.3f}')
            ax.axis('off')
            plt.colorbar(im, ax=ax)
            plt.tight_layout()
            frames.append(fig)
            plt.close(fig)
        
        # Check for percolation and break if found
        if percCheck(clust):
            percSite = [x, y]
            p = clab / (L * L)
            percolated = True
            break
    
    # Save animation
    if frames and save_file:
        print(f"Note: Saving animation frames. For full MP4/GIF, use imageio or similar.")
        print(f"Total frames created: {len(frames)}")
        # Save the last frame as example
        if frames:
            frames[-1].savefig(save_file.replace('.mp4', '_final.png'), dpi=150, bbox_inches='tight')
            plt.close(frames[-1])
    
    return clust, percSite, p, frames

# Run the animated percolation. This takes a while at large image sizes and high resolutions. Mine took ~20 secs to run.
clust, percSite, p, anim_frames = percolate_animated(50)

# Create MP4 video (it will stop at percolation). Could do an animated GIF but
# MP4 format supports higher frame rates and doesn't loop endlessly.
print(f"Animation created with {len(anim_frames)} frames. Use imageio to create MP4/GIF from frames.")


## Code for part (d)
# Improved version of the percolation simulation using the Hoshen-Kopelman algorithm
"""
    percolate_improved(L)

Percolates a square lattice of size LxL using the Hoshen-Kopelman algorithm.
This is more efficient than the naive approach, using union-find to track clusters.
Returns the labeled cluster, the coordinates of the percolating site, and the fraction of sites occupied.
"""
def percolate_improved(L):
    clust = np.zeros((L, L), dtype=int)
    list_sites = np.random.permutation(L * L) + 1  # 1-indexed labels
    percSite = [0, 0]
    p = 0.0
    
    # Union-Find data structure for Hoshen-Kopelman algorithm
    # parent[i] stores the parent of cluster label i (0-indexed in parent array)
    # Negative values indicate root nodes, with magnitude = cluster size
    parent = []
    # flags[i] records which sides of the lattice cluster i touches, one bit per side
    # (1 = x first row, 2 = x last row, 4 = y first column, 8 = y last column). 15 means all four.
    flags = []
    
    # Find root of a cluster label (with path compression)
    # label is 1-indexed in clust array
    def find_root(label):
        label_idx = label - 1  # Convert to 0-indexed for parent array
        if parent[label_idx] < 0:
            return label_idx
        else:
            # Path compression: make parent point directly to root
            parent[label_idx] = find_root(parent[label_idx] + 1)  # Convert back to 1-indexed for recursive call
            return parent[label_idx]
    
    # Union two clusters
    # Both labels are 1-indexed
    def union_clusters(label1, label2):
        root1_idx = find_root(label1)
        root2_idx = find_root(label2)
        
        if root1_idx == root2_idx:
            return root1_idx  # Already in same cluster
        
        # Merge smaller into larger (union by size)
        if abs(parent[root1_idx]) < abs(parent[root2_idx]):
            root1_idx, root2_idx = root2_idx, root1_idx
        
        # Merge root2 into root1
        parent[root1_idx] += parent[root2_idx]  # Update size
        parent[root2_idx] = root1_idx  # Point to root1
        flags[root1_idx] |= flags[root2_idx]  # The merged cluster touches every side either one touched
        
        return root1_idx
    
    for step, site in enumerate(list_sites, start=1):
        x = ((site - 1) % L) + 1
        y = ((site - 1) // L) + 1
        x_idx = x - 1
        y_idx = y - 1
        edge = (x == 1) | (x == L) << 1 | (y == 1) << 2 | (y == L) << 3  # sides this site touches
        
        # Get neighbor cluster labels (1-indexed)
        neighbors = []
        if x > 1 and clust[x_idx - 1, y_idx] > 0:
            neighbors.append(clust[x_idx - 1, y_idx])
        if x < L and clust[x_idx + 1, y_idx] > 0:
            neighbors.append(clust[x_idx + 1, y_idx])
        if y > 1 and clust[x_idx, y_idx - 1] > 0:
            neighbors.append(clust[x_idx, y_idx - 1])
        if y < L and clust[x_idx, y_idx + 1] > 0:
            neighbors.append(clust[x_idx, y_idx + 1])
        
        if len(neighbors) == 0:
            # New isolated cluster
            new_label = len(parent) + 1  # 1-indexed label
            flags.append(edge)
            parent.append(-1)  # Root with size 1 (0-indexed in parent array)
            clust[x_idx, y_idx] = new_label
        else:
            # Merge with existing clusters
            # Find root of first neighbor (returns 0-indexed)
            root_idx = find_root(neighbors[0])
            
            # Union with all other neighbors
            for neighbor in neighbors[1:]:
                root_idx = union_clusters(root_idx + 1, neighbor)  # Convert root to 1-indexed for union
            
            # Assign root label to current site
            clust[x_idx, y_idx] = root_idx + 1  # Convert back to 1-indexed for storage
            parent[root_idx] -= 1  # Increase cluster size
            flags[root_idx] |= edge
        
        # Check for percolation: does the cluster containing this site touch all four sides?
        # This is O(1). (Calling percCheck(clust) here would cost O(L) per step, and it compares
        # raw labels, which go stale after unions, so it detects spanning late.)
        if flags[clust[x_idx, y_idx] - 1] == 15:
            percSite = [x, y]
            p = step / (L * L)
            break
    
    # Relabel clusters to use root labels everywhere (optional, for consistency)
    for i in range(L):
        for j in range(L):
            if clust[i, j] > 0:
                root_idx = find_root(clust[i, j])
                clust[i, j] = root_idx + 1  # Convert to 1-indexed
    
    return clust, percSite, p

## Code for part (e)
L_values = [7 * round(10**i) for i in np.linspace(1, 1.5, 10)]  # Run for a bunch of different sizes (may be tedious on slow computers)
ps = []  # Store the densities at which percolation occurs for each size
nIt = 100  # Number of iterations to average over for each size

for l in L_values:  # Loop through each size
    print(f"L = {l}")
    p_sum = 0.0
    for it in range(1, nIt + 1):
        _, _, p = percolate_improved(l)  # _, _ discards output that isn't needed
        p_sum += p
        if it % round(nIt/10) == 0:  # Print progress every 10% of the way through
            print(f"Iteration {it}")
    ps.append(p_sum / nIt)  # Store the average this L

xs = 1.0 / np.array(L_values)  # 1/L for each lattice size (one value per L)

plt.figure(figsize=(10, 6))
plt.scatter(xs, ps, s=2, linewidths=0)
plt.xlabel("1/L")
plt.ylabel("p")
plt.title("p vs. 1/L")

# Linear fit: p = x[0] + x[1]*(1/L)
A = np.column_stack([np.ones(len(xs)), xs])
b = np.array(ps)
x = np.linalg.lstsq(A, b, rcond=None)[0]

xp = np.linspace(0, max(xs), 100)
plt.plot(xp, x[0] + x[1] * xp, 'r-', linewidth=2, label=f'Fit: p = {x[0]:.4f} + {x[1]:.4f}/L')
plt.ylim(0.59, 0.65)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("percolation_p_vs_L.png", dpi=150)
plt.show()

# part (f)
"""
    forestFire(L, p)

Simulates a forest fire on a square lattice of size LxL. The forest is initialized with a probability p of having a tree. The fire starts at the left side and spreads naturally. Returns an array containing the iteration when each cell burned and the number of iterations it took to burn out.
"""

""" 
    canBurn(x, y, forest, burned)

checks if a site can burn: has a tree, not previously on fire
"""
def canBurn(x, y, forest, burned):
    if not (0 <= x < forest.shape[0] and 0 <= y < forest.shape[1]):
        return False  # site [x,y] is out of bounds
    if forest[x, y] == 1 and burned[x, y] == 0:  # Has tree, not burned yet
        return True
    return False

def forestFire(L, p):
    forest = np.zeros((L, L), dtype=int)
    n_trees = round(L * L * p)
    list_sites = np.random.permutation(L * L)[:n_trees]
    
    for site in list_sites:
        x = (site % L)
        y = (site // L)
        forest[x, y] = 1
    
    it = 1
    burned = np.zeros((L, L), dtype=int)
    burned = it * (1 - forest)  # Empty spaces get burned=1, trees get burned=0
    
    # Find all sites in first column (left side) that are not trees (start burning)
    burning_sites = []
    for i in range(L):
        if forest[i, 0] == 0:  # Not a tree in first column (left side)
            burning_sites.append((i, 0))
            burned[i, 0] = it
    
    while len(burning_sites) > 0:
        it += 1
        next_burning_sites = []
        for x, y in burning_sites:
            neighbors = [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]
            for nx, ny in neighbors:
                if canBurn(nx, ny, forest, burned):
                    if (nx, ny) not in next_burning_sites:
                        next_burning_sites.append((nx, ny))
                    burned[nx, ny] = it
        burning_sites = list(set(next_burning_sites))  # unique
        if it > 900:
            break
    
    return burned, it

xp = np.linspace(0.55, 0.62, 10)
yp = []
for ip in xp:
    nIt = 100
    avgIt = 0
    for i in range(nIt):
        _, it = forestFire(50, ip)
        avgIt += it
    yp.append(avgIt / nIt)

plt.figure(figsize=(10, 6))
plt.scatter(xp, yp, s=3, linewidths=0)
plt.xlabel("Occupation Probability (p)")
plt.ylabel("Average Time to Burnout")
plt.title("Burnout Time vs. Occupation Probability")
plt.xlim(0.38, 0.70)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("forestFireBurnoutTime.png", dpi=150)
plt.show()

# Visualization of a specific forest fire
L_vis = 50
burned, it = forestFire(L_vis, 0.59)

# We need to track forest to properly visualize
def forestFire_with_forest(L, p):
    """Same as forestFire but also returns forest state for visualization."""
    forest = np.zeros((L, L), dtype=int)
    n_trees = round(L * L * p)
    list_sites = np.random.permutation(L * L)[:n_trees]
    
    for site in list_sites:
        x = (site % L)
        y = (site // L)
        forest[x, y] = 1
    
    it = 1
    burned = np.zeros((L, L), dtype=int)
    burned = it * (1 - forest)  # Empty spaces get burned=1, trees get burned=0
    
    # Find all sites in first column (left side) that are not trees (start burning)
    burning_sites = []
    for i in range(L):
        if forest[i, 0] == 0:  # Not a tree in first column
            burning_sites.append((i, 0))
            burned[i, 0] = it
    
    while len(burning_sites) > 0:
        it += 1
        next_burning_sites = []
        for x, y in burning_sites:
            neighbors = [(x, y+1), (x, y-1), (x+1, y), (x-1, y)]
            for nx, ny in neighbors:
                if canBurn(nx, ny, forest, burned):
                    if (nx, ny) not in next_burning_sites:
                        next_burning_sites.append((nx, ny))
                    burned[nx, ny] = it
        burning_sites = list(set(next_burning_sites))  # unique
        if it > 900:
            break
    
    return burned, it, forest

burned, it, forest = forestFire_with_forest(L_vis, 0.59)

# Copy 1s from forest to burned (for unburned tree sites)
# Julia: burned[forest .== 1 .& burned .== 0] .= 1
burned_vis = burned.copy()
unburned_trees = (forest == 1) & (burned == 0)
burned_vis[unburned_trees] = 1  # Mark unburned trees as 1 for green color

# Custom palette: black (0), darkgreen (1), inferno gradient (2 to it)
inferno = cm.get_cmap('inferno')
color_list = ['black', 'darkgreen']  # Empty (0), Unburned trees (1)
if it >= 2:
    for i in range(2, it + 1):
        rgba = inferno((i - 2) / max(1, it - 2))
        color_list.append(to_hex(rgba))  # Convert RGBA tuple to hex string
else:
    color_list.append('orange')  # Fallback if it < 2

custom_cmap = ListedColormap(color_list)

plt.figure(figsize=(10, 10))
plt.imshow(burned_vis, aspect='equal', origin='lower', cmap=custom_cmap, 
           vmin=0, vmax=it)
plt.colorbar(label='Burn iteration')
plt.axis('off')
plt.title('Forest Fire Simulation')
plt.tight_layout()
plt.show()

# Make an animation of the burning process
# Julia: anim = @animate for i in sort(unique(burned))[3:end]
unique_burned = sorted(set(burned_vis.flatten()))
if len(unique_burned) > 2:
    unique_burned = unique_burned[2:]  # Skip 0 and 1 (black and darkgreen background)
else:
    unique_burned = unique_burned

print(f"Creating animation frames (this may take a while)...")
for frame_idx, i in enumerate(unique_burned[:50]):  # Limit to 50 frames for demo
    temp = burned_vis.copy()
    temp[temp > i] = 0  # Hide sites that burn after iteration i
    plt.figure(figsize=(8, 8))
    plt.imshow(temp, aspect='equal', origin='lower', cmap=custom_cmap, 
               vmin=0, vmax=i, colorbar=False)
    plt.axis('off')
    plt.title(f'Forest Fire - Iteration {i}')
    plt.tight_layout()
    plt.savefig(f'burning_frame_{frame_idx:04d}.png', dpi=100, bbox_inches='tight')
    plt.close()

print(f"Note: For full GIF animation, use imageio or similar library to combine frames.")
print(f"Animation frames saved. Total iterations: {it}")
