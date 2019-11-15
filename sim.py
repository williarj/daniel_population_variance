import sys, argparse
import numpy as np


def main():
  args = parseArgs()
  

  print("Num males, Num females, p1, p2, h")
  print("%s, %s, %s, %s, %s" % (args.males, args.females, args.freqs[0], args.freqs[1], args.dominance)) 
  print("Male_pop, Female_pop, variance among broods, variance within broods, among to within ratio")

  for i in [0, 1]:
    for j in [0, 1]:
      variance_among, variance_within = trial(args.males, args.females, args.freqs[i], args.freqs[j], args.dominance, args.offspring)
      if variance_within > 0:
        ratio = variance_among/variance_within
      else:
        ratio = "NAN"
      print("%s, %s, %s, %s, %s"% (i, j, variance_among, variance_within, ratio))  


  return

##DEPRECATED
#breeds mapes from p1 with females samples from both p1 and p2
#returns the varaince in average phenotype amongst male broods 
#partitioned among female source population
def mateMales(num_males, num_females, p1, p2, h, num_offspring):
  broods_p1 = []
  broods_p2 = []
  for m in range(num_males):
    male_geno = sampInd(p1) 
    broods_p1.append(mateFemales(male_geno, p1, num_females, num_offspring, h))
    broods_p2.append(mateFemales(male_geno, p2, num_females, num_offspring, h))
    
  #calc the variance among brrod averages AND the average variance within broods 
  print(broods_p1[0:5])
  p1_stats = (np.var([a for (a,v) in broods_p1]), np.average([v for (a,v) in broods_p1]))
  p2_stats = (np.var([a for (a,v) in broods_p2]), np.average([v for (a,v) in broods_p2]))
  
  return (p1_stats, p2_stats)
    

#samples males from a given population
#mates them with females from another population
#returns the variance in average phenotype across broods
#and the average variance within broods
def trial(num_males, num_females, p_male, p_female, h, num_offspring):
  brood_avgs = []
  brood_vars = []

  for m in range(num_males):
    male_geno = sampInd(p_male)
    for f in range(num_females):
      female_geno = sampInd(p_female)
      offspring = breed(male_geno, female_geno, num_offspring)
      avg, var = getStats(offspring, h)
      brood_avgs.append(avg)
      brood_vars.append(var)

  variance_in_avg_brood = np.var(brood_avgs)
  mean_variance_in_brood = np.average(brood_vars)

  return (variance_in_avg_brood, mean_variance_in_brood)

##DEPRECATED##
#samples females from a given population to mate with a given male
#returns a list of the average phenotype of each brood sired by the male
def mateFemales(male, p_female, female_N, offspring_N, h):
  offspring_avg = []
  for f in range(female_N):
    female_geno = sampInd(p_female)
    children = breed(male, female_geno, offspring_N)
    offspring_avg.append(getStats(children, h))
  return offspring_avg

#get the average in kids phenotypes
#and the variance in phenotypes
#given the dominance coefficient
def getStats(kids, h):
  phenotypes = [phenotype(k, h) for k in kids]
  return (np.average(phenotypes), np.var(phenotypes))

#Samples an individual from population with allele frequency p
def sampInd(p):
  return np.random.binomial(2, p, 2)

#creates n children bred from male m and female f
def breed(m, f, n):
  children = []
  for i in range(n):
    children.append([np.random.choice(m), np.random.choice(f)])
  return children

#calculates and individuals phenotype based on genotype
#aa = 0; AA = 1; Aa = h
def phenotype(ind, h):
  total_A = sum(ind)
  if total_A == 0:
    return 0
  elif total_A == 2:
    return 1
  else:
    return h
  

def parseArgs():
  parser = argparse.ArgumentParser()
  parser.add_argument("-M", "--males", type=int, default=10, help="The number of males to sample from each population for breeding.")
  parser.add_argument("-F", "--females", type=int, default=5, help="The number of females from each population that each male will mate with (each male mates with F*2 females).")
  parser.add_argument("-p", "--freqs", type=float, default=[0.1, 0.9], nargs=2, help="The allele frequencies for the two populations we are sampling from.")
  parser.add_argument("-d", "--dominance", type=float, default=0, help="The dominance coefficient for calculating phenotype. Assumes additive phenotypes such that: aa=0, AA=1, Aa=h")
  parser.add_argument("-o", "--offspring", type=int, default=10, help="The number of offspring resulting from each mating")

  return parser.parse_args()

if __name__=="__main__":
  main()
