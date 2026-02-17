import requests
import os 

from bs4 import BeautifulSoup 
from dataclasses import dataclass 
from urllib.parse import urljoin


@dataclass
class requester:
    def fetch(self, target_url: str, stream: bool = False):
        headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
                }
        r = requests.get(target_url, headers=headers, stream=stream)
        

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
                if ".mkv" not in episode_link:
                    continue

                full_link = urljoin(season.link, episode_link)  
                episode = Episode(title=episode_title, link=full_link)
                collected_episodes.append(episode)

    
        return collected_episodes



    def start_downloading(self, episodes: list):
        os.makedirs("downloaded_series", exist_ok=True)

        for episode in episodes:
            print(f"downloading: {episode.title}")
            r = self.requester_instance.fetch(episode.link, stream=True)
            
            filename = os.path.join("downloaded_series", episode.title)
            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=1048576):
                    f.write(chunk)


            print("finished downloading")
    

    def crawl(self, target_url: str):
        print("started crawling...")
        seasons = self.find_seasons(target_url)
        episodes = self.get_episodes(seasons)

        self.start_downloading(episodes)



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
