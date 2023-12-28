from flask import Flask
import requests
from flask import request
from flask_cors import CORS,cross_origin

app = Flask(__name__)
CORS(app)

headers = {"Authorization": "Bearer 15bae2f95d72a9039a165a4fcb9c89bfb51416ed"}

query2 = """

 query { 
  repository(owner:"isaacs", name:"github") { 
    issues(states:OPEN) {
      totalCount
    }
  }
}

"""

query3 = """

 query { 
  repository(owner:"isaacs", name:"github") { 
    issues(states:OPEN createdAt:2019-02-23) {k
      totalCount
    }
  }
}

"""



issueCounts = [0,0,0,0]

#dummy values
issueCounts[0] = 1
issueCounts[1] = 2
issueCounts[2] = 3
issueCounts[3] = 4
owner = ""
reponame = ""


@cross_origin()
@app.route("/issues")
#@cross_origin(supports_credentials=True)
def index():
	owner = request.args['owner']
	reponame = request.args['reponame']

	queryTemplate = Template(
		"""{
		  repository(owner: $owner, name: $reponame) {
		    issues(states: OPEN) {
		    totalCount
		    }
		  }
		}
		"""
		)


  query = queryTemplate.substitute(owner=owner,reponame=reponame)

  request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)

	if request.status_code == 200:
		result = request.json()
		totalCount = result['data']['repository']['issues']['totalCount']
	else:
		raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


	# Open issues in last 24 hours
	# less than 7 days
	# more than 7 days

	queryTemplate = Template(
		"""query Counter {
		     repository(owner: $owner, name: $reponame) {
		       issues(states: OPEN, last:100) {
                 pageInfo {
                   startCursor
                   hasPreviousPage
                 }
                 nodes {
                   createdAt
                 }
               }
             }
           }
        """
    )

    query = queryTemplate.substitute(owner=owner,reponame=reponame)

    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    data = request.json()

    issues = data['data']['repository']['issues']
    prevPage = issues['pageInfo']['hasPreviousPage']

    below24 = 0
    below7 = 0

    now = datetime.now(tz=pytz.utc)
    oneDayAgo = now - timedelta(days=1)
    sevenDaysAgo = now - timedelta(days=7)


    while prevPage == True:
      done = False
      for i in reversed(issues['nodes']):
        createdAt = parser.parse(i['createdAt'])
        if createdAt > oneDayAgo:
            below24 = below24 + 1
        elif createdAt > sevenDaysAgo:
            below7 = below7 + 1
        else:
            # since we already have total count
            # we can subtract from that to get above 7 days count
            done = True
            break
      if done:
        break

      startCursor = issues['pageInfo']['startCursor']
      before = f"last:100, before:\"{startCursor}\""
      next_query = query.replace("last:100", before)
      request = requests.post('https://api.github.com/graphql', json={'query': next_query}, headers=headers)
      data = request.json()

      issues = data['data']['repository']['issues']
      prevPage = issues['pageInfo']['hasPreviousPage']

    above7 = totalCount - (below24 + below7)

    issueCounts[0] = totalCount
    issueCounts[1] = below24
    issueCounts[2] = below7
    issueCounts[3] = above7

    #find_issues() 
    return str(issueCounts)
    #return "hey"





@app.route("/findissues")
def find_issues():



	#http://127.0.0.1:5000/issues?owner=octocat&reponame=Hello-World

    #request = requests.post('https://api.github.com/graphql', json={'query': query2}, headers=headers)  works fine
    request = requests.post('https://api.github.com/graphql', json={'query': query3}, headers=headers)

    

    if request.status_code == 200:
    	result = request.json()
    	return str(result)
    else:
    	raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))





if __name__ == "__main__":
	app.run(debug=True)







"""

# An example to get the remaining rate limit using the Github GraphQL API.'''



#import requests









'''def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.

    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)

    if request.status_code == 200:

        return request.json()

    else:

        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))



        
@app.route("/repo")
def run_query():

	request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)

	if request.status_code == 200:
		result = request.json()
		return str(result["data"]["rateLimit"]["remaining"])
	else:
		raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
# The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.       

query = """

'''{

  viewer {

    login

  }

  rateLimit {

    limit

    cost

    remaining

    resetAt

  }

}

"""



result = run_query(query) # Execute the query

remaining_rate_limit = result["data"]["rateLimit"]["remaining"] # Drill down the dictionary

print("Remaining rate limit - {}".format(remaining_rate_limit))'''