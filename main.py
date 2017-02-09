import codecs
import json
import requests
import string


API_BASE_URL = 'https://sprint.ly/api'
OUTPUT_FILE = 'planning.txt'
STATUSES_TO_ROLLUP = ['completed', 'accepted']
TEMPLATE = "planning_template.txt"

# Search API URL for reference: https://sprint.ly/api/items/search.json?q=tag:spirit-112
# Requires basic auth, with Sprintly API token as "password", email as "username"
def count_points(stories):
  points = {"S": {"value": 1, "subtotal": 0, "count": 0},
            "M": {"value": 3, "subtotal": 0, "count": 0},
            "L": {"value": 5, "subtotal": 0, "count": 0}
            }
  for story in stories:
    sizing = story["score"]
    points[sizing]["subtotal"] += points[sizing]["value"]
    points[sizing]["count"] += 1
  return points
  

def main():
  """
  Retrieving items:

  make a request to get all the stories with a given tag

  Write the results to document.

  TEMPLATE:

  Accomplishments:

  [# of points]

  [[t-shirt size]] ([bug, feature, task]) [link to sprintly item] [[description of sprintly item]]
  [include interrupt tag if it exists]

  Points in progress:

  [points for unfinished stories (would be nice to have size breakdown, links here)]
  """
  # TODO:  Sum the points, count up sizes (aka score fields), include interrupt tags
  # TODO: Sum trailing 4 sprints for a "velocity"
  # TODO: Refactor template to be a template file of some sort, and render a template (html?)
  user_email = raw_input("Auth to the Sprintly API with which email?\n")
  api_token = raw_input("Auth to the Sprintly API with which API token?\n")
  query_tag = raw_input("Search the Sprintly API with which tag?\n")
  descriptions = raw_input("Would you like to include descriptions for each item? (y/n) ").lower()
  request_url = API_BASE_URL + '/items/search.json?q=tag:%s' % query_tag
  # store your sprintly token in an environmental variable from your .bashrc:  export SPRINTLY_TOKEN="abcdefg"
  response = requests.get(request_url, auth=requests.auth.HTTPBasicAuth(user_email, api_token))
  datum = json.loads(response.text)
  rollup_items = [item for item in datum['items'] if item['status'] in STATUSES_TO_ROLLUP]
  point_dict = count_points(rollup_items)
  with codecs.open(OUTPUT_FILE, mode='w', encoding="utf-8") as file, codecs.open(TEMPLATE, mode='r', encoding="utf-8") as template:
    src = string.Template(template.read())
    stories = []
    for item in rollup_items:
      # url = "%s/%s" % (SPRINTLY_URL_BASE, item['id'])
      title = item['title']
      size = item.get('score', '')
      type = item['type']
      link = item['short_url'].rstrip("/")
      description = ""
      if descriptions == "yes" or descriptions == "y":
        description = item['description']

      story = u'{title}\n{size} ({type}) [{link}]\n{description}'.format(
        title=title, size=size, type=type, link=link, description=description
      )
      stories.append(story)
    
    sprint_total_points = 0
    sprint_total_message = ""
    for size in ["S", "M", "L"]:
      sprint_total_points += point_dict[size]["subtotal"]
      sprint_total_message = u"""
      Total points: %s
      S: %s
      M: %s
      L: %s
      """ % (sprint_total_points, point_dict["S"]["count"],
             point_dict["M"]["count"], point_dict["L"]["count"])
    template_mapping = {"stories": "\n".join(stories), "sprint_total_message": sprint_total_message}
    result = src.safe_substitute(template_mapping)
    file.write(result)

  """
  Metrics:

  Get the metrics for all of the stories and also need to
  know how long each story took (do we care about tasks, bugs?)
  """


main()
