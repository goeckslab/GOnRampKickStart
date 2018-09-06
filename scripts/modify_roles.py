import argparse

from os import walk, path

parser = argparse.ArgumentParser()
parser.add_argument("gsk_base", help="the location of the base directory of GSK")
args = parser.parse_args()

basedir = args.gsk_base if args.gsk_base[-1] != "/" else args.gsk_base[:-1]

walkie = walk(basedir + "/modified_roles")

source_files = []
dest_files = []
for root, dirs, files in walkie:
  if files == []:
    continue
  else:
    for f in files:
      source_files.append("{}/{}".format(root, f))

for sf in source_files:
  split = sf.split("/modified_roles")
  dest_files.append(split[0] + "/roles" + split[1])

#check for file equivalence
for i in range(len(source_files)):
  sf = source_files[i]
  df = dest_files[i]
  same = False
  if path.getsize(sf) == path.getsize(df):
    if open(sf,'r').read() == open(df,'r').read():
      same = True
  if not same:
    # replace files
    with open(df, 'w') as wf:
      with open(sf, 'r') as rf:
        wf.write(rf.read())
