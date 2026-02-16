def normalize_class_distribution_dict(
    class_dist: Mapping[str, int]
) -> dict[str, float]:
    """
    Normalize a class distribution dictionary to percentages and different names.
    Finaly order the classes by percentage in descending order.

    Args:
        class_dist (dict[str, int]): A dictionary with class names as keys and counts as values.

    Returns:
        dict[str, int]: A dictionary with class names as keys and normalized percentages as values.
    """
    log.debug("Normalizing class distribution: %s", class_dist)

    # Work on a fresh mutable copy with integer counts
    counts: dict[str, int] = {k: int(v) for k, v in class_dist.items()}

    # Normalize names by folding counts into canonical names
    for source, target in [
        ("NRPS", "NRP"),
        ("PKS", "Polyketide"),
        ("other", "Other"),
        ("ribosomal", "RiPP"),
        ("saccharide", "Saccharide"),
        ("terpene", "Terpene"),
        ("alkaloid", "Alkaloid"),
    ]:
        if counts.get(source, 0):
            counts[target] = counts.get(target, 0) + counts.pop(source, 0)

        # remove empty entries
        if counts.get(target, 0) == 0:
            counts.pop(target, None)

    total_count = sum(counts.values())

    # Produce normalized percentages in a separate dict[str, float]
    if total_count > 0:
        percents: dict[str, float] = {
            k: round(v / total_count * 100, 1) for k, v in counts.items()
        }
    else:
        percents = {k: 0.0 for k in counts.keys()}

    # Return sorted by percentage (descending)
    return dict(sorted(percents.items(), key=lambda item: item[1], reverse=True))

def normalize_classes_list(class_names):
    return [x for x,y in normalize_class_distribution_dict(
                {name: 1 for name in class_names}
            )]