from mongoengine import connect, Document, StringField, ReferenceField, ListField
import json


connect(db="quotesdb", host="your_mongo_atlas_uri_here", alias="default")


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

    def __str__(self):
        return self.fullname


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, reverse_delete_rule=2)
    quote = StringField(required=True)


def load_authors(filename):
    with open(filename, "r", encoding="utf-8") as file:
        authors_data = json.load(file)
        for author in authors_data:
            if not Author.objects(fullname=author["fullname"]).first():
                Author(**author).save()


def load_quotes(filename):
    with open(filename, "r", encoding="utf-8") as file:
        quotes_data = json.load(file)
        for quote in quotes_data:
            author = Author.objects(fullname=quote["author"]).first()
            if author:
                Quote(tags=quote["tags"], author=author, quote=quote["quote"]).save()


def search_quotes():
    while True:
        command = input("Введіть команду (name, tag, tags, exit): ").strip()
        if command == "exit":
            print("Завершення роботи.")
            break

        try:
            cmd_type, value = command.split(":", 1)
            value = value.strip()
            
            if cmd_type == "name":
                author = Author.objects(fullname=value).first()
                if author:
                    quotes = Quote.objects(author=author)
                    for q in quotes:
                        print(q.quote)
                else:
                    print("Автор не знайдений.")

            elif cmd_type == "tag":
                quotes = Quote.objects(tags=value)
                for q in quotes:
                    print(q.quote)

            elif cmd_type == "tags":
                tags = value.split(",")
                quotes = Quote.objects(tags__in=tags)
                for q in quotes:
                    print(q.quote)

            else:
                print("Невідома команда.")
        except Exception as e:
            print(f"Помилка: {e}")


if __name__ == "__main__":

    load_authors("authors.json")
    load_quotes("qoutes.json")


    search_quotes()