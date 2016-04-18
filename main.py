import editdistance
import pickle
import numpy as np

p=[ [1,2,3],
    [1,9,9],[2,4]]

print list(p)

result = set(p[0])
for s in p[1:]:
    result.intersection_update(s)
#print result


#print editdistance.eval('banana', 'bama')

word_list=pickle.load( open( "dale_chall_shorter.p", "rb" ) )

print len(word_list)

#print word_list[88], word_list[1], word_list[100]

#print editdistance.eval(word_list[88], word_list[1])

#print editdistance.eval(word_list[88], word_list[1000])

#First round of edit distance calculation between all words
edit_dis_dict={}
for i in range(0,len(word_list)):
    for j in range(i+1,len(word_list)):
        val_loop=editdistance.eval(word_list[i], word_list[j])
        edit_dis_dict[(i,j)]=val_loop

#print edit_dis_dict[(1,2)]
#print word_list[1], word_list[2]

#If the edit distance between them is 1 put it in the same cluster
distance_one=[it for it in edit_dis_dict.keys() if edit_dis_dict[it]==1]
distance_one_list=list(np.unique(list(distance_one)))

distance_not_one=[it for it in range(len(word_list)) if it not in distance_one_list]

print len(distance_one_list),distance_one_list
print len(distance_not_one),distance_not_one
print len(word_list)


#test
val=[(k1,k2) for (k1,k2) in distance_one if (k1==212 or k1==212) ]
val2=[(k1,k2) for (k1,k2) in distance_one if (k2==212 or k2==212) ]

#print val
#print val2

#Very redundant but exact
first_clusters=[]
test=[distance_one[:3]]
print len(np.unique(list(distance_one)))
used=[]
for ky in distance_one:
    #If one is there the other is too
    #if ky[0] not in used:
    loop_cluster=[]
    loop_cluster=loop_cluster+list(ky)
    #print loop_cluster
    cluster_val=[k2 for (k1,k2) in distance_one if (k1==ky[0] or k1==ky[1]) ]
    cluster_val2=[k1 for (k1,k2) in distance_one if (k2==ky[0] or k2==ky[1]) ]
    res_loop=np.unique(loop_cluster+cluster_val+cluster_val2)
    #for i in cluster_val:
    #    cluster_val_l=[k2 for (k1,k2) in distance_one if (k1==i or k1==i) ]
    #print cluster_val
    #print cluster_val2
    #print 'unique', np.unique(loop_cluster+cluster_val+cluster_val2)
    #print loop_cluster+cluster_val
    #res_loop=np.unique(loop_cluster+cluster_val+cluster_val2)
    #print res_loop
    #Add it to the cluster list
    first_clusters.append(list(res_loop))
    #Updated the already set words
    used = used+list(res_loop)
    #if len(used) != len(np.unique(used)):
    #    print 'ERROR!'
    #    break
    #print 'used', sorted(used)

#print 'first clusters', first_clusters
#print 'first clusters', first_clusters[0]

#Compress the clusters
lp_cluster_old=first_clusters

len_fi=[len(x) for x in first_clusters]

print 'length comparison', sum(len_fi)
print first_clusters

#lp_cluster_old=[[1,2,3],[3,4,5],[5,6,7],[999], [888]]
while True:
#for i in range(4):
    #Check if there are cluster with elements in common
    #No checking with itself so eventually the value 1 should disappear
    common_dict={}
    for i in range(0,len(lp_cluster_old)):
        for j in range(i+1,len(lp_cluster_old)):
            res=[itt for itt in lp_cluster_old[i] if itt in lp_cluster_old[j]]
            if len(res) !=0:
                common_dict[(i,j)]=1
            else:
                common_dict[(i,j)]=0

    #Choose those keys that represent clusters with elements in common
    common_one=[it for it in common_dict.keys() if common_dict[it]==1]
    common_one_list=list(np.unique(list(common_one)))

    common_zero=[it for it in common_dict.keys() if common_dict[it]==0]
    common_zero_list=list(np.unique(list(common_zero)))
    common_zero_list2=[it for it in common_zero_list if it not in common_one_list]

    #common_zero=[(k1,k2) for (k1,k2) in common_dict.keys() if (k1 not in common_one_list)]
    #common_zero2=[it for it in common_zero if (it not in common_one_list)]
    #common_zero_list=list(np.unique(list(common_zero2)))

    print 'common zero', len(common_zero_list2), len(common_one_list), len(lp_cluster_old)
    print 'common zero list', len(common_zero_list2), common_zero_list2
    print 'common one list', len(common_one_list), common_one_list
    print common_one

    #If there are no clusters with elements in common stop the loop
    if 1 not in common_dict.values():
        break

    #Put the cluster with elements in common together
    new_clusters=[]
    used2=[]
    for ky in common_one:
        #If one is there the other is too
        #It is like saying that cluster has been already merged
        if ky[0] and ky[1] not in used2:
            loop_cluster=[]
            loop_cluster=loop_cluster+list(ky)
            #print loop_cluster
            cluster_val=[k2 for (k1,k2) in common_one if (k1==ky[0] or k1==ky[1]) ]
            cluster_val2=[k1 for (k1,k2) in common_one if (k2==ky[0] or k2==ky[1]) ]
            res_loop=np.unique(loop_cluster+cluster_val+cluster_val2)
            #for i in cluster_val:
            #    cluster_val_l=[k2 for (k1,k2) in distance_one if (k1==i or k1==i) ]
            #print cluster_val
            #print cluster_val2
            #print 'unique', np.unique(loop_cluster+cluster_val+cluster_val2)
            #print loop_cluster+cluster_val
            #res_loop=np.unique(loop_cluster+cluster_val+cluster_val2)
            #print res_loop
            #Add it to the cluster list
            new_clusters.append(list(res_loop))
            #Updated the already set words
            used2 = list(np.unique(used2+list(res_loop)))
            #if len(used) != len(np.unique(used)):
            #    print 'ERROR!'
            #    break
            #print 'used2', sorted(used2)
            #print'new clusters', new_clusters

    #Create the new list
    lp_cluster_new=[]
    #Unravel the cluster notation

    for elm in new_clusters:
        term_append=[]
        for it in elm:
            term_append = list(np.unique(term_append + lp_cluster_old[it]))
        lp_cluster_new.append(term_append)

    #Lets not forget to add those clusters that did not have anything in common
    for elm in common_zero_list2:
        lp_cluster_new.append(lp_cluster_old[elm])

    len_old=[len(x) for x in lp_cluster_old]
    len_new=[len(x) for x in lp_cluster_new]

    print 'length comparison', sum(len_old), sum(len_new)
    print lp_cluster_old
    print lp_cluster_new
    #Make the new list the old one
    lp_cluster_old=list(lp_cluster_new)


len_new=[len(x) for x in lp_cluster_new]
print sum(len_new), lp_cluster_new

#First clustering is now complete, let us now add the words that had no edit distance 1 with respect to any other

for elm in distance_not_one:
    lp_cluster_new.append([elm])

#Put an assert here
len_new=[len(x) for x in lp_cluster_new]
print sum(len_new), len(lp_cluster_new), lp_cluster_new

#Now we measure the edit distance between clusters.
#There are many ways of doing this: min, max, average,...
#We will use the average of the edit distance between elements of clusters










