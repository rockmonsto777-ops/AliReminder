import os, json, random, urllib.request
from datetime import datetime, timedelta, timezone

STATE_FILE = "state.json"

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

MIN_DAYS = float(os.getenv("MIN_DAYS", "15"))
MAX_DAYS = float(os.getenv("MAX_DAYS", "23"))

MESSAGE = os.getenv("MESSAGE", "Привет 👋")


def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = json.dumps({"chat_id": CHAT_ID, "text": text}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)


now = datetime.now(timezone.utc)
state = load_state()

next_send_at = state.get("next_send_at")

if next_send_at and now < datetime.fromisoformat(next_send_at):
    print("Пока рано отправлять.")
    raise SystemExit

send_message(MESSAGE)

delay_days = random.uniform(MIN_DAYS, MAX_DAYS)
next_time = now + timedelta(days=delay_days)

state["last_sent_at"] = now.isoformat()
state["next_send_at"] = next_time.isoformat()
state["delay_days"] = delay_days

save_state(state)

print(f"Сообщение отправлено. Следующее примерно через {delay_days:.2f} дней.")
