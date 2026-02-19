#!/usr/bin/env python3
"""
X GIF Maker - Slideshow Mode
Create multi-headline slideshow GIFs for 30-second social media content.
"""

from PIL import Image, ImageDraw, ImageFont
import textwrap
from typing import List, Optional
import os


class SlideshowGifMaker:
    def __init__(
        self,
        width: int = 640,
        height: int = 360,
        fps: int = 30
    ):
        self.width = width
        self.height = height
        self.fps = fps

    def _load_font(self, size: int = 36) -> ImageFont.FreeTypeFont:
        """Load font, falling back to default if not found."""
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]

        for path in font_paths:
            try:
                return ImageFont.truetype(path, size)
            except:
                continue

        return ImageFont.load_default()

    def create_gradient_background(self, colors: List[str]) -> Image.Image:
        """Create a gradient background from color list."""
        img = Image.new('RGB', (self.width, self.height), colors[0])
        draw = ImageDraw.Draw(img)

        if len(colors) == 1:
            return img

        for y in range(self.height):
            ratio = y / self.height

            if len(colors) == 2:
                c1 = self._hex_to_rgb(colors[0])
                c2 = self._hex_to_rgb(colors[1])
                color = tuple(int(c1[i] + (c2[i] - c1[i]) * ratio) for i in range(3))
            else:
                if ratio < 0.5:
                    r = ratio * 2
                    c1 = self._hex_to_rgb(colors[0])
                    c2 = self._hex_to_rgb(colors[1])
                else:
                    r = (ratio - 0.5) * 2
                    c1 = self._hex_to_rgb(colors[1])
                    c2 = self._hex_to_rgb(colors[2])
                color = tuple(int(c1[i] + (c2[i] - c1[i]) * r) for i in range(3))

            draw.line([(0, y), (self.width, y)], fill=color)

        return img

    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join(c * 2 for c in hex_color)
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> List[str]:
        """Wrap text to fit within max_width."""
        lines = []
        for line in text.split('\n'):
            if not line.strip():
                continue
            wrapped = textwrap.wrap(line, width=max_width // (font.getbbox('M')[2] // 2))
            lines.extend(wrapped)
        return lines

    def create_slideshow_gif(
        self,
        headlines: List[str],
        output_path: str,
        total_duration: int = 30,
        bg_colors: List[str] = ["#1a1a2e", "#16213e", "#0f3460"],
        text_color: str = "#ffffff",
        signature: str = "🐈 nanobot.srik.me",
        headline_number: bool = True,
        font_size: int = 32,
        skip_frames: int = 3  # Skip every N frames for faster rendering
    ):
        """
        Create a slideshow GIF with multiple headlines.

        Args:
            headlines: List of headline strings
            output_path: Output GIF file path
            total_duration: Total duration in seconds
            bg_colors: Background gradient colors
            text_color: Text color
            signature: Footer signature text
            headline_number: Show headline numbers (1/N, 2/N, etc.)
            font_size: Font size for headlines
            skip_frames: Skip every N frames for faster rendering (higher = faster, lower = smoother)
        """
        frames = []

        # Load fonts
        title_font = self._load_font(font_size)
        num_font = self._load_font(24)
        sig_font = self._load_font(14)

        # Calculate duration per headline
        num_headlines = len(headlines)
        frames_per_headline = int((self.fps * total_duration) / num_headlines)
        total_frames = frames_per_headline * num_headlines

        # Pre-wrap all headlines
        wrapped_headlines = []
        for hl in headlines:
            lines = self.wrap_text(hl, title_font, self.width - 100)
            wrapped_headlines.append(lines)

        headline_index = 0
        frame_in_headline = 0

        for frame_num in range(total_frames):
            # Determine which headline to show
            headline_index = frame_num // frames_per_headline
            frame_in_headline = frame_num % frames_per_headline

            # Progress within this headline (0 to 1)
            local_progress = frame_in_headline / frames_per_headline

            # Animation: Fade in, hold, fade out
            alpha = 1.0
            if local_progress < 0.15:
                # Fade in
                alpha = local_progress / 0.15
            elif local_progress > 0.85:
                # Fade out
                alpha = (1 - local_progress) / 0.15

            # Create background
            bg = self.create_gradient_background(bg_colors)
            draw = ImageDraw.Draw(bg)

            # Current headline
            current_lines = wrapped_headlines[headline_index]
            current_headline = headlines[headline_index]

            # Draw headline number
            if headline_number:
                num_text = f"{headline_index + 1}/{num_headlines}"
                num_rgba = self._hex_to_rgb(text_color) + (int(alpha * 180),)
                draw.text((self.width // 2, 40), num_text, font=num_font, fill=num_rgba, anchor="mm")

            # Draw headline lines
            line_height = 45
            total_height = len(current_lines) * line_height
            y_start = (self.height - total_height) // 2 + 10

            for i, line in enumerate(current_lines):
                text_y = y_start + i * line_height
                text_x = self.width // 2

                # Shadow for visibility
                shadow_rgba = (0, 0, 0, int(alpha * 80))
                draw.text((text_x + 2, text_y + 2), line, font=title_font, fill=shadow_rgba, anchor="mm")

                # Main text with alpha
                rgb = self._hex_to_rgb(text_color)
                rgba = rgb + (int(alpha * 255),)
                draw.text((text_x, text_y), line, font=title_font, fill=rgba, anchor="mm")

            # Draw signature at bottom
            sig_rgba = (255, 255, 255, int(alpha * 200))
            draw.text((self.width // 2, self.height - 25), signature, font=sig_font, fill=sig_rgba, anchor="mm")

            # Progress bar at bottom
            bar_width = int(self.width * 0.8)
            bar_height = 4
            bar_x = (self.width - bar_width) // 2
            bar_y = self.height - 15

            # Progress background
            draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height], fill=(255, 255, 255, 50))

            # Progress fill
            progress_width = int(bar_width * ((headline_index * frames_per_headline + frame_in_headline) / total_frames))
            draw.rectangle([bar_x, bar_y, bar_x + progress_width, bar_y + bar_height], fill=text_color)

            # Skip frames for faster rendering
            if frame_num % skip_frames == 0:
                frames.append(bg)

        # Save as GIF
        save_opts = {
            'save_all': True,
            'append_images': frames[1:],
            'duration': 1000 // self.fps,
            'loop': 0,
            'disposal': 2,
            'optimize': True
        }

        frames[0].save(output_path, **save_opts)

        file_size = os.path.getsize(output_path) / 1024
        print(f"✅ Slideshow GIF saved to: {output_path}")
        print(f"   Duration: {total_duration}s, Headlines: {num_headlines}")
        print(f"   Size: {len(frames)} frames, {self.width}x{self.height}")
        print(f"   File: {file_size:.1f} KB ({file_size/1024:.2f} MB)")


def main():
    """CLI entry point for slideshow mode."""
    import argparse

    parser = argparse.ArgumentParser(description="Create slideshow GIFs with multiple headlines")
    parser.add_argument("headlines", nargs="+", help="Headline texts")
    parser.add_argument("-o", "--output", default="slideshow.gif", help="Output file path")
    parser.add_argument("-d", "--duration", type=int, default=30, help="Total duration in seconds")
    parser.add_argument("--width", type=int, default=640, help="Width")
    parser.add_argument("--height", type=int, default=360, help="Height")
    parser.add_argument("--bg", nargs="+", default=["#1a1a2e", "#16213e", "#0f3460"],
                        help="Background colors (hex)")
    parser.add_argument("--text-color", default="#ffffff", help="Text color (hex)")
    parser.add_argument("--signature", default="🐈 nanobot.srik.me", help="Signature text")
    parser.add_argument("--no-numbers", action="store_true", help="Don't show headline numbers")
    parser.add_argument("--font-size", type=int, default=32, help="Font size")

    args = parser.parse_args()

    maker = SlideshowGifMaker(width=args.width, height=args.height, fps=30)
    maker.create_slideshow_gif(
        headlines=args.headlines,
        output_path=args.output,
        total_duration=args.duration,
        bg_colors=args.bg,
        text_color=args.text_color,
        signature=args.signature,
        headline_number=not args.no_numbers,
        font_size=args.font_size
    )


if __name__ == "__main__":
    main()
