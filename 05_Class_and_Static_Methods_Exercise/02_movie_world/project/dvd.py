import calendar

class DVD:
    def __init__(self, name: str, dvd_id: int, creation_year: int, creation_month: int, age_restriction: int):
        self.name = name
        self.id = dvd_id
        self.creation_year = creation_year
        self.creation_month = creation_month
        self.age_restriction = age_restriction
        self.is_rented = False

    @classmethod
    def from_date(cls, dvd_id, name, date, age_restriction ):
        day, month, year = [int(x) for x in date.split('.')]
        month_name = calendar.month_name[month]
        return cls(name, dvd_id, year, month_name, age_restriction)

    def __repr__(self):
        return (f"{self.id}: {self.name} ({self.creation_month} {self.creation_year}) "
                f"has age restriction {self.age_restriction}. Status: {'rented' if self.is_rented else 'not rented'}")

