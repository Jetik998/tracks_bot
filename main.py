import logging
from logger_config import setup_logger
import logic
from logic import pairs_to_string

setup_logger()

logger = logging.getLogger(__name__)


def search_track_name(track_name):
    search_tracks = logic.search_url_input_track(track_name)
    if search_tracks["found"]:
        results = main_flow(search_tracks["url"])
        logger.info("Словарь похожих треков: %s", results)
        return {"found": True, "response": results}

    else:
        tracks_dict = search_tracks["tracks"]
        logger.info("Словарь похожих треков: %s", tracks_dict)
        return {"found": False, "response": tracks_dict}


def main_flow(url):
    html = logic.fetch_page(url)
    mixes = logic.search_mixes_on_page(html)
    pairs_list = logic.process_mix_list(mixes)
    response = pairs_to_string(pairs_list)
    return response


if __name__ == "__main__":
    test_track = ""
    if test_track:
        result = search_track_name(test_track)
        print(result)
