import datetime
import logging
import os
import sys
import time
import zoneinfo
from functools import reduce
from operator import attrgetter

import yaml
from prometheus_client import CollectorRegistry, start_http_server

import modules.prometheus as prom
from modules.oura import Oura


def safe_getattr(obj, attr_path, default=None):
    """
    Safely get nested attributes, returning default if any intermediate object is None.

    Args:
        obj: The object to extract attributes from
        attr_path: Dot-separated string of attribute names (e.g., "spo2_percentage.average")
        default: Default value to return if path cannot be resolved

    Returns:
        The final attribute value or default if path is broken
    """
    try:
        # Split the path and navigate through attributes
        for attr in attr_path.split("."):
            if obj is None:
                return default
            obj = getattr(obj, attr)
        return obj if obj is not None else default
    except AttributeError:
        return default


ORIGIN_TZ = zoneinfo.ZoneInfo(os.environ.get("TZ", "UTC"))
OURA_ACCESS_TOKEN = os.environ.get("OURA_ACCESS_TOKEN", None)
HTTP_PORT = os.environ.get("PORT", 8000)
LOGLEVEL = os.environ.get("LOGLEVEL", logging.INFO)
CONF_FILE = "config/metrics.yml"

if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=LOGLEVEL,
        format="%(asctime)s - %(levelname)s : %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )

    metrics_definitions = prom.load_oura_metrics_configs(CONF_FILE)

    registry = CollectorRegistry()
    start_http_server(int(HTTP_PORT), registry=registry)

    if OURA_ACCESS_TOKEN == None:
        logging.fatal("OURA_ACCESS_TOKEN env is not defined. Please set it!")
        sys.exit(1)

    oura = Oura(personal_access_token=OURA_ACCESS_TOKEN)

    personal_info = oura.get_personal_info()

    if personal_info == None:
        logging.fatal("OURA_ACCESS_TOKEN is not usable. Please check it!")
        sys.exit(1)

    labels = [personal_info.email]

    root_metrics = {}

    while True:
        now = datetime.datetime.now(ORIGIN_TZ)
        today = now.date()
        days_ago = now - datetime.timedelta(days=7)
        start_date = days_ago.date()

        for category in metrics_definitions.categories:
            logging.debug(f"gathering {category.name} data...")

            if not category.name in root_metrics:
                root_metrics[category.name] = {}

            if category.name == "daily_activity":
                metrics = oura.get_daily_activity(start_date, today)
            elif category.name == "daily_readiness":
                metrics = oura.get_daily_readiness(start_date, today)
            elif category.name == "daily_resilience":
                metrics = oura.get_daily_resilience(start_date, today)
            elif category.name == "daily_sleep":
                metrics = oura.get_daily_sleep(start_date, today)
            elif category.name == "daily_spo2":
                metrics = oura.get_daily_spo2(start_date, today)
            elif category.name == "daily_stress":
                metrics = oura.get_daily_stress(start_date, today)
            elif category.name == "heartrate":
                # For heart rate, use a 24-hour window
                metrics = oura.get_heartrate(now - datetime.timedelta(days=1), now)
            elif category.name == "personal_info":
                metrics = oura.get_personal_info()
            elif category.name == "rest_mode_period":
                # For rest mode periods, use a 24-hour window
                metrics = oura.get_rest_mode_periods(
                    now - datetime.timedelta(days=1), now
                )
            elif category.name == "ring_configuration":
                metrics = oura.get_ring_configuration()
            elif category.name == "session":
                # For sessions, use a 24-hour window
                metrics = oura.get_sessions(now - datetime.timedelta(days=1), now)
            elif category.name == "sleep":
                # For detailed sleep data, use a 24-hour window
                metrics = oura.get_sleeps(now - datetime.timedelta(days=1), now)
            elif category.name == "sleep_time":
                metrics = oura.get_sleep_times(start_date, today)
            elif category.name == "vo2_max":
                metrics = oura.get_vo2_maxes(start_date, today)
            elif category.name == "workout":
                # For workouts, use a 24-hour window
                metrics = oura.get_workouts(now - datetime.timedelta(days=1), now)
            elif category.name == "enhanced_tag":
                # For enhanced tags, use a 24-hour window
                metrics = oura.get_enhanced_tags(now - datetime.timedelta(days=1), now)

            if metrics == None:
                logging.warning(f"getting {category.name} process was failed.")
                continue
            elif category.name != "personal_info" and len(metrics.data) == 0:
                logging.warning(
                    f"{category.name} data was not found for date range {start_date} to {today}."
                )
                continue

            if category.name != "personal_info":
                latest_metrics = metrics.data[-1]
                if category.name == "heartrate":
                    logging.info(
                        f"Found {len(metrics.data)} {category.name} entries, using latest from {latest_metrics.timestamp}"
                    )
                elif category.name == "ring_configuration":
                    logging.info(
                        f"Found {len(metrics.data)} {category.name} entries, using latest from {latest_metrics.timestamp or 'N/A'}"
                    )
                else:
                    logging.info(
                        f"Found {len(metrics.data)} {category.name} entries, using latest from {latest_metrics.day}"
                    )
            else:
                latest_metrics = metrics

            for m in category.metrics:
                iterator = m.iterator if m.iterator != None else m.name
                try:
                    # Use safe_getattr for nested attributes that might contain None values
                    if "." in iterator:
                        value = safe_getattr(latest_metrics, iterator)
                    else:
                        value = getattr(latest_metrics, iterator)

                    # Skip metrics with None values (they will be logged as debug)
                    if value is None:
                        logging.debug(
                            f"{category.prefix}{m.name}: None value, skipping"
                        )
                        continue

                    logging.debug(f"{category.prefix}{m.name}: {value}")
                    if not m.name in root_metrics[category.name]:
                        root_metrics[category.name][m.name] = (
                            prom.create_metric_instance(m, registry, category.prefix)
                        )
                    prom.set_metrics(root_metrics[category.name][m.name], labels, value)
                except Exception as e:
                    logging.error(f"Error processing metric {m.name}: {e}")
                    continue
            logging.info(f"gathering {category.name} metrics successful.")

        logging.info("gathering all metrics successful.")
        time.sleep(60)
