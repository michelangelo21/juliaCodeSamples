using Statistics
using Plots
using LaTeXStrings
using JLD2

pgfplotsx()
function plot_lattice(lattice::Array{Int8}, T::Number, fn::String = "lattice.tex")
    lat = heatmap(lattice,aspect_ratio=1.0,size=(800,800),grid=false,framestyle=(:box), colormap_name = "hot",legend=false) #blue=-1, red=1
    l::Int = size(lattice)[1]::Int
    hline!(lat,0.5:1:l+0.5, line=(:black))
    vline!(lat,0.5:1:l+0.5, line=(:black))
    title!(lat,"L=$l, T=$T")
    savefig(lat, fn)
    plot(lat)
end

function ising(L::Int, T::Number; MCS=230_000::Int, to_plot::Bool=false)
    #initialize random lattice, and indexes
    lattice = rand(Int8[-1,1], L, L)
    #lattice = ones(Int8,L,L)
    next_I = collect(2:L+1)
    prev_I = collect(0:L-1)
    next_I[L]=1 
    prev_I[1] = L
    
    # compute boltzmann factor as Dict
    boltzmann_factor = Dict{Int,Float64}(ΔE => exp(-ΔE / T) for ΔE = -8:4:8)

    #initial arrays (returned)
    magnetizations = zeros(0)
    energies = zeros(0)

    for k=1 : MCS
        for i=1:L, j=1:L
        #metropolis algorithm
            ΔE::Int = 2 * lattice[i,j] * (lattice[next_I[i],j] + lattice[prev_I[i],j] + lattice[i,next_I[j]] + lattice[i,prev_I[j]])
            w::Float64 = min(1, boltzmann_factor[ΔE])
            if rand() ≤ w
                lattice[i,j] *= -1
            end
        end

        if (30_000 < k && k%100 == 0)
            m_k::Float64 = abs(mean(lattice))
            push!(magnetizations, m_k)
            E::Float64 = 0.0
            for i=1:L, j=1:L
                E += 0.5 * lattice[i,j] * (lattice[next_I[i],j] + lattice[prev_I[i],j] + lattice[i,next_I[j]] + lattice[i,prev_I[j]])
            end
            push!(energies, E)
        end
    end
    if (to_plot)
        plot_lattice(lattice, T, "lattice_L$(L)_T$(trunc(Int,T)).png")
    end
    return magnetizations, energies
end

function run_MC(Ls::Array{Int}, Ts::Array{Float64})
    result = Dict{Int, Dict{Char, Dict{Float64,Float64}}}(l => Dict(c => Dict() for c in ['m','χ','C']) for l in Ls)
    Threads.@threads for (L,T) in collect(Iterators.product(Ls,Ts))
            magnetizations, energies = ising(L,T,to_plot=false,MCS=430_000)

            result[L]['m'][T] = mean(magnetizations)                                                    # mean magnetization        <m>
            result[L]['χ'][T] = L^2 / T * var(magnetizations, mean=result[L]['m'][T], corrected=false)  # magnetic susceptibility    χ
            result[L]['C'][T] = 1.0 / L^2 / T^2 * var(energies, corrected=false)                        # heat capacity              C
    end
    return result
end

function run_MC_one_thread(Ls::Array{Int},Ts::Array{Float64})
    for (L,T) in collect(Iterators.product(Ls,Ts))
        @time ising(L, T, MCS=430_000, to_plot=true)
    end
end


#= main =#
Ls = [6,20,70]
Ts = cat(0.5:0.05:1.75, 1.8:0.005:2.7, 2.75:0.05:3.5, dims=1)
result_ret = @time run_MC(Ls,Ts)
@save "result_ret_Ls_Ts_430.jld2" result_ret Ls Ts

#examples
Ls = [70]
Ts = [0.05, 2.269, 8.00]
@time run_MC_one_thread(Ls,Ts)


#= Plots =#
result = result_ret
plot()
for L in Ls
    plot!(result[L]['m'], markershape=:auto, label="L=$L", markersize=3, markerstrokealpha=0.1)
end
xlabel!(L"T^*")
ylabel!(L"<m>")
title!("Magnetization as a function of reduced temperature - random initial conditions", titlefontsize=10)
#savefig("magnetization.tex")

plot()
for L in Ls
    plot!(result[L]['χ'], markershape=:auto, label="L=$L", markersize=3, markerstrokealpha=0.1)
end
xlabel!(L"T^*")
ylabel!(L"\chi")
title!("Magnetic susceptibility as a function of reduced temperature - random initial conditions", titlefontsize=10)
#savefig("magnetic_suscepitibility.tex")

plot()
for L in Ls
    plot!(result[L]['C'], markershape=:auto, label="L=$L", markersize=3, markerstrokealpha=0.1)
end
xlabel!(L"T^*")
ylabel!(L"C \quad / k_B")
title!("Heat capacity as a function of reduced temperature - random initial conditions", titlefontsize=10)
#savefig("heat_capacity.tex")