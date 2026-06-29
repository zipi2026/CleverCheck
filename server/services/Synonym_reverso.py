from typing import List
import requests
from bs4 import BeautifulSoup
import urllib
import urllib3

class SynonymClient:
    def __init__(self) -> None:
        # מבטל אזהרות SSL
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    @staticmethod
    def get_synonyms(word: str) -> List[str]:
        try:
            # קידוד המילה ל-URL כדי למנוע שגיאות עם תווים מיוחדים
            encoded_word = urllib.parse.quote(word)
        except Exception as e:
            # קידוד נכשל (מעט נדיר)
            raise Exception(f"Error encoding the word '{word}': {e}")

        url = f"https://synonyms.reverso.net/synonym/he/{encoded_word}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        try:
            # שליחת הבקשה לשרת
            response = requests.get(url, headers=headers, verify=False)
        except requests.exceptions.SSLError as e:
            # שגיאת SSL (בעיות בתעודה, verify=False מונע)
            raise Exception(f"SSL Error while connecting to {url}: {e}")
        except requests.exceptions.ConnectionError as e:
            # שגיאת חיבור (שרת לא זמין, בעיות רשת)
            raise Exception(f"Connection Error while connecting to {url}: {e}")
        except Exception as e:
            # כל שגיאה אחרת בבקשה
            raise Exception(f"Error during request to {url}: {e}")

        if response.status_code != 200:
            # HTTP Error
            raise Exception(f"Failed to fetch data from {url}. HTTP Status: {response.status_code}")

        try:
            # ניתוח ה-HTML
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            # שגיאה בניתוח HTML
            raise Exception(f"Error parsing HTML content: {e}")

        try:
            # חיפוש אלמנטים עם class של מילים נרדפות
            synonym_elements = soup.select("a.synonym")
            synonyms = [elem.text.strip() for elem in synonym_elements]
        except Exception as e:
            # בעיה בחילוץ האלמנטים מה-HTML
            raise Exception(f"Error extracting synonyms from HTML: {e}")

        if not synonyms:
            # אם הרשימה ריקה, אולי שינוי ב-HTML או class לא קיים
            raise Exception("No synonyms found. Check if the HTML structure or class name has changed.")

        return synonyms


    def are_synonyms(self,word1: str, word2: str) -> bool:
            """
            בודקת אם שתי מילים הן נרדפות זו לזו (דו־כיווני) עם caching פנימי.
            אם המילים זהות, מחזירה מיד True.
            """
            # בדיקה אם המילים זהות בדיוק
            if word1 == word2:
                return True

            try:
                synonyms1 = SynonymClient.get_synonyms(word1)
            except Exception as e:
                print(f"Failed to get synonyms for '{word1}': {e}")
                synonyms1 = []

            try:
                synonyms2 = SynonymClient.get_synonyms(word2)
            except Exception as e:
                print(f"Failed to get synonyms for '{word2}': {e}")
                synonyms2 = []

            return word2 in synonyms1 or word1 in synonyms2