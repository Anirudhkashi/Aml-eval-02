from myhmm_log import *

obs= []

def main():
	single_model= genModel(getData('single_1_trg_vq.txt'))
	multi_model= genModel(getData('multi_1_trg_vq.txt'))
	silent_model= genModel(getData('silent_1_trg_vq.txt'))

	print(single_model.A)
	print(multi_model.A)
	print(silent_model.A)

def getData(file):
	fp= open(file, 'r')
	j= 1
	obs= []
	seq= []
	for line in fp:
		if(j== 10):
			seq= []
			obs.append(seq)
			j=0
		j+=1
		seq.append(line.strip('\n'))
	return obs

def genModel(obslist):
	mod= MyHmmLog('debate_initial.json')
	mod.forward_backward_multi(obslist)
	return mod

main()