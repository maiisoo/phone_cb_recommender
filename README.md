# Phone Content-based Recommendation

This project applies content-based approach to make recommendations for buying smart phone. The raw product dataset is crawled and extracted from the e-commerce site [cellphoneS](https:cellphones.com) using BeautifulSoup and Selenium. Some missing data handling and text preprocessing techniques applied to guarantee data quality. Finally, features are vectorized and computed similarity scores to make recommendation.

## Installation
1. Download chromedriver with compatible Chrome version
2. Clone project
```bash
git clone https://github.com/maiisoo/phone_content_based_recommender.git
```

## Code
**Crawler.py:** parse the Homepage to get product URLs  
**PhoneCrawler.py:** parse each product to get details  
**phone_rcmd.ipynb:** fill missings, process raw data and implement the recommender
