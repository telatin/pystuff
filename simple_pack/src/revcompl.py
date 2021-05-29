def revcompl(dna):
  dna = dna[::-1]
  return dna.translate(str.maketrans(
  	"ACGTUYRKMBDHVacgtuyrkmbdhv", 
  	"TGCAARYMKVHDBtgcaarymkvhdb"))
  