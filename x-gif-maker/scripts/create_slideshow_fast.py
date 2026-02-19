#!/usr/bin/env python3
"""
X GIF Maker - Fast Slideshow Mode
Quick slideshow GIF generation for social media.
"""

from PIL import Image, ImageDraw, ImageFont
import textwrap
from typing import List, Optional
import os


class FastSlideshowGifMaker:
    def __init__(self, width: int = 640, height: int = 360):
        self.width = width
        self.height = height

    def _load_font(self, size: int = 36) -> ImageFont.FreeTypeFont:
        """Load font, falling back to default if not found."""
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ]

        for path in font_paths:
            try:
                return ImageFont.truetype(path, size)
            except:
                continue

        return ImageFont.load_default()

    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color to RGB tuple."""
        hex_color = hex_color.lstrip('#')
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
        duration_per_headline: float = 3.0,
        bg_color: str = "#1a1a2e",
        text_color: str = "#ffffff",
        signature: str = "🐈 nanobot.srik.me",
        font_size: int = 28
    ):
        """
        Create a slideshow GIF with multiple headlines (fast version).
        """
        frames = []
        fps = 15  # Lower FPS for faster generation
        frames_per_headline = int(fps * duration_per_headline)

        # Load fonts
        title_font = self._load_font(font_size)
        num_font = self._load_font(20)
        sig_font = self._load_font(12)

        num_headlines = len(headlines)
        bg_rgb = self._hex_to_rgb(bg_color)
        text_rgb = self._hex_to_rgb(text_color)

        # Pre-wrap all headlines
        wrapped_headlines = []
        for hl in headlines:
            lines = self.wrap_text(hl, title_font, self.width - 100)
            wrapped_headlines.append(lines)

        for headline_index, (headline, lines) in enumerate(zip(headlines, wrapped_headlines)):
            # Create frames for this headline
            for frame_num in range(frames_per_headline):
                progress = frame_num / frames_per_headline

                # Fade in/out
                if progress < 0.1:
                    alpha = progress / 0.1
                elif progress > 0.9:
                    alpha = (1 - progress) / 0.1
                else:
                    alpha = 1.0

                # Create simple background
                img = Image.new('RGB', (self.width, self.height), bg_rgb)
                draw = ImageDraw.Draw(img)

                # Headline number
                num_rgba = text_rgb + (int(alpha * 150),)
                draw.text((self.width // 2, 35), f"{headline_index + 1}/{num_headlines}",
                          font=num_font, fill=num_rgba, anchor="mm")

                # Headline lines
                line_height = 40
                total_height = len(lines) * line_height
                y_start = (self.height - total_height) // 2

                for i, line in enumerate(lines):
                    text_y = y_start + i * line_height
                    # Shadow
                    shadow_rgba = (0, 0, 0, int(alpha * 80))
                    draw.text((self.width // 2 + 2, text_y + 2), line,
                              font=title_font, fill=shadow_rgba, anchor="mm")
                    # Main text
                    text_rgba = text_rgb + (int(alpha * 255),)
                    draw.text((self.width // 2, text_y), line,
                              font=title_font, fill=text_rgba, anchor="mm")

                # Signature
                sig_rgba = (255, 255, 255, int(alpha * 180))
                draw.text((self.width // 2, self.height - 22), signature,
                          font=sig_font, fill=sig_rgba, anchor="mm")

                frames.append(img)

        # Save as GIF
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=1000 // fps,
            loop=0,
            disposal=2,
            optimize=True
        )

        file_size = os.path.getsize(output_path) / 1024
        total_duration = num_headlines * duration_per_headline
        print(f"✅ Slideshow GIF: {output_path}")
        print(f"   Duration: {total_duration}s, Headlines: {num_headlines}")
        print(f"   Size: {len(frames)} frames, {self.width}x{self.height}")
        print(f"   File: {file_size:.1f} KB")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Create slideshow GIFs")
    parser.add_argument("headlines", nargs="+", help="Headlines")
    parser.add_argument("-o", "--output", default="slideshow.gif", help="Output file")
    parser.add_argument("-d", "--duration", type=float, default=3.0, help="Seconds per headline")
    parser.add_argument("--bg", default="#1a1a2e", help="Background color")
    parser.add_argument("--text-color", default="#ffffff", help="Text color")
    parser.add_argument("--signature", default="🐈 nanobot.srik.me", help="Signature")
    parser.add_argument("--font-size", type=int, default=28, help="Font size")

    args = parser.parse_args()

    maker = FastSlideshowGifMaker()
    maker.create_slideshow_gif(
        headlines=args.headlines,
        output_path=args.output,
        duration_per_headline=args.duration,
        bg_color=args.bg,
        text_color=args.text_color,
        signature=args.signature,
        font_size=args.font_size
    )


if __name__ == "__main__":
    main()
