"""
Ticket hasher.

Used for finding similar tickets based on notes. Raw tickets file should contain ticket number and notes in 2 columns.

This script hashes the tickets in order to retrieve them for later use.
"""
import re
import csv
import time

def get_seeds_from_file(seed_filename):
"""
Read pregenerated seeds from file. These will be used to generate any amount of hash functions.
"""
  seedz = []
  f = open(seed_filename, 'rt')
  try:
      reader = csv.reader(f)
      for row in reader:
          seedz.append(int(row[0]))
  finally:
      f.close()
  return seedz
    
def shingler(inputstring, shingle_length):
  """
  Convert ticket notes to a list of shingles.
  """
  reducedspaces = ' '.join(inputstring.split())
  preprocessed = re.sub('[^A-Za-z0-9 ]+', '', reducedspaces).lower()
  shinglelist = [preprocessed[i:i + shingle_length] for i in range(len(preprocessed) - shingle_length + 1)]
  return shinglelist

def hash_func(hash_what, seed):
  """
  Hashes the string and xors it with a seed, giving us many hash funcions.
  """
  tobereturned = str.__hash__(hash_what)^seed
  return tobereturned
    
def min_hash(shingles):
  """
  Generate minhashes for all shingles.
  """
  hashes = []
  for seed in seeds:
      hash_list = []
      for token in shingles:
          hash_val = hash_func(token, seed)
          hash_list.append(hash_val)
      if hash_list:
          min_hash = min(hash_list)
      else:
          min_hash = 0
      hashes.append(min_hash)
  return hashes
    
def get_raw_tickets(filename):
  """
  Read raw tickets. First column should be the ticket numbers, second column are the notes.
  """
  rawlist = []
  f = open(filename, 'rt')
  try:
      reader = csv.reader(f)
      for row in reader:
          rawlist.append(row)
  finally:
      f.close()
  return rawlist
    
def hash_and_save(filename, tktlist):
  """
  Performs hashing and saving of all our tickets.
  """
  RESULT = []
  howmanyintotal = len(tktlist)
  with open(filename, "a") as output:
      writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
      for idx,item in enumerate(tktlist):
          hsh = min_hash(shingler(item[1], 5))
          RESULT.append([item[0], hsh])
          writer.writerow([item[0], hsh])
          print '{percent:.2%}'.format(percent=idx/float(howmanyintotal))+' ('+str(idx)+'/'+str(howmanyintotal)+')'
  
if __name__=="__main__":
    startTime = time.time()
    userSeeds = raw_input("Seeds filename: ")
    rawTicketsName = raw_input("Raw ticket data: ")
    outputFileName = raw_input("Output file name: ")
    seeds = get_seeds_from_file(userSeeds)
    rawtickets = get_raw_tickets(rawTicketsName)
    hash_and_save(outputFileName, rawtickets)
    endTime = time.time()
    print 'Time elapsed: '+endTime-startTime