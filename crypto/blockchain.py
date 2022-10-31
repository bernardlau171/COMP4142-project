#!/usr/bin/python
# -*- coding: utf-8 -*-

#to use sha256 hash for the blockchain
from hashlib import sha256
from datetime import datetime


#Takes in any number of arguments and produces a sha256 hash as a result
def updatehash(*args):
  hashing_text = ""
  h = sha256()

  #loop through each argument and hash
  for arg in args:
    hashing_text += str(arg)

  h.update(hashing_text.encode('utf-8'))
  return h.hexdigest()


#The "node" of the blockchain. Points to the previous block by its unique hash in previous_hash.
class Block():

  #default data for block defined in constructor. Minimum specified should be number and data.
  def __init__(self,
               index=0,
               timestamp=0,
               previous_hash="0" * 64,
               data=None,
               nonce=0,
               difficulty=0):
    self.data = data
    self.index = index
    self.timestamp = timestamp
    self.previous_hash = previous_hash
    self.difficulty = difficulty
    self.nonce = nonce

  #returns a sha256 hash for the block's data. Function instead of variable in constructor
  #to avoid corruption of the variable.
  def hash(self):
    return updatehash(self.index, self.timestamp, self.previous_hash,
                      self.difficulty, self.data, self.nonce)

  #returns a string of the block's data. Useful for diagnostic print statements.
  def __str__(self):
    return str(
      "Block index#: %s\nTimestamp: %s\nPrevious Hash: %s\nHash: %s\nDifficulty: %s\nNonce: %s\nData: %s\n"
      % (self.index, self.timestamp, self.previous_hash, self.hash(),
         self.difficulty, self.nonce, self.data))


#The "LinkedList" of the blocks-- a chain of blocks.
class Blockchain():
  #the number of zeros in front of each hash
  difficulty = 2

  #restarts a new blockchain or the existing one upon initialization
  def __init__(self):
    self.chain = []

  #add a new block to the chain
  def add(self, block):
    self.chain.append(block)

  #remove a block from the chain
  def remove(self, block):
    self.chain.remove(block)

  #find the nonce of the block that satisfies the difficulty and add to chain
  def mine(self, block):
    #attempt to get the hash of the previous block.
    #this should raise an IndexError if this is the first block.
    try:
      block.previous_hash = self.chain[-1].hash()
    except IndexError:
      pass

    #loop until nonce that satisifeis difficulty is found
    while True:
      if block.hash()[:self.difficulty] == "0" * self.difficulty:
        self.add(block)
        break
      else:
        #increase the nonce by one and try again
        block.nonce += 1

  #find the timestamp of current time
  def timestamp(self):
    #current_time = datetime.now()
    #time_stamp = datetime.now().timestamp()
    #print("timestamp: ", time_stamp)
    #date_time = datetime.fromtimestamp(time_stamp)
    #str_date_time = date_time.strftime("%d-%m-%Y, %H:%M:%S")
    #print("Current timestamp", str_date_time)
    #self.timestamp = time_stamp
    return datetime.now().timestamp()

  #check if blockchain is valid
  def isValid(self):
    #loop through blockchain
    for i in range(1, len(self.chain)):
      _previous = self.chain[i].previous_hash
      _current = self.chain[i - 1].hash()
      #compare the previous hash to the actual hash of the previous block
      if _previous != _current or _current[:self.
                                           difficulty] != "0" * self.difficulty:
        return False

    return True


#for testing purposes
def main():
  
    # Process pairs. For odd length, the last is skipped
    #for i in range(0, len(hashList)-1, 2):
    #    newHashList.append(hashIt(hashList[i], hashList[i+1]))
    #if len(hashList) % 2 == 1: # odd, hash last item twice
    #    newHashList.append(hashIt(hashList[-1], hashList[-1]))
    #return merkleCalculator(newHashList)
  
  blockchain = Blockchain()
  database = ["COMP4142", "goodbye", "test", "DATA here"]


  
  num = 0
  for data in database:
    num += 1
    d_timestamp = blockchain.timestamp()
    blockchain.mine(
      Block(num,
            data=data,
            timestamp=d_timestamp,
            difficulty=blockchain.difficulty))

  for block in blockchain.chain:
    print(block)

  print(blockchain.isValid())

  blockchain.chain[2].data = "NEW DATA"
  blockchain.mine(blockchain.chain[2])
  print(blockchain.isValid())


if __name__ == '__main__':
  main()
  
