## Carrier Statistics

Let's start by looking at the center of an infinitely large crystalline semiconductor. Below follows the standard derivation of semiconductor carrier density in such a sample. From first principles, we take the electron (n) and hole (p) densities as:

$$n = \int_{E_C}^{\infty} g_c(E) f_F(E) dE$$

$$p = \int_{-\infty}^{E_V} g_v(E) \left(1-f_F(E)\right) dE$$

where $f_{F}(E)=\left( 1+exp\left(\frac{E-E_f}{k_BT}\right)\right)^{-1}$ is the Fermi-dirac distribution, where the Fermi level $E_f$ is defined by $f_F(E_f)=1/2$. Spin degeneracy of the conduction and valence levels is accounted for by the density of states $g_c(E)$ and $g_v(E)$. $f(E)$ is the probability of finding an electron in a state with energy $E$ and $(1-f(E))$ is the probability of finding a hole in a state with energy $E$. Of course, in setting the limits of these integrals we have assumed zero temperature, but if the band gap is much greater than thermal smearing ($\sim25$meV), we take this approximation is valid even at room temperature. A typical band gap is on the order of 1~eV, so this is a standard approximation.

At relevant energetic scales, we find that the Fermi-Dirac distribution (quantum) approaches the Maxwell-Boltzmann distribution (classical), given by $f_M(E)=exp\left(\frac{E_f-E}{k_BT}\right)$. Therefore, the integrals above are rewritten as:

$$n = \int_{E_C}^{\infty} g_c(E) f_M(E) dE$$

$$p = \int_{-\infty}^{E_V} g_v(E) \left(1-f_M(E)\right) dE$$

Throughout this text I have been careless with my use of the Fermi function $E_f$, rather than the chemical potential $\mu$. Strictly speaking, $E_f$ is only defined at zero temperature, and as the temperature increases, $\mu$ and $E_f$ deviate. Up to room temperature, however, $\mu$ and $E_f$ agree to a high degree of precision, so I used $E_f$ to match the notation in semiconductor texts. But for a solid state physicist or for high temperature experiments, everywhere I have written $E_f$ should be replaced with $\mu$.

Equipped with the weak binding density of states $g_c(E)$ and $g_v(E)$ we can solve the integrals above. The solution yields:

$$n = N_C\:exp\left(\frac{E_f-E_C}{k_BT}\right)$$
$$p = N_V\:exp\left(\frac{E_V-E_f}{k_BT}\right)$$

where we have defined an "effective number of states", $N_C$ and $N_V$, of the conduction and valence band respectively. This solution is generically true.


### Intrinsic Semiconductors

If a semiconductor is intrinsic (that is, completely free of dopants and defects), $n$ and $p$ are necessarily equal, due to charge conservation. The Fermi level of the intrinsic semiconductor, $E_i$, is mid-gap: $E_i=\frac{E_g}{2}$, where $E_g=E_C-E_V$. (Note that this is in fact an approximation: $E_i$ lies only exactly mid-gap if the effective masses of the majority and minority carriers are equal. Simply subbing both of these definitions into the $n$ and $p$ equations above gives the intrinsic carrier density ($n_i=n=p$) as:

$$n_i = \sqrt{N_CN_V}\:exp\left(\frac{-E_g/2}{k_BT}\right)$$

Given this expression, we can see that while $n_i=n=p$ is only true in the case of intrinsic semiconductors, since $Eg=E_C-E_V$ is true by definition, it is always true that:

$$n\times p =N_C N_V = exp\left(\frac{-E_g}{k_BT}\right)$$


This result is true in the case of both intrinsic and extrinsic semiconductors, and does not demand that the electron and hole effective masses be equal. This result is useful, but except for the very particular intrinsic semiconductor case where we say that $E_f=E_i=\frac{E_g}{2}$,  we cannot use it to determine the Fermi energy, which is arguably the most important energetic quantity in a semiconductor system, since it is not generally true that $E_f = E_i$.


### Extrinsic Semiconductors

An intrinsic semiconductor that has been doped or has defects is called an extrinsic semiconductor. A dopant/defect necessarily has a bond mismatch with the intrinsic lattice, meaning that in some way it modifies the density of states $g(E)$. Of particular relevance are cases where dopants/defects introduce localized states inside the band gap, as this modifies the transport dynamics. If a dopant has excess electrons as compared to the intrinsic lattice, this means that it introduces extra electron states, and n-type (electron) conduction occurs in the conduction band. If the dopant lacks electrons as compared to the intrinsic lattice, it has extra hole states, so p-type (hole) conduction occurs in the valence band. The mechanism of these transport dynamics is explained below.

In the case of the n-type semiconductor, the mid-gap states have an energy $\Delta E_D$ below the conduction band edge, such that $E_D$ is the ionization energy of the dopant/defect. If the electron in this state is excited (thermally or otherwise) into the conduction band, current flows in the form of electrons through the conduction band, such that the total density electrons in the conduction band $n_c$ is:

$$n=n_D^++p$$

where $n_D^+$ is the density of thermally ionized donors and p, as before, is the density of holes in the valence band (and therefore, by conservation, the density of electrons that have been thermally excited across the band gap). In the case of the p-type semiconductor, the mid-gap states have an energy $\Delta E_A$ above the valence band edge, such that $E_A$ is the electron affinity (energy) of the dopant/defect. If an electron in the valence band is excited (thermally or otherwise) into this state, current flows in the form of holes through the valence band, such that the total density of holes in the valence band $p_v$ is:

$$p=n_A^-+n$$

where $n_A^-$ is the density of thermally ionized acceptors and n is the density of electrons in the conduction band (and therefore, by conservation, the density of holes that have been thermally excited across the gap).

These equations are simple, yet very powerful, and we can immediately make several important observations. Firstly, the system *always* maintains charge neutrality. Secondly, if $n_D^+$ and $n_A^-$ are both zero then we recover the intrinsic case where $n=p$, as expected. Thirdly, we can see by inspection that since the $n\times p$ equation above is always true (for extrinsic as well as intrinsic semiconductors), it implies that the effect of dopants/defects in a semiconductor is to shift the Fermi energy, since $E_C$, $E_V$, $N_C$, and $N_V$ are independent with respect to dopant/defect concentration.

If we have an n-type semiconductor, there are occupied states in the conduction band that would not normally be present. Therefore, the probability of finding an electron in the conduction band is higher. In the case of a p-type semiconductor, there are vacant (electron) states in the valence band that would not normally be present, so the probability of finding a hole in the valence band is higher.

The electron and hole populations ($n$ and $p$) are not simply determined by the thermal smearing of $f(E)$ because the density of ionized donors ($n_D^+$) and ionized acceptors ($n_A^-$) are also temperature dependent. In general, however, dopants are fully ionized at room temperature (that is, $n_D^+\approx n_D$ and $n_A^-\approx n_A$), so in the low-intermediate temperature range, temperature effects can be neglected. With higher temperature there will be more thermal smearing, and $p$ (n-type) or $n$ (p-type) will increase, thus causing $n$ (n-type) and $p$ (p-type) to increase. In general, however, the magnitude of this smearing is very small at typical device doping concentrations.

By rearranging the equations above, we can find the Fermi level of an extrinsic semiconductor:

$$E_f-E_i=k_BT\:ln\left(\frac{n_D^++p}{n_i}\right)$$
$$E_i-E_f=k_BT\:ln\left(\frac{n_A^-+n}{n_i}\right)$$

So, we see that the Fermi level moves upward with increasing n-type dopant concentration, and downward with increasing p-type dopant concentration. If there are no ionized dopants, $n_D^+=n_A^-=0$, these equations both reduce to:

$$E_f-E_i=k_BT\:ln\left(\sqrt{\frac{p}{n}}\right)$$

And furthermore, if $n_D^+=n_A^-=0$, $n=p$ so we recover the intrinsic case:

$$E_f-E_i=0$$

which is redundant to write, but which is also presented in this form for clarity and to show that the equations above are true for extrinsic as well as intrinsic semiconductors.

Note that these results assume low dopant concentrations, such that the interaction between dopants is negligible. At higher densities, the impurity levels may form a band, and all of the energetics derived above, including the Fermi level, intrinsic level, etc., would change in value.

It's important to keep in mind we are not charging the system - that is, we are still net charge-neutral, presuming our dopant atoms are neutral. The entire consequence of the extrinsic $g(E)$ states is to change the respective *populations* of electrons and holes in the conduction and valence bands. In addition, we are still operating in the nearly free electron approximation. If we introduce too many dopants, our system will no longer be approximately crystalline, and the nearly free approximation becomes invalid. Alternatively, if the dopants are very different in size from the intrinsic atoms, or if they otherwise dramatically disrupt the lattice, the nearly free approximation suffers.
