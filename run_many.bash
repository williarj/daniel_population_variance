
COUNT=1
h=(0 0.25 0.5 0.75 1)
n_male=50
n_female=50
n_offspring=10

p1=0.05
p2=0.95

counter=1
while [ $counter -le $COUNT ]
do
  for d in "${h[@]}"
  do

    python sim.py -M $n_male -F $n_female -p $p1 $p2 -d $d -o $n_offspring

  done
  ((counter++))
done

p1=0.05
p2=0.8

counter=1
while [ $counter -le $COUNT ]
do
  for d in "${h[@]}"
  do

    python sim.py -M $n_male -F $n_female -p $p1 $p2 -d $d -o $n_offspring

  done
  ((counter++))
done

p1=0.05
p2=0.6

counter=1
while [ $counter -le $COUNT ]
do
  for d in "${h[@]}"
  do

    python sim.py -M $n_male -F $n_female -p $p1 $p2 -d $d -o $n_offspring

  done
  ((counter++))
done
