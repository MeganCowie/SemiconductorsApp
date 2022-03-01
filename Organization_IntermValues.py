import Physics_Semiconductors

def Surface_values(Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T,sampletype):
    NC,NV = Physics_Semiconductors.Func_NCNV(T,mn,mp)
    ni = Physics_Semiconductors.Func_ni(NC,NV,Eg,T)
    Ec,Ev = Physics_Semiconductors.Func_EcEv(T,Eg)
    Ei = Physics_Semiconductors.Func_Ei(Ev,Ec,T,mn,mp)
    Ef = Physics_Semiconductors.Func_Ef(NC,NV,Ec,Ev,T,Nd,Na)
    CPD = Physics_Semiconductors.Func_CPD(WFmet,EAsem,Ec,Ef)
    LD = Physics_Semiconductors.Func_LD(epsilon_sem,T,Na,Nd)

    Cins = C_l= Physics_Semiconductors.epsilon_o*100/(zins/100) #C/Vm**2

    return NC,NV,ni,Ec,Ev,Ei,Ef,CPD,LD,Cins


#Vg,zins,Eg,epsilon_sem,WFmet,EAsem,Nd,Na,mn,mp,T
