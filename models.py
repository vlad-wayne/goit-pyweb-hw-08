from mongoengine import Document, StringField, BooleanField, connect


connect(host="mongodb+srv://<username>:<password>@cluster.mongodb.net/emails?retryWrites=true&w=majority")

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    is_sent = BooleanField(default=False)
