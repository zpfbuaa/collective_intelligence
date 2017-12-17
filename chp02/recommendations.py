# -*- coding: utf-8 -*-
# @Time    : 2017/12/16 上午12:12
# @Author  : 伊甸一点
# @FileName: recommendations.py
# @Software: PyCharm
# @Blog    : http://zpfbuaa.github.io

import matplotlib.pyplot as plt
import math
import csv
import time
import pylast
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

def print_demp():
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

def plot_person_like(critics,person1,person2,show_flag = 0, save_flag = 0): # plot the like item between person1 and person2
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
    if (save_flag==1):
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

def getSimarity(critics,person,top_n=5,similarity = sim_person):
    other_dic = {}

    for other in critics:
        if other == person:
            continue
        sim = similarity(critics,person,other)
        other_dic.setdefault(other,0)
        other_dic[other] = sim

    result = sorted(other_dic.iteritems(), key=lambda asd: asd[1],reverse=True)  # True from large to small, False: from small to large

    return result[0:top_n]
#
# test = (getSimarity(critics,'Lisa Rose'))
# for key in test:
#     print key
print 'getSimarity',getSimarity(critics,'Lisa Rose')
# print type(critics)

def getRecommendation(critics,person,similarity = sim_person,preCalSim = getSimarity,top_n=5,accelerator_flag = 0):
    totals = {}
    simSums = {}
    other_list = []
    pre_other = []
    if accelerator_flag==1:
        pre_other = preCalSim(critics,person,top_n)
        for i in range(top_n):
            other_list.append(pre_other[i][0])
    else:
        other_list = [item for item in critics]
    print 'other_list:',other_list
    for other in other_list:
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


plot_person_like(movies,'Just My Luck','Superman Returns',show_flag=0,save_flag=1)

def calculateSimiliarItems(critics, n=10):

    result = {}
    convert_critics = convertItem(critics)
    for item in convert_critics:
        scores = topMatch(convert_critics, item, n=n, similarity=sim_dist)
        result[item] = scores
    return result

print calculateSimiliarItems(critics,10)

def getRecommendationItems(critics,item_match, person):
    userRatings = critics[person]
    scores = {}
    totalSim = {}
    for (item, rating) in userRatings.items():
        for (similarity, item2) in item_match[item]:
            if item2 in userRatings:
                continue
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity

    rankings = [(score / totalSim[item], item) for item, score in scores.items()]
    rankings.sort()
    rankings.reverse()
    return rankings

for person in x_person:

    item_match = calculateSimiliarItems(critics,10)

    result = getRecommendationItems(critics,item_match,person)
    if len(result) == 0:
        print person+' don\'t have recommendation.'
    else:
        print person+' recommendations are:',result



def load_data(root_path,movies_path = 'movies.csv',rating_path='ratings.csv'):
    movies = {}
    prefs = {}
    with open(root_path+movies_path) as csvfile:
        movies_data = csv.reader(csvfile,delimiter=',')
        header = True
        number = 0 # just to get the top 3000 lines
        for item_movie in movies_data: # (id,title,genres)
            if number>3000: # the running_result_pic: this value is 10000
                break
            id = item_movie[0]
            title = item_movie[1]
            # genres = item_movie[3] # this genres now is useless 2017.12.16 20:06:59
            if header == True:
                header = False
                continue
            movies[id] = title
            number+=1

    with open(root_path+rating_path) as csvfile:
        prefs_data = csv.reader(csvfile,delimiter=',')
        header = True
        number = 0
        for item_pref in prefs_data: #(userId,movieId,rating,timestamp)
            if number > 10000: # the running_result_pic: this value is the total line in ratings.csv 100005
                break
            userId = item_pref[0]
            movieId = item_pref[1]
            rating = item_pref[2]
            # timestamp = item_pref[3] # this timestamp is useless
            prefs.setdefault(userId, {}) # create a dic
            if(movieId in movies.keys()):
                prefs[userId][movies[movieId]] = float(rating) # key is userId, (key is movies_title, value is rating)
                number+=1
    return movies, prefs

moviese, prefs = load_data(root_path='data/ml-latest-small/') # loading data may cost some time
print prefs['15']

def running_movies_demo(run_flag=0):
    if(run_flag==1):
        time1 = time.time()
        recommend1 =  getRecommendation(prefs,'15',accelerator_flag=1)[0:50] # this cost time much than others
        print 'recommend1 are:',recommend1
        time2 = time.time()
        print 'getRecommendation cost time:',time2-time1

        time3 = time.time()
        itemsim = calculateSimiliarItems(prefs,n=10) # just to get the top 10 # the running_result_pic: this value is 20
        time4 = time.time()
        print 'calculateSimiliarItems cost time:',time4-time3

        time5 = time.time()
        recommend2 = getRecommendationItems(prefs,itemsim,'15')[0:50] # this cost longer time to build a total item-based filter

        print 'recommend2 are:',recommend2
        time6 = time.time()
        print 'getRecommendationItems cost time:',time6-time5
        print 'total cost time:',time.time()-time1

run_flag = 0
running_movies_demo(run_flag=run_flag)

def sim_tanimoto(critics, person1, person2): # add exercise 1
    set_a = critics[person1]
    set_b = critics[person2]
    share_dic = {}
    for item in set_a:
        if (item in set_b):
            share_dic[item] = 1

    c = float(len(share_dic))
    if 0 == c:
        return 0
    a = len(set_a)
    b = len(set_b)
    return float(c/(a+b+c))

result = []
[result.append(sim_tanimoto(critics,x_person[i],x_person[j]))for i in range(len(x_person)) for j in range(i+1,len(x_person))]
print 'sim_tanimoto on critics',result
print 'sim_tanimoto on movies',sim_tanimoto(prefs,'10','15')


API_KEY = 'ef90c448f8f4a6cae53d39d57de91f74' # password add exercise 4
API_SECRET ='72a2f98a3f405737382c9255ee54ffc1'
username = '*******'
password_hash = pylast.md5('****************')
network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET, username = username, password_hash = password_hash)

artist = network.get_artist("System of a Down")
print artist
track = network.get_track("Iron Maiden", "The Nomad")
print track
track.love()
track.add_tags(("awesome", "favorite"))
