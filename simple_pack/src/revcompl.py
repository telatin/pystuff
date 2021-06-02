def revcompl(dna):
  return dna[::-1].translate(str.maketrans(
  	"ACGTUYRKMBDHVacgtuyrkmbdhv", 
  	"TGCAARYMKVHDBtgcaarymkvhdb"))
  