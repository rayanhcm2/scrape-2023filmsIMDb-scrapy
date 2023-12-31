from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from filmsImdb.items import FilmsimdbItem

class CrawlfilmsSpider(CrawlSpider):
    name = "crawlFilms"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/list/ls082239486/"]

    # Définition des règles de navigation et de parsing des pages
    rules = (
        # Suivre les liens des films et appeler la méthode parse_item pour extraire les données
        Rule(LinkExtractor(restrict_xpaths=r"//div[@class='lister-item-image ribbonize']/a"), callback="parse_item", follow=True),
        # Suivre le lien de pagination
        Rule(LinkExtractor(restrict_xpaths=r"//div[@class='list-pagination']//a[2]"))
    )
    
    # Méthode pour extraire les données d'un film à partir de sa page
    def parse_item(self, response):
        film = FilmsimdbItem()
        
        # Extraire les données à partir des expressions XPath correspondantes
        film['title'] = response.xpath("//span[@class='sc-afe43def-1 fDTGTb']/text()").get()
        film['Image'] = response.urljoin(response.xpath("//a[@class='ipc-lockup-overlay ipc-focusable']/@href").get())
        film['Catégorie'] = response.xpath("//a[@class='ipc-chip ipc-chip--on-baseAlt']/span/text()").getall()
        film['description'] = response.xpath("//span[@class='sc-466bb6c-2 eVLpWt']/text()").get()
        film['rate_IMDb'] = response.xpath('//div[@class="sc-bde20123-2 gYgHoj"]/span[1]/text()').get()
        film['Realisation'] = response.xpath("//ul[@class='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt']/li[1]/a/text()").get()
        film['Scénario'] = response.xpath("//ul[@class='ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt']/li[2]/a/text()").get()            

        # Renvoyer les données du film pour le traitement ultérieur
        yield film
