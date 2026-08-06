#!/usr/bin/env python3
"""Tests for the overlap geometry logic (pure, no GTK needed).

Run from the release root:
    python3 -m unittest discover -s tests -t .
"""
import os
import sys
import random
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mydisplays_geom as geom


def mon(name, width, height, scale, x, y):
    return {"name": name, "width": width, "height": height, "scale": scale, "x": x, "y": y}


def assert_no_overlap(testcase, monitors):
    for i, a in enumerate(monitors):
        for b in monitors[i + 1:]:
            testcase.assertFalse(
                geom.rects_overlap(geom.monitor_rect(a), geom.monitor_rect(b)),
                f"overlap between {a['name']} and {b['name']}",
            )


class TestRectsOverlap(unittest.TestCase):
    def test_separate_rects_no_overlap(self):
        a = (0, 0, 100, 100)
        b = (200, 0, 100, 100)
        self.assertFalse(geom.rects_overlap(a, b))

    def test_touching_edges_is_not_overlap(self):
        a = (0, 0, 100, 100)
        b = (100, 0, 100, 100)
        self.assertFalse(geom.rects_overlap(a, b))

    def test_overlapping_rects(self):
        a = (0, 0, 100, 100)
        b = (50, 50, 100, 100)
        self.assertTrue(geom.rects_overlap(a, b))


class TestClampPosition(unittest.TestCase):
    def setUp(self):
        # Two monitors side by side; eDP 2880x1800@1.67, HDMI 3840x2160@1.0
        self.m1 = mon("eDP-1", 2880, 1800, 1.67, 0, 0)
        self.m2 = mon("HDMI-A-2", 3840, 2160, 1.0, 1725, 0)

    def test_no_overlap_position_is_kept(self):
        x, y = geom.clamp_position([self.m1, self.m2], self.m2, 2000, 0)
        self.assertEqual((x, y), (2000, 0))

    def test_single_drag_into_overlap_is_pushed(self):
        # HDMI dragged on top of eDP-1
        x, y = geom.clamp_position([self.m1, self.m2], self.m2, 0, 0)
        rect = (x, y, self.m2["width"] / self.m2["scale"], self.m2["height"] / self.m2["scale"])
        self.assertFalse(geom.rects_overlap(rect, geom.monitor_rect(self.m1)))
        # result must be an integer position
        self.assertIsInstance(x, int)
        self.assertIsInstance(y, int)

    def test_diagonal_overlap_is_pushed(self):
        # HDMI partially overlapping eDP-1 corner
        x, y = geom.clamp_position([self.m1, self.m2], self.m2, 1200, 800)
        rect = (x, y, self.m2["width"] / self.m2["scale"], self.m2["height"] / self.m2["scale"])
        self.assertFalse(geom.rects_overlap(rect, geom.monitor_rect(self.m1)))

    def test_three_monitor_cluster_converges(self):
        # eDP in the middle, HDMI left and right both overlapping it
        left = mon("A", 1920, 1080, 1.0, -300, 0)
        center = self.m1
        right = mon("C", 1920, 1080, 1.0, 1000, 0)
        monitors = [left, center, right]
        # drag center over both neighbors
        x, y = geom.clamp_position(monitors, center, 0, 0)
        rect = (x, y, center["width"] / center["scale"], center["height"] / center["scale"])
        self.assertFalse(geom.rects_overlap(rect, geom.monitor_rect(left)))
        self.assertFalse(geom.rects_overlap(rect, geom.monitor_rect(right)))

    def test_grid_of_four_monitors_converges(self):
        m1 = mon("1", 1920, 1080, 1.0, 0, 0)
        m2 = mon("2", 1920, 1080, 1.0, 1920, 0)
        m3 = mon("3", 1920, 1080, 1.0, 0, 1080)
        m4 = mon("4", 1920, 1080, 1.0, 1920, 1080)
        monitors = [m1, m2, m3, m4]
        x, y = geom.clamp_position(monitors, m1, 1500, 900)
        rect = (x, y, m1["width"] / m1["scale"], m1["height"] / m1["scale"])
        self.assertFalse(geom.rect_overlaps_any(rect, [m2, m3, m4]))

    def test_random_5_monitor_fuzz(self):
        rng = random.Random(42)
        for trial in range(50):
            monitors = [mon(f"M{i}", rng.randint(800, 4000), rng.randint(600, 3000),
                             rng.choice([1.0, 1.25, 1.5, 1.67, 2.0]),
                             rng.randint(-2000, 2000), rng.randint(-1000, 1000)) for i in range(5)]
            victim = monitors[0]
            tx = rng.randint(-2000, 2000)
            ty = rng.randint(-1000, 1000)
            x, y = geom.clamp_position(monitors, victim, tx, ty)
            rect = (x, y, victim["width"] / victim["scale"], victim["height"] / victim["scale"])
            for other in monitors[1:]:
                self.assertFalse(
                    geom.rects_overlap(rect, geom.monitor_rect(other)),
                    f"trial {trial}: clamp left overlap with {other['name']}",
                )


class TestSnapMonitors(unittest.TestCase):
    def test_resolves_overlap_created_by_resize(self):
        m1 = mon("1", 1920, 1080, 1.0, 0, 0)
        m2 = mon("2", 1920, 1080, 1.0, 1900, 0)
        monitors = [m1, m2]
        geom.snap_monitors(monitors)
        assert_no_overlap(self, monitors)

    def test_does_not_move_non_overlapping(self):
        m1 = mon("1", 1920, 1080, 1.0, 0, 0)
        m2 = mon("2", 1920, 1080, 1.0, 1920, 0)
        monitors = [m1, m2]
        geom.snap_monitors(monitors)
        self.assertEqual((m1["x"], m1["y"]), (0, 0))
        self.assertEqual((m2["x"], m2["y"]), (1920, 0))

    def test_resolves_three_way_overlap(self):
        m1 = mon("1", 1920, 1080, 1.0, 0, 0)
        m2 = mon("2", 1920, 1080, 1.0, 100, 100)
        m3 = mon("3", 1920, 1080, 1.0, 200, 200)
        monitors = [m1, m2, m3]
        geom.snap_monitors(monitors)
        assert_no_overlap(self, monitors)


if __name__ == "__main__":
    unittest.main()
