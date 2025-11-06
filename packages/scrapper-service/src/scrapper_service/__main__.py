"""Entry point for running scrapper-service-mock as a standalone application."""

import argparse
import logging
import sys

from dotenv import load_dotenv

from scrapper_messaging.consumer import ScrapperConsumer
from scrapper_service.manager import ScrapperManager


def setup_logging(log_level: str = "INFO") -> None:
    """Configure logging for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def main() -> None:
    """Main entry point for scrapper-service-mock."""
    load_dotenv()
    parser = argparse.ArgumentParser(description="Scrapper Service Mock - RabbitMQ Consumer")
    parser.add_argument(
        "--rabbitmq-url",
        type=str,
        default=None,
        help="RabbitMQ connection URL (default: from RABBITMQ_URL env var)",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level (default: INFO)",
    )

    args = parser.parse_args()

    setup_logging(args.log_level)

    logger = logging.getLogger(__name__)
    logger.info("Starting Scrapper Service Mock...")

    try:
        service = ScrapperManager()
        consumer = ScrapperConsumer(service=service, rabbitmq_url=args.rabbitmq_url)
        consumer.start()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
