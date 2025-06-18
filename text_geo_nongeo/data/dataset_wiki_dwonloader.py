import wikipediaapi
import pandas as pd
from tqdm import tqdm
import os
import time
from requests.exceptions import ReadTimeout, ConnectionError

# Configuration
USER_AGENT = "Kiimia_NLP/1.0 (https://github.com/kimiya-git/Kiimia_NLP.git; ghassemzadehkimia@gmail.com)"
MAX_RETRIES = 3
RETRY_DELAY = 10
REQUEST_DELAY = 1
TIMEOUT = 120
MAX_ARTICLES_PER_CATEGORY = 30
MAX_TEXT_LENGTH = 5000


class WikipediaDataCollector:
    def __init__(self):
        self.wiki = wikipediaapi.Wikipedia(
            language='en',
            user_agent=USER_AGENT,
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            timeout=TIMEOUT
        )
        self.data_dir = ''

    def safe_fetch_page(self, title, retry_count=0):

        try:
            page = self.wiki.page(title)
            return page if page.exists() else None
        except (ReadTimeout, ConnectionError) as e:
            if retry_count < MAX_RETRIES:
                sleep_time = RETRY_DELAY * (retry_count + 1)
                print(f"Timeout fetching {title}, retry {retry_count + 1} in {sleep_time}s...")
                time.sleep(sleep_time)
                return self.safe_fetch_page(title, retry_count + 1)
            print(f"Failed after {MAX_RETRIES} retries for {title}: {str(e)}")
            return None
        except Exception as e:
            print(f"Error fetching {title}: {str(e)}")
            return None

    def fetch_category_articles(self, category):

        articles = []
        cat_page = self.safe_fetch_page(f"Category:{category}")

        if not cat_page:
            return articles

        category_members = list(cat_page.categorymembers.values())[:MAX_ARTICLES_PER_CATEGORY]

        for article in tqdm(category_members, desc=f"  {category}", leave=False):
            if article.ns == 0:  # Only main namespace articles
                page = self.safe_fetch_page(article.title)
                if page and page.text:
                    articles.append({
                        'title': article.title,
                        'text': page.text[:MAX_TEXT_LENGTH],
                        'category': category,
                        'url': page.fullurl
                    })
                time.sleep(REQUEST_DELAY)
        return articles

    def create_labeled_dataset(self):

        geo_categories = [
            'Geography', 'Countries', 'Cities',
            'Mountains', 'Rivers', 'Lakes',
            'Islands', 'Deserts', 'Oceans',
            'Continents'
        ]

        non_geo_categories = [
            'Mathematics', 'Literature', 'data science',
            'Music', 'Philosophy', 'socialogy',
            'Chemistry', 'Painting', 'Physics',
            'Economics', 'Netflix','film'
        ]

        # Collect data
        all_articles = []

        print("Fetching geographic articles...")
        for category in tqdm(geo_categories, desc="Geo Categories"):
            all_articles.extend(self.fetch_category_articles(category))
            time.sleep(REQUEST_DELAY * 2)

        geo_df = pd.DataFrame(all_articles)
        geo_df['label'] = 1

        all_articles = []
        print("\nFetching non-geographic articles...")
        for category in tqdm(non_geo_categories, desc="Non-Geo Categories"):
            all_articles.extend(self.fetch_category_articles(category))
            time.sleep(REQUEST_DELAY * 2)

        non_geo_df = pd.DataFrame(all_articles)
        non_geo_df['label'] = 0


        combined_df = pd.concat([geo_df, non_geo_df]).sample(frac=1).reset_index(drop=True)


        os.makedirs(self.data_dir, exist_ok=True)
        output_path = os.path.join(self.data_dir, 'wiki_dataset.csv')
        combined_df.to_csv(output_path, index=False)


        print("\nData Collection Complete!")
        print(f"Saved {len(combined_df)} articles to {output_path}")
        print(f"Geographic: {len(geo_df)} articles")
        print(f"Non-geographic: {len(non_geo_df)} articles")

        return combined_df


if __name__ == "__main__":
    print("Starting Wikipedia Data Collection...")
    print(f"User Agent: {USER_AGENT}")

    collector = WikipediaDataCollector()
    dataset = collector.create_labeled_dataset()

    if not dataset.empty:
        print("\nSample of collected data:")
        print(dataset[['title', 'category', 'label']].head())
    else:
        print("\nWarning: No data was collected - check your internet connection")