from project.category import Category
from project.document import Document
from project.topic import Topic


class Storage:
    def __init__(self):
        self.categories:list[Category] = []
        self.topics:list[Topic] = []
        self.documents:list[Document] = []

    def add_category(self, category:Category) -> None:
        if category not in self.categories:
            self.categories.append(category)

    def add_topic(self, topic:Topic) -> None:
        if topic not in self.topics:
            self.topics.append(topic)

    def add_document(self, document:Document) -> None:
        if document not in self.documents:
            self.documents.append(document)

    def edit_category(self, category_id:int, new_name: str) -> None:
        for category in self.categories:
            if category.id == category_id:
                category.name = new_name

    def edit_topic(self, topic_id:int, new_file_name: str) -> None:
        for topic in self.topics:
            if topic.id == topic_id:
                topic.name = new_file_name

    def edit_document(self, document_id:int, new_file_name: str) -> None:
        for document in self.documents:
            if document.id == document_id:
                document.name = new_file_name

    def delete_category(self, category_id:int) -> None:
        for category in self.categories:
            if category.id == category_id:
                self.categories.remove(category)

    def delete_topic(self, topic_id:int) -> None:
        for topic in self.topics:
            if topic.id == topic_id:
                self.topics.remove(topic)

    def delete_document(self, document_id:int) -> None:
        for document in self.documents:
            if document.id == document_id:
                self.documents.remove(document)

    def get_document(self, document_id:int) -> Document:
        return next((d for d in self.documents if d.id == document_id), None)

    def __repr__(self):
        return "\n".join([str(d) for d in self.documents])