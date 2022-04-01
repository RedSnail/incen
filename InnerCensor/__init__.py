from telethon import TelegramClient
import datetime

# api_id = int(os.getenv("API_ID"))
# api_hash = os.getenv("API_HASH")

__version__ = "0.0.1"

api_id = 16133923
api_hash = "9c758d86808f7798fa9b161975be492b"

client = TelegramClient("censor", api_id, api_hash)

DANGEROUS_LIST = "украина путин путен донбасс киев донецк харьков чернигов мариуполь луганск крым война захват " \
                 "солдат танк мирный мир мент навальный чернобыль запорожский аннексия митинг автозак омон обыск " \
                 "преследование свобода росгвардия цензура народный оборона обстрел диктатор диктатура демократия " \
                 "зеленский вооруженный истребитель беспилотник наземный фашизм гитлер геббельс гестапо эсэс".split()

# sorry if you see that

