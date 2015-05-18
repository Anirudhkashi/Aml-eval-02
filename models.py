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
	val= silent_model.forward(vec)
	clss="silent"
	if(single_model.forward(vec)>val):
		val=single_model.forward(vec)
		clss="single"
	if(multi_model.forward(vec)>val):
		val=multi_model.forward(vec)
		clss="multi"
	return clss

obs= []

#output.txt
def genVariable(var, stri):
	op= []
	fp= open(stri+ '_output.txt', 'w')
	s= ''
	i= 0
	for val in var:
		d= {}
		d[i]= val
		op.append(d)
		i+= 50

	op= str(op)
	fp.write(op)
	fp.close() 


def cState(li):
	count1=0
	count2=0
	count3=0
	for i in li:
		if(i=="silent"):
				count1+= 1
		elif(i=="single"):
				count2+= 1
		elif(i=="multi"):
				count3+= 1
		di={"silent":count1,"single":count2,"multi":count3}
	return di


def qIndex(vec):
	stDic=cState(vec)
	qInd=10*stDic['silent']+10*stDic['single']-10*stDic['multi']
	qInd/= len(vec)
	return qInd




single_model= genModel(getData('single_1_trg_vq.txt'))
multi_model= genModel(getData('multi_1_trg_vq.txt'))
silent_model= genModel(getData('silent_1_trg_vq.txt'))

# var1= testVals('single_2_trg_vq.txt')
# var2= testVals('multi_2_trg_vq.txt')

# genVariable(var1, 'single')
# genVariable(var2, 'multi')

# print(qIndex(var1))
# print(qIndex(var2))

var= []
for i in range(1, 11):
	var.append(testVals('test/c'+str(i)+'_test_vq.txt'))

j=1
for i in var:
	genVariable(i, 'output/c'+str(j))
	j+=1

j=1
for i in var:
	print 'Test for file c',j, ' =', qIndex(i)
	j+=1