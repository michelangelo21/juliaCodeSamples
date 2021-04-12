using Plots
plotlyjs()

function Feven(ε, V₀, a)
    k = √(2 * (ε+V₀))
    κ = √(-2ε)
    return sin(k*a/2) - κ/k * cos(k*a/2)
end

function Fodd(ε, V₀, a)
    k = √(2 * (ε+V₀))
    κ = √(-2ε)
    return sin(k*a/2) + k/κ * cos(k*a/2)
end


# tabulating functions Feven i Fodd
function tabulate(V₀, a, Np)
    h = 0.99 * V₀ / (Np-1)
    FevenFodd_out = Array{Float64,2}(undef,Np,3)
    for iₚ in 1:Np
        ε = - V₀ + 0.001*V₀ + (iₚ-1)*h
        FevenFodd_out[iₚ,:] = [ε, Feven(ε, V₀, a), Fodd(ε, V₀, a)]
    end
    # plot(FevenFodd_out[:,1], FevenFodd_out[:,2:3], labels=["Feven","Fodd"])
    plt = plot(FevenFodd_out[:,1], FevenFodd_out[:,2], label="Feven", legend=:right)
    plot!(plt, FevenFodd_out[:,1], FevenFodd_out[:,3], label="Fodd")
    display(plt)
    return FevenFodd_out
end


FevenFodd_out = tabulate(0.6467085229953451, 3.966800146218089,100)


# searcing for eigen energies

function bisec(xₗ, xᵣ, ϵ, fun::Function, V₀, a)
    xl = xₗ
    xr = xᵣ

    if fun(xr, V₀, a) * fun(xl, V₀, a) > 0
        return "No 0 in specified range"
    end

    while xr-xl ≥ ϵ 
        xₘ = (xl + xr)/2
        if fun(xl, V₀, a) * fun(xₘ, V₀, a) ≤ 0
            fun(xₘ, V₀, a) == 0 && return xₘ
            xr = xₘ
        else
            xl = xₘ
        end
    end

    return (xl + xr)/2
end

function find_eigen_energies(V₀,a,how_many=Inf,ϵ=0.0001)
    Elevels = []
    ΔE = V₀ / 100
    # ϵ = V₀ / 1000
    E₁ = -V₀ + 0.001*V₀
    iₚ = 0
    while E₁ < -ΔE && iₚ < how_many
        E₂ = E₁ + ΔE
        #print(E₂)
        if Feven(E₁, V₀, a) * Feven(E₂, V₀, a) < 0
            iₚ += 1
            push!(Elevels, bisec(E₁, E₂, ϵ, Feven, V₀, a))
        end
        if Fodd(E₁, V₀, a) * Fodd(E₂, V₀, a) < 0
            iₚ += 1
            push!(Elevels, bisec(E₁, E₂, ϵ, Fodd, V₀, a))
        end
        E₁ = E₂
    end
    return Elevels
end

Elevels = find_eigen_energies(0.6467085229953451, 3.966800146218089)

# find parameters of given energies
function loss(V₀, a, E₁, E₂, ϵ=0.0001)
    try
        Ê₁, Ê₂ = find_eigen_energies(V₀,a,2,ϵ)[1:2]
        return (E₁ - Ê₁)^2 + (E₂ - Ê₂)^2
    catch err
        return Inf
    end
end


function find_params(E₁, E₂, V₀_max, a_max, ϵ=0.0001, Np=100)
    if E₂ < E₁
        E₁, E₂ = E₂, E₁
        println("Energies swapped (E₁ < E₂)")
    end
    #println(E₁, E₂)
    if E₂ > -0.2
        println("E₂ is close to 0, may give inaccurate results")
    end
    if ϵ < 1e-15
        ϵ = 1e-15
        println("ϵ changed to 1e15")
    end
    V₀, a = undef, undef
    Vₗ, Vᵣ = 0, V₀_max
    aₗ, aᵣ = 0, a_max
    for i in 1:100
        V₀s = range(Vₗ, Vᵣ; length=Np)
        as = range(aₗ, aᵣ; length=Np)
        loss_map = [loss(V₀,a,E₁,E₂,ϵ) for V₀ = V₀s, a = as]
        m, i_min = findmin(loss_map)
        V₀,a  = V₀s[i_min[1]], as[i_min[2]]
        println(i, "\t", m,"\t", i_min)
        if m < ϵ
            break
        end
        middle = Np ÷ 2
        i_min[1] > middle ? (Vₗ = V₀s[middle]) : (Vᵣ = V₀s[middle])
        i_min[2] > middle ? (aₗ = as[middle]) : (aᵣ = as[middle])
        # hmp = heatmap(as,V₀s,loss_map, xlabel="a", ylabel="V₀")
        # display(hmp)
    end
    return V₀, a, find_eigen_energies(V₀, a, 2, ϵ)
end

find_params(-0.5,-0.125, 1, 5, 1e-12)

# function TEST(V₀, a, ϵ=0.0000001)
#     try
#         Ê₁, Ê₂ = find_eigen_energies(V₀,a,2,ϵ)[1:2]
#         return Ê₁, Ê₂
#     catch err
#         try
#             Ê₁ = find_eigen_energies(V₀,a,2,ϵ)[1]
#             return Ê₁, Inf
#         catch err1
#             return Inf, Inf
#         end
#     end
# end
# TEST_a = collect(range(0,100; length=1000))
# TEST_map = [TEST(100,a) for a = TEST_a]
# E1 = first.(TEST_map)
# E2 = last.(TEST_map)
# plot(TEST_a,[E1,E2])
# TEST_map[2]
