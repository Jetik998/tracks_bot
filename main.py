import logging
from logger_config import setup_logger
import logic
from logic import pairs_to_string

setup_logger()

logger = logging.getLogger(__name__)


def search_track_name(track_name):
    search_tracks = logic.search_url_input_track(track_name)
    if search_tracks["found"]:
        response = main_flow(search_tracks["url"])
        return {"found": True, "response": response}
    else:
        return {"found": False, "response": search_tracks["tracks"]}


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
