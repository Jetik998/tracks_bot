import logging
from bs4 import BeautifulSoup
from utils import save_to_file, save_captcha_image
from client import get_html
from config import (
    SEARCH_URL,
    SEARCH_INPUT_TRACK_LIMIT,
    BASE_URL,
    MIX_RETRY_COUNT,
    MIX_COUNT_LIMIT,
    PARCE_MIX_COUNT_LIMIT,
)
from utils import save_to_json
import sys


logger = logging.getLogger(__name__)

input_track = None
input_track_url = None


def set_input_track(track_name):
    global input_track
    input_track = track_name


def search_track():
    """Ищет трек по названию, возвращает страницу со списком треков"""
    payload = {
        "main_search": input_track,
        "search_selection": "2",  # 2 = поиск tracks
        "orderby": "added",
    }
    html = get_html(SEARCH_URL, data=payload)
    save_to_file(html, "InputTrackPage", "html")
    return html


def detect_captcha(html):
    """Возвращает True, если капча есть, иначе False"""
    soup = BeautifulSoup(html, "html.parser")
    if soup.find("div", id="kTZXcvbn"):
        logger.info("Ввод капчи не потребовался")
        return False
    else:
        logger.info("Нужно ввести капчу")
        return True


def get_input_track_url(html):
    """Принимает страницу со списком треков, ищет совпадение с искомым треком
    Если трек найден, возвращает ссылку на страницу с треком"""
    global input_track_url
    soup = BeautifulSoup(html, "html.parser")
    tracks_dives = soup.select("div.bItm.oItm")
    count = 0
    for div in tracks_dives:
        count += 1
        logger.info(f"{count} Попытка поиска искомого трека")
        if count >= SEARCH_INPUT_TRACK_LIMIT:
            logger.info(
                "Количество попыток поиска искомого трека(SEARCH_INPUT_TRACK_LIMIT): %s",
                count,
            )
            break
        link = div.select_one("div.bCont.acSa > div.bTitle > a")
        if link and link.text.strip() == input_track:
            input_track_url = link.get("href")
            input_track_url = BASE_URL + input_track_url
            logger.info(f"Найдена ссылка на искомый трек {input_track_url}")
            return input_track_url


def solve_captcha(html):
    """Принимает страницу, находит капчу, сохряняет в jpg"""
    soup = BeautifulSoup(html, "html.parser")
    captcha_img = soup.find("img", alt="Captcha")
    if captcha_img:
        captcha_url = captcha_img.get("src")
        save_captcha_image(captcha_url)
        logger.error("Появилась страница с капчей, изображение сохранено.")
        input("Введите капчу: ")  # Останавливаемся и ждём ввода

    else:
        logger.info("Капча не найдена")
        sys.exit(0)


def search_url_input_track():
    """Ищет страницу для (input_track). Возвращает ссылку если найдено совпадение."""
    html = search_track()
    if detect_captcha(html):
        solve_captcha(html)

    url = get_input_track_url(html)
    logger.info("search_url_input_track: Выполнено!")
    return url


def fetch_page(url):
    """Загружает HTML-страницу по URL,
    обрабатывает капчу при необходимости,
    возвращает HTML-код страницы.
    """
    html = get_html(url)
    if detect_captcha(html):
        solve_captcha(html)

    logger.info("load_page_input_track: Выполнено!")
    return html


def search_mixes_on_page(html):
    """
    Принимает html страницу с треком (input_track), парсит миксы,
    возвращает список словарей с инфой по миксу.
    """
    mixes = []
    retry_count = 0
    mix_count = 0
    soup = BeautifulSoup(html, "html.parser")
    mix_dives = soup.select("#kTZXcvbn > div.bItm.action.oItm")
    for div in mix_dives:
        retry_count += 1
        mix_count += 1
        if retry_count > MIX_RETRY_COUNT:
            logger.info(
                "Количество попыток поиска миксов(MIX_RETRY_COUNT): %s", retry_count
            )
            break
        if mix_count > MIX_COUNT_LIMIT:
            logger.info("Количество найденных миксов(MIX_COUNT_LIMIT): %s", mix_count)
            break
        logger.info("Попытка поиска микса №: %s", mix_count)
        mix_link = div.select_one("div.bCont > div.bTitle > a")
        mix_name = mix_link.text.strip()
        mix_url = mix_link.get("href")
        mix_url = BASE_URL + mix_url
        mix_count += 1
        mixes.append({"mix_id": mix_count, "mix_name": mix_name, "url": mix_url})
        logger.info("Микс найден и добавлен: %s", mix_name)
    return mixes


def parse_tracklist(html):
    """
    Принимает HTML с треклистом, парсит и возвращает словарь.
    """
    global input_track
    tracklist = {}
    soup = BeautifulSoup(html, "html.parser")
    tracks_dives = soup.select("#tlTab > div[data-trno]")
    count = 0
    tracklist["input_track"] = None
    for div in tracks_dives:  # track_id = div.get("data-trno")
        try:  # track_id = int(track_id)
            count += 1
            track_selector = div.select_one("div.bCont.tl meta[itemprop='name']")
            if track_selector:
                track_name = track_selector.get("content")
                logger.info("Найден трек: %s", track_name)
                tracklist[count] = track_name
                if track_name == input_track:
                    if tracklist["input_track"] is None:
                        tracklist["input_track"] = count
                    else:
                        logger.error(
                            "Внимание! Трек '%s' уже найден раньше (номер %s), а сейчас снова на позиции %s.",
                            input_track,
                            tracklist["input_track"],
                            count,
                        )

            else:
                logger.info("Найден трек без названия!")
                tracklist[count] = None

        except Exception as e:
            logger.error("Ошибка при получении трека:%s", e)
            tracklist[count] = None

    return tracklist


def search_pairs(tracklist_dict):
    """Принимает словарь с треклистом, проверяет наличие (input_track)
    Возвращает пары треков after and before"""
    pairs = {}
    input_track_id = tracklist_dict["input_track"]
    if input_track_id is not None:

        before_id = input_track_id - 1
        after_id = input_track_id + 1

        before = tracklist_dict.get(before_id)
        if before:
            pairs["before"] = before

        after = tracklist_dict.get(after_id)
        if after:
            pairs["after"] = after

    return pairs


def process_mix_list(mix_list):
    """
    Принимает список словарей с миксами, передаёт ссылки в другую функцию,
    получает словари с треклистами, сохраняет их в список и возвращает этот список.
    """
    before_tracks = []
    after_tracks = []
    parse_count = 0
    for mix in mix_list:
        if parse_count > PARCE_MIX_COUNT_LIMIT:
            logger.info(
                "Количество спарсенных миксов(PARCE_MIX_COUNT_LIMIT): %s", parse_count
            )
            break

        html = fetch_page(mix["url"])
        tracklist = parse_tracklist(html)
        mix["tracklist"] = tracklist
        pairs = search_pairs(tracklist)
        mix["pairs"] = pairs
        before_tracks.append(pairs.get("before"))
        after_tracks.append(pairs.get("after"))
        parse_count += 1

    save_to_json(mix_list, "mixes")
    return [before_tracks, after_tracks]
