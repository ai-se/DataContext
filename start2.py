# __author__ = 'WeiFu'
from __future__ import division,print_function
from tuner import *
from where2 import *
from time import strftime
import os
from sk import *
from tool import *

class Learner(object):
  def __init__(i, train, tune, test):
    i.train = train
    i.tune = tune
    i.test = test

  def untuned(i):
    The.data.predict = i.test
    The.data.train = i.train
    i.default()
    The.option.tuning = False
    score = i.call()
    return score

  def tuned(i):
    The.data.predict = i.tune
    The.data.train = i.train
    The.option.tuning = True
    i.optimizer()
    The.option.tuning = False
    The.data.predict = i.test
    score = i.call()
    return score

  def call(i):
    raise NotImplementedError

  def optimizer(i):
    raise NotImplementedError

  def default(i):
    raise NotImplementedError


class Where(Learner):
  def __init__(i, train, tune, predict):
    super(Where, i).__init__(train, tune, predict)
    i.tunelst = ["The.what.threshold", "The.what.wriggle",
                 "The.what.depthMax", "The.what.depthMin", "The.what.minSize", "The.what.prune"]
    i.tune_min = [0.01, 0.01, 1, 1, 1, False]
    i.tune_max = [1, 1, 20, 6, 20, False]

  def default(i):
    The.what.threshold = 0.5
    The.what.wriggle = 0.2
    The.what.depthMax = 10
    The.what.depthMin = 2
    The.what.minSize = 10

  def call(i):
    return callWhere()

  def optimizer(i):
    tuner = WhereDE(i)
    tuner.DE()


def createfile(objective):
  pwd = os.getcwd()[:os.getcwd().find("Github")]
  The.option.resultname = pwd+'Google Drive/myresult' + strftime("%Y-%m-%d %H:%M:%S") + objective
  f = open(The.option.resultname, 'w').close()


def writefile(s):
  global The
  f = open(The.option.resultname, 'a')
  f.write(s + '\n')
  f.close()


def run():
  X =defectModel()
  model= Where(X['ant'][0],X['ant'][0],X['ant'][0])
  model.untuned()
  # model.optimizer()

  print(The)
  print("Done!")


def start(path="./defect"):
  def keep(learner, score):  # keep stats from run
    NDef = learner + ": N-Def"
    YDef = learner + ": Y-Def"
    for j, s in enumerate(lst):
      s[NDef] = s.get(NDef, []) + [(float(score['Non-Def'][j] / 100))]
      s[YDef] = s.get(YDef, []) + [(float(score['Def'][j] / 100))]  # [YDef] will void to use myrdiv.

  def printResult(dataname):
    def myrdiv(d):
      stat = []
      for key, val in d.iteritems():
        val.insert(0, key)
        stat.append(val)
      return stat

    print("\n" + "+" * 20 + "\n DataSet: " + dataname + "\n" + "+" * 20)
    for j, k in enumerate(["pd", "pf", "prec", "f", "g"]):
      express = "\n" + "*" * 10 + k + "*" * 10
      writefile(express)
      rdivDemo(myrdiv(lst[j]))
    writefile("End time :" + strftime("%Y-%m-%d %H:%M:%S") + "\n" * 2)
    print("\n")

  global The
  The.option.tunedobjective = 3  # 0->pd, 1->pf,2->prec, 3->f, 4->g
  objectives = {0: "pd", 1: "pf", 2: "prec", 3: "f", 4: "g"}
  createfile(objectives[The.option.tunedobjective])
  folders = [f for f in listdir(path) if not isfile(join(path, f))]
  allModels =defectModel()
  for folder in folders[2:3]:
    nextpath = join(path, folder)
    data = [join(nextpath, f) for f in listdir(nextpath) if isfile(join(nextpath, f))]
    for i in range(len(data)):
      random.seed(1)
      pd, pf, prec, F, g = {}, {}, {}, {}, {}
      lst = [pd, pf, prec, F, g]
      expname = folder + "V" + str(i)
      try:
        predict = allModels[folder][i + 2]
        tune = allModels[folder][i + 1]
        train = allModels[folder][i]
        pdb.set_trace()
      except IndexError as e:
        print(folder + "done!")
        break
      print(objectives[The.option.tunedobjective] + " as the objective\n" + "Begin time :" + strftime(
        "%Y-%m-%d %H:%M:%S"))
      for model in [Where]:  # add learners here!
        for task in ["Tuned_", "Naive_"]:
          timeout = time.time()
          name = task + model.__name__
          thislearner = model(train, tune, predict)
          keep(name, thislearner.tuned() if task == "Tuned_" else thislearner.untuned())
          print(name + "Running Time:" + str(round(time.time() - timeout, 3)))
      printResult(expname)


if __name__ == "__main__":
  start()
