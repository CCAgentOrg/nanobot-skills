# X GIF Maker

Create animated GIFs for X (Twitter), Instagram, LinkedIn, Discord, and other social media platforms in under 30 seconds.

![x-gif-maker](https://img.shields.io/badge/Style-10%2B-blue)
![python](https://img.shields.io/badge/Python-3.6%2B-green)

## Features

- **10+ Animation Styles**: fade, pulse, slide, bounce, glow, shake, typewriter, zoom, wave, glitch
- **20+ Color Palettes**: Pre-configured beautiful gradients for any vibe
- **Platform Presets**: Optimized sizes for X, Instagram, LinkedIn, Discord, TikTok
- **Batch Generation**: Create multiple GIFs at once from JSON config
- **Logo/Watermark Support**: Add branding to your GIFs
- **CLI & Python API**: Use from command line or as a library

## Installation

```bash
pip install pillow
```

## Quick Start

### Command Line

```bash
python3 scripts/create_gif.py "Hello World!" -o output.gif --style fade
```

### Python API

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

## Animation Styles

| Style | Best For | Vibe |
|-------|----------|------|
| `fade` | Introductions, quotes | Clean, minimalist |
| `pulse` | Call-to-actions | Urgent, attention-grabbing |
| `slide_up` | Success stories | Uplifting, positive |
| `slide_down` | Announcements | Professional, reveal |
| `bounce` | Fun updates | Playful, energetic |
| `glow` | Premium features | Luxurious, highlight |
| `shake` | Breaking news | Urgent, alert |
| `typewriter` | Code/tech | Progressive, developer |
| `zoom` | Impact reveals | Bold, punchy |
| `wave` | Casual content | Friendly, organic |
| `glitch` | Tech/edgy | Cyberpunk, digital |

## Color Palettes

Purple Dreams, Ocean Blues, Sunset Glow, Dark Mode, Mint Fresh, Neon Vibes, Corporate Blue, Fire & Ice, Forest Green, Cyber Pink, Midnight Purple, Sunrise Orange, Space Dark, Rose Gold, Electric Blue, Earth Tones, Neon Green, Lavender Dreams, Ruby Red

## Examples

### Product Launch
```bash
python3 scripts/create_gif.py "🚀 New Feature!" \
  --style slide_down \
  --bg "#667eea" "#764ba2" \
  --signature "YourBrand"
```

### Quote Post
```bash
python3 scripts/create_gif.py '"Just do it"' \
  --style fade \
  --bg "#0f0c29" "#302b63" \
  --text-color "#00d2ff"
```

### Tech Announcement
```bash
python3 scripts/create_gif.py "v2.0 Released!" \
  --style glitch \
  --bg "#0f0f0f" "#1a1a1a" \
  --text-color "#00ff88"
```

## Batch Generation

Create multiple GIFs from a JSON file:

```bash
python3 scripts/create_gif.py --batch examples/batch.json
```

**batch.json format:**
```json
[
  {
    "text": "🚀 New Feature!",
    "output": "feature.gif",
    "style": "slide_down",
    "bg_colors": ["#667eea", "#764ba2"],
    "signature": "🤖 nanobot"
  },
  {
    "text": "Bug Fixes!",
    "output": "fix.gif",
    "style": "bounce"
  }
]
```

## CLI Options

```
positional arguments:
  text                  Text to animate

options:
  -h, --help            Show help message
  -o, --output OUTPUT   Output file path (default: output.gif)
  -s, --style STYLE     Animation style (default: fade)
  --width WIDTH         Width in pixels (default: 640)
  --height HEIGHT       Height in pixels (default: 360)
  --duration DURATION   Duration in seconds (default: 2)
  --bg COLORS           Background colors (hex, space-separated)
  --text-color COLOR    Text color (hex, default: #ffffff)
  --signature SIGNATURE Signature text at bottom
  --logo PATH           Path to logo image
  --logo-pos POS        Logo position (default: bottom-right)
  --font-size SIZE      Font size (default: 36)
  --quality QUALITY     GIF quality 1-100 (default: 85)
  --batch PATH          JSON file for batch generation
```

## Platform Presets

```python
# X (Twitter) - 640x360
maker = GifMaker(width=640, height=360)

# Instagram Story - 640x1136
maker = GifMaker(width=640, height=1136)

# Instagram Feed - 640x640
maker = GifMaker(width=640, height=640)

# LinkedIn - 640x360
maker = GifMaker(width=640, height=360)

# Discord - 480x270
maker = GifMaker(width=480, height=270)

# TikTok - 720x1280
maker = GifMaker(width=720, height=1280)
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

    # Send to user
    await send_file(output)
```

## Documentation

- **[SKILL.md](SKILL.md)** - Complete documentation
- **[references/styles.md](references/styles.md)** - Animation styles & color palettes
- **[references/templates.md](references/templates.md)** - Pre-configured templates
- **[examples/batch.json](examples/batch.json)** - Batch generation example

## Performance Tips

- Keep GIFs under 5MB for best platform compatibility
- Use 30fps for smooth animations
- Limit to 3 colors in gradient backgrounds
- Shorter text = faster rendering
- Use `--quality 75` for smaller file sizes

## License

MIT License - Feel free to use in your projects!

## Contributing

Contributions welcome! Feel free to submit issues or pull requests.

---

Made with ❤️ by [nanobot](https://nanobot.srik.me)
