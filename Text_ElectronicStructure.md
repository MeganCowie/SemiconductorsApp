## Electronic Structure

We will start by giving a very brief overview of the free electron model (a.k.a. the Sommerfeld model) and the nearly free electron model (a.k.a. the weak binding model). I won't provide a full derivation here, but will rather outline some key points. Firstly, we find the energy of a free electron: Considering only the particle's kinetic energy ($E=\frac{p^2}{2m}$) and the de Broglie wave-particle duality theory ($\lambda=\frac{h}{p}$) we find the dispersion relation of a free electron:

$$E=\frac{\hbar^2 k^2}{2m}$$

In three dimensions, the free electron density of states is:

$$g(E)=\frac{1}{2\pi^2}\left(\frac{2m}{\hbar^2}\right)^{3/2}\sqrt{E}$$

If a particle is not completely free, but rather is influenced by the small periodic perturbation of the lattice, it does not have the parabolic dispersion given above. Rather, a nearly free electron (weak binding model) leads to forbidden values in the dispersion function, or band gaps. In a semiconductor, the levels up to the bottom of a band gap are occupied (by electrons), and levels above the band gap are unoccupied (by electrons) at zero temperature at equilibrium. So it is generally more useful to think of holes in the valence band, since they are the particles involved in valence band transport. At the edge of each gap the energy is nearly parabolic, so we can approximate the energy near the band gap edge:

$$E=\frac{\hbar^2 k^2}{2m_n}+E_C$$
$$E=-\frac{\hbar^2 k^2}{2m_p}+E_V$$

where $E_C$ is the energy lowest energy above the gap (conduction band energy) and $E_V$ is the highest energy below the gap (valence band energy). Following directly from the equations above, we can find the density of states of the valence and conduction bands:

$$g_c(E)=\frac{1}{2\pi^2}\left(\frac{2m_n}{\hbar^2}\right)^{3/2}\sqrt{E-E_C}$$
$$g_v(E)=\frac{1}{2\pi^2}\left(\frac{2m_p}{\hbar^2}\right)^{3/2}\sqrt{E_V-E}$$

where $g_c(E)$ is the density of electron states in the conduction band and $g_v(E)$ is the density of hole states in the valence band. Whether a material is metallic or semiconducting is defined by the occupation of the bands. The effective mass of the electron and hole, respectively, are given by $m_n$ and $m_p$. In general, the effective mass $m^*$ is:

$$m^*\equiv \hbar^2\left(\frac{\partial^2 E}{\partial k^2}\right)^{-1}$$

i.e. the effective mass is defined by the band curvature. For the free electron model, this gives a constant mass for all E and all k, equal to the electron rest mass, $m=m_e$. For the nearly free model, the effective mass depends on the $E-k$ landscape, which varies from band to band. In general, $m_p>m_n$, i.e. the curvature of the conduction band is usually greater than that of the valence band.

Therefore, we can see that the parabolic band edge approximation is directly reflected in the effective mass. If the band edge is parabolic, the effective mass is constant. If there are non-parabolic corrections, the effective mass is not constant. In general, in real materials the band edge is anisotropic, and so the effective mass is better represented by a three-dimensional tensor. All of the carrier density derivations to follow are done with the approximation that the effective mass is isotropic, and $m_n\approx m_p$. Note that the effective $m_n$ and $m_p$ are both positive. Why is the negative sign for the holes accounted for in the dispersion relation rather than the effective mass, given that the valence band curvature is negative? This is because the effective mass of an electron in the valence band is negative, but not so for the hole.
