import scrapy
from scrapy_splash import SplashRequest


class ReviewSpider(scrapy.Spider):
    name = 'review'
    allowed_domains = ['amazon.com']
    base_urls = [
        # "https://www.amazon.com/Acer-Display-Graphics-Keyboard-A515-43-R19L/product-reviews/B07RF1XD36/"
        # "https://www.amazon.com/Fitbit-Inspire-Fitness-Tracker-Included/product-reviews/B08DFGPTSK/"
        # "https://www.amazon.com/Samsonite-Omni-Hardside-Spinner-Black/product-reviews/B013WFNVGY/"
        "https://www.amazon.com/1984-Signet-Classics-George-Orwell/product-reviews/0451524934/"]

    start_urls = []

    for url in base_urls:
        first_page_url = f'{url}ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1'
        start_urls.append(first_page_url)

        for page in range(2, 51):
            next_page_url = f'{url}ref=cm_cr_getr_d_paging_btm_next_{page}?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber={page}'
            start_urls.append(next_page_url)

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        data = response.css('#cm_cr-review_list')

        star_ratings = data.css('.review-rating')

        comments = data.css('.review-text')

        for count in range(1, len(star_ratings)):
            yield {'stars': "".join(star_ratings[count].xpath('.//text()').extract()),
                   'comment': "".join(comments[count].xpath('.//text()').extract())}
