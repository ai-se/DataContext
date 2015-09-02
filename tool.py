from __future__ import division, print_function
from os import listdir
from os.path import isfile, join

# from where2 import *
from effort import *

"""
class to hold global variables.

"""


class o:
  def __init__(i,**d): i.__dict__.update(d)
  def update(i,**d) : i.__dict__.update(d); return i
  def __repr__(i)   :
    show=[':%s %s' % (k,i.__dict__[k])
      for k in sorted(i.__dict__.keys() )
      if k[0] is not "_"]
    txt = ' '.join(show)
    if len(txt) > 60:
      show=map(lambda x: '\t'+x+'\n',show)
    return '{'+' '.join(show)+'}'




def setp():
  return o(what = o(
             minSize  = 4,    # min leaf size
             depthMin= 2,      # no pruning till this depth
             depthMax= 10,     # max tree depth
             wriggle = 0.2,    # min difference of 'better'
             prune   = True,   # pruning enabled?
             b4      = '|.. ', # indent string
             verbose = True  # show trace info?
             # goal    = lambda m,x : scores(m,x)
             ),
        seed = 1,
        cache = o(size = 128),
        option = o(tunedobjective = 1)
        )

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

if __name__ == "__main__":
  # defectModel()
  effortModel()
  # x= csv2py("./defect/ant/ant-1.3.csv")
  # callWhere(x)
  # print(x, sep="\n=====\n")
  # callWhere(china.china())
  # print(china.china())
