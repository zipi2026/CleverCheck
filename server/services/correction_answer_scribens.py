import requests
import urllib3
import threading

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ScribensService:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        # Singleton כדי למנוע כמה sessions
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance._init_session()
        return cls._instance

    def _init_session(self):
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "Mozilla/5.0"
        })

        # warmup (פעם אחת בלבד)
        try:
            self.session.get(
                "https://www.scribens.com",
                verify=False,
                timeout=10
            )
        except Exception as e:
            print("Scribens warmup failed:", e)

    def correct_text(self, text: str) -> str:
        url = "https://www.scribens.fr/Scribens/OtherAlg_Ref_Servlet"

        data = {
            "FunctionName": "Get_Correction",
            "Plugin": "Website_desktop",
            "Text": text,
            "IdLanguage": "he",
            "IdLangDisplay": "he",
            "Tone": "nope",
            "Settings": "points:none|title:no|conclusion:no|inclusive:no|function:None"
        }

        try:
            res = self.session.post(
                url,
                data=data,
                verify=False,
                timeout=15
            )

            if res.status_code != 200:
                print("HTTP error:", res.status_code)
                return text

            try:
                data = res.json()
            except Exception as e:
                print("JSON error:", e, res.text)
                return text

            return data.get("ResultSt", text)

        except Exception as e:
            print("Scribens request failed:", e)
            return text

scribens = ScribensService()

result = scribens.correct_text("לך עלשלום")
print(result)

