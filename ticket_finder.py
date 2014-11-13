# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
D:\WinPython\settings\.spyder2\.temp.py
"""
import socket, getpass
import re
import csv
import operator
import ast
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

def min_hash_similarity(hashesA, hashesB, N):
  """
  Calculate the similarity of 2 hash lists, giving us an approximation of the Jaccard Similarity of ticket notes.
  """
  count = 0
  for i in xrange(N):
      if hashesA[i] == hashesB[i]:
          count += 1
  return float(count)/N

def find_max(notes, tktlist, N):
  """
  Return the 10 most similar tickets.
  """
  compare = min_hash(shingler(notes, 5))
  bigList = []
  for idx,item in enumerate(tktlist):
      similarity = min_hash_similarity(compare, item[1], N)
      bigList.append([item[0], similarity])
  return sorted(bigList, key=operator.itemgetter(1), reverse=True)[:10]
    
def read_hashed_tickets(hashed_filename):
  """
  Read previously hashed tickets to keep them in memory for fast processing.
  """
  tkts = []
  f = open(hashed_filename, 'rt')
  try:
      reader = csv.reader(f, delimiter=',')
      for row in reader:
          tkts.append([row[0],ast.literal_eval(row[1])])
  finally:
      f.close()
  return tkts

def wait_for_notes(N):
  """
  Open a socket and wait for connection. Upon receiving notes from the other end, find the most similar tickets and return them via the socket.
  """
  while True:
      channel, details = my_socket1.accept()
      receivednotes = channel.recv(2048)
      break
  maks = find_max(receivednotes, hashedtickets, N)
  my_socket2 = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
  my_socket2.connect ( ( 'localhost', 4242 ) )
  my_socket2.send(', '.join([x[0] for x in maks]))
  time.sleep(2)
  my_socket2.close()
  wait_for_notes(N)

if __name__=="__main__":
    seeds = get_seeds_from_file("30seeds.csv")
    hashedtickets = read_hashed_tickets("hashedtickets.csv")
    print "Ready for input!"
    my_socket1 = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
    my_socket1.bind ( ( '', 2727 ) )
    my_socket1.listen ( 1 )
    wait_for_notes(len(seeds))