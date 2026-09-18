set terminal pngcairo size 600, 1250
set output "nihanje.png"

set title "dušeno nihanje"
set xlabel "t"
set ylabel "x(t)"

set key box

f1(x) = A1 * cos(sqrt(w1**2 - b1**2)*x + d1) * exp(-b1 * x)
fit f1(x) "mapa_1/data_1" via A1, w1, b1, d1

f2(x) = A2 * cos(sqrt(w2**2 - b2**2)*x + d2) * exp(-b2 * x)
fit f2(x) "mapa_2/data_2" via A2, w2, b2, d2

f3(x) = A3 * cos(sqrt(w3**2 - b3**2)*x + d3) * exp(-b3 * x)
fit f3(x) "mapa_3/data_3" via A3, w3, b3, d3

set multiplot layout 3, 1
plot "mapa_1/data_1" using 1:2 lw 0.5 lc rgb "#8b0000" w lines title sprintf('{/Symbol b}_1 = %.2e', b1), f1(x) lc 0 lw 1 title "f_1(x)"
plot "mapa_2/data_2" using 1:2 lw 0.5 lc rgb "#8b0000" w lines title sprintf('{/Symbol b}_2 = %.2e', b2), f2(x) lc 0 lw 1 title "f_2(x)"
plot "mapa_3/data_3" using 1:2 lw 0.5 lc rgb "#8b0000" w lines title sprintf('{/Symbol b}_3 = %.2e', b3), f3(x) lc 0 lw 1 title "f_3(x)"