import random
####### Inputs ######
numOfTargets = 7        # possible targets inside the cone
rof = 10                # rate-of-fire of the weapon, limits max hits per salvo
toHitChance = 35        # in %, to-hit chance per target - most important input
iterations = 100_000    # raise to increase precision of sim, will take longer


### Repeatative to-hit chance reduction function ###
# To try out another reduction function proceed as follows:
# - comment out current one (by writing a # in front of the respective return statement)
# - remove comment of the one you want (by deleting the leading # in front of it)
def followUpHitChance (prevHits):
  # Current strategy: half the to-hit chance per previous hit, e.g. 80-40-20-10...
  return toHitChance / (pow(2, prevHits))
  # Alternative 1: reduce to-Hit chance by 10 per previous hit, e.g. 80-70-60...
  # return toHitChance - (prevHits*10)
  # Alternative 2: do not reduce to-Hit chance at all
  # return toHitChance


### Internal variables to hold various statistic values ###
totalHits = 0
targetGotHitCnt = [0]
hitCntPerTarget = [0]
maxPerTarget = [0]
hitCnt = [0]
# Adjust lists to number of targets
for t in range (0,numOfTargets-1):
  targetGotHitCnt.append(0)
  hitCntPerTarget.append(0)
  maxPerTarget.append(0)
# Adjust list to RoF
for r in range (0,rof):
  hitCnt.append(0)


### Recursive Reroll function ###
def multiHit(numOfPrevHits):
  multiHitChance = followUpHitChance(numOfPrevHits)
  # cancel recursion if hit-chance drops to/below 5% or if prevHit reaches RoF
  if multiHitChance <= 5 | numOfPrevHits == rof:  
    return numOfPrevHits
  else:
    roll = random.randrange(1,100)
    if roll<=multiHitChance:
      return multiHit(numOfPrevHits+1)
    else:
      # cancel recursion if follow-up to-hit roll did not hit
      return numOfPrevHits

### Start Screen: ###
print("Input parameters are: ")
print("Base-Hit chance: " + str(toHitChance) + "%")
print("Number of targets: " + str(numOfTargets))
print("Rate of Fire: " + str(rof))
print("********************************************");
print("*** Start Simulation, Iterations: " + str(iterations) + " ***")
print("********************************************");

### Monte Carlo Experiment ###
for i in range (0,iterations):
  salvoHits = 0
  for j in range (0,numOfTargets):
    if salvoHits >= rof: continue
    x = random.randrange(1,100)
    if x<= toHitChance:
      targetGotHitCnt[j]+=1
      hits = multiHit(1)
      if (salvoHits + hits)>rof: 
        hits = rof - salvoHits
      totalHits += hits
      salvoHits += hits
      hitCntPerTarget[j] += hits
      if hits > maxPerTarget[j]:
        maxPerTarget[j] = hits
  hitCnt[salvoHits] += 1
  if i % (iterations//10) == 0:
    print("Simulation in progress: [{0}]%".format(i*100/iterations))

### Result interpretation and output ###      
print("********************************************");
print("***************** DONE *********************")
print("********************************************");
print("Per Salvo Statistics:")
print("* Total hits: " + str(totalHits) + " | " + str(totalHits*100/(iterations*rof)) + "%" + " | Average Hits: " + str(totalHits/iterations))
print("* Salvo hit count distribution:")
times = 0
for hit in hitCnt:
    print("** " + str(times) +" hit(s): " + str(hit) + " | " + str(hit*100/iterations) + "%")
    times += 1
print("Per Target Statistics:")
times = 1
for cnt in hitCntPerTarget:
  print("* Target " + str(times) + " was hit: " + str(cnt) + "  (" + str(targetGotHitCnt[times-1]*100/iterations) + "%) | Max hits: " + str(maxPerTarget[times-1]) + " | Average hits: " + str(cnt/iterations))
  times += 1
