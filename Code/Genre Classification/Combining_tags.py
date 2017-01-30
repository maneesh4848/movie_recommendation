import json
ob=open("train/movies.json")
data=json.load(ob)

def sorted_tags(data):
    tag = {}
    for i in data:
        for j in data[i][1]:
            j=j.lower()
            if j in tag:
                tag[j] += 1
            else:
                tag[j] = 1

    x = sorted(tag.items(), key=lambda (x, y): -y)
    tags={}
    tags['tag_counts']=x        # tag_counts gives the count of each tags in the entire train data
    all_tags = []
    for i in x:
        all_tags.append(i[0])
    tags['tag_names']=all_tags  #tag_names gives the names of all individual tags
    return tags


def combined_tags(tags,tag_name): #gives the list tags that is a combination of two different primary tags(action/adventure->action and adventure)
    c_tags=[]
    for i in tags:
        if tag_name in i:
            c_tags.append(i)
    return c_tags

def count_tag(tag_counts,tag): #gives the count of any particular tag
    for i in tag_counts:
        if i[0]==tag:
            return i[1]
    return "tag not found"

def top_n_tags(data,n): # Returns n genres that have the highest number of movies classifed under them
    tag_names = sorted_tags(data)['tag_names'][:n]
    return  tag_names


def movies_with_only_secondary_tags(data,n):
    movie_list = []
    primary_tags=top_n_tags(data,n)
    for i in data:
        itags=[]
        for z in data[i][1]:
            itags.append(z.lower())
        itags=set(itags)

        ptags=set(primary_tags)
        res=itags.intersection(ptags)
        if len(res)==0:
            movie_list.append(i)
    return movie_list





tag_counts= sorted_tags(data)['tag_counts']   #Dictionary containing genre name as key and the number of movies under each genre as value
tag_names= sorted_tags(data)['tag_names'] #List of all genres



new_tags=['drama','comedy','romance','action','thriller','adventure','crime','horror','indie','western','music','fantasy','horror','world cinema','science fiction','mystery','war film','family','other language','sports','romantic','musical','history','historical','other category','coming of age']
rename={'romantic':'romance', 'musical':"music", 'parody':'comedy','japanese movies':'world cinema','filipino movies':'world cinema','chinese movies':'world cinema','slasher':'horror','martial arts film':'action','bollywood':'world cinema','historical':'history', 'swashbuckler films':'action', 'satire':'comedy','media satire':'comedy','animation':'family',"short film":'other category','documentary':'other category',"children's":"family","silent film":'other category',"film noir":'crime',"pornographic movie":'other category',"lgbt":'other category',"surrealism":'other category', "experimental film":'other category', "avant-garde":'other category',"spy":'other category',"anime":'family',"biographical film":'other category','disaster':'other category','teen':'other category','black-and-white':''}
#musical=music, roamce=romantic, action/adventure=action and adventure 'black-and-white'=nil,romantic drama= romance.drama

#if new tags were extracted and rename was done, we would loose tags like 'japanese movies','suspense movies' etc which could have ben converted to thriller and world cinema
#if rename was done and then new tags were extracted,  then we would have romantic and romance as seperate similarly musial and music would be seprate tags

tag={}
for i in tag_names:
    x=combined_tags(tag_names,i)
    if len(x)>1:
        tag[i]=len(x)


print  tag_counts
y=sorted(tag.items(),key= lambda (a,b): -b)
print y
z={}
for i in tag_names:
    y=combined_tags(tag_names,i)
    if len(y)>1:
        z[i]=y



new_tags_dic1={}    # replace secondary tags with main tags, (filipinio movies-> world movies)
for i in data:
    new_tags_dic1[i]=[]
    temp=[]
    for k in data[i][1]:
        temp.append(k.lower())
    for l in temp:
        if l in rename:
            new_tags_dic1[i].append(rename[l])
        else:
            new_tags_dic1[i].append(l)

# print new_tags_dic1['6301978242']




new_tags_dic2={}             #extracts main genres hidden inside subgenres (melodraam->drama)
for i in new_tags_dic1:
    new_tags_dic2[i]=[]
    temp=[]
    for k in new_tags_dic1[i]:
        temp.append(k.lower())
    for l in temp:
        for j in new_tags:
            if j in l:
                new_tags_dic2[i].append(j)

    new_tags_dic2[i]=set(new_tags_dic2[i])
    new_tags_dic2[i]=list(new_tags_dic2[i])


# print new_tags_dic2['6301978242']


new_tags_dic3={}    # again replace  newly generated secondary tags with main tags,
for i in data:
    new_tags_dic3[i]=[]
    temp=[]
    for k in new_tags_dic2[i]:
        temp.append(k.lower())
    for l in temp:
        if l in rename:
            new_tags_dic3[i].append(rename[l])
        else:
            new_tags_dic3[i].append(l)


    new_tags_dic3[i]=set(new_tags_dic3[i])
    new_tags_dic3[i]=list(new_tags_dic3[i])
#
# print new_tags_dic3['6301978242']


count=0           #finding movies with no tags
lst=[]
for i in new_tags_dic3:
    if len(new_tags_dic2[i])<1:
        count+=1
        lst.append(data[i][0])


print len(lst)


dic={}

for i in data:
    dic[i]=data[i]
    dic[i][1]=new_tags_dic3[i]


keys=dic.keys()
for i in keys:
    if len(dic[i][1])<1:
        del dic[i]      #Removing movies with no tags, so that they can be added to th test data

lst=[]
for i in dic:
    if len(dic[i][1])<1:
        lst.append(dic[i][0])




ob1=open("train/movies3.json",'w+')
json.dump(dic,ob1)
