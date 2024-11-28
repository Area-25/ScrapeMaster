import argparse
import json
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import random
import time
from typing import List, Dict
from pathlib import Path
from googlesearch import search
from concurrent.futures import ThreadPoolExecutor
import yaml
import re

class ScrapeMaster:
    def __init__(self, num_websites: int, topics: List[str]):
        self.num_websites = num_websites
        self.topics = [t.strip() for t in topics.split(',')]
        self.urls_per_topic = num_websites // len(self.topics)
        
        # Initialize storage files
        self.master_file = Path('websites_master.json')
        self.completed_file = Path('websites_completed.json')
        self.errors_file = Path('websites_errors.json')
        
        # Create final_dataset directory if it doesn't exist
        self.output_dir = Path('final_dataset')
        self.output_dir.mkdir(exist_ok=True)
        self.output_file = self.output_dir / 'dataset.jsonl'
        
        # Load or create tracking files
        self.master_urls = self._load_or_create_json(self.master_file)
        self.completed_urls = self._load_or_create_json(self.completed_file)
        self.error_urls = self._load_or_create_json(self.errors_file)

    @staticmethod
    def _load_or_create_json(file_path: Path) -> Dict:
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        return {}

    def _search_google_sync(self, topic: str) -> List[str]:
        try:
            urls = []
            for url in search(topic, num_results=self.urls_per_topic, lang="en"):
                urls.append(url)
                time.sleep(2.0)
            return urls
        except Exception as e:
            print(f"Error during search for {topic}: {e}")
            return []

    async def search_google(self, topic: str, session: aiohttp.ClientSession) -> List[str]:
        # Run the synchronous search in a thread pool
        with ThreadPoolExecutor() as executor:
            urls = await asyncio.get_event_loop().run_in_executor(
                executor,
                self._search_google_sync,
                topic
            )
            return urls

    async def scrape_website(self, url: str, session: aiohttp.ClientSession) -> Dict:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        
        try:
            async with session.get(url, headers=headers, timeout=30) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Extract text content
                    text = ' '.join([p.get_text() for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])
                    
                    return {
                        'url': url,
                        'title': soup.title.string if soup.title else '',
                        'content': text
                    }
                else:
                    raise Exception(f"HTTP {response.status}")
        except Exception as e:
            self.error_urls[url] = str(e)
            return None

    async def process_urls(self):
        async with aiohttp.ClientSession() as session:
            # First, collect URLs if master list is empty
            if not self.master_urls:
                print("Collecting URLs from Google...")
                for topic in self.topics:
                    urls = await self.search_google(topic, session)
                    for url in urls:
                        self.master_urls[url] = topic
                    
                    # Save master URLs
                    with open(self.master_file, 'w') as f:
                        json.dump(self.master_urls, f, indent=2)
                    
                    # Random delay to avoid rate limiting
                    await asyncio.sleep(random.uniform(1, 3))

            # Process URLs that haven't been completed or errored
            pending_urls = [url for url in self.master_urls.keys() 
                          if url not in self.completed_urls and url not in self.error_urls]

            print(f"Processing {len(pending_urls)} websites...")
            for url in pending_urls:
                result = await self.scrape_website(url, session)
                if result:
                    self.completed_urls[url] = result
                    # Append to JSONL file
                    with open(self.output_file, 'a') as f:
                        f.write(json.dumps(result) + '\n')
                
                # Save progress
                with open(self.completed_file, 'w') as f:
                    json.dump(self.completed_urls, f, indent=2)
                with open(self.errors_file, 'w') as f:
                    json.dump(self.error_urls, f, indent=2)
                
                await asyncio.sleep(random.uniform(0.5, 1.5))

    @staticmethod
    def load_topics_from_file(file_path: str) -> List[str]:
        """Load topics from various file formats."""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Handle different file formats
        if path.suffix == '.json':
            with open(path, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and 'topics' in data:
                    return data['topics']
                raise ValueError("JSON file must contain a list or a dict with 'topics' key")
                
        elif path.suffix in ['.yaml', '.yml']:
            with open(path, 'r') as f:
                data = yaml.safe_load(f)
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and 'topics' in data:
                    return data['topics']
                raise ValueError("YAML file must contain a list or a dict with 'topics' key")
                
        elif path.suffix == '.txt':
            with open(path, 'r') as f:
                # Remove empty lines and whitespace
                return [line.strip() for line in f.readlines() if line.strip()]
                
        elif path.suffix == '.md':
            with open(path, 'r') as f:
                content = f.read()
                # Look for topics in markdown lists (both - and *)
                topics = re.findall(r'[-*]\s*(.+)', content)
                if topics:
                    return [topic.strip() for topic in topics]
                # If no lists found, try line by line
                return [line.strip() for line in content.split('\n') if line.strip()]
        
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")

def main():
    parser = argparse.ArgumentParser(description='ScrapeMaster - Website Scraping Tool')
    parser.add_argument('--websites', type=int, required=True, help='Number of websites to scrape')
    parser.add_argument('--topics', type=str, required=True, 
                      help='Either a comma-separated list of topics or a path to a file (.json, .yaml, .txt, .md)')
    
    args = parser.parse_args()
    
    # Check if topics is a file path
    if Path(args.topics).exists():
        topics = ScrapeMaster.load_topics_from_file(args.topics)
        topics_str = ','.join(topics)
    else:
        topics_str = args.topics
    
    scraper = ScrapeMaster(args.websites, topics_str)
    asyncio.run(scraper.process_urls())

if __name__ == "__main__":
    main() 