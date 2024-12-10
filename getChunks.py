import re
import os
import random
import json

def getChunks(lines) :
	chunks = list()
	currentChunk = ''
	shortLine = False
	for line in lines :
		numWords = len(line.split(' '))
		if not numWords or (numWords == 1 and not bool(re.search(r'[a-zA-Z0-9]', line))) :
			continue
		if numWords < 11 :
			if shortLine :
				currentChunk += line
			else :
				chunks.append(currentChunk)
				currentChunk = line
			shortLine = True
		else :
			currentChunk += line
			shortLine = False
	chunks.append(currentChunk)
	del chunks[0]

	return chunks

def main(name) :
	dirs = os.listdir('/Users/Maxthesavage/Desktop/dataset-tosdr-2024-07-15/' + name)
	docType = 'Privacy Policy'
	if 'Privacy Policy' not in dirs :
		docType = dirs[1]
	policyDir = '/Users/Maxthesavage/Desktop/dataset-tosdr-2024-07-15/' + name + '/' + docType
	policies = os.listdir(policyDir)
	with open(policyDir + '/' + policies[0], 'r') as file :
		lines = file.readlines()
		chunks = getChunks(lines)
		toReturn = list()
		for chunk in chunks :
			chunk = chunk.replace('<br>', ' ')
			if len(chunk.split('. ')) < 11 :
				toReturn.append({
					"text": chunk,
					"important": None,
					"label": None
				})
			else :
				sentences = chunk.split('. ')
				shortened = ''
				count = 0
				for sentence in sentences :
					if count == 10 :
						toReturn.append({
							"text": shortened,
							"important": None,
							"label": None
						})
						shortened = ''
						count = 0
					shortened += sentence + '. '
					count += 1
		return toReturn

def getData() :
	myIds = list()
	with open('classifier_data2.json', 'r') as file :
		read = json.load(file)
		for i in read :
			myIds.append(i['id'])

	data = list()

	ids = list()
	dirs = os.listdir('/Users/Maxthesavage/Desktop/dataset-tosdr-2024-07-15')
	for i in range(40) :
		index = random.randint(0, len(dirs) - 1)
		while not os.path.isdir('/Users/Maxthesavage/Desktop/dataset-tosdr-2024-07-15/' + dirs[index]) or 'Privacy Policy' not in os.listdir('/Users/Maxthesavage/Desktop/dataset-tosdr-2024-07-15/' + dirs[index]) or dirs[index] in myIds :
			index = random.randint(0, len(dirs) - 1)
		ids.append(dirs[index])

	for i in ids :
		data.append({
			'id': i,
			'chunks': main(i)
		})

	with open('classifier_data2.json', 'r') as file :
		read = json.load(file)
		print(read[74]['chunks'][0]['label'])
		# read.extend(data)
		# with open('classifier_data2.json', 'w') as file2 :
		# 	json.dump(read, file2, indent=2)

getData()


# go through data and if same label combine those chunks. Idk think about this
# because what if some parts are important and other's aren't - combine important and non-important parts I guess. Also,
# how would this work for new data? Try out different groupings? I think I was saying to use this for summarization
# but the grouping could maybe help with labeling as well?
# seems like the previous chunks sometimes matter so seems you you could do some sort of grouping system? Need to think more about this
# in report can say that we could implement a better way to initially chunk up the data to solve the above issue - issue of headers
# for the groupings, if there was a confidence thing that could help becasue then if when you group some sections, you have high confidence could go with that?
# analyze training data for some based stuff like if surronded by non imoprtant, maybe you are not important. Like personal data label which is around other stuff often not important maybe

# combine end and random, and maye intro?

# could do something like look for labels and important and then if there are the same labels next to eachother and more than half is important, summarize it all? Also sometimes seperated by one, so maybe group those together?

# can say something in report how categories emerged which weren't noted like california law. Just put in other category

# sometimes label header as important but if following two aren't maybe change that label?

# emails - this was added halway through creating the dataset

# on 31

# baseyian next category or important given previous one or two -> see if that makes the predictions any better. I think that
# this would be really good

# data sharing and third parties can be interchangable sometimes

# If data rights are below international thing, then they probably apply to that

# analyze trends in what label comes next

# after data from other countries, data rights aren't important - just don't want to give people's data rights that aren't included. I guess this would mostly be for the US

# could do rule based thing to look for California or other countries to put a label on top of it
# so I want you to do some processing and look for good stuff like data rights and data sharing which has california in it and make 
# some of the important. It would probably be data rights and data sharing
# then add location property to them
# europe, EU, EEA



# Need naive bayes I think bc first few things about personal data usually important while later ones usually not as important. Maybe only for some categories. Because like data rights is usually always important

# bias in labeling -> more likely to be previous label. Could have randomized it but seems like order does matter too

# maybe if one line is important, add the previous few lines? and then summarize?

# maybe could have further categories like google analytics -> possiblity for more rule based stuff






