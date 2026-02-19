---
name: x-gif-maker
description: Create animated GIFs and MP4s for X (Twitter), Instagram, LinkedIn, Discord, and other social media platforms. Use when you need to generate: (1) Text-based animated content with 11+ styles (fade, pulse, slide, bounce, glow, shake, typewriter, zoom, wave, glitch), (2) Multi-headline slideshow GIFs for news updates and announcements, (3) Social media post visuals from text content, (4) Quick announcement or quote GIFs/MP4s, (5) Branded content with custom colors and signatures, (6) Batch generation for multiple posts, (7) Auto-upload to catbox.moe for sharing. Generates GIFs/MP4s in under 30 seconds with customizable dimensions, colors, animation effects, and watermarks.
---

# X GIF Maker

Create animated GIFs and MP4s for social media posts in under 30 seconds. Features 11+ animation styles, auto-upload, and batch generation.

## What's New in v2.0

- ✅ **MP4 Export**: Export your animations as MP4 videos
- ✅ **Auto-Upload**: One-command create & upload to catbox.moe
- ✅ **Comprehensive Tests**: Full test coverage with pytest
- ✅ **Better CLI**: Enhanced command-line interface

## Quick Start

### Create a simple GIF

```python
from scripts.create_gif import GifMaker

maker = GifMaker(width=640, height=360, duration=2)
maker.create_text_gif(
    text="Hello World!",
    output_path="output.gif",
    style="fade",
    signature="🤖 @nanobot"
)
```

### Available styles
**Basic:** fade, pulse, slide_up, slide_down, bounce
**Advanced:** glow, shake, typewriter, zoom, wave, glitch

See [references/styles.md](references/styles.md) for style descriptions and color palettes.

See [references/templates.md](references/templates.md) for pre-configured templates.

## CLI Usage

```bash
python3 scripts/create_gif.py "Your text here" -o output.gif --style fade --duration 2
```

### Common options
- `-s, --style`: Animation style (fade, pulse, slide_up, slide_down, bounce, glow, shake, typewriter, zoom, wave, glitch)
- `--width`: Width in pixels (default: 640)
- `--height`: Height in pixels (default: 360)
- `--duration`: Duration in seconds (default: 2)
- `--bg`: Background colors (space-separated hex codes)
- `--text-color`: Text color (hex)
- `--signature`: Signature text at bottom
- `--logo`: Path to logo image (PNG with transparency recommended)
- `--logo-pos`: Logo position (top-left, top-right, bottom-left, bottom-right, center)
- `--font-size`: Font size for main text (default: 36)
- `--quality`: GIF quality 1-100, higher = better but larger (default: 85)

### Examples

```bash
# Product announcement
python3 scripts/create_gif.py "🚀 New Feature!" -o announcement.gif --style slide_down

# Quote with custom colors
python3 scripts/create_gif.py '"Just do it"' -o quote.gif --style fade --bg "#0f0c29" "#302b63" --text-color "#00d2ff"

# Call-to-action
python3 scripts/create_gif.py "🔥 Limited Offer!" -o cta.gif --style pulse --duration 3

# Tech announcement with glitch
python3 scripts/create_gif.py "v2.0 Released!" -o release.gif --style glitch --bg "#0f0f0f" "#1a1a1a" --text-color "#00ff88"

# With logo
python3 scripts/create_gif.py "Breaking News" -o news.gif --style shake --logo logo.png --logo-pos top-right

# Typewriter effect
python3 scripts/create_gif.py "This text appears..." -o type.gif --style typewriter --bg "#2c3e50" "#34495e"
```

## Social Media Sizes

| Platform | Recommended Size | Duration | Max Size |
|----------|------------------|----------|----------|
| X (Twitter) | 640x360 | 1-3 sec | 15MB |
| X (Twitter) Premium | 1280x720 | 1-3 sec | 15MB |
| Instagram Story | 640x1136 | 2-4 sec | 4MB |
| Instagram Feed | 640x640 | 2-4 sec | 4MB |
| LinkedIn | 640x360 | 2-3 sec | 5MB |
| Discord | 480x270 | 1-2 sec | 8MB |
| TikTok | 720x1280 | 2-4 sec | 4MB |

## MP4 Export

Export your animations as MP4 videos for better quality and smaller file sizes.

### Python API

```python
from scripts.create_gif import GifMaker

maker = GifMaker(width=640, height=360, duration=2)

# Create GIF first (frames are cached)
maker.create_text_gif(
    text="Hello World!",
    output_path="output.gif",
    style="fade"
)

# Export as MP4
maker.export_mp4(
    output_path="output.mp4",
    codec="libx264",  # or "libx265" for smaller files
    bitrate="2M"      # 2Mbps bitrate
)
```

### CLI

```bash
# Create GIF + MP4
python3 scripts/create_gif.py "Your text" --mp4

# Custom bitrate
python3 scripts/create_gif.py "Your text" --mp4 --bitrate 5M

# Use different codec
python3 scripts/create_gif.py "Your text" --mp4 --codec libx265
```

### MP4 CLI Options
- `--mp4`: Also export as MP4 (same filename, .mp4 extension)
- `--bitrate`: Video bitrate (default: 2M, e.g., 1M, 2M, 5M)
- `--codec`: Video codec (default: libx264, options: libx264, libx265, libvpx-vp9)

### Dependencies

```bash
pip install imageio imageio-ffmpeg
```

## Auto-Upload

Automatically upload your GIFs/MP4s to catbox.moe for easy sharing.

### Python API

```python
from scripts.create_gif import GifMaker

maker = GifMaker(width=640, height=360, duration=2)

# Create and upload in one step
results = maker.create_and_upload(
    text="Breaking News!",
    output_path="news.gif",
    style="shake",
    upload=True,
    export_mp4=True
)

print(f"GIF URL:  {results['gif_url']}")
print(f"MP4 URL:  {results['mp4_url']}")
```

### CLI

```bash
# Auto-upload GIF
python3 scripts/create_gif.py "Your text" --auto-upload

# Create + MP4 + Upload both
python3 scripts/create_gif.py "Your text" --mp4 --auto-upload

# Create first, then upload separately
python3 scripts/create_gif.py "Your text" -o output.gif
python3 scripts/create_gif.py --upload -o output.gif  # Upload existing file
```

### Upload CLI Options
- `--upload`: Upload file(s) to catbox.moe
- `--auto-upload`: Create and upload in one step (implies --upload)
- `--batch --upload`: Upload all batch-generated files

### Upload URLs

Uploaded files are hosted on catbox.moe with temporary links:
- Direct file access via returned URL
- Files are kept permanently (no expiration for direct uploads)
- Example: `https://files.catbox.moe/abc123.gif`

### Dependencies

```bash
pip install requests
```

### Upload Batch Files

```bash
# Upload all files from batch
python3 scripts/create_gif.py --batch posts.json --upload
```

## Batch Generation

Create multiple GIFs at once:

```python
from scripts.create_gif import GifMaker

maker = GifMaker(width=640, height=360, duration=2)

# Generate multiple posts
posts = [
    ("🚀 New Feature!", "feature.gif", "slide_down"),
    ("Bug Fixes!", "fix.gif", "bounce"),
    ("API Update", "api.gif", "typewriter"),
]

for text, output, style in posts:
    maker.create_text_gif(
        text=text,
        output_path=output,
        style=style,
        signature="🤖 @nanobot"
    )
```

```bash
# CLI batch mode
python3 scripts/create_gif.py --batch posts.json
```

**posts.json format:**
```json
[
    {
        "text": "🚀 New Feature!",
        "output": "feature.gif",
        "style": "slide_down"
    },
    {
        "text": "Bug Fixes!",
        "output": "fix.gif",
        "style": "bounce"
    }
]
```

## Advanced Customization

### Custom color gradients

```python
maker.create_text_gif(
    text="Your text",
    output_path="output.gif",
    bg_colors=["#ff6b6b", "#feca57", "#ff9ff3"],  # 3-color gradient
    text_color="#ffffff"
)
```

### Multi-line text

```python
maker.create_text_gif(
    text="Line 1\nLine 2\nLine 3",  # Use \n for newlines
    output_path="multi-line.gif"
)
```

### Long duration (slower animation)

```python
maker = GifMaker(duration=3)  # 3 seconds = 90 frames @ 30fps
```

### Custom font

```python
maker.create_text_gif(
    text="Custom Font",
    output_path="custom.gif",
    font_path="/path/to/your/font.ttf",
    font_size=48
)
```

### Add logo/watermark

```python
maker.create_text_gif(
    text="Branded Content",
    output_path="branded.gif",
    logo_path="logo.png",
    logo_position="top-right"
)
```

## Nanobot Integration

Use from nanobot commands:

```python
# In your nanobot skill
from skills.x_gif_maker import GifMaker

async def make_post_gif(text: str, style: str = "fade"):
    """Create a GIF and send it to the user."""
    maker = GifMaker(width=640, height=360, duration=2)
    output = f"/tmp/{hash(text)}.gif"
    
    maker.create_text_gif(
        text=text,
        output_path=output,
        style=style,
        signature="🤖 @nanobot"
    )
    
    # Send to user (depends on your platform)
    await send_file(output)
```

## Slideshow Mode

Create multi-headline slideshow GIFs for news, updates, or announcements:

### Python API

```python
from scripts.create_slideshow_fast import FastSlideshowGifMaker

maker = FastSlideshowGifMaker(width=640, height=360)

headlines = [
    "Headline 1 goes here",
    "Headline 2 goes here",
    "Headline 3 goes here",
    "Headline 4 goes here",
]

maker.create_slideshow_gif(
    headlines=headlines,
    output_path="slideshow.gif",
    duration_per_headline=3.0,  # Seconds per headline
    bg_color="#0a0e17",
    text_color="#00d4ff",
    signature="📰 Your Brand • nanobot.srik.me",
    font_size=24
)
```

### CLI Usage

```bash
python3 scripts/create_slideshow_fast.py "Headline 1" "Headline 2" "Headline 3" -o slideshow.gif --duration 5
```

### Slideshow Options
- `-d, --duration`: Seconds per headline (default: 3.0)
- `--bg`: Background color (single hex, no gradient for speed)
- `--text-color`: Text color (hex)
- `--signature`: Footer signature text
- `--font-size`: Font size (default: 28)

### Example: Chennai News Slideshow

```bash
python3 scripts/create_slideshow_fast.py \
    "Chennai to become global deep-tech cluster by 2040" \
    "Suburban train services cut for 45 days from Feb 20" \
    "Tamil Nadu Budget 2026: FM attacks Centre" \
    "Chennai Fintech Tower nears completion" \
    -o chennai_news.gif --duration 5 --bg "#0a0e17" --text-color "#00d4ff"
```

### Slideshow Features
- Fade in/out transitions
- Headline numbering (1/N)
- Progress bar indicator
- Signature branding
- Fast generation (~10s for 6 headlines)

## Performance Tips

- Keep GIFs under 5MB for best platform compatibility
- Use 30fps for smooth animations (single GIF mode)
- Slideshow mode uses 15fps for faster generation
- Limit to 3 colors in gradient backgrounds
- Shorter text = faster rendering
- Use `--quality 75` for smaller file sizes
- For slideshows, limit to 6-8 headlines for optimal performance

## Troubleshooting

### "Font not found"
The script uses DejaVuSans-Bold.ttf. If missing, it falls back to default PIL font. For custom fonts:

```python
maker.create_text_gif(
    text="Custom Font",
    output_path="output.gif",
    font_path="/usr/share/fonts/truetype/custom.ttf"
)
```

### "File too large"
Reduce resolution or duration:
```python
maker = GifMaker(width=480, height=270, duration=1.5)
```

### Animation too slow/fast
Adjust fps:
```python
maker = GifMaker(fps=24)  # Slower
maker = GifMaker(fps=60)  # Faster
```

## Resources

### scripts/create_gif.py
Main GIF generation script with `GifMaker` class.

### references/styles.md
Animation style descriptions and 20+ color palettes.

### references/templates.md
Pre-configured templates for 20+ common use cases.

## Tips

- Keep text short and impactful (best for social media)
- Use 2-3 colors for gradient backgrounds
- Add emoji for visual interest
- Include signature for branding
- Duration of 2 seconds works best for most use cases
- Test on mobile before posting (small screens matter)
- Use high contrast colors for readability

## Testing

Run the test suite to verify functionality:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=scripts --cov-report=html

# Run specific test
pytest tests/test_gif_maker.py::TestGifMakerBasics::test_initialization -v
```

### Test Coverage

- ✅ Basic functionality (initialization, color conversion)
- ✅ Gradient backgrounds (1-3 colors)
- ✅ All 11 animation styles
- ✅ GIF creation (single, multi-line, long text)
- ✅ Batch generation
- ✅ MP4 export (when imageio installed)
- ✅ Upload error handling
- ✅ CLI interface

### Test Files

- `tests/test_gif_maker.py` - Complete test suite for GifMaker class