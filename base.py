from __future__ import division
import sys
import random
import math
import datetime
import time
import re
import pdb

sys.dont_write_bytecode = True


class Options:
  def __init__(i, **d):
    i.__dict__.update(d)


Settings = Options(de=Options(np=10, repeats=1000, f=0.75, cr=0.3, threshold=0.0001, limit=[1, 10, 1, 1, 20, 6, 1],
                              # infoPrune, minSize, threshold, wriggle, depthMax, depthMin, treeMin, treeprune,
                              # whereprune
                              whereLimit_Max=[1, 10, 1, 1, 20, 6, 1, True, False],
                              whereLimit_Min=[0.01, 1, 0.01, 0.01, 1, 1, 0.01, True, False],
                              cartLimit_Max=[1, 50, 20, 20, 1, 100], cartLimit_Min=[0.01, 1, 2, 1, 0.01, 0],
                              # max_features, max_depth, min_samples_split, min_samples_leaf, threshold, random_state
                              rfLimit_Max=[20, 20, 50, 150, 1, 1], rfLimit_Min=[1, 2, 10, 50, 0.01, 0.01],
                              #  min_samples_split, min_samples_leaf,max_leaf_nodes, m_estimators, max_features,
                              # threshold
                              svmLimit_Max=[1.5, ["rbf", "sigmoid"], 10, 1.0, 1.0, True, True, 0.01, 1, 1],
                              svmLimit_Min=[0.5, ["rbf", "sigmoid"], 1, 0.0, 0.0, False, False, 0.0001, 0.01, 0.1],
                              # C, kernel, degree, gamma, coef0,probability, shrinking, tol, threshold, epsilon
                              life=5, k=0, run=20))
