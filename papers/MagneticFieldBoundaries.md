<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Magnetic Fields as Boundary Constraints in GS-DeepNet's Plasma Equilibrium Reconstruction

---

## Magnetic Boundary Conditions in the Grad-Shafranov Framework

### Governing Equations and Measurement Constraints

The Grad-Shafranov (GS) equation governs axisymmetric magnetohydrodynamic (MHD) equilibria in tokamaks:

$$
\Delta^* \psi = -\mu_0 R^2 \frac{dp}{d\psi} - F\frac{dF}{d\psi}
$$

where $$
\psi
$$

is the poloidal magnetic flux, $$
p
$$

the plasma pressure, and $$
F
$$
the poloidal current function. GS-DeepNet solves this nonlinear partial differential equation using **externally measured magnetic fields** as boundary conditions, specifically:

1. Radial ($$
B_R
$$

) and vertical ($$
B_Z
$$
) poloidal magnetic field components from pickup probes
2. Poloidal flux ($$
\psi_{FL}
$$

) measurements from flux loops

These measurements constrain the solution at the tokamak's vacuum vessel wall (Fig. 1), providing:

- **Dirichlet conditions** for $$
\psi
$$
at flux loop locations
- **Neumann conditions** through derivatives of $$
\psi
$$

related to $$
B_R
$$

and $$
B_Z
$$

---

## Architectural Implementation of Magnetic Diagnostics

### Maxwell Net: Embedding Field Measurements

GS-DeepNet's first neural network module ($$
NN_\Theta^1
$$
) directly ingests magnetic diagnostics as structured inputs:
\$\$

Input = \left[ B_R^{MD}(r_i), B_Z^{MD}(r_i), \psi_{FL}^{MD}(r_j) \right]

\$\$

where $$
r_i
$$

and $$
r_j
$$

denote spatial positions of 31 magnetic probes and 45 flux loops respectively. The network output is the poloidal flux distribution $$
\psi(R,Z)
$$
across a 41×41 grid, constrained by:
\$\$

\psi_{network}(R_{wall}, Z_{wall}) = \psi_{FL}^{MD}

\$\$

$$
\frac{\partial \psi}{\partial R}\bigg|_{\text{wall}} = -B_Z^{MD}, \quad \frac{\partial \psi}{\partial Z}\bigg|_{\text{wall}} = B_R^{MD}
$$

This architecture enforces Maxwell's equations at the boundary through a custom loss function:

$$
\mathcal{L}_{\text{Maxwell}} = \sum \left( B_{R/Z}^{\text{pred}} - B_{R/Z}^{MD} \right)^2 + \lambda \left( \psi_{\text{FL}}^{\text{pred}} - \psi_{FL}^{MD} \right)^2
$$

with $$
\lambda
$$
balancing flux versus field measurement uncertainties[^1][^2].

---

## Magnetic Field Roles in Plasma Boundary Detection

### Last Closed Flux Surface (LCFS) Identification

The auxiliary boundary detection module uses magnetic field-derived $$
\psi
$$
to locate the LCFS through:
1. **Magnetic X-point detection**:
\$\$

\nabla \psi|_{X-point} = 0 \Rightarrow B_R = B_Z = 0

\$\$

2. **Flux surface topology classification**:
    - Limited plasmas: $$
\psi_{\text{LCFS}}
$$
determined by inner wall contact
    - Diverted plasmas: $$
\psi_{\text{LCFS}}
$$
set by X-point location

Magnetic measurements resolve the $$
\psi
$$
gradient ambiguity inherent to free-boundary GS solutions, reducing LCFS position errors to <2 cm in KSTAR experiments[^1].

---

## Field Continuity and Neural Network Regularization

### Physics-Informed Constraints

GS-DeepNet incorporates electromagnetic continuity conditions through architectural constraints:

1. **Perpendicular B-field continuity** (from $$
\nabla \cdot \mathbf{B} = 0
$$
):
\$\$

B_{\perp, plasma} = B_{\perp, vacuum}

\$\$

enforced via skip connections between plasma/vacuum region networks
2. **Parallel H-field continuity** (assuming no wall currents):

$$
\mathbf{H}_{\parallel, \text{plasma}} = \mathbf{H}_{\parallel, \text{vacuum}}
$$

implemented through shared $$
\mu_0
$$
normalization across all layers
3. **Toroidal flux conservation**:

$$
\oint B_\phi dl = \mu_0 I_p
$$

with total plasma current $$
I_p
$$
from Rogowski coils included as input

---

## Performance Metrics and Validation

### Magnetic Consistency in KSTAR Experiments

GS-DeepNet achieves sub-1% normalized errors in boundary field reconstruction:


| Quantity | RMS Error | Correlation Coefficient |
| :-- | :-- | :-- |
| $$
B_R
$$ |  |  |
| (mT) | 0.32 | 0.997 |
| $$
B_Z
$$ |  |  |
| (mT) | 0.29 | 0.998 |
| $$
\psi_{FL}
$$ |  |  |
| (Wb) | 0.021 | 0.999 |

The model maintains $$
\chi^2 < 1.5
$$
across 10,000+ KSTAR discharges, outperforming traditional EFIT solvers in real-time applications by 10× speedup with equivalent accuracy[^1][^2].

---

## Implications for Fusion Control Systems

### Real-Time Equilibrium Feedback

By providing magnetic field-constrained equilibria at 10 kHz rates, GS-DeepNet enables:

1. **Active position control**:  $$
\delta R_{\text{plasma}} < 0.5
$$

mm through $$
B_R/B_Z
$$
-guided actuation
2. **Divertor heat load management**:  $$
\psi_{\text{LCFS}}
$$

-based impurity injection timing

3. **Disruption prediction**:  Early detection of vertical displacement events via $$
\partial B_Z/\partial t
$$
anomalies

The integration of raw magnetic diagnostics directly into the neural architecture eliminates traditional signal processing latencies, achieving 500 μs response times critical for burning plasma regimes.

---

The GS-DeepNet framework demonstrates that magnetic field boundary conditions are not merely constraints but **active participants** in the equilibrium reconstruction process. By encoding Maxwell's equations into the neural network's loss landscape and architecture, the model achieves physics-consistent solutions while maintaining the computational efficiency required for next-step fusion devices. Future extensions will incorporate vector magnetic tomography for 3D equilibrium reconstructions, further leveraging advances in high-density magnetic diagnostics.

<div style="text-align: center">⁂</div>

[^1]: https://www.nature.com/articles/s41598-023-42991-5

[^2]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10516960/

[^3]: https://phys.libretexts.org/Bookshelves/Electricity_and_Magnetism/Electromagnetics_and_Applications_(Staelin)/02:_Introduction_to_Electrodynamics/2.06:_Boundary_conditions_for_electromagnetic_fields

[^4]: https://www.researchgate.net/publication/374116696_GS-DeepNet_mastering_tokamak_plasma_equilibria_with_deep_neural_networks_and_the_Grad-Shafranov_equation

[^5]: https://www.researchgate.net/figure/Equilibrium-prediction-using-the-trained-GS-DeepNet-a-First-column-example-of-limited_fig3_374116696

[^6]: https://www.youtube.com/watch?v=AwSxY7E7dTA

[^7]: https://osiris-code.github.io/osiris/other/boundary_conditions

[^8]: https://www.semanticscholar.org/paper/Deep-neural-network-Grad–Shafranov-solver-with-Joung-Kim/526ecfa2c774af9e07f334ac1bbdef54c05bda33

[^9]: https://galileoandeinstein.phys.virginia.edu/Elec_Mag/2022_Lectures/EM_34_Magnetostatic_Bdry_Conds.html

[^10]: https://www.antenna-theory.com/tutorial/electromagnetics/magnetic-field-boundary-conditions.php

[^11]: https://space.mit.edu/RADIO/CST_online/mergedProjects/3D/special_solvopt/special_solvopt_boundary_conditions_boundaries.htm

[^12]: https://engineering.purdue.edu/wcchew/ece604f20/Lecture Notes/Lect4.pdf

[^13]: https://www.nature.com/articles/s41586-021-04301-9

[^14]: https://pubs.aip.org/aip/pop/article/31/8/082507/3307563/Augmenting-machine-learning-of-Grad-Shafranov

[^15]: https://pubs.aip.org/aip/pop/article-pdf/doi/10.1063/5.0213625/20106149/082507_1_5.0213625.pdf

