from importlib.metadata import packages_distributions, version


def dist_version(anchor: str, default: str = "unknown") -> str:
    try:
        top = anchor.split(".", 1)[0]
        dist = (packages_distributions().get(top) or [top])[0]
        return version(dist)
    except Exception:
        return default
