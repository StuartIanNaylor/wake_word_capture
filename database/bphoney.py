from big_phoney import BigPhoney
phoney = BigPhoney()

words_meta = open('words_meta-j.txt', 'a')
words_alpha = open('words_alpha-j.txt', 'r')

top_line = 'word,scount'
for x in range(30):
  top_line = top_line + ",p" + str(x)
top_line = top_line + ',pcount\n'

words_meta.write(top_line)

while True:
  word = words_alpha.readline()
  if not word:
    break
  syl_count = phoney.count_syllables(word)
  phoneme = phoney.phonize(word)
  phoneme_count = len(phoneme.split())
  phoneme = phoneme.replace(' ', ',')
  phoneme = phoneme.rstrip()
  nullpad_count = 31 - phoneme_count
  null_pad = ',' * nullpad_count
  line = word.rstrip() + ',' + str(syl_count) + ',' + phoneme + null_pad + str(phoneme_count) + '\n'
  words_meta.write(line)
      

    
