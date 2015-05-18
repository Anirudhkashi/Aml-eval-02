from myhmm_log import *

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

def testVals(file):
	tstFile=open(file,'r')
	tstVec=tstFile.read().split('\n')
	i=0
	k=1
	vecVec=[[]]
	for j in range(len(tstVec)-1):	
		vecVec[i].append(tstVec[j])
		k+=1
		if(k==10):
			k=0
			i+=1
			vecVec.append([])
	yVec=yVals(vecVec[:-1])
	return yVec

def yVals(vecVec):
	yVec=[]
	for i in vecVec:
		yVec.append(argMax(i))
	return yVec

def argMax(vec):
	val= modi_model.forward(vec)
	clss="modi"
	if(arnab_model.forward(vec)>val):
		val=arnab_model.forward(vec)
		clss="arnab"
	if(other_model.forward(vec)>val):
		val=other_model.forward(vec)
		clss="other"
	return clss

obs= []

#output.txt
def genVariable(var, stri):
	op= []
	fp= open(stri+ '_output.txt', 'w')

	i= 0
	res= observe(var)
	for dic in res:
		fp.write("For time interval "+str(i)+" to "+str(i+1)+" Arnab- "+str(dic[0])+", modi- "+str(dic[1])+", other- "+str(dic[2])+"\n")
		i+=1

	fp.close()

def observe(li):
	res=[]
	div=0
	count1=0
	count2=0
	count3=0
	for i in li:
		if(div==20):
			res.append([((float)(count1)/(float)(div))*100,((float)(count2)/(float)(div))*100,((float)(count3)/(float)(div))*100])
			div=0
			count1=0
			count2=0
			count3=0
		if(i=="arnab"):
			count1+=1
		elif(i=="modi"):
			count2+=1
		elif(i=="other"):
			count3+=1
		div+=1
	if(div!=1):
		res.append([((float)(count1)/(float)(div))*100,((float)(count2)/(float)(div))*100,((float)(count3)/(float)(div))*100])
	return res



arnab_model= genModel(getData('arnab_1_trg_vq.txt'))
modi_model= genModel(getData('modi_1_trg_vq.txt'))
other_model= genModel(getData('music_1_trg_vq.txt'))


var= []
var.append(testVals('test/a1_p2_test_vq.txt'))
var.append(testVals('test/c7_p2_test_vq.txt'))
var.append(testVals('test/c8_p2_test_vq.txt'))
var.append(testVals('test/c9_p2_test_vq.txt'))

genVariable(var[0], 'output/a1_p2')
genVariable(var[1], 'output/c7_p2')
genVariable(var[2], 'output/c8_p2')
genVariable(var[3], 'output/c9_p2')