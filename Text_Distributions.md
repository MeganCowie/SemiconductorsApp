Here we show when it is appropriate to use the Maxwell Boltzmann distribution in lieu of Fermi Dirac. The Fermi-Dirac $f_F$ and Maxwell-Boltzmann $f_M$ distribution functions are given below:

$$f_F(E)=\frac{1}{1+e^{(E-E_f)/k_BT}}$$
$$f_M(E)=\frac{1}{e^{(E-E_f)/k_BT}}$$

We can immediately see that in the limit $exp\left(\frac{E-E_f}{k_BT}\right)>>1$, we have $f_F(E)\approx f_M(E)$. But I scratched my head looking at this limit for a while before I actually understood it, due to two points of confusion. First of all, this limit is sometimes called the "high-temperature limit", and as an experimentalist, when I read "high temperature" I immediately looked at $T$. But as $T$ increases the functions deviate. What is meant by "temperature" in this statement is the particle energy $E$, since the system in question is a grand canonical ensemble with constant $\mu$ ($E_f$) and constant $T$. So of course, this limit makes sense, since at high energy $E$ the density of states is large, approaching the classical (non-quantized) case. Secondly, the limit is often rephrased as $E-E_f>>k_BT$. But I find that since in experiments we are at nonzero $T$, it is hard to know at a glance when the limit is satisfied, and in particular it appeared to me that the limit might only be satisfied far from the Fermi energy. What I find much clearer is the approach shown in Neamen, Chapter 2, where we find the energy $E$ where $f_F(E)$ and $f_M(E)$ agree within 5%:

$$ \frac{f_M(E)-f_F(E)}{f_F(E)}=0.05 $$
$$ \frac{1+e^{(E-E_f)/k_BT}}{e^{(E-E_f)/k_BT}}-1=0.05 $$
$$ e^{-(E-E_f)/k_BT}=0.05 $$
$$ E \approx 3 k_BT +E_f $$

This, to me, is the more obvious "limit": $f_M(E)$ may be used in lieu of $f_F(E)$ when $E \approx 3 k_BT +E_f$, for any (thermal) temperature $T$ and state $E$.

&nbsp
