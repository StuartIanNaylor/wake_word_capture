males = open('Voices-Male.csv', 'r')
females = open('Voices-Female.csv', 'r')
emotp = open('unk3-emotp.txt', 'r')

tts = open('words-emot.txt', 'w')

emots=['|Happy|','|Sad|','|Angry|','|Surprised|']

gender = 0
emot = 0
while True:

  wordp = emotp.readline()
  if not wordp:
    break
  
  if gender == 0: 
    male = males.readline()
    if not male:
      males = open('Voices-Male.csv', 'r')
      male = males.readline()
    tts.write(male.split(",")[0] + emots[emot] + wordp.strip() + '|Word\n')
    gender = 1
  else:
    female = females.readline()
    if not female:
      females = open('Voices-Female.csv', 'r')
      female = females.readline()
    gender = 0
    tts.write(female.split(",")[0] + emots[emot] + wordp.strip() + '|Word\n')
    emot += 1
    if emot > 3:
      emot = 0


