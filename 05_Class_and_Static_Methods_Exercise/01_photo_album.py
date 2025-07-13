from math import ceil


class PhotoAlbum:
    PAGE_SIZE = 4
    def __init__(self, pages: int):
        self.pages = pages
        self.photos: list[list[str]] = [[] for _ in range(self.pages)]

    @classmethod
    def from_photos_count(cls, photo_count: int):
        return cls(ceil(photo_count / cls.PAGE_SIZE))

    def add_photo(self, label) -> str:
        for i, page in enumerate(self.photos):
            if len(page) < self.PAGE_SIZE:
                page.append(label)
                return f"{label} photo added successfully on "\
                       f"page {i + 1} of {self.PAGE_SIZE} "\
                       f"slot {len(page)}"
        return "No more free slots"

    def display(self) -> str:
        separator = "-" * 11 + '\n'
        result = separator
        for photo in self.photos:
            result += ' '.join(["[]" for _ in photo]) + "\n"
            result += separator

        return result.strip()



# Test Code
album = PhotoAlbum(2)

print(album.add_photo("baby"))
print(album.add_photo("first grade"))
print(album.add_photo("eight grade"))
print(album.add_photo("party with friends"))
print(album.photos)
print(album.add_photo("prom"))
print(album.add_photo("wedding"))

print(album.display())
