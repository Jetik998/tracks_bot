import logging
from logger_config import setup_logger
import logic


setup_logger()

logger = logging.getLogger(__name__)

def main_flow():
    url = logic.search_url_input_track()
    html = logic.load_page_input_track(url)





if __name__ == "__main__":
