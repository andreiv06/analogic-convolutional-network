.include model_mos.lib
Vdd vdd 0 DC 1.8
Vref vref 0 DC 0.5
RsumP vdd bus_p 100k
RsumN vdd bus_n 100k
M1 bus_p vin tail 0 NMOS W=5u L=0.18u
M2 bus_n vref tail 0 NMOS W=5u L=0.18u
V0 vin 0 DC 0.55
It tail 0 DC 1u
.control
dc It 1n 2u 20n
wrdata sim_data.txt (v(vdd)-v(bus_p))/100k (v(vdd)-v(bus_n))/100k
quit
.endc
.end