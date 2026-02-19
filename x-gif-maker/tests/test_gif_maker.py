#!/usr/bin/env python3
"""
Tests for x-gif-maker skill.
"""

import pytest
import os
import sys
import json
import tempfile
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.create_gif import GifMaker


class TestGifMakerBasics:
    """Test basic GifMaker functionality."""

    def test_initialization(self):
        """Test GifMaker initialization with defaults."""
        maker = GifMaker()
        assert maker.width == 640
        assert maker.height == 360
        assert maker.fps == 30
        assert maker.font_size == 36

    def test_initialization_custom(self):
        """Test GifMaker initialization with custom values."""
        maker = GifMaker(width=1280, height=720, fps=60, duration=3)
        assert maker.width == 1280
        assert maker.height == 720
        assert maker.fps == 60
        assert maker.total_frames == 180

    def test_hex_to_rgb(self):
        """Test hex color conversion."""
        maker = GifMaker()
        assert maker._hex_to_rgb("#ff0000") == (255, 0, 0)
        assert maker._hex_to_rgb("#00ff00") == (0, 255, 0)
        assert maker._hex_to_rgb("#0000ff") == (0, 0, 255)
        assert maker._hex_to_rgb("#fff") == (255, 255, 255)
        assert maker._hex_to_rgb("ffffff") == (255, 255, 255)

    def test_default_colors(self):
        """Test default color palette."""
        maker = GifMaker()
        colors = maker.default_colors()
        assert len(colors) == 3
        assert colors[0] == "#667eea"
        assert colors[1] == "#764ba2"
        assert colors[2] == "#f64f59"


class TestGradientBackground:
    """Test gradient background generation."""

    def test_single_color_gradient(self):
        """Test gradient with single color."""
        maker = GifMaker()
        bg = maker.create_gradient_background(["#ff0000"])
        assert bg.size == (640, 360)
        assert bg.mode == "RGB"

    def test_two_color_gradient(self):
        """Test gradient with two colors."""
        maker = GifMaker()
        bg = maker.create_gradient_background(["#ff0000", "#0000ff"])
        assert bg.size == (640, 360)
        assert bg.mode == "RGB"

    def test_three_color_gradient(self):
        """Test gradient with three colors."""
        maker = GifMaker()
        bg = maker.create_gradient_background(["#ff0000", "#00ff00", "#0000ff"])
        assert bg.size == (640, 360)
        assert bg.mode == "RGB"


class TestAnimationStyles:
    """Test animation style parameters."""

    def test_fade_style(self):
        """Test fade animation parameters."""
        maker = GifMaker()
        alpha, offset_y, offset_x, scale, glow, glitch = maker._get_animation_params("fade", 0.5)
        assert alpha == 1.0
        assert offset_y == 0
        assert scale == 1.0

        alpha, *_ = maker._get_animation_params("fade", 0.25)
        assert alpha == 0.5

    def test_pulse_style(self):
        """Test pulse animation parameters."""
        maker = GifMaker()
        _, _, _, _, glow, _ = maker._get_animation_params("pulse", 0.5)
        assert glow >= 0

    def test_slide_up_style(self):
        """Test slide_up animation parameters."""
        maker = GifMaker()
        alpha, offset_y, *_ = maker._get_animation_params("slide_up", 0.25)
        assert alpha < 1.0
        assert offset_y > 0

    def test_slide_down_style(self):
        """Test slide_down animation parameters."""
        maker = GifMaker()
        alpha, offset_y, *_ = maker._get_animation_params("slide_down", 0.25)
        assert alpha < 1.0
        assert offset_y < 0

    def test_bounce_style(self):
        """Test bounce animation parameters."""
        maker = GifMaker()
        alpha, offset_y, *_ = maker._get_animation_params("bounce", 0.5)
        assert 0 <= alpha <= 1
        # Bounce can have various offsets, test at middle point
        alpha, offset_y, *_ = maker._get_animation_params("bounce", 0.25)
        assert 0 <= alpha <= 1
        # At start, should have offset
        _, offset_y_start, *_ = maker._get_animation_params("bounce", 0.0)
        assert offset_y_start > 0 or offset_y_start < 0  # Should have initial offset

    def test_glow_style(self):
        """Test glow animation parameters."""
        maker = GifMaker()
        _, _, _, _, glow, _ = maker._get_animation_params("glow", 0.8)
        assert glow > 0

    def test_shake_style(self):
        """Test shake animation parameters."""
        maker = GifMaker()
        _, _, offset_x, *_ = maker._get_animation_params("shake", 0.75)
        # shake can have random offset
        assert isinstance(offset_x, int)

    def test_zoom_style(self):
        """Test zoom animation parameters."""
        maker = GifMaker()
        # Return order: (alpha, offset_y, offset_x, scale, glow_intensity, glitch_amount)
        # At middle of animation
        alpha, _, _, scale, _, _ = maker._get_animation_params("zoom", 0.5)
        assert scale >= 0.5
        assert scale <= 1.0
        assert alpha >= 0
        # At start, should be smaller
        alpha_start, _, _, scale_start, _, _ = maker._get_animation_params("zoom", 0.0)
        assert scale_start == 0.5
        assert alpha_start == 0
        # At end, should be full size
        alpha_end, _, _, scale_end, _, _ = maker._get_animation_params("zoom", 1.0)
        assert scale_end == 1.0
        assert alpha_end == 1.0

    def test_wave_style(self):
        """Test wave animation parameters."""
        maker = GifMaker()
        alpha, offset_y, *_ = maker._get_animation_params("wave", 0.5)
        assert alpha <= 1.0
        # wave oscillates
        assert isinstance(offset_y, int)

    def test_glitch_style(self):
        """Test glitch animation parameters."""
        maker = GifMaker()
        _, _, _, _, _, glitch = maker._get_animation_params("glitch", 0.5)
        # glitch only active in middle
        assert isinstance(glitch, int)


class TestGifCreation:
    """Test GIF creation functionality."""

    def test_create_simple_gif(self, tmp_path):
        """Test creating a simple GIF."""
        maker = GifMaker(width=320, height=180, duration=1, fps=10)
        output_path = str(tmp_path / "test.gif")

        maker.create_text_gif(
            text="Test",
            output_path=output_path,
            style="fade"
        )

        assert os.path.exists(output_path)
        file_size = os.path.getsize(output_path)
        assert file_size > 0

    def test_create_gif_with_signature(self, tmp_path):
        """Test creating a GIF with signature."""
        maker = GifMaker(width=320, height=180, duration=1, fps=10)
        output_path = str(tmp_path / "test_sig.gif")

        maker.create_text_gif(
            text="Test",
            output_path=output_path,
            style="fade",
            signature="@test"
        )

        assert os.path.exists(output_path)

    def test_create_all_styles(self, tmp_path):
        """Test creating GIFs with all animation styles."""
        styles = ["fade", "pulse", "slide_up", "slide_down", "bounce",
                  "glow", "shake", "typewriter", "zoom", "wave", "glitch"]

        maker = GifMaker(width=320, height=180, duration=1, fps=10)

        for style in styles:
            output_path = str(tmp_path / f"test_{style}.gif")
            maker.create_text_gif(
                text=style,
                output_path=output_path,
                style=style
            )
            assert os.path.exists(output_path), f"Failed for style: {style}"

    def test_custom_colors(self, tmp_path):
        """Test creating GIF with custom colors."""
        maker = GifMaker(width=320, height=180, duration=1, fps=10)
        output_path = str(tmp_path / "test_custom.gif")

        maker.create_text_gif(
            text="Custom Colors",
            output_path=output_path,
            bg_colors=["#000000", "#ffffff"],
            text_color="#ff0000"
        )

        assert os.path.exists(output_path)

    def test_multi_line_text(self, tmp_path):
        """Test creating GIF with multi-line text."""
        maker = GifMaker(width=320, height=180, duration=1, fps=10)
        output_path = str(tmp_path / "test_multiline.gif")

        maker.create_text_gif(
            text="Line 1\nLine 2\nLine 3",
            output_path=output_path,
            style="fade"
        )

        assert os.path.exists(output_path)

    def test_long_text_wrapping(self, tmp_path):
        """Test that long text is wrapped properly."""
        maker = GifMaker(width=320, height=180, duration=1, fps=10)
        output_path = str(tmp_path / "test_wrap.gif")

        long_text = "This is a very long text that should be wrapped across multiple lines to fit within the specified width"
        maker.create_text_gif(
            text=long_text,
            output_path=output_path,
            style="fade"
        )

        assert os.path.exists(output_path)


class TestMP4Export:
    """Test MP4 export functionality."""

    @pytest.mark.skipif(
        sys.version_info < (3, 8),
        reason="imageio requires Python 3.8+"
    )
    def test_export_mp4(self, tmp_path):
        """Test exporting to MP4 format."""
        try:
            import imageio
        except ImportError:
            pytest.skip("imageio not installed")

        maker = GifMaker(width=320, height=180, duration=1, fps=10)
        gif_path = str(tmp_path / "test.gif")
        mp4_path = str(tmp_path / "test.mp4")

        # Create GIF first
        maker.create_text_gif(
            text="Test MP4",
            output_path=gif_path,
            style="fade"
        )

        # Export MP4
        maker.export_mp4(mp4_path)

        assert os.path.exists(mp4_path)
        file_size = os.path.getsize(mp4_path)
        assert file_size > 0


class TestBatchCreation:
    """Test batch GIF creation."""

    def test_batch_creation(self, tmp_path):
        """Test creating multiple GIFs from batch data."""
        posts = [
            {"text": "First", "output": "first.gif", "style": "fade"},
            {"text": "Second", "output": "second.gif", "style": "pulse"},
            {"text": "Third", "output": "third.gif", "style": "bounce"},
        ]

        maker = GifMaker(width=320, height=180, duration=1, fps=10)
        results = maker.create_batch(posts, output_dir=str(tmp_path))

        assert len(results) == 3
        for result in results:
            assert os.path.exists(result)


class TestUpload:
    """Test upload functionality (mocked)."""

    def test_upload_nonexistent_file(self):
        """Test uploading a non-existent file raises error."""
        maker = GifMaker()
        with pytest.raises(FileNotFoundError):
            maker.upload_to_catbox("/nonexistent/path.gif")


class TestCLI:
    """Test CLI interface."""

    def test_cli_help(self, monkeypatch):
        """Test CLI help output."""
        monkeypatch.setattr("sys.argv", ["create_gif.py", "--help"])
        with pytest.raises(SystemExit):
            from scripts.create_gif import main
            main()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
