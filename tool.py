from __future__ import division, print_function
import sys
from lib import *
from where2 import *
from effort import *
from os import listdir
from os.path import isfile, join
import pdb


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
  #pdb.set_trace()
  return effort_model


if __name__ == "__main__":
  # defectModel()
  effortModel()
  # x= csv2py("./defect/ant/ant-1.3.csv")
  # callWhere(x)
  # print(x, sep="\n=====\n")
  # callWhere(china.china())
  # print(china.china())
