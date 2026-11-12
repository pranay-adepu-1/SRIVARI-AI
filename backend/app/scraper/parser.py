import re
import hashlib
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from email.utils import parsedate_to_datetime

def generate_content_hash(source_url: str, title: str) -> str:
    raw = f"{source_url.strip()}|{title.strip()}".encode('utf-8')
    return hashlib.sha256(raw).hexdigest()

def clean_html(raw_html: str) -> str:
    if not raw_html:
        return ""
    # Strip HTML tags
    clean = re.sub(r'<[^>]+>', ' ', raw_html)
    # Decode basic entities
    clean = clean.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#8217;', "'").replace('&#8211;', '-')
    # Normalize spaces
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

def categorize_article(title: str, content: str) -> Dict[str, Any]:
    """
    Categorizes the announcement using deterministic keyword matching.
    """
    text = f"{title} {content}".lower()
    
    is_quota = False
    quota_keywords = ["quota", "release", "online dip", "electronic dip", "booking open", "కోటా", "విడుదల"]
    if any(k in text for k in quota_keywords):
        is_quota = True

    if any(k in text for k in ["srivari seva", "parakamani", "laddu seva", "sevak", "సేవ", "శ్రీవారి సేవ"]):
        return {"slug": "srivari-seva", "is_quota": is_quota}
    elif any(k in text for k in ["sed", "special entry", "sarva darshan", "ssd", "vip break", "srivani", "darshan", "దర్శనం"]):
        return {"slug": "darshan", "is_quota": is_quota}
    elif any(k in text for k in ["accommodation", "cottage", "room", "rest house", "caution deposit", "గది", "వసతి"]):
        return {"slug": "accommodation", "is_quota": is_quota}
    elif any(k in text for k in ["brahmotsavam", "vaikunta", "rathasapthami", "garuda seva", "utsavam", "festival", "ఉత్సవ", "బ్రహ్మోత్సవ"]):
        return {"slug": "festivals", "is_quota": is_quota}
    elif any(k in text for k in ["laddu", "potu", "prasadam", "dittam", "లడ్డూ", "ప్రసాదం"]):
        return {"slug": "laddu-prasadam", "is_quota": is_quota}
    elif any(k in text for k in ["recruitment", "employment", "job", "notification", "ఉద్యోగ", "నోటిఫికేషన్"]):
        return {"slug": "recruitment", "is_quota": is_quota}
    else:
        return {"slug": "general-notice", "is_quota": is_quota}

def parse_rss_feed(xml_content: str) -> List[Dict[str, Any]]:
    """
    Parses TTD WordPress RSS feed and extracts clean articles.
    """
    articles = []
    try:
        root = ET.fromstring(xml_content)
        channel = root.find("channel")
        if channel is None:
            return articles

        for item in channel.findall("item"):
            title_node = item.find("title")
            link_node = item.find("link")
            desc_node = item.find("description")
            pub_date_node = item.find("pubDate")

            title = title_node.text if title_node is not None and title_node.text else ""
            link = link_node.text if link_node is not None and link_node.text else ""
            desc = desc_node.text if desc_node is not None and desc_node.text else ""
            
            clean_title = clean_html(title)
            clean_content = clean_html(desc)
            
            pub_date = datetime.now(timezone.utc)
            if pub_date_node is not None and pub_date_node.text:
                try:
                    pub_date = parsedate_to_datetime(pub_date_node.text)
                    if pub_date.tzinfo is not None:
                        pub_date = pub_date.replace(tzinfo=None)
                except Exception:
                    pub_date = datetime.now(timezone.utc)

            if not link or not clean_title:
                continue

            content_hash = generate_content_hash(link, clean_title)
            cat_info = categorize_article(clean_title, clean_content)

            articles.append({
                "title_en": clean_title,
                "title_te": clean_title,  # Will be mapped or populated
                "content_en": clean_content,
                "content_te": clean_content,
                "source_url": link.strip(),
                "source_domain": "news.tirumala.org",
                "publication_date": pub_date,
                "content_hash": content_hash,
                "category_slug": cat_info["slug"],
                "is_quota_alert": cat_info["is_quota"]
            })
    except Exception as e:
        print(f"Error parsing RSS XML: {e}")

    return articles
