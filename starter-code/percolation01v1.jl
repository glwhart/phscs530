using Plots
using Random

# Code for part (a)
# This is a really naive implementation of percolation. It works but it relies on an inefficient approach that scales as O(L^2) in the number of sites, L. It doesn't do anything clever to relabel sites when clusters merge.
"""
    percCheck(clust)

Checks if the cluster percolates. Returns true if the cluster percolates, false otherwise. Assumes that sites that are positive (>0) are part of the cluster. Percolation happens when *one* cluster touches all four sides of the simulation cell.  """
    function percCheck(clust)
        s1 = clust[1,:][clust[1,:].>0]
        s2 = clust[end,:][clust[end,:].>0]
        s3 = clust[:,1][clust[:,1].>0]
        s4 = clust[:,end][clust[:,end].>0]
        return !isempty(intersect(s1,s2,s3,s4))
    end

""" 
    percolate(L)

Models percolation on a square lattice of size LxL by occupying sites in a random order, one at a time, until a percolating cluster is formed. Returns an array containing the values of each site in the simulation cell, the x,y coordinates of the final site that caused percolation, and the fraction of sites occupied.
"""
function percolate(L)
    clust = zeros(Int,L,L); 
    list = randperm(L*L); # determine the order to occupy the sites
    percSite = [0,0]; # initialize this variable so that it is defined outside the loop
    p = 0; # fraction of sites occupied
    for (clab,site) in enumerate(list) # loop through the list of sites in random order
        x = mod(site-1,L)+1
        y = div(site-1,L)+1
        clust[x,y] = clab
        # check if neighboring sites are already occupied. Relabel them if so.
        if x > 1 && clust[x-1,y] > 0
            clust[clust .== clust[x-1,y]] .= clab
        end
        if x < L && clust[x+1,y] > 0
            clust[clust .== clust[x+1,y]] .= clab
        end
        if y > 1 && clust[x,y-1] > 0
            clust[clust .== clust[x,y-1]] .= clab
        end
        if y < L && clust[x,y+1] > 0
            clust[clust .== clust[x,y+1]] .= clab
        end
        if percCheck(clust)
            percSite = [x,y] # coordinates of the percolating site
            p = clab/(L*L) # fraction of sites occupied
            break
        end
    end    
    return clust, percSite, p
end


# Run the percolation simulation and visualize the clusters
L = 50 
clust, percSite, p = percolate(L)
# Visualize all the different clusters with different colors
heatmap(clust,aspect_ratio=:equal,legend=false,xlims=(0.5,L+.5),ylims=(0.5,L+.5),axis=false,color=:Paired,clims=(0,maximum(clust)),colorbar=true)

# Color the non-percolating sites gray, the percolating cluster yellow, and the final connecting site red
clust[(clust.>0) .& (clust.<clust[percSite...])] .= 1
clust[clust.==clust[percSite...]] .= 2
clust[percSite...] = 3
heatmap(clust,aspect_ratio=:equal,legend=false,xlims=(0.5,L+.5),ylims=(0.5,L+.5),axis=false,color=[:black,:gray,:lightyellow,:red],clims=(0,3))


## Code for part (b)
# Animated version that stops when percolation occurs
"""
    percolate_animated(L)

An animated version of the percolation simulation that stops when percolation occurs. Returns the labeled cluster, the coordinates of the percolating site, and the fraction of sites occupied. It creates an animation of the percolation process, showing the cluster at each step.
"""
function percolate_animated(L)
    clust = zeros(Int,L,L)
    list = randperm(L*L)
    percSite = [0,0]
    p = 0
    max_clab = 0
    
    # Create animation
    anim = @animate for (clab,site) in enumerate(list)
        x = mod(site-1,L)+1
        y = div(site-1,L)+1
        clust[x,y] = clab

        # check if neighboring sites are already occupied. Relabel them if so.
        if x > 1 && clust[x-1,y] > 0
            clust[clust .== clust[x-1,y]] .= clab
        end
        if x < L && clust[x+1,y] > 0
            clust[clust .== clust[x+1,y]] .= clab
        end
        if y > 1 && clust[x,y-1] > 0
            clust[clust .== clust[x,y-1]] .= clab
        end
        if y < L && clust[x,y+1] > 0
            clust[clust .== clust[x,y+1]] .= clab
        end
        # Create frame showing current cluster state
        heatmap(clust, aspect_ratio=:equal, legend=false, 
                xlims=(0.5,L+.5), ylims=(0.5,L+.5), axis=false,
                color=:tab10, clims=(0,clab), colorbar=true, 
                title="Step: $clab / $(L*L), p = $(round(clab/(L*L), digits=3))",size=(512,512))
        # Check for percolation and break if found
        if percCheck(clust)
            percSite = [x,y]
            p = clab/(L*L)
            break
        end
    end every 3
    return clust, percSite, p, anim
end

# Run the animated percolation. This takes a while at large image sizes and high resolutions. Mine took ~20 secs to run.
clust, percSite, p, anim = percolate_animated(50)

# Create MP4 video (it will stop at percolation). Could do an animated GIF but
# MP4 format supports higher frame rates and doesn't loop endlessly.
mp4(anim, "percolation_animation.mp4", fps=60)


## Code for part (d)
# Improved version of the percolation simulation using the Hoshen-Kopelman algorithm
"""
    percolate_improved(L)

Percolates a square lattice of size LxL using the Hoshen-Kopelman algorithm.
This is more efficient than the naive approach, using union-find to track clusters.
Returns the labeled cluster, the coordinates of the percolating site, and the fraction of sites occupied.
"""
function percolate_improved(L)
    clust = zeros(Int, L, L)
    list = randperm(L*L)
    percSite = [0, 0]
    p = 0.0
    
    # Union-Find data structure for Hoshen-Kopelman algorithm
    # parent[i] stores the parent of cluster label i
    # Negative values indicate root nodes, with magnitude = cluster size
    parent = Int[]
    # flags[i] records which sides of the lattice cluster i touches, one bit per side
    # (1 = x first row, 2 = x last row, 4 = y first column, 8 = y last column). 15 means all four.
    flags = Int[]
    
    # Find root of a cluster label (with path compression)
    function find_root(label)
        if parent[label] < 0
            return label
        else
            # Path compression: make parent point directly to root
            parent[label] = find_root(parent[label])
            return parent[label]
        end
    end
    
    # Union two clusters
    function union_clusters(label1, label2)
        root1 = find_root(label1)
        root2 = find_root(label2)
        
        if root1 == root2
            return root1  # Already in same cluster
        end
        
        # Merge smaller into larger (union by size)
        if abs(parent[root1]) < abs(parent[root2])
            root1, root2 = root2, root1
        end
        
        # Merge root2 into root1
        parent[root1] += parent[root2]  # Update size
        parent[root2] = root1  # Point to root1
        flags[root1] |= flags[root2]  # The merged cluster touches every side either one touched
        
        return root1
    end
    
    for (step, site) in enumerate(list)
        x = mod(site-1, L) + 1
        y = div(site-1, L) + 1
        edge = (x == 1) | (x == L) << 1 | (y == 1) << 2 | (y == L) << 3  # sides this site touches
        
        # Get neighbor cluster labels
        neighbors = Int[]
        if x > 1 && clust[x-1, y] > 0
            push!(neighbors, clust[x-1, y])
        end
        if x < L && clust[x+1, y] > 0
            push!(neighbors, clust[x+1, y])
        end
        if y > 1 && clust[x, y-1] > 0
            push!(neighbors, clust[x, y-1])
        end
        if y < L && clust[x, y+1] > 0
            push!(neighbors, clust[x, y+1])
        end
        
        if isempty(neighbors)
            # New isolated cluster
            new_label = length(parent) + 1
            push!(parent, -1)  # Root with size 1
            push!(flags, edge)
            clust[x, y] = new_label
        else
            # Merge with existing clusters
            # Find root of first neighbor
            root = find_root(neighbors[1])
            
            # Union with all other neighbors
            for neighbor in neighbors[2:end]
                root = union_clusters(root, find_root(neighbor))
            end
            
            # Assign root label to current site
            clust[x, y] = root
            parent[root] -= 1  # Increase cluster size
            flags[root] |= edge
        end
        
        # Check for percolation: does the cluster containing this site touch all four sides?
        # This is O(1). (Calling percCheck(clust) here would cost O(L) per step, and it compares
        # raw labels, which go stale after unions, so it detects spanning late.)
        if flags[clust[x, y]] == 15
            percSite = [x, y]
            p = step / (L*L)
            break
        end
    end
    
    # Relabel clusters to use root labels everywhere (optional, for consistency)
    for i in 1:L
        for j in 1:L
            if clust[i, j] > 0
                clust[i, j] = find_root(clust[i, j])
            end
        end
    end
    
    return clust, percSite, p
end

## Code for part (e)
L =  [7*round(Int,10^i) for i in range(1,1.5,10)] # Run for a bunch of different sizes (may be tedious on slow computers)
ps = Real[] # Store the densities at which percolation occurs for each size
nIt = 100 # Number of iterations to average over for each size 
@time for l in L # Loop through each size
    println("L = $l")
    p_sum = 0.0
    for it in 1:nIt
        _, _, p = percolate_improved(l) # _, _ discards output that isn't needed
        p_sum += p
        if mod(it,round(Int,nIt/10)) == 0 # Print progress every 10% of the way through 
            println("Iteration $it")
        end
    end
    push!(ps, p_sum/nIt)  # Store the average this L
end
xs = 1.0./L  # 1/L for each lattice size (one value per L)
plot(xs,ps,xlabel="L",ylabel="p",title="p vs. L",st=:scatter,msw=0,ms=2,legend=false)

A = hcat(ones(length(xs)),xs)#,xs.^2) #,xs.^3);
b = ps;
x = A\b
xp = range(0,maximum(xs),100)
plot!(xp,x[1].+x[2].*xp#.+x[3].*xp.^2 #.+x[4].*xp.^3 .+x[1]
,xlabel="1/L",ylabel="p",title="p vs. 1/L",st=:line,lw=2,ylims=(0.59,0.65))
savefig("percolation_p_vs_L.png")


# part (f)
"""
    forestFire(L,p)

Simulates a forest fire on a square lattice of size LxL. The forest is initialized with a probability p of having a tree. The fire starts at the left side and spreads naturally. Returns an array containing the iteration when each cell burned and the number of iterations it took to burn out.
"""
function forestFire(L,p)

""" 
    canBurn(x,y,forest,onfire)

checks if a site can burn: has a tree, not previously on fire"""    
function canBurn(x,y,forest,burned)
    if !(1 <= x <= size(forest,2) && 1 <= y <= size(forest,1))
        return false # site [x,y] is out of bounds
    end
    if forest[x,y] == 1 && burned[x,y] == 0 # Has tree, not burned yet
        return true
    end
    return false
end

forest = zeros(Int,L,L)
list = randperm(L*L)[1:round(Int,L*L*p)]
for site in list    
    x = mod(site-1,L)+1
    y = div(site-1,L)+1
    forest[x,y] = 1
end    
it = 1
burned = zeros(Int,L,L)
burned = it*(1 .- forest)
# Find all Cartesian indices where element is 1 and in first column
burning_sites = [CartesianIndex(i, 1) for i in 1:L if forest[i,1] == 0]
for site in burning_sites
    burned[site.I...] = it
end
while burning_sites != []
    it += 1
    #println("It: $it")
    next_burning_sites = []
    for site in burning_sites 
        x, y = site.I
        #println("site: ",(x,y))
        neighbors = [CartesianIndex(x,y+1), CartesianIndex(x,y-1), CartesianIndex(x+1,y), CartesianIndex(x-1,y)]
        for ineigh in neighbors
            if canBurn(ineigh.I...,forest,burned)
                push!(next_burning_sites, ineigh)
                #println("next_burning_sites",ineigh)
                burned[ineigh.I...] = it
            end
        end
    end 
    burning_sites = unique(next_burning_sites)
    if it > 900
        break
    end
end
return burned, it
end

xp = range(0.55,0.62,10)
yp = Float64[]
for ip in xp
nIt = 100
avgIt = 0
for i in 1:nIt
    _, it = forestFire(50,ip)
    avgIt += it
end
push!(yp, avgIt/nIt)
end
plot!(xp,yp,xlabel="Occupation Probability (p)",ylabel="Average Time to Burnout",title="Burnout Time vs. Occupation Probability",st=:scatter,msw=0,ms=3,legend=false,xlims=(0.38,0.70))
savefig("forestFireBurnoutTime.png")



# T
# Copy 1s from forest to burned (for unburned tree sites)
burned[forest .== 1 .& burned .== 0] .= 1

# Custom palette: black (0), darkgreen (1), inferno gradient (2 to it)
using Colors
color_palette = vcat([colorant"darkgreen"], [colorant"black"], [cgrad(:inferno)[(i-2)/(it-2)] for i in 2:it])
heatmap(burned,aspect_ratio=:equal,legend=false,xlims=(0.5,L+.5),ylims=(0.5,L+.5),axis=false,clims=(0,it),colorbar=true,color=color_palette)

# Make an animation of the burning process
anim = @animate for i in sort(unique(burned))[3:end]
    temp = copy(burned)
    temp[temp .> i] .= 0
    heatmap(temp,aspect_ratio=:equal,legend=false,xlims=(0.5,L+.5),ylims=(0.5,L+.5),axis=false,clims=(0,i),colorbar=false,color=color_palette,size=(800,800))
end
gif(anim, "burning_animation.gif", fps=10)
