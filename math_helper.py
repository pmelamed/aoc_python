from typing import Optional


def progression_sum[ T: Optional[ int ] ]( first: T = None, last: T = None, delta: T = None, count: int = None ) -> int:
    if first is None: first = last - delta * (count - 1)
    if last is None: last = first + delta * (count - 1)
    if count is None: count = (last - first) // delta + 1
    return (first + last) * count // 2
