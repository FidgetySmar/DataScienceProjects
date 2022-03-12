"""
Scraping Top 30 Repositories of GitHub's Topic:

>> Web scraping is acquiring poorly structured data from websites and converting it into a structured format.
    Here, I am using .csv format for structured data.

>> GitHub is a distributed VCS (Version Control System). It is a code hosting platform for "version control" and 
    "collaboration".
TODO
1. We are going to scrape https://github.com/topics.
2. We are going to using Python and Python's requests, BeautifulSoup, Pandas library.
"""
"""
Steps to be followed in order to complete this project:
>> Outline
 1. We are going to scrape https://github.com/topics
 2. We'll get a list of topics. For each topic we'll get topic title, topic page URL and topic description.
 3. From each topic, we'll get the top 30 repositories.
 4. For each repository, we'll get the repo name, username, stars and rpo URL.
 5. For each topic we'll create a CSV file in the following format:
       "Repo Name, Username, Stars, Repo URL"
"""

"""
>> Getting the list of topics from GitHub:
TODO It is divided into following parts: 
        1. downloading the webpage using requests library.
        2. parsing the information using BeautifulSoup.
        3. extracting the info from parsed documents.
        4. saving the extracted info into a Pandas' data frame.
        5. atlast, creating a .csv file using data frame
"""
from operator import ge
from re import A, S
from tempfile import gettempdir
from webbrowser import get
import requests
import os
from bs4 import BeautifulSoup
import pandas as pd

def getTopics():
    """ download the topics page of GitHub and will return parsed .html document """
    topics_url = 'https://github.com/topics'
    response = requests.get(topics_url) # will create a response object
    # Check for successful response
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(topics_url))
    # >> Using BeautifulSoup to parse the html file
    doc = BeautifulSoup(response.text, 'html.parser')
    return doc

# doc = getTopics() # to store the parsed .html document from getTopics()

# Creating some helper function to get information from the page. 
def topicTitles(doc):
    """ collects the topic titles into a list and returns it. """
    selection_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
    topic_title_tags = doc.find_all('p', {'class': selection_class})

    topic_titles = []
    for tag in topic_title_tags:
        topic_titles.append(tag.text)
    
    return topic_titles

# titles = topicTitles(doc)
# print(len(titles))

def topicDescs(doc):
    """ collects the topic description into a list and returns it. """
    class_selector = 'f5 color-fg-muted mb-0 mt-1'
    topic_desc_tags = doc.find_all('p', {'class': class_selector})

    topic_descs = []
    for tag in topic_desc_tags:
        topic_descs.append(tag.text.strip())
    
    return topic_descs

# descs = topicDescs(doc)
# print(len(descs))

def getTopicURL(doc):
    """ collects the topic URL into a list and returns it. """
    topic_link_tags = doc.find_all('a', {'class': 'no-underline flex-grow-0'})

    topic_urls = []
    base_url = 'https://github.com'
    for tag in topic_link_tags:
        topic_urls.append(base_url + tag['href'])
    
    return topic_urls

# url = getTopicURL(doc)
# print(len(url))

# Lets put this altogether in one function. 
def getTopicsDF():
    """ storing topics' title, description and URL into a dictionary and return a Pandas data frame """
    doc = getTopics() # to store the parsed .html document from getTopics()
    topics_dict = {
        'Title': topicTitles(doc),
        'Description': topicDescs(doc),
        'URL': getTopicURL(doc)
    }

    return pd.DataFrame(topics_dict)

# topics_df = getTopicsDF()
# print(topics_df)

"""
>> Getting top 30 repositories from each topic:
TODO It is divided into following parts: 
        1. download topic page using request. 
        2. parsing the information using BeautifulSoup. 
        3. getting the repo info i.e. repo name, username, stars and rpo URL.
        4. storing all repos info in Pandas dataframe. 
        5. saving Pandas dataframe into .csv file.
"""

def getTopicPage(topic_url):
    """ Download the topoic page and return the parsed document. """
    response = requests.get(topic_url) # response object is created
    # Check for successful response
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(topic_url))
    # html parsing using Beautiful Soup
    topic_doc = BeautifulSoup(response.text, 'html.parser')
    return topic_doc

# print(getTopicPage('https://github.com/topics'))

def getStarCount(stars_str):
    """returns number of stars of a repository"""
    stars_str = stars_str.strip()
    if stars_str[-1] == 'k':
        return int(float(stars_str[:-1]) * 1000)
    return int(stars_str)

def getRepoInfo(h3_tag, star_tag):
    """returns all the required info about a repository"""
    base_url = 'https://github.com'
    a_tags = h3_tag.find_all('a')
    username = a_tags[0].text.strip()
    repo_name = a_tags[1].text.strip()
    repo_url = base_url + a_tags[1]['href']
    stars = getStarCount(star_tag.text)
    return username, repo_name, stars, repo_url

# collecting info about all the repository of all topic pages into a dictionary.
def getTopicRepos(topic_doc):
    """ Collecting info about all the repository of all topic pages into a dictionary and returning Pandas dataframe."""
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

def scrapeTopic(topic_url, topic_path):
    """ Wrapper to save info of a topic's top 30 repo info in .csv file at any location as per your wish. """
    # check for existing file to avoid duplication.
    if os.path.exists(topic_path):
        print(f"File {topic_path} already exists. Skipping...")
        return
    topic_df = getTopicRepos(getTopicPage(topic_url))
    topic_df.to_csv(os.path.join(topic_path), index=None)

def scrapeTopicRepos():
    # file path for my pc is "D:\Programming\DataScienceProjects\webScrapping\githubTopics\data"
    print('Scraping list of topics')
    topic_df = getTopicsDF()

    os.makedirs('D:\Programming\DataScienceProjects\webScrapping\githubTopics\data', exist_ok=True)

    for index, row in topic_df.iterrows():
        print('Scraping top repositories for "{}"'.format(row['Title']))
        scrapeTopic(row['URL'], 
            f"D:\Programming\DataScienceProjects\webScrapping\githubTopics\data\{row['Title']}.csv")

scrapeTopicRepos()

"""
Future work: 
    1. try to get top 30 repos for all the featured topics on GitHub.
"""