"""Northline Cut — vertical cards and captions for the «Одна страница» series.

Run: python generate.py
Writes PNGs, caption texts, and a local preview page into out/.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "out"
CARDS = OUT / "cards"
CAPTIONS = OUT / "captions"
POSTS = OUT / "posts"

W, H = 1080, 1920
POST_URL = "https://boosty.to/lerash/posts/9724a49e-e3c5-41b1-9b84-ba365b37b59a"
PRICE = "590 ₽"

FOREST = (23, 46, 37)
FOREST_DEEP = (16, 32, 26)
CREAM = (244, 239, 230)
CREAM_DIM = (214, 206, 192)
TERRACOTTA = (184, 92, 62)
INK = (28, 36, 32)
MUTED = (96, 108, 100)
STAR = (232, 196, 140)
LINE = (214, 206, 192)

EPISODES = [
    {
        "hook": "Куда делись деньги за выходные",
        "voice": "Три строки. Без таблицы и без приложения. Остаток оказался меньше, чем казалось в кармане.",
        "page": "Журнал трат",
        "rows": [("Еда", 1800), ("Дорога", 400), ("Мелочи", 900)],
        "start": 4000,
    },
    {
        "hook": "Подписки, которые списываются сами",
        "voice": "Музыка, облако и игра. По отдельности мелочь. Вместе — треть кармана.",
        "page": "Трекер подписок",
        "rows": [("Музыка", 199), ("Облако", 149), ("Игра", 499)],
        "start": 1200,
    },
    {
        "hook": "Дорога съела больше, чем казалось",
        "voice": "Метро, автобус и одно такси. На странице это видно сразу, в истории банка — нет.",
        "page": "Месячный бюджет",
        "rows": [("Метро", 700), ("Автобус", 280), ("Такси", 650)],
        "start": 2000,
    },
    {
        "hook": "Еда вне дома за одну неделю",
        "voice": "Кофе, обед и перекус. Это не «ничего не тратил». Это отдельная строка.",
        "page": "Журнал трат",
        "rows": [("Кофе", 840), ("Обед", 2100), ("Перекус", 460)],
        "start": 4000,
    },
    {
        "hook": "Коплю на наушники одной строкой",
        "voice": "Цель живёт на странице накоплений. Взнос записывается в тот же вечер, не «когда-нибудь».",
        "page": "Цели накоплений",
        "rows": [("Взнос", 1500), ("Еда", 1600), ("Дорога", 500)],
        "start": 5000,
    },
    {
        "hook": "Подработка: куда делить смену",
        "voice": "Смена кончилась. Домой, еда, запас. Остаток — то, что можно потратить без стыда.",
        "page": "Месячный бюджет",
        "rows": [("Дорога", 400), ("Еда", 900), ("В запас", 3000)],
        "start": 6000,
    },
    {
        "hook": "Месяц на одной странице",
        "voice": "Двенадцать таких страниц уже лежат в наборе, с января по декабрь 2027.",
        "page": "Месячный бюджет",
        "rows": [("Еда", 6500), ("Дорога", 2200), ("Связь", 900)],
        "start": 12000,
    },
    {
        "hook": "Привычка, которая тихо стоит денег",
        "voice": "Кофе каждый день, две доставки и одна импульсная покупка. Привычка видна, только если её записать.",
        "page": "Трекер привычек",
        "rows": [("Кофе", 2100), ("Доставка", 1800), ("Импульс", 700)],
        "start": 6000,
    },
    {
        "hook": "Остаток, который нельзя трогать",
        "voice": "Сначала записывается неприкосновенное. Потом еда и дорога. Не наоборот.",
        "page": "Годовой обзор",
        "rows": [("Не трогать", 3000), ("Еда", 2500), ("Дорога", 800)],
        "start": 8000,
    },
    {
        "hook": "Подарок без дыры в неделе",
        "voice": "Подарок, упаковка, дорога до человека. Если это влезло в остаток — неделя целая.",
        "page": "Журнал трат",
        "rows": [("Подарок", 2500), ("Упаковка", 200), ("Дорога", 300)],
        "start": 4000,
    },
    {
        "hook": "План был один, факт другой",
        "voice": "Еда вышла за план, дорога уложилась, подписки тоже вышли. Дыра считается на странице, не в голове.",
        "page": "План и факт",
        "rows": [("Еда", 5200), ("Дорога", 1100), ("Подписки", 1100)],
        "start": 6300,
    },
    {
        "hook": "Четыре цели, один вечер",
        "voice": "Наушники, курс, поездка, запас. Четыре строки на странице целей. Один вечер, чтобы их назвать.",
        "page": "Цели накоплений",
        "rows": [("Наушники", 1500), ("Курс", 1000), ("Поездка", 2000)],
        "start": 6000,
    },
    {
        "hook": "Год помещается на одном листе",
        "voice": "Доход, расход, запас. Декабрь потом сравнивается с январём, а не с ощущением.",
        "page": "Годовой обзор",
        "rows": [("Доход", 12000), ("Расход", 9000), ("В запас", 2000)],
        "start": 12000,
        "leftover_label": "СВОБОДНО",
        "leftover_value": "1 000 ₽",
    },
    {
        "hook": "Сначала напечатай одну страницу",
        "voice": "Масштаб 100 процентов, фактический размер. Неделя, приоритеты и остаток. Остальные двадцать одна могут подождать до вечера.",
        "page": "Недельный разворот",
        "rows": [("Приоритеты", 3), ("Дни", 7), ("Списки", 1)],
        "start": 11,
        "unit": "",
        "leftover_label": "ОДИН ЛИСТ",
        "leftover_value": "A4",
    },
]


def load_font(candidates: list[str], size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    fonts = Path(r"C:\Windows\Fonts")
    for name in candidates:
        path = fonts / name
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def font_regular(size: int):
    return load_font(["segoeui.ttf", "arial.ttf"], size)


def font_bold(size: int):
    return load_font(["segoeuib.ttf", "arialbd.ttf"], size)


def font_light(size: int):
    return load_font(["segoeuil.ttf", "segoeui.ttf", "arial.ttf"], size)


def rub(amount: int) -> str:
    return f"{amount:,}".replace(",", " ") + " ₽"


def wrap(draw: ImageDraw.ImageDraw, text: str, font, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if draw.textlength(trial, font=font) <= max_w:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_star(draw: ImageDraw.ImageDraw, cx: float, cy: float, outer: float, inner: float, fill) -> None:
    points = []
    for i in range(8):
        angle = -math.pi / 2 + i * math.pi / 4
        radius = outer if i % 2 == 0 else inner
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    draw.polygon(points, fill=fill)


def fit_hook(draw, text: str, max_w: int, max_lines: int = 4):
    for size in range(76, 46, -2):
        font = font_bold(size)
        lines = wrap(draw, text, font, max_w)
        if len(lines) <= max_lines:
            return font, lines
    font = font_bold(46)
    return font, wrap(draw, text, font, max_w)


def render(episode: dict, index: int) -> Image.Image:
    image = Image.new("RGB", (W, H), FOREST)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 18), fill=TERRACOTTA)

    draw_star(draw, 118, 128, 22, 9, STAR)
    brand = font_bold(34)
    draw.text((158, 108), "NORTHLINE", font=brand, fill=CREAM)
    year = font_light(32)
    year_text = "2027"
    draw.text((W - 96 - draw.textlength(year_text, font=year), 110), year_text, font=year, fill=STAR)

    count = font_regular(28)
    label = f"{index:02d}  /  14"
    draw.text((96, 196), label, font=count, fill=CREAM_DIM)
    page_font = font_regular(28)
    page = episode["page"].upper()
    draw.text((W - 96 - draw.textlength(page, font=page_font), 196), page, font=page_font, fill=CREAM_DIM)

    hook_font, hook_lines = fit_hook(draw, episode["hook"], W - 192)
    y = 280
    for line in hook_lines:
        draw.text((96, y), line, font=hook_font, fill=CREAM)
        y += hook_font.size + 12

    card_top = y + 56
    rows = episode["rows"]
    start = episode["start"]
    spent = sum(amount for _, amount in rows)
    unit = episode.get("unit", "₽")
    row_top = card_top + 48
    row_h = 108
    foot_y = row_top + len(rows) * row_h + 8
    card_bottom = foot_y + 230
    draw.rounded_rectangle((72, card_top, W - 72, card_bottom), radius=36, fill=CREAM)
    label_font = font_regular(36)
    amount_font = font_bold(40)
    for i, (name, amount) in enumerate(rows):
        ry = row_top + i * row_h
        draw.text((120, ry), name, font=label_font, fill=INK)
        shown = rub(amount) if unit == "₽" else str(amount)
        aw = draw.textlength(shown, font=amount_font)
        draw.text((W - 120 - aw, ry - 2), shown, font=amount_font, fill=INK)
        if i < len(rows) - 1:
            draw.line((120, ry + 78, W - 120, ry + 78), fill=(226, 218, 206), width=2)

    leftover = start - spent
    draw.line((120, foot_y, W - 120, foot_y), fill=(226, 218, 206), width=2)
    leftover_label = episode.get("leftover_label", "ОСТАЁТСЯ")
    draw.text((120, foot_y + 28), leftover_label, font=font_regular(28), fill=MUTED)
    if "leftover_value" in episode:
        value = episode["leftover_value"]
        value_color = INK
    else:
        value = ("−" if leftover < 0 else "") + rub(abs(leftover))
        value_color = TERRACOTTA if leftover < 0 else FOREST
    value_font = font_bold(92)
    draw.text((120, foot_y + 72), value, font=value_font, fill=value_color)

    price_y = card_bottom + 64
    draw.text((96, price_y), PRICE, font=font_bold(54), fill=CREAM)
    sub = font_regular(30)
    draw.text((96, price_y + 76), "4 PDF  ·  22 страницы планировщика и 21 страница бюджета", font=sub, fill=CREAM_DIM)
    draw.text((96, price_y + 122), "каждый файл в A4 и US Letter", font=sub, fill=CREAM_DIM)
    draw.text((96, price_y + 196), "boosty.to/lerash", font=font_bold(32), fill=STAR)
    return image


def money_tail(episode: dict) -> str:
    spent = sum(amount for _, amount in episode["rows"])
    leftover = episode["start"] - spent
    if "leftover_value" in episode:
        return f"{episode['leftover_label']}: {episode['leftover_value']}"
    sign = "−" if leftover < 0 else ""
    return f"Остаётся: {sign}{rub(abs(leftover))}"


def row_line(episode: dict) -> str:
    unit = episode.get("unit", "₽")
    parts = []
    for name, amount in episode["rows"]:
        shown = rub(amount) if unit == "₽" else str(amount)
        parts.append(f"{name} {shown}")
    return ", ".join(parts)


def caption(episode: dict, index: int) -> str:
    rows = "\n".join(
        f"{name}: {rub(amount) if episode.get('unit', '₽') == '₽' else amount}"
        for name, amount in episode["rows"]
    )
    tail = money_tail(episode)
    return (
        f"{episode['hook']}\n\n"
        f"{episode['voice']}\n"
        f"Страница в наборе: {episode['page']}.\n\n"
        f"{rows}\n{tail}\n\n"
        "22 страницы планировщика и 21 страница бюджета, каждый файл в A4 и US Letter.\n"
        f"{PRICE}\n{POST_URL}\n\n"
        f"Кадр {index:02d}. Говори текст сверху, в конце покажи цену и ссылку.\n"
    )


def platform_post(episode: dict, index: int) -> str:
    tail = money_tail(episode)
    return (
        f"День {index:02d} из 14\n"
        f"Кадр: out/cards/{index:02d}.png\n"
        f"Страница набора: {episode['page']}\n\n"
        "YouTube Shorts — название\n"
        f"{episode['hook']}\n\n"
        "Подпись для TikTok, Shorts и Reels\n"
        f"{episode['hook']}.\n"
        f"{row_line(episode)}. {tail}.\n"
        "4 PDF, A4 и Letter. 590 ₽. Ссылка в первом комментарии.\n\n"
        "Первый комментарий\n"
        f"{POST_URL}\n"
        "22 страницы планировщика и 21 страница бюджета, каждый файл в A4 и US Letter.\n\n"
        "Говорить в кадре\n"
        f"{episode['voice']}\n"
    )


def write_preview(names: list[str]) -> None:
    cards = "\n".join(
        f'<figure><img src="cards/{name}" alt="{name}"><figcaption>{name}</figcaption></figure>'
        for name in names
    )
    html = f"""<!doctype html>
<html lang="ru">
<meta charset="utf-8">
<title>Northline Cut</title>
<style>
  body {{ margin: 0; background: #10201a; color: #f4efe6; font-family: "Segoe UI", sans-serif; }}
  h1 {{ font-weight: 600; font-size: 28px; padding: 28px 32px 0; }}
  p {{ padding: 8px 32px 0; color: #d6cec0; }}
  .row {{ display: flex; gap: 28px; overflow-x: auto; padding: 28px 32px 48px; }}
  figure {{ margin: 0; }}
  img {{ height: 78vh; border-radius: 18px; display: block; }}
  figcaption {{ margin-top: 8px; font-size: 13px; color: #d6cec0; }}
</style>
<h1>Одна страница · 14 кадров</h1>
<p>Листай вправо. Эти картинки и есть кадр для TikTok, Shorts и Reels.</p>
<div class="row">
{cards}
</div>
</html>
"""
    (OUT / "index.html").write_text(html, encoding="utf-8")


def write_schedule() -> None:
    lines = ["День — заголовок — страница", ""]
    for index, episode in enumerate(EPISODES, start=1):
        lines.append(f"{index:02d}. {episode['hook']} — {episode['page']}")
    lines.append("")
    lines.append("Один и тот же ролик выкладывается в TikTok, YouTube Shorts и Reels.")
    lines.append("Ссылка на пост — только в первом комментарии и в шапке профиля.")
    lines.append(POST_URL)
    (POSTS / "00-порядок.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    CARDS.mkdir(parents=True, exist_ok=True)
    CAPTIONS.mkdir(parents=True, exist_ok=True)
    POSTS.mkdir(parents=True, exist_ok=True)
    names = []
    for index, episode in enumerate(EPISODES, start=1):
        name = f"{index:02d}.png"
        render(episode, index).save(CARDS / name, "PNG")
        (CAPTIONS / f"{index:02d}.txt").write_text(caption(episode, index), encoding="utf-8")
        (POSTS / f"{index:02d}.txt").write_text(platform_post(episode, index), encoding="utf-8")
        names.append(name)
        print(name)
    write_preview(names)
    write_schedule()
    print(f"wrote {len(names)} cards to {OUT}")


if __name__ == "__main__":
    main()
