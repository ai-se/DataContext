from __future__ import division, print_function
import sys
from lib import *
from where2 import *


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
  rows = [map(float,row.split(",")[miss_index[-1] + 1:]) for row in
          content[1:]]  # here, assume missing columns happen at the beginning columns
  x = data(indep=indep_head, less=less_head, _rows= rows)
  return x


if __name__ == "__main__":
  x= csv2py("./defect/ant/ant-1.3.csv")
  callWhere(x)
  print(x, sep="\n=====\n")
