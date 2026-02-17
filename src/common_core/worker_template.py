from __future__ import annotations

import argparse
import logging

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

from common_core.versioning import dist_version
from common_core.config_loader import LoaderOptions, load_settings
from common_core.logging_setup import LoggingConfig, setup_logging

log = logging.getLogger(__name__)


class ExampleDbConfig(BaseModel):
    bucket: str
    prefix: str = ""


class WorkerASettings(BaseSettings):
    job_name: str = "worker-example"
    exampledb: ExampleDbConfig

    api_token: str = Field(repr=False)

    logging: LoggingConfig = Field(default_factory=LoggingConfig)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--config", help="Path to YAML config for this job")
    p.add_argument("--job-name")
    p.add_argument("--exampledb-bucket")
    p.add_argument("--exampledb-prefix")
    p.add_argument("--log-level")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    cli_overrides = {}
    if args.job_name:
        cli_overrides["job_name"] = args.job_name
    if args.exampledb_bucket:
        cli_overrides.setdefault("exampledb", {})["bucket"] = args.exampledb_bucket
    if args.exampledb_prefix:
        cli_overrides.setdefault("exampledb", {})["prefix"] = args.exampledb_prefix
    if args.log_level:
        cli_overrides.setdefault("logging", {})["level"] = args.log_level

    cfg = load_settings(
        WorkerASettings,
        yaml_path=args.config,
        cli_overrides=cli_overrides,
        options=LoaderOptions(env_prefix="WORKERA_"),
    )

    setup_logging(cfg.logging)

    pkg_version = dist_version(__name__)
    log.info("running %s version %s", cfg.job_name, pkg_version)
    log.info("config: %s", cfg.dict(exclude={"api_token"}))

    # Worker logic here...


if __name__ == "__main__":
    main()
