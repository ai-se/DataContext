from __future__ import division
from os import listdir
from os.path import isfile, join
# from where2 import *
from effort import *
from lib import *
import pdb


"""
class to hold global variables.

"""


class o:
  def __init__(i, **d): i.__dict__.update(d)

  def update(i, **d): i.__dict__.update(d); return i

  def __repr__(i):
    show = [':%s %s' % (k, i.__dict__[k]) for k in sorted(i.__dict__.keys()) if k[0] is not "_"]
    txt = ' '.join(show)
    if len(txt) > 60:
      show = map(lambda x: '\t' + x + '\n', show)
    return '{' + ' '.join(show) + '}'


"""
 pd, pf, prec, f, g

"""


def abcd(actual_lst, pred_lst):
  n = lambda x: int(x)
  p = lambda x: int(x * 100)
  def getLabel():
    label = []
    for i in actual_lst:
      if i not in label:
        label.append(i)
    return label

  def getABCD(label):
    for actual, predict in zip(actual_lst, pred_lst):
      for i in label:
        if actual == i:
          if actual == predict:
            D[i] = D.get(i, 0) + 1
          else:
            B[i] = B.get(i, 0) + 1
        else:
          if predict == i:
            C[i] = C.get(i, 0) + 1
          else:
            A[i] = A.get(i, 0) + 1
    return A, B, C,D

  def score(label, show = False):
    out = {}
    for i in label:
      pd = pf = prec = f = g = acc = 0
      a = A.get(i,0);b = B.get(i,0);c = C.get(i,0);d = D.get(i,0)
      if b + d: pd = d / (b + d)
      if a + c: pf = c / (a + c)
      if c + d: prec = d / (c + d)
      if prec + pd: f = 2 * pd * prec / (pd + prec)
      if pd + 1 - pf: g = 2 * pd * (1 - pf) / (1 - pf + pd)
      if a + b + c + d: acc = (a + d) / (a + b + c + d)
      if show:
        print "#", (
        '{0:20s}{1:10s} {2:4d} {3:4d} {4:4d} ' +
        '{5:4d} {6:4d} {7:4d} {8:3d} {9:3d} ' +
        '{10:3d} {11:3d} {12:3d} {''13:10s}').format(
        "hello","test", n(b + d), n(a), n(b), n(c),
        n(d), p(acc), p(pd), p(pf), p(prec), p(f), p(g), i)
      out[i]=[p(pd), p(pf), p(prec), p(f), p(g)]
    return out

  A = {}; B ={}; C ={}; D = {}
  labels = getLabel()
  A,B,C,D = getABCD(labels)
  return score(labels)


def setp():
  return o(what=o(minSize=4,  # min leaf size
                  depthMin=2,  # no pruning till this depth
                  depthMax=10,  # max tree depth
                  wriggle=0.2,  # min difference of 'better'
                  prune=True,  # pruning enabled?
                  b4='|.. ',  # indent string
                  verbose=False,  # show trace info?
                  goal=lambda m, x: scores(m, x)),
             seed=1,
             cache=o(size=128),
             option=o(tunedobjective=1,
                      tuning = False,
                      threshold = 0.5,
                      mean = True,
                      resultname = ""
                      ),
             data=o(train = None,
                    predict = None))


def csv2py(src):
  f = open(src, "r")
  content = f.read().splitlines()
  less_cond = lambda cell: "<" in cell
  miss_cond = lambda cell: "?" in cell
  indep_cond = lambda cell: not miss_cond(cell) and not less_cond(cell) and ">" not in cell
  indep_index, miss_index, less_index = [], [], []
  for index, cell in enumerate(content[0].split(",")):
    if miss_cond(cell):
      miss_index += [index]
    elif indep_cond(cell):
      indep_index += [index]
    elif less_cond(cell):
      less_index += [index]
  indep_head = [content[0].split(",")[i][1:] for i in indep_index]
  less_head = [cell[2:] for index, cell in enumerate(content[0].split(",")) if less_cond(cell)]
  rows = [map(float, row.split(",")[miss_index[-1] + 1:]) for row in
          content[1:]]  # here, assume missing columns happen at the beginning columns
  x = data(indep=indep_head, less=less_head, _rows=rows)
  return x


def defectModel(src="./defect"):
  folder = [i for i in listdir(src) if ".DS" not in i and not isfile(join(src, i))]
  defect_model = {}
  for one in folder:
    nextpath = join(src, one)
    data = [join(nextpath, f) for f in listdir(nextpath) if isfile(join(nextpath, f))]
    for d in data:
      defect_model[one] = defect_model.get(one, []) + [csv2py(d)]
  return defect_model


def effortModel(src="./effort"):
  effort_model = {"albrecht": albrecht.albrecht(), "china": china.china(), "coc81": coc81.coc81(),
                  "cocomo": cocomo.cocomo(), "cosmic": cosmic.cosmic(), "isbsg10": isbsg10.isbsg10(),
                  "kemerer": kemerer.kemerer(), "kitchenham": kitchenham.kitchenham(), "maxwell": maxwell.maxwell(),
                  "miyazaki": miyazaki.miyazaki(), "Mystery1": Mystery1.Mystery1(), "Mystery2": Mystery2.Mystery2(),
                  "nasa93": nasa93.nasa93(), "telecom": telecom.telecom(), "usp05": usp05.usp05()}
  # pdb.set_trace()
  return effort_model


The = setp()


def _Abcd():
  import random
  train = ["Non-Def","Def","Non-Def","Def","Non-Def","Non-Def","Def","Non-Def","Non-Def","Def","Non-Def"]
  test = train[:]
  random.shuffle(test)
  abcd(train, test)


if __name__ == "__main__":
  _Abcd()
  # defectModel()
  # effortModel()
  # x= csv2py("./defect/ant/ant-1.3.csv")
  # callWhere(x)
  # print(x, sep="\n=====\n")
  # callWhere(china.china())
  # print(china.china())
