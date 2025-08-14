Males = open('Voices-Male.csv', 'r')
Females = open('Voices-Female.csv', 'r')
TTS = open('single-word.txt', 'w')
Emot=['|高兴|','|兴奋|','|悲伤|','|生气|']
Count = 0
while True:
  MaleVoice = Males.readline()
  FemaleVoice = Females.readline()
  if not MaleVoice:
    break
  if not FemaleVoice:
    break
  Count += 1          
  print(MaleVoice.split(",")[0], FemaleVoice.split(",")[0])
  TTS.write(MaleVoice.split(",")[0] + Emot[0] + '<sos/eos> [JH] [AE1] [K] [AH0] [L] [IH0] [N] <sos/eos>|Computer\n' + FemaleVoice.split(",")[0] + Emot[0] + '<sos/eos> [JH] [AE1] [K] [AH0] [L] [IH0] [N] <sos/eos>|Computer\n')  
  TTS.write(MaleVoice.split(",")[0] + Emot[1] + '<sos/eos> [JH] [AE1] [K] [AH0] [L] [IH0] [N] <sos/eos>|Computer\n' + FemaleVoice.split(",")[0] + Emot[1] + '<sos/eos> [JH] [AE1] [K] [AH0] [L] [IH0] [N] <sos/eos>|Computer\n') 
  TTS.write(MaleVoice.split(",")[0] + Emot[2] + '<sos/eos> [JH] [AE1] [K] [AH0] [L] [IH0] [N] <sos/eos>|Computer\n' + FemaleVoice.split(",")[0] + Emot[2] + '<sos/eos> [JH] [AE1] [K] [AH0] [L] [IH0] [N] <sos/eos>|Computer\n') 
  TTS.write(MaleVoice.split(",")[0] + Emot[3] + '<sos/eos> [JH] [AE1] [K] [AH0] [L] [IH0] [N] <sos/eos>|Computer\n' + FemaleVoice.split(",")[0] + Emot[3] + '<sos/eos> [JH] [AE1] [K] [AH0] [L] [IH0] [N] <sos/eos>|Computer\n')     

print(Count)

