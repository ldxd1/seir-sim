# -*- coding: utf-8 -*-
"""
@author: Nick Terry

A test script for seir-sim that generates a random contact network and runs the
simulation
"""
import matplotlib.pyplot as plt

from experiment import Experiment
from seirSim import SeirSim
from policies import vaccinateTopNDIL,vaccinateNRandom,vaccinateTopNDegree,vaccinateTopNTSH, vaccinateNAcquaintance
from tallyFuncs import numNodesInState
from networkalgs import generateRandomGraph
from plotting import plotExperiment
import networkViz as nv


numNodes = 10000

G = generateRandomGraph(numNodes)

#Use parameters estimated from Ebola epidemics in Sierra Leone
#Source: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4169395/
exposureRate = .45 #Beta
infectionRate = 1/5.3 #Sigma
recoveryRate = 1/5.61 #Gamma

numVaccinated = 1000

DILPolicy = vaccinateTopNDIL(numVaccinated)
randomVaccPolicy = vaccinateNRandom(numVaccinated)
DegPolicy = vaccinateTopNDegree(numVaccinated)
tshPolicy = vaccinateTopNTSH(numVaccinated)
acquPolicy = vaccinateNAcquaintance(numVaccinated)

simulation = SeirSim(G,exposureRate,infectionRate,recoveryRate,
                     logSim=True, 
              tallyFuncs=[numNodesInState(0),numNodesInState(1),
                          numNodesInState(2),numNodesInState(3)])

exper = Experiment(simulation)

logList,statsList = exper.compare([[None],[randomVaccPolicy],
                                   [DegPolicy],[DILPolicy],
                                   [tshPolicy],[acquPolicy]])

titles = ['No Vaccination','Random Vaccination',
          'Degree-Ranked Vaccination','DIL-Ranked Vaccination',
          'TSH-Ranked Vaccination','Acquaintance Vaccination']
plotExperiment(exper,titles)