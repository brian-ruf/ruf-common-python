stats = {}

# -----------------------------------------------------------------------------
def increment_stat(stat_name: str, increment: int = 1) -> None:
    """Increment a statistic value."""
    global stats

    if stat_name in stats:
        stats[stat_name] += increment
    else:
        stats[stat_name] = increment

def get_stat(stat_name: str) -> int:
    """Retrieve the value of a statistic."""
    global stats

    return stats.get(stat_name, 0)

# -----------------------------------------------------------------------------
def stats_summary(heading: str = "Summary") -> str:
    global stats
    content = ""

    if heading:
        content += f"\n\{heading}:\n"
    else:
        content += "\n\n"

    for stat in stats:
        content += (f"  {stat}: {stats[stat]}")

    return content
# -----------------------------------------------------------------------------

# =============================================================================
#  --- MAIN: Only runs if the module is executed stand-alone. ---
# =============================================================================
if __name__ == '__main__':
    print("Stats Module. Not intended to be run as a stand-alone file.")
