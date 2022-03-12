#>> Outline
# 1. We are going to scrape https://github.com/topics
# 2. We'll get a list of topics. For each topic we'll get topic title, topic page URL and topic description.
# 3. From each topic, we'll get the top 30 repositories.
# 4. For each repository, we'll get the repo name, username, stars and rpo URL.
# 5. For each topic we'll create a CSV file in the following format:
#       "Repo Name, Username, Stars, Repo URL"

from re import A, S
import requests
import os
from bs4 import BeautifulSoup
import pandas as pd

# >>>>>>>>>>Scraping https://github.com/topics <<<<<<<<<<
# >> Scraping has two parts:
#   1. Getting the information of the webpage.
#   2. Parsing the webpage.
topics_url = 'https://github.com/topics'
response = requests.get(topics_url) # requests.get(topics_url) will create a response object
# print(response.status_code)   # status code indicates whether the response was successful
                                # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
page_contents = response.text
with open(os.path.join('D:\Programming\DataScienceProjects\webScrapping\githubTopics','webpage.html'), 'w', encoding='utf-8') as f:
    f.write(page_contents)

# >> Using BeautifulSoup to parse the html file
doc = BeautifulSoup(page_contents, 'html.parser')
# collecting all the title from first page of topics
selection_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
topic_title_tags = doc.find_all('p', {'class': selection_class})
# collecting description of all the title from first page of topics
class_selector = 'f5 color-fg-muted mb-0 mt-1'
topic_desc_tags = doc.find_all('p', {'class': class_selector})
# collecting link of all the title from first page of topics
topic_link_tags = doc.find_all('a', {'class': 'no-underline flex-grow-0'})
# print('https://github.com/' + topic_link_tags[0]['href'])
# collecting all the title from topic_title_tags in a list
topic_titles = []
for tag in topic_title_tags:
    topic_titles.append(tag.text)
# collecting description of all the title from topic_title_tags in a list
topic_descs = []
for tag in topic_desc_tags:
    topic_descs.append(tag.text.strip())
# collecting URL of all the title from topic_title_tags in a list
topic_urls = []
base_url = 'https://github.com'
for tag in topic_link_tags:
    topic_urls.append(base_url + tag['href'])

# >> Using pandas to create a pandas dataframe <<
topics_dict = {
    'title': topic_titles,
    'description': topic_descs,
    'url': topic_urls
}
topics_df = pd.DataFrame(topics_dict)

# >>create CSV file(s) with the extracted information<<
topics_df.to_csv(os.path.join('D:\Programming\DataScienceProjects\webScrapping\githubTopics', 'topics.csv')
                , index=None)

# >> Getting information out of a topic page <<
topic_page_url = topic_urls[0]
# print(topic_page_url)
response = requests.get(topic_page_url)
# print(response.status_code)
# print(len(response.text))
topic_doc = BeautifulSoup(response.text, 'html.parser')
# Collecting the repo info from topic_page_url
h3_selection_class = 'f3 color-fg-muted text-normal lh-condensed'
repo_tags = topic_doc.find_all('h3', {'class': h3_selection_class})
# print(len(repo_tags))
a_tags = repo_tags[0].find_all('a')
# print(a_tags)
# print(a_tags[0].text.strip())
# print(a_tags[1].text.strip())
# print(base_url + a_tags[1]['href'])
# Collecting number of stars for each repo
star_tags = topic_doc.find_all('span', {'class': 'Counter js-social-count'})
# print(star_tags[0].text.strip())

# >> defining functions <<
def parseStarCount(stars_str):
    """returns number of stars of a repository"""
    stars_str = stars_str.strip()
    if stars_str[-1] == 'k':
        return int(float(stars_str[:-1]) * 1000)
    return int(stars_str)

# print(parseStarCount(star_tags[0].text))

# def getRepoInfo(h3_tag, star_tag):
#     """returns all the required info about a repository"""
#     a_tags = h3_tag.find_all('a')
#     username = a_tags[0].text.strip()
#     repo_name = a_tags[1].text.strip()
#     repo_url = base_url + a_tags[1]['href']
#     stars = parseStarCount(star_tag.text)
#     return username, repo_name, stars, repo_url

# print(getRepoInfo(repo_tags[0], star_tags[0]))
# print(range(len(repo_tags)))

# collecting info about all the repository of a topic page into a dictionary.
# topic_repos_dict = {
#     'Username':[],
#     'Repo_name':[],
#     'Stars':[],
#     'Repo_URL':[]
# }
# for i in range(len(repo_tags)):
#     repo_info = getRepoInfo(repo_tags[i], star_tags[i])
#     topic_repos_dict['Username'].append(repo_info[0])
#     topic_repos_dict['Repo_name'].append(repo_info[1])
#     topic_repos_dict['Stars'].append(repo_info[2])
#     topic_repos_dict['Repo_URL'].append(repo_info[3])
# print(topic_repos_dict)

# converting topic's repo infos into a data frame using pandas
# topic_repos_df = pd.DataFrame(topic_repos_dict)
# print(topic_repos_df)

def getTopicPage(topic_url):

    # Download the page
    response = requests.get(topic_url) # response object is created
    # Check for successful response
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(topic_url))
    # html parsing using Beautiful Soup
    topic_doc = BeautifulSoup(response.text, 'html.parser')
    return topic_doc

def getRepoInfo(h3_tag, star_tag):
    """returns all the required info about a repository"""
    a_tags = h3_tag.find_all('a')
    username = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    repo_url = base_url + a_tags[1]['href']
    stars = parseStarCount(star_tag.text)
    return username, repo_name, stars, repo_url

# collecting info about all the repository of all topic pages into a dictionary.
def getTopicRepos(topic_doc):
    
    # Collecting the repo info from topic_page_url
    h3_selection_class = 'f3 color-fg-muted text-normal lh-condensed'
    repo_tags = topic_doc.find_all('h3', {'class': h3_selection_class})

    # Collecting number of stars for each repo
    star_tags = topic_doc.find_all('span', {'class': 'Counter js-social-count'})

    # collecting info about all the repository of a topic page into a dictionary.
    topic_repos_dict = {
        'Username':[],
        'Repo_name':[],
        'Stars':[],
        'Repo_URL':[]
    }
    for i in range(len(repo_tags)):
        repo_info = getRepoInfo(repo_tags[i], star_tags[i])
        topic_repos_dict['Username'].append(repo_info[0])
        topic_repos_dict['Repo_name'].append(repo_info[1])
        topic_repos_dict['Stars'].append(repo_info[2])
        topic_repos_dict['Repo_URL'].append(repo_info[3])
    # returning topic's repo infos into a data frame using pandas
    return pd.DataFrame(topic_repos_dict)

# def scrapeTopic(topic_url, topic_name):
#     file_name = topic_name + '.csv'
#     if os.path.exists('D:\Programming\DataScienceProjects\webScrapping\githubTopics\\' + file_name):
#         print(f"File {file_name} already exists. Skipping...")
#         return
#     topic_df = getTopicRepos(getTopicPage(topic_url))
#     topic_df.to_csv(os.path.join('D:\Programming\DataScienceProjects\webScrapping\githubTopics', file_name),
#                     index=None)
def scrapeTopic(topic_url, topic_path):
    
    if os.path.exists(topic_path):
        print(f"File {topic_path} already exists. Skipping...")
        return
    topic_df = getTopicRepos(getTopicPage(topic_url))
    topic_df.to_csv(os.path.join(topic_path), index=None)

# print(topic_urls)

# topic4_doc = getTopicPage(topic_urls[4])
# topic4_repos = getTopicRepos(topic4_doc)
# OR
# topic4_repos = getTopicRepos(getTopicPage(topic_urls[4]))
# print(topic4_repos)
# print(topic_urls[6])
# getTopicRepos(getTopicPage(topic_urls[6])).to_csv(
#     os.path.join('D:\Programming\DataScienceProjects\webScrapping\githubTopics', 'ansible.csv'), index=None)

"""
Write a single function to:
1. Get the list of topics from the topics page.
2. Get the list of top repos from the individual topic pages.
3. For each topic, create a CSV of the top repos for the topic.
"""

def topicTitles(doc):
    selection_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
    topic_title_tags = doc.find_all('p', {'class': selection_class})

    topic_titles = []
    for tag in topic_title_tags:
        topic_titles.append(tag.text)
    
    return topic_titles

def topicDescs(doc):
    class_selector = 'f5 color-fg-muted mb-0 mt-1'
    topic_desc_tags = doc.find_all('p', {'class': class_selector})

    topic_descs = []
    for tag in topic_desc_tags:
        topic_descs.append(tag.text.strip())
    
    return topic_descs

def getTopicURL(doc):
    topic_link_tags = doc.find_all('a', {'class': 'no-underline flex-grow-0'})

    topic_urls = []
    base_url = 'https://github.com'
    for tag in topic_link_tags:
        topic_urls.append(base_url + tag['href'])
    
    return topic_urls

def getTopics():
    topics_url = 'https://github.com/topics'
    response = requests.get(topics_url)
    if response.status_code != 200:
        raise Exception('Failed to load page'.format(topics_url))
    
    topics_dict = {
        'Title': topicTitles(doc),
        'Description': topicDescs(doc),
        'URL': getTopicURL(doc)
    }

    return pd.DataFrame(topics_dict)

# print(getTopic())
# def scrapeTopicRepos():
#     print('Scraping list of topics')
#     topic_df = getTopics()
#     for index, row in topic_df.iterrows():
#         print('Scraping top repositories for "{}"'.format(row['Title']))
#         scrapeTopic(row['URL'], row['Title'])
def scrapeTopicRepos():
    print('Scraping list of topics')
    topic_df = getTopics()

    os.makedirs('D:\Programming\DataScienceProjects\webScrapping\githubTopics\data', exist_ok=True)

    for index, row in topic_df.iterrows():
        print('Scraping top repositories for "{}"'.format(row['Title']))
        scrapeTopic(row['URL'], 
            f"D:\Programming\DataScienceProjects\webScrapping\githubTopics\data\{row['Title']}.csv")

scrapeTopicRepos()

