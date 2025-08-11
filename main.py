import logging
from logger_config import setup_logger
import logic

setup_logger()

logger = logging.getLogger(__name__)


def main_flow():
    url = logic.search_url_input_track()
    html = logic.fetch_page(url)
    mixes = logic.search_mixes_on_page(html)
    logic.process_mix_list(mixes)


if __name__ == "__main__":
    main_flow()
