# DoublePendulumLangrangianLaypunoveExponent
The system uses Lagrangian Mechanics, yielding coupled nonlinear ODEs. Chaos is quantified via the Maximum Lyapunov Exponent (λ) by tracking two trajectories starting δZ₀ = 10⁻⁵ apart and measuring δZ(t). A positive λ confirms deterministic chaos through exponential divergence.


Proof of Chaos: Measuring the Lyapunov Exponent 📈
The double pendulum is a classic example of a nonlinear dynamical system exhibiting deterministic chaos. To model its motion, we use Lagrangian Mechanics, focusing on energy states rather than force vectors.
1. Generalized Coordinates
The system is defined by two angles, θ₁ and θ₂, measured from the vertical. The positions of the masses (m₁, m₂) are:
• Mass 1: x₁ = L₁ sin(θ₁), y₁ = -L₁ cos(θ₁)
• Mass 2: x₂ = x₁ + L₂ sin(θ₂), y₂ = y₁ - L₂ cos(θ₂)
2. Kinetic (T) & Potential (V) Energy
• T = ½m₁v₁² + ½m₂v₂²
• V = -(m₁ + m₂)gL₁ cos(θ₁) - m₂gL₂ cos(θ₂)
3. The Lagrangian & Equations of Motion
The Lagrangian is L = T - V. By applying the Euler-Lagrange Equation, we derive two coupled, non-linear second-order Ordinary Differential Equations (ODEs) for angular accelerations (where Δ = θ₁ - θ₂):
• θ̈₁ = [m₂g sin(θ₂) cos(Δ) - m₂ sin(Δ) (L₁θ̇₁² cos(Δ) + L₂θ̇₂²) - (m₁+m₂)g sin(θ₁)] / [L₁(m₁ + m₂ sin²(Δ))]
• θ̈₂ = [(m₁+m₂)(L₁θ̇₁² sin(Δ) - g sin(θ₂) + g sin(θ₁) cos(Δ)) + m₂L₂θ̇₂² sin(Δ) cos(Δ)] / [L₂(m₁ + m₂ sin²(Δ))]
4. Numerical Solution (RK45)
Since no analytical solution exists, we reduce the system to a state-space of four first-order ODEs: y = [θ₁, θ̇₁, θ₂, θ̇₂]. We solve this using the RK45 algorithm (Explicit Runge-Kutta), which captures the extreme sensitivity to initial conditions.
5. Quantifying Chaos: The Lyapunov Exponent (λ)
To mathematically prove the presence of chaos, we calculate the Maximum Lyapunov Exponent. This measures the exponential rate at which two trajectories diverge. By tracking the separation (δZ) between two pendulums starting with an initial difference of δZ₀ = 10⁻⁵, we calculate:
λ ≈ (1/t) ln(|δZ(t)| / |δZ₀|)
A positive λ indicates that the system is chaotic, meaning it "forgets" its initial state and becomes unpredictable over time—the formal definition of the Butterfly Effect.
