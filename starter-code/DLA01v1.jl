using Plots
using LinearAlgebra

""" 
    randomStep([x,y])

Returns a random step from the current position, [x,y]. The step is 1 step to the left or right, or up or down."""
function randomStep(pos)
    return pos + rand([[-1,0],[1,0],[0,-1],[0,1]])
end

"""
    walkerStart(rstart)

Returns a random starting position for a walker. The starting position is a distance rstart from the origin, at a random angle.
"""
function walkerStart(rstart,rad)
     theta = 2π*rand()
    return round.(Int, rstart * [cos(theta), sin(theta)])+[rad+1,rad+1]
end

"""
    clusterCheck(position,cluster,radius)

Checks if the position is part of the cluster (if it is inside the box).
"""
function clusterCheck(position,cluster,radius)
    if !(any(position .< 1) || any(position .> 2*radius+1)) && cluster[position[1],position[2]] > 0
        return true
    end
    return false
end

rad = 200 # Smaller than 50 will give poor statistics, bigger than 200 takes too long to run (depending on your computer)
rstart = 2  
clust = zeros(Int,2*rad+1,2*rad+1);
clust[rad+1,rad+1] = 1
done = false
count = 0
while !done # keep starting walkers until the cluster touches the boundary
    pos = walkerStart(rstart,rad)
    while true # keep stepping until the walker wanders off or sticks to the cluster
        newpos = randomStep(pos) # take a random step
        #println("New position: ", newpos)
        if norm(newpos-[rad+1,rad+1]) > 1.5*rstart # if the walker wanders off, start a new walker 
            break
        end
        # If the walker is inside the box and touches the cluster, stick it to the cluster
        if clusterCheck(newpos,clust,rad)
            count += 1
            clust[pos[1],pos[2]] = count # keep track of the order so that we can make an animation later
            # Extend the starting radius, if necessary
            rstart = max(rstart, ceil(norm(newpos-[rad+1,rad+1]))+2)
            # If the cluster touches any boundary, the simulation is done
            if any(pos .== [1,1]) || any(pos .== [2*rad+1,2*rad+1])
                done = true
            end
            break
        end
        pos = newpos
    end
    if done # Cluster touches the boundary
        break
    end
    if mod(count,1000) == 0 # Just so we know it's still running
        println("Count: ", count)
    end
end
#heatmap(clust,aspect_ratio=:equal,legend=false,xlims=(1,2*rad+1),ylims=(1,2*rad+1),axis=false)

# Get cluster points, coordinates of nonzero values in clust
cp = findall(!iszero, clust)
x_cp = [coord[1] for coord in cp]
y_cp = [coord[2] for coord in cp]

# Create scatter plot (adjust markersize depending on the radius of the cluster, `rad`)
scatter(x_cp, y_cp, aspect_ratio=:equal, legend=false, 
        xlims=(1,2*rad+1), ylims=(1,2*rad+1), 
        markersize=1, markerstrokewidth=0, axis=false,color=:black)

# Get distances from the center of the cluster
dists = [norm([c[1],c[2]]-[rad+1,rad+1]) for c in cp]

# compute m(r) and plot on log scale. Like Fig. 7.20 in "Random Systems" Chap. 7 of Giordano
xr = 10:round(Int,rad/2) # Skip the first few points which have larger jitter due to the discrete lattice
mr = [sum(dists.<r) for r in xr]
plot(xr,mr,xlabel="Radius",ylabel="Number of particles",title="Number of particles vs. Radius",axis=:log10,st=:scatter,msw=0,ms=2)

# Fit a line to the log of the data
A =  hcat(ones(length(xr)),log10.(xr))
b = log10.(mr)
x = A\b # Solve the linear system to find the slope and intercept
begin # Wrapping the plot in begin/end block executes all the plot commands at once
plot(log10.(xr),log10.(mr),xlabel="Radius",ylabel="Number of particles",title="Number of particles vs. Radius",st=:scatter,msw=0,ms=2,label="Data")
plot!(log10.(xr),x[2]*log10.(xr).+x[1],xlabel="Radius",ylabel="Number of particles",title="Number of particles vs. Radius",st=:line,lw=2,label="Fit")
annotate!(log10.(xr)[end]*0.9, log10.(mr)[end]*0.8, text("Slope: $(round(x[2], digits=3))", :left, 10))
end

# Animate the growth of the cluster, just for fun 
lcp = maximum(clust) # last cluster point
fs = max(1, lcp ÷ 200) # frame step. ÷ is the integer division operator (like // in python)
frames = [1:fs:lcp; lcp; repeat([lcp], 30)]  # Repeat last frame 30 times to give the animation a "pause" at the end

anim = @animate for frame in frames
    mask = clust .> 0 .&& clust .<= frame # mask to get all cluster points in the current frame
    cp_frame = findall(mask) # get the cluster point coordinates in the current frame
    x_frame = [coord[1] for coord in cp_frame]
    y_frame = [coord[2] for coord in cp_frame]
    colors_frame = [clust[coord[1], coord[2]] for coord in cp_frame]
    
    scatter(x_frame, y_frame, 
            aspect_ratio=:equal, 
            legend=false,
            xlims=(1,2*rad+1), 
            ylims=(1,2*rad+1),
            markersize=0.8, # Adjust this depending on the radius of the cluster, `rad`
            markerstrokewidth=0,
            axis=false,
            zcolor=colors_frame, # color the points by the cluster number
            colorbar=false,
            color=:viridis,
            clims=(1, lcp),
            title="DLA Cluster Growth (n = $frame)",
            dpi=300)
end every 1

gif(anim, "julia-src/DLA_cluster_growth.gif", fps=15)

