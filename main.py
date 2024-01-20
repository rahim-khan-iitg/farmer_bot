from src.utils import main
import argparse
from src.logger import logging
from src.Bhashini.bhashini_config import update_inference_key

if __name__=="__main__":
    parser=argparse.ArgumentParser("this is farmers bot")
    parser.add_argument(
        "--model",
        choices=['gemini','mixtral'],
        default='gemini',
        help="gemini works for all languages and mixtral only works for english language"
        )
    args=parser.parse_args()
    logging.info("updating the bhashini inference api key")
    update_inference_key()
    logging.info(f"bot started with {args.model}")
    main(args.model)

    