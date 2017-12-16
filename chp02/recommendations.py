# -*- coding: utf-8 -*-
# @Time    : 2017/12/16 上午12:12
# @Author  : 伊甸一点
# @FileName: recommendations.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

import matplotlib.pyplot as plt
import math

# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
      'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
      'The Night Listener': 3.0},
     'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
      'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
      'You, Me and Dupree': 3.5},
     'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
      'Superman Returns': 3.5, 'The Night Listener': 4.0},
     'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
      'The Night Listener': 4.5, 'Superman Returns': 4.0,
      'You, Me and Dupree': 2.5},
     'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
      'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
      'You, Me and Dupree': 2.0},
     'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
      'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
     'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

print type(critics)

x_durpre = []
y_snakes = []
key_list = []

for key in critics.keys():
    if(critics[key].has_key('Snakes on a Plane') and critics[key].has_key('You, Me and Dupree')):
        key_list.append(key)
        x_durpre.append(critics[key]['You, Me and Dupree'])
        y_snakes.append(critics[key]['Snakes on a Plane'])

print x_durpre,y_snakes
n = len(x_durpre)

fig = plt.figure(111)
plt.xlim(xmax=5,xmin=0)
plt.ylim(ymax=5,ymin=0)
plt.plot(x_durpre,y_snakes,'ro')

for i in range(n):
    plt.annotate(key_list[i]+'\n',xy=[x_durpre[i],y_snakes[i]])
plt.title('Snakes and Dupree')
fig.savefig('pics/Snakes and Dupree result.jpg')
plt.show()

matrix_distance = [[]] * n

for i in range(n):
    dis_vect = []
    for j in range(n):
        if(i == j):
            dist = 0
        else:
            dist = math.sqrt(math.pow(x_durpre[i]-x_durpre[j],2) + math.pow(y_snakes[i] - y_snakes[j],2))
        dis_vect.append(dist)
    matrix_distance[i] = dis_vect

for i in range(n):
    print matrix_distance[i]

def sim_dist(critics, person1, person2):
    share_list = {}
    for item in critics[person1]:
        if(item in critics[person1]):
            share_list[item] = 1
    if(len(share_list)==0):
        return 0
    sum_num = sum(math.pow(critics[person1][item]-critics[person2][item],2)
               for item in critics[person1].keys() if item in critics[person2].keys())
    return 1/(1+sum_num) # here can be different
    #return 1/(1+ math.sqrt(sum_num))
print 'Lisa Rose and Gene Seymour sim is:'+ str(sim_dist(critics,'Lisa Rose','Gene Seymour'))

def sim_person(critics,person1,person2): # calculate the similarity between person1 and person2
    share_dic = {}
    for item in critics[person1].keys():
        if item in critics[person2].keys():
            share_dic[item]=1
    n = len(share_dic)
    if 0==n:
        return 0 # here is different in english book and Zh-cn
        #return 1 # chinese
    sum1 = sum([critics[person1][item] for item in share_dic])
    sum2 = sum([critics[person2][item] for item in share_dic])

    sumPow1 = sum([math.pow(critics[person1][item],2) for item in share_dic])
    sumPow2 = sum([math.pow(critics[person2][item],2) for item in share_dic])

    productSum = sum([critics[person1][item] * critics[person2][item] for item in share_dic])

    num = productSum - (sum1*sum2)/n
    den = math.sqrt((sumPow1 - math.pow(sum1,2)/n) * (sumPow2 - math.pow(sum2,2)/n))

    if den == 0:
        return 0
    return num/den

def plot_person_like(critics,person1,person2,show_flag = 0): # plot the like item between person1 and person2
    plt.clf()
    x = []
    y = []
    share_key = []
    for key in critics[person1].keys():
        if(key in critics[person2].keys()):
            x.append(critics[person1][key])
            y.append(critics[person2][key])
            share_key.append(key)
    plt.xlim(xmax=6, xmin=0)
    plt.ylim(ymax=6, ymin=0)
    plt.plot(x,y,'or',label=person1+' and '+person2)
    plt.legend()
    for i in range(len(x)):
        plt.annotate(share_key[i]+'\n',xy=[x[i],y[i]])
    old_sim = str(sim_dist(critics,person1,person2))
    sim = str(sim_person(critics, person1, person2))
    print person1+' and '+ person2+' old_sim: '+old_sim + ' sim: '+sim
    # plt.title(person1+' and '+person2 +
    #           ' share numbers: '+str(len(share_key))) # add share interests numbers
    # plt.title(person1 + ' and ' + person2 +
    #           ' share numbers: ' + str(len(share_key)) + # add share interests numbers
    #           ' similarity is: '+ str(sim_person(critics,person1,person2))) # add similarity to title
    plt.title(' share numbers: ' + str(len(share_key)) +  # add share interests numbers
              ' old sim is: '+ old_sim + # add old similarity to title
              ' similarity is: ' + sim)  # add similarity to title
    plt.xlabel(person1)
    plt.ylabel(person2)
    plt.savefig('pics/'+person1+' and '+person2+' result.jpg')
    if(show_flag==1):
        plt.show()


x_person = [item for item in critics.keys()]
y_person = x_person
num = len(x_person)
[plot_person_like(critics,x_person[item_i],y_person[item_j]) for item_i in range(num) for item_j in range(item_i+1,num)]

def topMatch(critics, person, n, similarity = sim_person):
    scores = [(similarity(critics,person,other),other) for other in critics if other!=person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

for person in x_person:
    print person+' top 3 are: ',topMatch(critics,person,3)

def getRecommendation(critics,person,similarity = sim_person):
    totals = {}
    simSums = {}
    for other in critics:
        if other == person:
            continue
        sim = similarity(critics,person,other)
        if sim <= 0 :
            continue
        for item in critics[other]:
            if item not in critics[person] or critics[person][item]==0:
                totals.setdefault(item,0)
                totals[item] += sim*critics[other][item]
                simSums.setdefault(item,0)
                simSums[item]+=sim
    rankings = [ (total / simSums[item], item) for item,total in totals.items()]
    rankings.sort()
    rankings.reverse()

    return rankings

for person in x_person:
    if len(getRecommendation(critics,person,sim_person)) == 0:
        print person +' have watched moveis : '+ str(len(critics[person]))+'-------- no other recommendations.'
    else :
        print person +' have watched moveis : '+ str(len(critics[person]))+' -------- otehr recommendations are',str(getRecommendation(critics,person,similarity=sim_dist))

def convertItem(critics):
    convert = {}
    for person in critics:
        for item in critics[person]:
            convert.setdefault(item,{})
            convert[item][person] = critics[person][item]
    return convert

movies = convertItem(critics)
print 'Superman Returns top matches',topMatch(movies,'Superman Returns',5,similarity=sim_person)
print 'Just My Luck getRecommendation are',getRecommendation(movies,'Just My Luck',similarity=sim_person)


plot_person_like(movies,'Just My Luck','Superman Returns',1)