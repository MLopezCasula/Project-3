class Book:
    def __init__(self, title, authors, category, publisher, publish_month, publish_year, price):
        self.title = title
        self.authors = authors
        self.category = category
        self.publisher = publisher
        self.publish_month = publish_month
        self.publish_year = publish_year


    def getTitle(self):
        return self.title
    
    def getAuthors(self):
        return self.authors
    
    def getCategory(self):
        return self.category
    
    def getPublisher(self):
        return self.publisher
    
    def getPublishMonth(self):
        return self.publish_month
    
    def getPublishYear(self):
        return self.publish_year
