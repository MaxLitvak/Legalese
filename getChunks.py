import re
import os
import random
import json

# method for getting the chunks given the lines of a privacy policy
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

# method for getting the data for specific privacy policy
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

# method for getting the data for a certain amount of privacy policies
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






