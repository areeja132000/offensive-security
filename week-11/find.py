for i in range(256):
  str_analyzed = "xortool_out/"
  if len(str(i)) == 3:
    str_analyzed = str_analyzed  + str(i) + ".out"
  elif len(str(i)) == 2:
    str_analyzed = str_analyzed  + "0" + str(i) + ".out"
  else:
    str_analyzed = str_analyzed  + "00" + str(i) + ".out"
  with open(str_analyzed, encoding="utf-8", errors="ignore") as my_file:
    if ("flag" in my_file.read()):
      print(str_analyzed)





 
