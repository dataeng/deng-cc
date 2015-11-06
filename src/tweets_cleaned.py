import sys,re,json,time,collections
from tweet import tweetnode
from tweets_graph import hashtaggraph

# to remove unicode characters
def rmv_non_ascii(text):
	return re.sub(r'[^\x00-\x7F]+','', text)

# to remove escape characters
def rmv_escape(text):
	tt = text.replace('\/', '/')
	tt = tt.replace(r'\\', '\\')
	tt = tt.replace('\"', '"')
	tt = tt.replace('\'', "'")
	tt = tt.replace('\n', ' ')
	tt = tt.replace('\t', ' ')
	return ' '.join(tt.split())


if len(sys.argv) != 4:
	raise Exception('Usage: python tweets_cleaned.py input_path output_ft1_path output_ft2_path')

input_path = sys.argv[1]
output_f1_path = sys.argv[2]
output_f2_path = sys.argv[3]

try:
	# open file with raw tweets
	rawdata = open(input_path, 'r')
	# open output file with cleaned tweets
	output_f1 = open(output_f1_path, 'w')
	# open output file with average degrees
	output_f2 = open(output_f2_path, 'w')
except Exception, e:
	raise e

# num. of tweets with unicode characters
ucounter = 0

# hashtag graph structure
# defined in 'tweets_graph.py'
htg = hashtaggraph()

# deque() from collections is used for keeping (60 s)-window of tweets
# tweet objects in deque defined in 'tweet.py'
deque = collections.deque()
# add 'artificial' first empty tweet to simplify processing of the first real tweet from the batch 
deque.append( tweetnode('',time.mktime(time.strptime("Sat Oct 1 00:00:00 +0000 2005",'%a %b %d %H:%M:%S +0000 %Y'))) );


# read tweets from input file
for line in rawdata:

	# transform json to dictionary		
	tweet = json.loads(line)

	# to avoid dealing with lines like '{"limit": ...'
	# only lines with 'text' and 'created_at' are considered 
	if (tweet.get('text') and tweet.get('created_at') ):

		# remove non-ASCII characters
		ascii_text = rmv_non_ascii(tweet['text'])
		# calculate those with unicode characters
		if len(tweet['text']) != len(ascii_text):
			ucounter += 1
		
		# remove escape chars
		ascii_text = rmv_escape(ascii_text)
		# extract timestamp
		time_text = ' (timestamp: ' + tweet['created_at'] + ')'
		# write cleaned tweet to file
		output_f1.write(ascii_text + time_text + '\n')
		
		# create tweet object for 'window'-structure
		# transform timestamp to float number  
		tweet_pr = tweetnode(ascii_text,time.mktime(time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))

		# remove tweets which are out of 60s window and remove hashtags from graph
		while len(deque)>0 and (tweet_pr.timetweet - deque[0].timetweet > 60):
			# 'process' is boolean attribute to indicate whether there is two or more 
			# hashtags (True) or less than two (False)
			# no updates in hashtag graph needed if False
			if deque[0].process:
				htg.remove(deque.popleft().tags)
			else:
				deque.popleft()

		# add tweet object to 'window'-deque and update graph
		htg.update(tweet_pr.tags)
		deque.append(tweet_pr)

		# write average degree for current hashtag graph		
		output_f2.write('{:.2f}'.format(htg.get_average_degree()) + '\n')

	else:
		continue

# append info about tweets with unicode to the end of output_f1
output_f1.write(str(ucounter) + ' tweets contained unicode.')

# close files
rawdata.close()
output_f1.close()
output_f2.close()
