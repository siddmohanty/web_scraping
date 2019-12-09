import requests
from bs4 import BeautifulSoup


'''
scrape http://books.toscrape.com/ and extract
    • book title
    • price
    • availability
    • image
    • category
    • rating

'''

if __name__ == "__main__":
	base_url = r"http://books.toscrape.com/"
	response = requests.get(base_url)
	html_page = response.content
	soup = BeautifulSoup(html_page, features="html.parser")

	side_categories = soup.find("div", attrs={"class" : "side_categories"}) \
							.find("ul", attrs={"class" : "nav nav-list"}) \
							.find("li").find("ul")

	category_names_urls = []
	for li in side_categories.find_all("li"):
		category_name = li.find("a").text.strip()
		category_href = li.find("a")["href"].strip()
		category_url = base_url + category_href
		category_names_urls.append([category_name, category_url])

	# print(category_names_urls)

	for category_name, category_url in category_names_urls:
		response = requests.get(category_url)
		html_page = response.content
		soup = BeautifulSoup(html_page, features="html.parser")

		for item in soup.find_all("article", attrs={"class" : "product_pod"}):
			image_href = item.find("div", attrs={"class" : "image_container"}) \
						.find("a").find("img")["src"].replace("../", "")
			image_url = base_url + image_href

			rating = item.find("p")["class"][-1]
			book_title = item.find("h3").find("a")["title"]
			price_div = item.find("div", attrs={"class" : "product_price"})
			price = price_div.find("p", attrs={"class" : "price_color"}).text
			availability = price_div.find("p", attrs={"class" : "instock availability"}).text.strip()

			print(category_name)
			print(image_url)
			print(rating)
			print(book_title)
			print(price)
			print(availability)
			print("\n\n\n")



