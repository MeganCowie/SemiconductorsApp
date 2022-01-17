## Carrier Statistics

Let's start by looking at the center of an infinitely large crystalline semiconductor. Below follows the standard derivation of semiconductor carrier density in such a sample. From first principles, we take the electron (n) and hole (p) densities as:

$$n = \int_{E_C}^{\infty} g_c(E) f_F(E) dE$$

$$p = \int_{-\infty}^{E_V} g_v(E) \left(1-f_F(E)\right) dE$$

where $f_{F}(E)=\left( 1+exp\left(\frac{E-E_f}{k_BT}\right)\right)^{-1}$ is the Fermi-dirac distribution, where the Fermi level $E_f$ is defined by $f_F(E_f)=1/2$. Spin degeneracy of the conduction and valence levels is accounted for by the density of states $g_c(E)$ and $g_v(E)$. $f(E)$ is the probability of finding an electron in a state with energy $E$ and $(1-f(E))$ is the probability of finding a hole in a state with energy $E$. Of course, in setting the limits of these integrals we have assumed zero temperature, but if the band gap is much greater than thermal smearing ($\sim25$meV), we take this approximation is valid even at room temperature. A typical band gap is on the order of 1~eV, so this is a standard approximation.
