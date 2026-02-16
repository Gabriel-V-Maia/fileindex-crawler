import requests
import re

from bs4 import BeautifulSoup 
from dataclasses import dataclass 
from typing import Optional


@dataclass
class requester:
    def fetch(self, target_url: str):
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
                }
        r = requests.get(target_url, headers=headers)
        

        if r.status_code != 200:
            print(f"something went wrong when fetching html content, {r.status_code}")
            exit()


        return r

@dataclass
class Season:
    link: str 

@dataclass 
class Episode:
    title: str
    link: str

@dataclass
class crawler:
    html_content: str
    requester_instance: requester
    parser: BeautifulSoup


    def collect_links(self):
        parser = self.parser
        links = parser.find_all('a')

        return links

    def find_seasons(self, target_url):
        parser = self.parser
        found_seasons = list()

        collected_links = self.collect_links()
        
        for tag in collected_links:
            href = tag.get('href')

            if not href:
                continue

            link_text = tag["href"]

            if "Season" in link_text or "season" in link_text:
                season = Season(target_url + link_text)
                found_seasons.append(season)

        return found_seasons


    def get_episodes(self, seasons: list):
        collected_episodes = list()
    
        for season in seasons:
            response = self.requester_instance.fetch(season.link)
        
            season_parser = BeautifulSoup(response.text, "html.parser")
            links = season_parser.find_all('a')
        
            for link in links:
                episode_link = link.get("href")      
                episode_title = link.get("title")    
            
                if not episode_link or not episode_title:
                    continue

                if not ".mkv" in episode_link:
                    continue

                episode = Episode(title=episode_title, link=episode_link)
                collected_episodes.append(episode)

        return collected_episodes

    def start_downloading(self, seasons: list, episodes: list):

        pass
        
        
    def crawl(self, target_url: str):
        print("started crawling...")
        seasons = self.find_seasons(target_url)
        episodes = self.get_episodes(seasons)

        print("finished")
        
        

def main():
    print("Enter URL to crawl: ")
    target_url = str(input("> "))    

    req = requester()
    response = req.fetch(target_url)
   
    parser = BeautifulSoup(response.text, "html.parser")
    crawl = crawler(html_content=response.text,requester_instance=req, parser=parser)

    crawl.crawl(target_url)

if __name__ == "__main__":
    main()
