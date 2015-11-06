# used as an object representing a tweet in 'window'-deque structure
class tweetnode:
	def __init__(self,s,t):
		# lower-cases tweet text (which was cleaned from unicode/escape * earlier)
		# removes all hashtag duplicates as well as empty hashtags
		self.tags = filter(None, set(part[1:] for part in s.lower().split() if part.startswith('#')))
		self.timetweet = t
		# boolean-flag to indicate that there are at least two hashtags
		if len(self.tags)>1:
			self.process = True
		else:
			self.process = False
