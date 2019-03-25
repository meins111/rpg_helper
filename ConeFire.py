import random

targetEvadeList = [5, 0, 0]
toHitModifierList = [30+10, 30+20, 30+20]
useEqualMod = 0
areaModifier = 30
attackerRof = 8
attackerDos = 1
storm = 0
twinLinked = 0
toHitChance = 0
targetToHitList = [0]
targetHitCntList = [0]

### Caluclation of milti-hit chance
def followUpHitChance (baseToHit, prevHits):
  # Current strategy: half the to-hit chance per previous hit, e.g. 80-40-20-10...
  return baseToHit / (pow(2, prevHits))
  
### Recursive Reroll function ###
def multiHit(curTarget, numOfPrevHits):
  multiHitChance = followUpHitChance(targetToHitList[curTarget], numOfPrevHits)
  # cancel recursion if hit-chance drops to/below 5% or if prevHit reaches RoF
  if multiHitChance <= 5 | numOfPrevHits == attackerRof:  
    return numOfPrevHits
  else:
    roll = random.randrange(1,100)
    if roll<=multiHitChance:
      return multiHit(curTarget, numOfPrevHits+1)
    else:
      # cancel recursion if follow-up to-hit roll did not hit
      return numOfPrevHits

### ToHitChance Calculation ###
def initialToHitChance ():
    baseChance = attackerRof*2 + 5*attackerDos
    if storm: baseChance += 20
    if twinLinked: baseChance += 10
    del(targetToHitList[0])
    for i in range(0,len(targetEvadeList)):
        if useEqualMod:
            targetToHitList.append(baseChance+areaModifier-targetEvadeList[i])
        else:
            targetToHitList.append(baseChance+toHitModifierList[i]-targetEvadeList[i])



#### Preparation ####
initialToHitChance()
print("Hit chances per target:")
for hitChance in targetToHitList:
  print(hitChance, end=',')
print("")
#### Start of Main method ####
numOfTargets=len(targetToHitList)
salvoHits = 0
del(targetHitCntList[0])
for j in range (0,numOfTargets):
    targetHitCntList.append(0)
    if salvoHits >= attackerRof: continue
    x = random.randrange(1,100)
    if x <= targetToHitList[j]:
        hits = multiHit(j, 1)
        if (salvoHits + hits) > attackerRof: 
            hits = attackerRof - salvoHits
        salvoHits += hits
        targetHitCntList[j]=hits

### Outpurlt results ###
print("Total salvo hits: " + str(salvoHits))
print("Hits per target:")
cnt = 1
for x in targetHitCntList:
    print("Target " + str(cnt) + " was hit " + str(x) +" times!")
    cnt+=1
