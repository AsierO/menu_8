import editdistance
import pickle

print editdistance.eval('banana', 'bama')

word_list=pickle.load( open( "dale_chall_shorter.p", "rb" ) )

print word_list[88], word_list[1], word_list[100]

print editdistance.eval(word_list[88], word_list[1])

#print editdistance.eval(word_list[88], word_list[1000])

#First round of edit distance calculation between all words
edit_dis_dict={}
for i in range(0,len(word_list)):
    for j in range(i+1,len(word_list)):
        val_loop=editdistance.eval(word_list[i], word_list[j])
        edit_dis_dict[(i,j)]=val_loop

print edit_dis_dict[(1,2)]
print word_list[1], word_list[2]






