# hashtag graph
# nodes attribute leads to dictionary with keys - hashtagnames
# x.nodes[key] leads to list of relevant hashtags including key itself
class hashtaggraph:
	def __init__(self):
		self.nodes = {} 
	
	# to add hashtags to graph
	def update(self, hashtags):
		# do nothing if only no or just one hashtag 
		if (not hashtags or len(hashtags)<2):
			return

		hashtags = [x.encode('ascii') for x in hashtags]
		
		# update
		for tag in hashtags:
			if tag not in self.nodes.keys():
				self.nodes[tag] = hashtags
			else:
				self.nodes[tag] = list( set(self.nodes[tag] + hashtags) )

	# to remove hashtags to graph        
	def remove(self, hashtags):
		# do nothing if only no or just one hashtag
		if (not hashtags or len(hashtags)<2):
			return

		hashtags = [x.encode('ascii') for x in hashtags]

		# remove		
		for tag in hashtags:
			if tag in self.nodes:
				self.nodes[tag] = list( set(self.nodes[tag]) - set(hashtags) )
				self.nodes[tag] = self.nodes[tag] + [tag]
				# node removal condition
				if len(self.nodes[tag])<2:
					self.nodes.pop(tag, None)
			else:
				return

	# print out vertices
	def tostring(self):
		for key in self.nodes:
			print(key + " - " + str(self.nodes[key]))

	# average degree calculation
	def get_average_degree(self):
		sum = 0
		for key in self.nodes:
			sum += len(self.nodes[key]) - 1;
		if len(self.nodes)==0:
			return 0
		else:
			return round(float(sum) / float(len(self.nodes)), 2)
