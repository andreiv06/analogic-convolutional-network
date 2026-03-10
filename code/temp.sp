.include model_mos.lib
Vdd vdd 0 DC 1.8
Vref vref 0 DC 0.5
RsumP vdd bus_p 10k
RsumN vdd bus_n 10k
V0 in0 0 DC 0.6000000000000001
It0 tail0 0 DC 0.0
M1_0 bus_p in0 tail0 0 NMOS W=5u L=0.18u
M2_0 bus_n vref   tail0 0 NMOS W=5u L=0.18u
V1 in1 0 DC 0.6000000000000001
It1 tail1 0 DC 0.0001
M1_1 bus_n in1 tail1 0 NMOS W=5u L=0.18u
M2_1 bus_p vref   tail1 0 NMOS W=5u L=0.18u
V2 in2 0 DC 0.6000000000000001
It2 tail2 0 DC 0.0
M1_2 bus_p in2 tail2 0 NMOS W=5u L=0.18u
M2_2 bus_n vref   tail2 0 NMOS W=5u L=0.18u
V3 in3 0 DC 0.6000000000000001
It3 tail3 0 DC 0.0001
M1_3 bus_n in3 tail3 0 NMOS W=5u L=0.18u
M2_3 bus_p vref   tail3 0 NMOS W=5u L=0.18u
V4 in4 0 DC 0.6000000000000001
It4 tail4 0 DC 0.0004
M1_4 bus_p in4 tail4 0 NMOS W=5u L=0.18u
M2_4 bus_n vref   tail4 0 NMOS W=5u L=0.18u
V5 in5 0 DC 0.6000000000000001
It5 tail5 0 DC 0.0001
M1_5 bus_n in5 tail5 0 NMOS W=5u L=0.18u
M2_5 bus_p vref   tail5 0 NMOS W=5u L=0.18u
V6 in6 0 DC 0.6000000000000001
It6 tail6 0 DC 0.0
M1_6 bus_p in6 tail6 0 NMOS W=5u L=0.18u
M2_6 bus_n vref   tail6 0 NMOS W=5u L=0.18u
V7 in7 0 DC 0.6000000000000001
It7 tail7 0 DC 0.0001
M1_7 bus_n in7 tail7 0 NMOS W=5u L=0.18u
M2_7 bus_p vref   tail7 0 NMOS W=5u L=0.18u
V8 in8 0 DC 0.6000000000000001
It8 tail8 0 DC 0.0
M1_8 bus_p in8 tail8 0 NMOS W=5u L=0.18u
M2_8 bus_n vref   tail8 0 NMOS W=5u L=0.18u
.op
.control
run
let rez = (v(vdd)-v(bus_p))-(v(vdd)-v(bus_n))
print rez > rezultat.txt
quit
.endc
.end