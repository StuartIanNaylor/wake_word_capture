import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--csv_name', default='./word-list', help='word last unk3 without extention')
args = parser.parse_args()
  

words = open(args.csv_name + '.csv', 'r')
cc = open(args.csv_name + '-cc.txt', 'w')
emot = open(args.csv_name + '-emot.txt', 'w')
pi = open(args.csv_name + '-pi.txt', 'w')
kk = open(args.csv_name + '-kk.txt', 'w')
vk = open(args.csv_name + '-vk.txt', 'w')

emot_count = 3.21
pi_count = 13.77
kk_count = 44.99
vk_count = 113.93

emot_last = 0
pi_last = 0
kk_last = 0
vk_last = 0


count = 0
while True:
  word = words.readline()
  if not word:
    break
  word = word.strip()      
  if int(count / emot_count) > emot_last:
      emot_last = int(count / emot_count)
      emot.write(word + '\n')
      print("emot")
  elif  int(count / pi_count) > pi_last:
      pi_last = int(count / pi_count)
      pi.write(word + '\n')
      print("pi")
  elif  int(count / kk_count) > kk_last:
      kk_last = int(count / kk_count)
      kk.write(word + '\n')
      print("kk")
  elif int(count / vk_count) > vk_last:
      vk_last = int(count / vk_count)
      vk.write(word + '\n')
      print("vk")
  else:
      cc.write(word + '\n')         
      print("cc")
  count += 1          

  

