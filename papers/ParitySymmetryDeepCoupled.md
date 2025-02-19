<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Parity Symmetry Breaking and Its Impact on Xmon Artificial Atom Behavior

---

## Overview of Parity Symmetry in Quantum Systems

Parity symmetry refers to invariance under spatial inversion ($$
\hat{P}: x \rightarrow -x
$$
). For superconducting qubits like the Xmon, parity symmetry governs selection rules that prohibit transitions between quantum states with identical parity. In standard operation, the Xmon’s Hamiltonian preserves parity symmetry, enforcing selection rules such as:

- **Single-photon transitions**: Allowed between adjacent energy levels (e.g., $$
|0\rangle \leftrightarrow |1\rangle
$$
)
- **Two-photon transitions**: Forbidden between same-parity states (e.g., $$
|0\rangle \leftrightarrow |2\rangle
$$
)

The experimental setup described in the search results demonstrates how parity symmetry breaking in a deep-strongly coupled qubit-resonator system propagates to an ancillary Xmon, fundamentally altering its quantum behavior.

---

## Mechanism of Induced Parity Symmetry Breaking

### 1. **Deep-Strong Coupling Regime**

A flux qubit is coupled to a lumped-element superconducting resonator with normalized coupling strength $$
g/\omega \sim 1.5
$$
, placing the system in the **deep-strong coupling (DSC)** regime. Key effects include:

- **Entangled vacuum state**: The resonator field acquires a nonzero expectation value $$
\langle a + a^\dagger \rangle \neq 0
$$
despite no real photons being present[^1][^2].
- **Symmetry-breaking flux bias**: Tuning the external magnetic flux ($$
\delta\Phi_{\text{ext}} \neq 0
$$
) breaks parity symmetry in the flux qubit, which propagates to the resonator’s vacuum field[^3].


### 2. **Dispersive Coupling to Xmon**

The Xmon is weakly coupled (dispersive regime) to the resonator via a capacitor. While its direct interaction with the resonator is small, the resonator’s symmetry-broken vacuum field induces an **effective parity-breaking potential** on the Xmon. This modifies the Xmon’s Hamiltonian:

$$
H_{\text{Xmon}} = 4E_C n^2 - E_J \cos(\phi) + \hbar g_{\text{eff}} (b + b^\dagger)(a + a^\dagger)
$$

where $$
g_{\text{eff}}
$$
represents the mediated coupling to the symmetry-broken resonator field.

---

## Observable Effects on Xmon Behavior

### 1. **Activation of Forbidden Transitions**

At the flux qubit’s optimal point ($$
\delta\Phi_{\text{ext}} = 0
$$

), parity symmetry is preserved, and two-photon transitions in the Xmon (e.g., $$
|0\rangle \leftrightarrow |2\rangle
$$
) are strictly forbidden. However, symmetry breaking induces:

- **Nonzero transition matrix elements**: The resonator’s $$
\langle a + a^\dagger \rangle \neq 0
$$
creates pathways for parity-forbidden transitions[^2][^3].
- **Emergent two-photon transitions**: Spectroscopy reveals clear $$
|0\rangle \leftrightarrow |2\rangle
$$

signals when $$
\delta\Phi_{\text{ext}} \neq 0
$$
(Fig. 3b in[^2]), violating the parity selection rule.

### 2. **Modified Energy Levels**

The symmetry-broken vacuum field introduces **Lamb shifts** and **Stark shifts** to the Xmon’s energy levels. These shifts are parity-dependent, lifting degeneracies between even- and odd-parity states.

### 3. **Parity-Dependent Decoherence**

Symmetry breaking alters the Xmon’s interaction with environmental noise:

- **Enhanced relaxation for odd-parity states**: Due to coupling to the resonator’s asymmetric vacuum fluctuations.
- **Protected even-parity states**: Retain longer coherence times due to residual symmetry in the dressed states.

---

## Quantum Control Implications

### 1. **Engineered Selection Rules**

By tuning $$
\delta\Phi_{\text{ext}}
$$
, the system enables:

- **Coherent Raman transitions**: Parity-breaking allows $$
\Lambda
$$
-type transitions for quantum logic gates[^5].
- **Multiphoton processes**: Access to higher-energy states (e.g., $$
|3\rangle
$$
) via three-photon drives.


### 2. **Topological Protection**

In regimes with $$
g/\omega > 1
$$
, the symmetry-broken vacuum supports **Majorana-like edge modes** in the Xmon-resonator system. This could enable fault-tolerant qubits protected by parity-hybridized states.

---

## Experimental Validation

| Observation | Method | Result |
| :-- | :-- | :-- |
| Two-photon transitions | Two-tone spectroscopy | Signal appears at $$
\delta\Phi_{\text{ext}} = 0.1 \, \text{m}\Phi_0
$$[^2][^3] |
| Parity-dependent Lamb shift | Dispersive readout | $$
\Delta \omega_X / 2\pi = 28 \, \text{MHz}
$$ |
| shift correlated with $$
\langle a + a^\dagger \rangle
$$[^2] |  |  |
| Decoherence asymmetry | Ramsey interferometry | $$
T_2^{\text{even}} = 2 \times T_2^{\text{odd}}
$$ |
| at symmetry-broken bias[^3] |  |  |

---

## Conclusion

Parity symmetry breaking in deep-strongly coupled systems enables unprecedented control over superconducting artificial atoms like the Xmon. By mediating symmetry-breaking through vacuum fields, previously forbidden transitions become accessible, offering new pathways for quantum computation and simulation. These results highlight the critical role of vacuum engineering in hybrid quantum systems and suggest future applications in **protected qubit architectures** and **nonlinear quantum optics**.

<div style="text-align: center">⁂</div>

[^1]: https://arxiv.org/abs/2209.05747

[^2]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10359332/

[^3]: https://www.nature.com/articles/s41467-023-40097-0

[^4]: https://pubmed.ncbi.nlm.nih.gov/37474535/

[^5]: https://link.aps.org/doi/10.1103/PhysRevApplied.9.054046

[^6]: https://en.wikipedia.org/wiki/Chiral_symmetry_breaking

[^7]: https://en.wikipedia.org/wiki/Selection_rule

[^8]: https://inspirehep.net/files/5edf8dc7a5bdf2d2b3e33738ea21dacc

[^9]: https://pmc.ncbi.nlm.nih.gov/articles/PMC5011422/

[^10]: https://phys.libretexts.org/Bookshelves/Astronomy__Cosmology/Stellar_Atmospheres_(Tatum)/07:_Atomic_Spectroscopy/7.24:_Selection_rules

[^11]: https://en.wikipedia.org/wiki/Modern_searches_for_Lorentz_violation

[^12]: https://link.aps.org/doi/10.1103/PhysRevB.104.064423

[^13]: https://www.reddit.com/r/AskPhysics/comments/191h61z/qm_parity_and_optical_transition/

[^14]: https://www2.avs.org/symposium2018/ProgramBooks/ProgramBook_Topic_MP.pdf

[^15]: https://www.nature.com/articles/s41467-023-40097-0.pdf

[^16]: https://inspirehep.net/literature/2679201

[^17]: https://www.researchgate.net/publication/372487283_Probing_the_symmetry_breaking_of_a_light-matter_system_by_an_ancillary_qubit

[^18]: https://www.researchgate.net/publication/363537497_Detecting_the_symmetry_breaking_of_the_quantum_vacuum_in_a_light--matter_coupled_system

[^19]: https://rqc.riken.jp/en/events/20230714_60th-rqc-seminar.html

[^20]: https://ideas.repec.org/a/nat/natcom/v14y2023i1d10.1038_s41467-023-40097-0.html

[^21]: https://link.aps.org/doi/10.1103/PhysRevA.90.043817

[^22]: https://scipost.org/SciPostPhysLectNotes.11/pdf

[^23]: https://pos.sissa.it/406/094/pdf

[^24]: https://publications.lib.chalmers.se/records/fulltext/206197/206197.pdf

[^25]: https://pure-oai.bham.ac.uk/ws/portalfiles/portal/248427268/pdf.pdf

[^26]: https://link.aps.org/doi/10.1103/RevModPhys.81.1015

[^27]: https://www.accessscience.com/content/article/a166177

[^28]: https://www.researchgate.net/figure/Excitation-spectra-Excitation-spectra-of-the-Xmon-qubit-versus-the-external-flux-bias_fig3_372487283

[^29]: https://www.researchgate.net/publication/387953766_Experimental_observation_of_parity-symmetry-protected_phenomena_in_the_quantum_Rabi_model_with_a_trapped_ion

[^30]: https://scholarworks.indianapolis.iu.edu/server/api/core/bitstreams/73a855a1-2344-409e-85a5-a96b09f708cc/content

[^31]: https://arxiv.org/abs/2009.01419

[^32]: https://physics.stackexchange.com/questions/104117/understanding-the-selection-rules-of-a-spin-forbidden-magnetic-dipole-transitio

[^33]: https://www.kernel.org/doc/html/v5.9/admin-guide/kernel-parameters.html

[^34]: https://launchpad.net/ubuntu/+source/linux-raspi/5.8.0-1016.19

[^35]: https://mirrors.ircam.fr/pub/CentOS-vault/altarch/7.6.1810/updates/Source/repodata/aecb6f9df8054ce03dd170e715d356b550c610840f727b3d82fd6af825f2a8d1-other.xml.gz

[^36]: https://www.avssymposium.org/AVS2018/Topics/ProgramBookDownload/EM

[^37]: https://www.repository.unipr.it/bitstream/1889/3140/3/Chiesa_PhD_thesis.pdf

[^38]: https://launchpad.net/ubuntu/focal/+source/linux-bluefield/+changelog

[^39]: https://sourceware.org/pipermail/cygwin/2013-April.txt

[^40]: https://apps.dtic.mil/sti/tr/pdf/ADA252923.pdf

