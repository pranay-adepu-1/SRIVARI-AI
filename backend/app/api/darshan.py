from typing import List
from fastapi import APIRouter
from app.schemas.darshan import DarshanTypeGuide, SevaGuide, AccommodationGuide, FestivalEvent

router = APIRouter(tags=["Devotee Guides"])

DARSHAN_GUIDES = [
    {
        "id": "special_entry_darshan_300",
        "name_en": "₹300 Special Entry Darshan (Sheeghra Darshan)",
        "name_te": "రూ. 300 ప్రత్యేక ప్రవేశ దర్శనం (శీఘ్ర దర్శనం)",
        "cost": "₹300 per pilgrim",
        "booking_mode": "Online Advance Booking at ttdevasthanams.ap.gov.in",
        "reporting_location_en": "ATC Circle, Tirumala",
        "reporting_location_te": "ఏటీసీ సర్కిల్, తిరుమల",
        "description_en": "Quick access darshan introduced to provide smooth and faster darshan of Lord Venkateswara Swamy. Typically released online 3 months in advance.",
        "description_te": "శ్రీవారి శీఘ్ర దర్శనం కోసం ప్రవేశపెట్టిన దర్శన మార్గం. ప్రతి నెలా ఆన్‌లైన్ ద్వారా 3 నెలల ముందుగా కోటాను విడుదల చేస్తారు.",
        "guidelines_en": [
            "Devotees must report at the exact time slot printed on the ticket.",
            "Original Photo ID card used during online booking must be produced.",
            "Traditional dress code is strictly compulsory.",
            "1 free Laddu prasadam is provided per ticket.",
            "Children below 12 years do not require a separate ticket (ID proof mandatory)."
        ],
        "guidelines_te": [
            "టికెట్‌పై ముద్రించిన సమయానికి మాత్రమే ఏటీసీ సర్కిల్ వద్ద రిపోర్ట్ చేయాలి.",
            "బుకింగ్ సమయంలో ఉపయోగించిన అసలు గుర్తింపు కార్డు (ఆధార్) తప్పనిసరిగా చూపించాలి.",
            "సాంప్రదాయ వస్త్రధారణ తప్పనిసరి.",
            "ప్రతి టికెట్‌కు ఒక ఉచిత లడ్డూ ప్రసాదం ఇస్తారు.",
            "12 సంవత్సరాల లోపు పిల్లలకు టికెట్ అవసరం లేదు (వయస్సు ధృవీకరణ పత్రం ఉండాలి)."
        ],
        "official_link": "https://ttdevasthanams.ap.gov.in/"
    },
    {
        "id": "sarva_darshan",
        "name_en": "Sarva Darshan (Free / SSD Token Darshan)",
        "name_te": "సర్వ దర్శనం (ఉచిత / ఎస్‌ఎస్‌డి టోకెన్లు)",
        "cost": "Free (No charges)",
        "booking_mode": "Offline Counters in Tirupati & Direct Queue at VQC-2 Tirumala",
        "reporting_location_en": "Vaikuntam Queue Complex-2 (VQC-2), Tirumala",
        "reporting_location_te": "వైకుంఠం క్యూ కాంప్లెక్స్-2, తిరుమల",
        "description_en": "Free darshan accessible to all pilgrims without discrimination. Slotted Sarva Darshan (SSD) tokens are issued at designated counters in Tirupati to minimize waiting hours.",
        "description_te": "భక్తులందరికీ అందుబాటులో ఉండే ఉచిత దర్శనం. భక్తుల నిరీక్షణ సమయాన్ని తగ్గించడానికి తిరుపతిలో టైమ్ స్లాట్ టోకెన్లు (SSD) జారీ చేస్తారు.",
        "guidelines_en": [
            "SSD Token Counters: Bhudevi Complex (Alipiri), Srinivasam Complex, Govindaraja Swamy Choultries.",
            "Tokens issued on biometric Aadhaar verification on a first-come, first-served basis.",
            "Pilgrims without tokens can join general compartments in VQC-2 directly.",
            "Free food (Annaprasadam), milk, and water are provided continuously in compartments."
        ],
        "guidelines_te": [
            "టోకెన్ కౌంటర్లు: భూదేవి కాంప్లెక్స్ (అలిపిరి), శ్రీనివాసం కాంప్లెక్స్, గోవిందరాజస్వామి సత్రాలు.",
            "ఆధార్ కార్డు బయోమెట్రిక్ ద్వారా ముందు వచ్చిన వారికి ముందు ప్రాతిపదికన టోకెన్లు ఇస్తారు.",
            "టోకెన్లు లేని వారు నేరుగా తిరుమల వైకుంఠం క్యూ కాంప్లెక్స్-2 కంపార్ట్‌మెంట్లలో ప్రవేశించవచ్చు.",
            "కంపార్ట్‌మెంట్లలో వేచి ఉన్న భక్తులకు ఉచిత అన్నప్రసాదం, పాలు, మంచినీరు నిరంతరం అందిస్తారు."
        ],
        "official_link": "https://www.tirumala.org/"
    },
    {
        "id": "vip_break_darshan",
        "name_en": "VIP Break Darshan (SRIVANI Trust)",
        "name_te": "విఐపి బ్రేక్ దర్శనం (శ్రీవాణి ట్రస్ట్)",
        "cost": "₹10,000 Donation to SRIVANI Trust + ₹500 Darshan Ticket",
        "booking_mode": "Online at ttdevasthanams.ap.gov.in or Current Booking at Tirupati Airport / Gokulam",
        "reporting_location_en": "Vaikuntam Queue Complex-1, Tirumala",
        "reporting_location_te": "వైకుంఠం క్యూ కాంప్లెక్స్-1, తిరుమల",
        "description_en": "Provides VIP Break Darshan access through donor contribution to the Sri Venkateswara Aalayala Nirmanam (SRIVANI) Trust for temple construction in backward areas.",
        "description_te": "వెనుకబడిన ప్రాంతాలలో ఆలయాల నిర్మాణం కోసం ఉద్దేశించిన శ్రీవాణి ట్రస్ట్‌కు విరాళం ఇచ్చే దాతలకు కేటాయించే విఐపి బ్రేక్ దర్శనం.",
        "guidelines_en": [
            "Donor pays ₹10,000 donation plus ₹500 ticket price per head.",
            "Darshan takes place during morning VIP break slots.",
            "Strict protocol dress code must be adhered to.",
            "Income tax 80G exemption receipt is provided for the donation."
        ],
        "guidelines_te": [
            "ఒక్కొక్కరికి రూ. 10,000 విరాళం + రూ. 500 దర్శన రుసుము చెల్లించాలి.",
            "ఉదయం కేటాయించిన వీఐపీ బ్రేక్ సమయంలో దర్శనం జరుగుతుంది.",
            "సాంప్రదాయ వస్త్రధారణ నిబంధనలు ఖచ్చితంగా పాటించాలి.",
            "విరాళానికి ఆదాయపు పన్ను 80G మినహాయింపు రసీదు లభిస్తుంది."
        ],
        "official_link": "https://ttdevasthanams.ap.gov.in/"
    },
    {
        "id": "divya_darshan_footpaths",
        "name_en": "Divya Darshan (Pedestrian Footpath Pilgrims)",
        "name_te": "దివ్య దర్శనం (కాలిబాట భక్తులు)",
        "cost": "Free",
        "booking_mode": "Footpath Token Counters on Trekking Routes",
        "reporting_location_en": "Alipiri (3,550 steps) or Srivari Mettu (2,388 steps)",
        "reporting_location_te": "అలిపిరి (3,550 మెట్లు) లేదా శ్రీవారి మెట్టు (2,388 మెట్లు)",
        "description_en": "Dedicated darshan tokens issued to pious devotees trekking to the holy seven hills on foot through ancient sacred pathways.",
        "description_te": "తిరుమల కొండకు కాలిబాట ద్వారా కాలినడకన చేరుకునే భక్తులకు అందించే పవిత్ర దివ్య దర్శన టోకెన్లు.",
        "guidelines_en": [
            "Alipiri Route: 9 km distance, 3,550 steps; open 24 hours (tokens at Galigopuram).",
            "Srivari Mettu Route: 2.1 km distance, 2,388 steps; open 6:00 AM to 5:00 PM (tokens at 1200th step).",
            "Free luggage transport service available from Alipiri to Tirumala.",
            "Footpath tokens are subject to daily quota limits."
        ],
        "guidelines_te": [
            "అలిపిరి మార్గం: 9 కి.మీ దూరం, 3,550 మెట్లు; నిరంతరం తెరిచి ఉంటుంది (గాలిగోపురం వద్ద టోకెన్లు).",
            "శ్రీవారి మెట్టు మార్గం: 2.1 కి.మీ దూరం, 2,388 మెట్లు; ఉదయం 6:00 నుండి సాయంత్రం 5:00 వరకు తెరిచి ఉంటుంది.",
            "అలిపిరి నుండి తిరుమలకు భక్తుల లగేజీని ఉచితంగా తరలించే సదుపాయం ఉంది.",
            "కాలిబాట టోకెన్లు రోజువారీ పరిమిత కోటాకు లోబడి ఉంటాయి."
        ],
        "official_link": "https://www.tirumala.org/"
    }
]

SEVA_GUIDE = {
    "title_en": "Srivari Seva Voluntary Service Guidelines",
    "title_te": "శ్రీవారి సేవ స్వచ్ఛంద సేవ మార్గదర్శకాలు",
    "eligibility_en": "Hindu devotees aged between 18 and 60 years in good physical and mental health. Parakamani Seva requires 35 to 65 years with banking/government service background.",
    "eligibility_te": "18 నుండి 60 సంవత్సరాల వయస్సు కలిగిన శారీరక, మానసిక దృఢత్వం గల హిందూ భక్తులు. పరకామణి సేవకు 35 నుండి 65 ఏళ్ల ప్రభుత్వ/బ్యాంకింగ్ ఉద్యోగులకు ప్రాధాన్యత.",
    "tenure": "7-day tenure (reporting every Friday or Tuesday) / 4-day tenure",
    "dress_code_en": "Female Sevaks: Saree with Maroon scarf (Kavacham). Male Sevaks: White Dhoti & Kurta or White Pant & Shirt with Yellow scarf.",
    "dress_code_te": "మహిళా సేవకులు: చీర మరియు కుంకుమ రంగు కండువా. పురుష సేవకులు: తెల్లటి ధోతీ/కుర్తా లేదా తెల్లటి చొక్కా/ప్యాంట్ మరియు పసుపు రంగు కండువా.",
    "guidelines_en": [
        "Registration is completely free on https://ttdevasthanams.ap.gov.in/.",
        "Sevaks must report at the Srivari Seva Sadan, PAC-4, Tirumala with Aadhaar card and allotment receipt.",
        "Accommodation and food are provided free during the service tenure.",
        "Duties include queue line assistance, water distribution, Annaprasadam serving, luggage counter management, and information desk support.",
        "Strict discipline and selfless devotional attitude are expected."
    ],
    "guidelines_te": [
        "https://ttdevasthanams.ap.gov.in/ లో రిజిస్ట్రేషన్ పూర్తిగా ఉచితం.",
        "సేవకులు ఆధార్ కార్డు మరియు అలాట్‌మెంట్ రసీదుతో తిరుమల పీఏసీ-4 వద్ద ఉన్న శ్రీవారి సేవా సదన్‌లో రిపోర్ట్ చేయాలి.",
        "సేవా కాలంలో వసతి మరియు భోజన సౌకర్యం టీటీడీ ఉచితంగా కల్పిస్తుంది.",
        "క్యూ లైన్ నిర్వహణ, మంచినీటి పంపిణీ, అన్నప్రసాదం వడ్డన, లగేజీ కౌంటర్లు మరియు సమాచార కేంద్రాల్లో విధులు ఉంటాయి.",
        "నిస్వార్థ భక్తిభావం మరియు క్రమశిక్షణతో సేవ చేయాలి."
    ],
    "official_link": "https://ttdevasthanams.ap.gov.in/"
}

ACCOMMODATION_GUIDES = [
    {
        "category_en": "Tirumala Cottages & Rest Houses",
        "category_te": "తిరుమల కాటేజీలు మరియు విశ్రాంతి భవనాలు",
        "location": "Tirumala Hills",
        "tariff_range": "₹100 to ₹2,000 per 24 hours",
        "caution_deposit": "Equal to 100% of room tariff (Refunded to bank account in 3-7 days)",
        "max_stay_hours": 24,
        "guidelines_en": [
            "Online Quota: Released monthly on ttdevasthanams.ap.gov.in (requires valid Darshan booking).",
            "Current Spot Allotment: Available at Central Reception Office (CRO) General counter, Tirumala.",
            "Maximum stay is strictly 24 hours; extension is not permitted under any circumstances.",
            "Check-in reporting window is 3 hours from the allotted slot time."
        ],
        "guidelines_te": [
            "ఆన్‌లైన్ కోటా: ttdevasthanams.ap.gov.in లో దర్శన టికెట్ ఉన్న భక్తులకు నెలకు ఒకసారి విడుదల చేస్తారు.",
            "కరెంట్ స్పాట్ బుకింగ్: తిరుమల సిఆర్ఓ (CRO) జనరల్ కౌంటర్ వద్ద లభిస్తుంది.",
            "గరిష్టంగా 24 గంటలు మాత్రమే బస చేయవచ్చు; పొడిగింపు ఎట్టి పరిస్థితుల్లోనూ ఉండదు.",
            "కేటాయించిన సమయం నుండి 3 గంటల లోపు సబ్‌-ఎంక్వైరీ ఆఫీస్‌లో రిపోర్ట్ చేయాలి."
        ],
        "official_link": "https://ttdevasthanams.ap.gov.in/"
    },
    {
        "category_en": "Tirupati Pilgrim Rest Houses",
        "category_te": "తిరుపతి యాత్రికుల సత్రాలు & కాంప్లెక్స్‌లు",
        "location": "Tirupati Downhill",
        "tariff_range": "₹200 to ₹1,500 per 24 hours",
        "caution_deposit": "Standard refundable deposit",
        "max_stay_hours": 24,
        "guidelines_en": [
            "Srinivasam Complex: Located opposite Central Bus Station (RTC Bus Stand).",
            "Vishnu Nivasam: Located opposite Tirupati Railway Station.",
            "Madhavan Rest House: Located adjacent to Srinivasam Complex.",
            "Current spot counters and online advance booking both available."
        ],
        "guidelines_te": [
            "శ్రీనివాసం కాంప్లెక్స్: ఆర్టీసీ బస్ స్టాండ్ ఎదురుగా ఉంది.",
            "విష్ణు నివాసం: తిరుపతి రైల్వే స్టేషన్ ఎదురుగా ఉంది.",
            "మాధవం రెస్ట్ హౌస్: శ్రీనివాసం కాంప్లెక్స్ పక్కనే ఉంది.",
            "కరెంట్ బుకింగ్ కౌంటర్లు మరియు ఆన్‌లైన్ అడ్వాన్స్ బుకింగ్ రెండూ అందుబాటులో ఉన్నాయి."
        ],
        "official_link": "https://ttdevasthanams.ap.gov.in/"
    }
]

FESTIVAL_EVENTS = [
    {
        "id": "salakatla_brahmotsavam",
        "name_en": "Salakatla Annual Brahmotsavam",
        "name_te": "సాలకట్ల వార్షిక బ్రహ్మోత్సవాలు",
        "date_display": "Ashwayuja Masa (September / October)",
        "significance_en": "The grand 9-day annual festival initiated by Lord Brahma featuring celestial vahanams like Garuda Seva, Hanumantha Vahanam, Rathotsavam, and Chakrasnanam.",
        "significance_te": "బ్రహ్మదేవునిచే ప్రారంభించబడిన 9 రోజుల అత్యంత వైభవమైన బ్రహ్మోత్సవాలు. గరుడ సేవ, రథోత్సవం, చక్రస్నానం విశేష ఘట్టాలు.",
        "location": "Four Mada Streets, Tirumala"
    },
    {
        "id": "vaikunta_ekadasi",
        "name_en": "Vaikunta Ekadasi (Mukkoti Ekadasi)",
        "name_te": "వైకుంఠ ఏకాదశి (ముక్కోటి ఏకాదశి)",
        "date_display": "Dhanurmasa (December / January)",
        "significance_en": "Sacred 10-day opening of the holy Vaikunta Dwaram. Devotees passing through Vaikunta Dwaram attain liberation and immense spiritual merit.",
        "significance_te": "పవిత్రమైన వైకుంఠ ద్వార దర్శనం 10 రోజుల పాటు భక్తులకు కల్పిస్తారు. ఈ ద్వార దర్శనం ముక్తిదాయకం.",
        "location": "Sanctum Sanctorum, Tirumala"
    },
    {
        "id": "rathasapthami",
        "name_en": "Rathasapthami (Mini Brahmotsavam)",
        "name_te": "రథసప్తమి (ఒకరోజు బ్రహ్మోత్సవం)",
        "date_display": "Magha Shuddha Saptami (January / February)",
        "significance_en": "Known as one-day Brahmotsavam where Lord Malayappa Swamy rides 7 different divine vahanams in a single day from sunrise to night around the four mada streets.",
        "significance_te": "ఒకే రోజులో శ్రీ మలయప్ప స్వామివారు సూర్యోదయం నుండి రాత్రి వరకు 7 దివ్య వాహనాలపై తిరువీధుల్లో విహరిస్తారు.",
        "location": "Four Mada Streets, Tirumala"
    },
    {
        "id": "garuda_seva_pournami",
        "name_en": "Monthly Pournami Garuda Seva",
        "name_te": "నెలవారీ పౌర్ణమి గరుడ సేవ",
        "date_display": "Every Full Moon Night (Pournami)",
        "significance_en": "Lord Venkateswara rides majestically on His supreme carrier Garuda Vahana on every full moon night to bless pilgrims around Mada streets.",
        "significance_te": "ప్రతి పౌర్ణమి రాత్రి శ్రీ మలయప్ప స్వామివారు అత్యంత ప్రీతిపాత్రమైన గరుడ వాహనంపై భక్తులకు దర్శనమిస్తారు.",
        "location": "Four Mada Streets, Tirumala"
    }
]

@router.get("/darshan/guides", response_model=List[DarshanTypeGuide])
def get_darshan_guides():
    return DARSHAN_GUIDES

@router.get("/seva/guide", response_model=SevaGuide)
def get_seva_guide():
    return SEVA_GUIDE

@router.get("/accommodation/guides", response_model=List[AccommodationGuide])
def get_accommodation_guides():
    return ACCOMMODATION_GUIDES

@router.get("/festivals/calendar", response_model=List[FestivalEvent])
def get_festival_calendar():
    return FESTIVAL_EVENTS

