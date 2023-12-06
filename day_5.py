from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class Range:

    dst_start: int
    src_start: int
    length: int

    def inside(self, x: int) -> bool:
        return self.src_start <= x < self.src_start + self.length

    def __call__(self, x: int) -> int:
        offset = x - self.src_start
        return self.dst_start + offset


@dataclass
class Map:

    ranges: List[Range]

    def __call__(self, x: int) -> int:
        for r in self.ranges:
            if r.inside(x):
                return r(x)

        return x


def read() -> Tuple[List[int], List[Map]]:
    with open("input.txt") as file:
        lines = [x.strip() for x in file.readlines()]

        seeds = lines[0].split(": ")[1]
        seeds = list(map(int, seeds.split(" ")))

        idx = 2
        maps = []

        while idx < len(lines):
            assert "map" in lines[idx]
            idx += 1
            ranges = []

            while idx < len(lines) and lines[idx]:
                dst_start, src_start, length = map(int, lines[idx].split(" "))
                ranges.append(Range(dst_start, src_start, length))
                idx += 1

            maps.append(Map(ranges))
            idx += 1

        return seeds, maps


def apply_maps_to_seeds(seeds: List[int], maps: List[Map]) -> int:
    locations = []

    for s in seeds:
        for map_ in maps:
            s = map_(s)

        locations.append(s)

    return min(locations)


def apply_maps_to_seed_ranges(seeds: List[int], maps: List[Map]) -> int:
    locations = []
    from tqdm import tqdm

    for i in range(0, len(seeds), 2):
        print(f"{i}/{len(seeds)}")
        start = seeds[i]
        length = seeds[i+1]
        for s in tqdm(range(start, start + length)):
            for map_ in maps:
                s = map_(s)

            locations.append(s)

    return min(locations)


def fuse_maps(maps: List[Map]) -> Map:
    """Fuse the stack of maps into a single map."""


def fuse(idx: int, maps: List[Map]) -> List[Range]:
    if idx == len(maps) - 1:  # Basecase
        return maps[idx].ranges

    fused_ranges = []
    fused_ranges_prior = fuse(idx + 1, maps)

    for r1 in maps[idx].ranges:
        for r2 in fused_ranges_prior:
            # Check if ranges are disjoint
            # If so, no need to do anything
            if r1.dst_start + r1.length <= r2.src_start or r2.src_start + r2.length <= r1.dst_start:
                continue

            if r1.dst_start + r1.length > r2.src_start and 



def main():
    seeds, maps = read()
    print(f"First: {apply_maps_to_seeds(seeds, maps)}")
    print(f"Second: {apply_maps_to_seed_ranges(seeds, maps)}")


if __name__ == "__main__":
    main()
