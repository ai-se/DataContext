from __future__ import division
import random, pdb
from base import *
import collections
from start2 import *


class DeBase(object):
  def __init__(i, model):
    global The
    i.tobetuned = model.tunelst
    i.limit_max = model.tune_max
    i.limit_min = model.tune_min
    i.np = Settings.de.np
    i.fa = Settings.de.f
    i.cr = Settings.de.cr
    i.repeats = Settings.de.repeats
    i.life = Settings.de.life
    i.obj = The.option.tunedobjective
    # i.obj = 2  ### need to change this to the above line after done!
    i.evaluation = 0
    i.scores = {}
    i.frontier = [i.generate() for _ in xrange(i.np)]
    i.evaluate()
    i.bestconf, i.bestscore = i.best()

  def generate(i):
    candidates = []
    for n, item in enumerate(i.limit_min):
      if isinstance(item, float):
        candidates.append(round(random.uniform(i.limit_min[n], i.limit_max[n]), 2))
      elif isinstance(item, bool):
        candidates.append(random.random() <= 0.5)
      elif isinstance(item, list):
        pass
      elif isinstance(item, int):
        candidates.append(int(random.uniform(i.limit_min[n], i.limit_max[n])))
      else:
        raise ValueError("type of limits are wrong!")
    # pdb.set_trace()
    return i.treat(candidates)

  def evaluate(i):
    for n, arglst in enumerate(i.frontier):
      i.assign(i.tobetuned, arglst)
      i.scores[n] = i.callModel()  # main return [[pd,pf,prec,f,g],[pd,pf,prec,f,g]], which are N-defective,Y-defecitve

  def assign(i, tobetuned, tunedvalue):
    for key, val in zip(tobetuned, tunedvalue):
      exec (key + "= " + str(val))
      # tobetuned[key] = val

  def best(i):
    sortlst = []
    if i.obj == 1:  # this is for pf
      sortlst = sorted(i.scores.items(), key=lambda x: x[1][i.obj], reverse=True)  # alist of turple
    else:
      sortlst = sorted(i.scores.items(), key=lambda x: x[1][i.obj])  # alist of turple
    bestconf = i.frontier[sortlst[-1][0]]  # [(0, [100, 73, 9, 42]), (1, [75, 41, 12, 66])]
    bestscore = sortlst[-1][-1][i.obj]
    return bestconf, bestscore

  def callModel(i):
    raise NotImplementedError("callMode error")

  def treat(i):
    """
    some parameters may have constraints, for example:
    when generating a parameter list, p[4]should be greater than p[5]
    You should implement this function in subclass
    """
    return NotImplementedError("treat error")

  def trim(i, n, x):
    if isinstance(i.limit_min[n], float):
      return max(i.limit_min[n], min(round(x, 2), i.limit_max[n]))
    elif isinstance(i.limit_max[n], int):
      return max(i.limit_min[n], min(int(x), i.limit_max[n]))
    else:
      raise ValueError("wrong type here in parameters")

  def gen3(i, n, f):
    seen = [n]

    def gen1(seen):
      while 1:
        k = random.randint(0, i.np - 1)
        if k not in seen:
          seen += [k]
          break
      return i.frontier[k]

    a = gen1(seen)
    b = gen1(seen)
    c = gen1(seen)
    return a, b, c

  def update(i, n, old):
    newf = []
    a, b, c = i.gen3(n, old)
    for k in xrange(len(old)):
      if isinstance(i.limit_min[k], bool):
        newf.append(old[k] if i.cr < random.random() else not old[k])
      elif isinstance(i.limit_min[k], list):
        pass
      else:
        newf.append(old[k] if i.cr < random.random() else i.trim(k, (a[k] + i.fa * (b[k] - c[k]))))
    return i.treat(newf)

  def DE(i):
    changed = False

    def isBetter(new, old):
      return new < old if i.obj == 1 else new > old

    for k in xrange(i.repeats):
      if i.life <= 0:
        break
      nextgeneration = []
      for n, f in enumerate(i.frontier):
        new = i.update(n, f)
        i.assign(i.tobetuned, new)
        newscore = i.callModel()
        i.evaluation += 1
        if isBetter(newscore[i.obj], i.scores[n][i.obj]):
          nextgeneration.append(new)
          i.scores[n] = newscore[:]
        else:
          nextgeneration.append(f)
      i.frontier = nextgeneration[:]
      newbestconf, newbestscore = i.best()
      if isBetter(newbestscore, i.bestscore):
        print "newbestscore %s:" % str(newbestscore)
        print "bestconf %s :" % str(newbestconf)
        i.bestscore = newbestscore
        i.bestconf = newbestconf[:]
        changed = True
      if not changed:
        i.life -= 1
      changed = False
    i.assign(i.tobetuned, i.bestconf)
    print "DONE !!!!"


class WhereDE(DeBase):
  def __init__(i, model):
    super(WhereDE, i).__init__(model)

  def treat(i, lst):
    def ig(l): return int(random.uniform(i.limit_min[l], i.limit_max[l]))

    if lst[-1] and lst[4] <= lst[5]:
      lst[4] = ig(4)
      lst[5] = ig(5)
      lst = i.treat(lst)
    return lst

  def callModel(i):
    callWhere()


if __name__ == "__main__":
  Where().DE()
