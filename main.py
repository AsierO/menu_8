import editdistance
import pickle
import numpy as np

#My approach to pseudo-semantic clustering it is based on edit distance. It is a greedy algorithm with an input corresponding
#to the date_chall_shorter.txt file of words. We will proceed bottom-up by creating mini clusters of words
#that are 1 edit distance away. Then we will calculate the edit distance for all combinations of clusters, find the most
#similar clusters (those with smaller edit distance) and merge them together. Repeat this process until we obtain the required
#amount of clusters, in this case 4. The cluster distance can be defined in many ways: min, max, average,.. In this case
#we have use the average edit distance between all posible combinations of elements in the clusters.
#Note that for the first part of generating the initial clusters and then merging them we have similar but different approachs.
#

#Load the input file

word_list=pickle.load( open( "dale_chall_shorter.p", "rb" ) )

print 'Generating initial clusters...'
#First round of edit distance calculation between all words
edit_dis_dict={}
for i in range(0,len(word_list)):
    for j in range(i+1,len(word_list)):
        val_loop=editdistance.eval(word_list[i], word_list[j])
        edit_dis_dict[(i,j)]=val_loop


#Separate the strings that have edit distance with respect to any other string from those who do not.
distance_one=[it for it in edit_dis_dict.keys() if edit_dis_dict[it]==1]
distance_one_list=list(np.unique(list(distance_one)))

distance_not_one=[it for it in range(len(word_list)) if it not in distance_one_list]



#If the edit distance between them is 1 put it in the same cluster
#This approach it is a bit redundant but exact
first_clusters=[]
used=[]
for ky in distance_one:
    #If one is there the other is too
    loop_cluster=[]
    loop_cluster=loop_cluster+list(ky)
    #print loop_cluster
    cluster_val=[k2 for (k1,k2) in distance_one if (k1==ky[0] or k1==ky[1]) ]
    cluster_val2=[k1 for (k1,k2) in distance_one if (k2==ky[0] or k2==ky[1]) ]
    res_loop=np.unique(loop_cluster+cluster_val+cluster_val2)
    #Add it to the cluster list
    first_clusters.append(list(res_loop))
    #Updated the already set words
    used = used+list(res_loop)


#Proceed to compress the clusters
lp_cluster_old=first_clusters


while True:
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

    #If there are no clusters with elements in common stop the loop
    if 1 not in common_dict.values():
        break

    #Put the cluster with elements in common together
    new_clusters=[]
    used2=[]
    for ky in common_one:
        #If one is there the other is too
        #Determine which clusters have been merged
        if ky[0] and ky[1] not in used2:
            loop_cluster=[]
            loop_cluster=loop_cluster+list(ky)
            #print loop_cluster
            cluster_val=[k2 for (k1,k2) in common_one if (k1==ky[0] or k1==ky[1]) ]
            cluster_val2=[k1 for (k1,k2) in common_one if (k2==ky[0] or k2==ky[1]) ]
            res_loop=np.unique(loop_cluster+cluster_val+cluster_val2)
            #Add it to the cluster list
            new_clusters.append(list(res_loop))
            #Updated the already set words
            used2 = list(np.unique(used2+list(res_loop)))

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

    #Make the new list the old one
    lp_cluster_old=list(lp_cluster_new)

#First clustering is now complete, let us now add the words that had no edit distance 1 with respect to any other

for elm in distance_not_one:
    lp_cluster_new.append([elm])

#Now we measure the edit distance between clusters.
#There are many ways of using the edit distance: min, max, average,...
#We will use the average of the edit distance between elements of each clusters

lp_cluster_old=sorted(list(lp_cluster_new))

print 'Reducing the number of Clusters...'
while True:
#for i in range(21):
    edit_dis_clus_dict={}
    for i in range(0,len(lp_cluster_old)):
        for j in range(i+1,len(lp_cluster_old)):
            #Selected i and j cluster calculate the edit distance
            edit_dis_clus=[]
            for elmi in lp_cluster_old[i]:
                for elmj in lp_cluster_old[j]:
                    val_loop=editdistance.eval(word_list[elmi], word_list[elmj])
                    edit_dis_clus.append(val_loop)
            edit_dis_clus_dict[(i,j)]=float(sum(edit_dis_clus))/len(edit_dis_clus)

    #Determine minimum distance
    min_dist=min(edit_dis_clus_dict.values())

    common_one=[it for it in edit_dis_clus_dict.keys() if edit_dis_clus_dict[it]==min_dist]
    #common_one=sorted(common_one)
    common_one_list=list(np.unique(list(common_one)))

    common_zero=[it for it in edit_dis_clus_dict.keys() if edit_dis_clus_dict[it]!=min_dist]
    common_zero_list=list(np.unique(list(common_zero)))
    common_zero_list2=[it for it in common_zero_list if it not in common_one_list]

    new_clusters=[]
    used2=[]
    for ky in common_one:
        if (ky[0] not in used2) and (ky[1] not in used2):
            loop_cluster=[]
            loop_cluster=loop_cluster+list(ky)
            res_loop=np.unique(loop_cluster)
            new_clusters.append(list(res_loop))
            #Updated the already set words
            used2 = list(np.unique(used2+list(res_loop)))

    #Check for missing clusters
    missing_clusters=[it for it in common_one_list if it not in used2]

    #Create the new list
    lp_cluster_new=[]

    #Unravel the cluster notation
    for elm in new_clusters:
        term_append=[]
        for it in elm:
            term_append = list(np.unique(term_append + lp_cluster_old[it]))
        lp_cluster_new.append(term_append)

    #And the clusters we have missed
    for elm in missing_clusters:
        lp_cluster_new.append(lp_cluster_old[elm])

    #Lets not forget to add those clusters that did not have the minimum amount in common
    for elm in common_zero_list2:
        lp_cluster_new.append(lp_cluster_old[elm])

    new_old=[item for sublist in lp_cluster_old for item in sublist]
    new_new=[item for sublist in lp_cluster_new for item in sublist]
    vals=[it for it in new_old if it not in new_new]

    print 'Cluster reduction from '+str(len(lp_cluster_old))+' to '+ str(len(lp_cluster_new))
    #Make the new list the old one
    lp_cluster_old=list(lp_cluster_new)

    if len(lp_cluster_old)<5:
        print 'Enough done...'
        break


print 'Results by cluster:'

for i in range(len(lp_cluster_new)):
    elm_list=[word_list[it] for it in lp_cluster_new[i]]
    print 'Cluster number '+str(i+1)+' :'
    print len(elm_list),elm_list

#Due to the fact that the input file has words starting with a,b,c,d. I divided my data into 4 clusters.
#The approach works roughly ok, the main problem is the existence of a huge cluster (cluster 1) that takes
#most of the data. Once limitations are set to the size of the clusters this approach could work.
# Other features to be implemented would be different parameters controlling the interaction between clusters.
#It should be studied the way the average edit distance behaves for different clusters.
#Other distances should be taken into consideration besides the edit distance to improve the results.
#





















