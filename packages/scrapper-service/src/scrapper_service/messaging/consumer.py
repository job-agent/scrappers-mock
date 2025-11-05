"""RabbitMQ consumer for processing scrape job requests."""

import json
import logging
from datetime import datetime
from typing import Optional

import pika
from job_scrapper_contracts import ScrapeJobsRequest, ScrapeJobsResponse

from scrapper_service.manager import ScrapperManager
from scrapper_service.messaging.connection import RabbitMQConnection


class ScrapperConsumer:
    """RabbitMQ consumer that processes scrape job requests.

    Listens to the job.scrape.request queue and processes messages
    by calling ScrapperManager to scrape jobs, then sends responses
    back to the reply_to queue.
    """

    QUEUE_NAME = "job.scrape.request"

    def __init__(
        self,
        scrapper_manager: Optional[ScrapperManager] = None,
        rabbitmq_url: Optional[str] = None,
    ):
        """Initialize the consumer.

        Args:
            scrapper_manager: ScrapperManager instance for scraping jobs
            rabbitmq_url: RabbitMQ connection URL
        """
        self.scrapper_manager = scrapper_manager or ScrapperManager()
        self.rabbitmq_connection = RabbitMQConnection(rabbitmq_url)
        self.logger = logging.getLogger(__name__)

    def start(self) -> None:
        """Start consuming messages from the queue.

        This method blocks indefinitely and processes messages as they arrive.
        """
        channel = self.rabbitmq_connection.connect()

        # Declare the queue (idempotent operation)
        channel.queue_declare(queue=self.QUEUE_NAME, durable=True)

        # Set QoS to process one message at a time
        channel.basic_qos(prefetch_count=1)

        # Start consuming
        channel.basic_consume(
            queue=self.QUEUE_NAME, on_message_callback=self._on_message
        )

        self.logger.info(f"Started consuming from {self.QUEUE_NAME}")
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            self.logger.info("Stopping consumer...")
            channel.stop_consuming()
        finally:
            self.rabbitmq_connection.close()

    def _on_message(
        self,
        channel: pika.channel.Channel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes,
    ) -> None:
        """Callback for processing incoming messages.

        Args:
            channel: Pika channel
            method: Delivery method
            properties: Message properties
            body: Message body
        """
        correlation_id = properties.correlation_id
        reply_to = properties.reply_to

        self.logger.info(
            f"Received message with correlation_id={correlation_id}, reply_to={reply_to}"
        )

        try:
            # Parse request
            request_data = json.loads(body.decode("utf-8"))
            request = ScrapeJobsRequest(**request_data)

            # Process request
            response = self._process_request(request)

            # Send response
            if reply_to:
                self._send_response(channel, reply_to, correlation_id, response)

            # Acknowledge message
            channel.basic_ack(delivery_tag=method.delivery_tag)
            self.logger.info(f"Successfully processed message {correlation_id}")

        except Exception as e:
            self.logger.error(f"Error processing message: {e}", exc_info=True)

            # Send error response
            error_response: ScrapeJobsResponse = {
                "jobs": [],
                "success": False,
                "error": str(e),
                "jobs_count": 0,
            }

            if reply_to:
                self._send_response(channel, reply_to, correlation_id, error_response)

            # Acknowledge message even on error (to avoid reprocessing)
            # In production, you might want to use a dead-letter queue instead
            channel.basic_ack(delivery_tag=method.delivery_tag)

    def _process_request(self, request: ScrapeJobsRequest) -> ScrapeJobsResponse:
        """Process a scrape jobs request.

        Args:
            request: Scrape jobs request

        Returns:
            ScrapeJobsResponse: Response with scraped jobs or error
        """
        # Convert ISO format string to datetime if present
        posted_after = None
        if request.get("posted_after"):
            posted_after = datetime.fromisoformat(request["posted_after"])

        # Call scrapper manager
        jobs = self.scrapper_manager.scrape_jobs_as_dicts(
            salary=request.get("salary", 4000),
            employment=request.get("employment", "remote"),
            posted_after=posted_after,
            timeout=request.get("timeout", 30),
        )

        # Build response
        response: ScrapeJobsResponse = {
            "jobs": jobs,
            "success": True,
            "error": None,
            "jobs_count": len(jobs),
        }

        return response

    def _send_response(
        self,
        channel: pika.channel.Channel,
        reply_to: str,
        correlation_id: str,
        response: ScrapeJobsResponse,
    ) -> None:
        """Send response to the reply queue.

        Args:
            channel: Pika channel
            reply_to: Reply queue name
            correlation_id: Correlation ID for matching request/response
            response: Response to send
        """
        channel.basic_publish(
            exchange="",
            routing_key=reply_to,
            properties=pika.BasicProperties(
                correlation_id=correlation_id,
                content_type="application/json",
            ),
            body=json.dumps(response).encode("utf-8"),
        )

        self.logger.info(f"Sent response to {reply_to} with correlation_id={correlation_id}")
