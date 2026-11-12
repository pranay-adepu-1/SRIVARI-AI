from typing import List, Optional
from pydantic import BaseModel

class DarshanTypeGuide(BaseModel):
    id: str
    name_en: str
    name_te: str
    cost: str
    booking_mode: str
    reporting_location_en: str
    reporting_location_te: str
    description_en: str
    description_te: str
    guidelines_en: List[str]
    guidelines_te: List[str]
    official_link: str

class SevaGuide(BaseModel):
    title_en: str
    title_te: str
    eligibility_en: str
    eligibility_te: str
    tenure: str
    dress_code_en: str
    dress_code_te: str
    guidelines_en: List[str]
    guidelines_te: List[str]
    official_link: str

class AccommodationGuide(BaseModel):
    category_en: str
    category_te: str
    location: str
    tariff_range: str
    caution_deposit: str
    max_stay_hours: int
    guidelines_en: List[str]
    guidelines_te: List[str]
    official_link: str

class FestivalEvent(BaseModel):
    id: str
    name_en: str
    name_te: str
    date_display: str
    significance_en: str
    significance_te: str
    location: str

