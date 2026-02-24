# Digest Tracker Skill

Track topics, fetch news from media/blog sources, and generate digests for WhatsApp or blog posts.

## Description

This skill wraps the `digest-tracker` CLI tool, which allows you to:
- Create and manage topics (e.g., "digital-payments", "chennai-transit")
- Add RSS feeds and web content sources
- Fetch articles incrementally (only new content since last run)
- Generate daily/weekly/monthly digests
- Publish digests to local blogs (Jekyll, Hugo, etc.)

## Requirements

- Turso database (free tier available at https://turso.tech)
- Environment variables set:
  - `TURSO_DATABASE_URL` - Your Turso database URL
  - `TURSO_AUTH_TOKEN` - Your Turso auth token

## Commands

### Topic Management

```
digest topic add <name> [--desc <description>]
```
Add a new topic to track.

```
digest topic list
```
List all topics.

```
digest topic remove <name>
```
Remove a topic.

```
digest topic info <name>
```
Show topic details including sources, blog links, and recent digests.

### Source Management

```
digest source add <topic> <url> [--type rss|web] [--config <json>]
```
Add a content source to a topic.
- `--type`: Source type (default: rss)
- `--config`: JSON configuration for the source

```
digest source list <topic>
```
List all sources for a topic.

```
digest source remove <source_id>
```
Remove a source by ID.

### Blog Management

```
digest blog add <name> <blog_type> [--config <json>]
```
Add a blog configuration.
- `blog_type`: "local" (for Jekyll, Hugo, etc.), "github" (planned), "wordpress" (planned)
- `config`: JSON config with blog settings

Example for local blog:
```
digest blog add "my-blog" "local" --config '{"path": "/home/user/blog/_posts"}'
```

```
digest blog list
```
List all configured blogs.

```
digest blog link <topic> <blog> [--category <tag>] [--slug-prefix <prefix>]
```
Link a blog to a topic for automatic publishing.
- `--category`: Blog category/tag for posts
- `--slug-prefix`: URL prefix for posts (e.g., "payments/")

```
digest blog unlink <topic>
```
Unlink a blog from a topic.

### Fetching Articles

```
digest fetch <topic> [--days 7]
```
Fetch new articles for a topic.
- `--days`: Look back N days for new articles (default: 7)

### Generating Digests

```
digest generate <topic> <daily|weekly|monthly|custom> [--days 7] [--from <date>] [--to <date>]
```
Generate a digest for a topic.
- `frequency`: daily, weekly, monthly, or custom
- `--days`: Number of days to include (for standard frequencies)
- `--from`: Start date (ISO format, e.g., "2026-02-17")
- `--to`: End date (ISO format, e.g., "2026-02-24")

```
digest history <topic> [--limit 10]
```
Show digest history for a topic.

```
digest view <digest_id>
```
View a specific digest.

```
digest export <digest_id> [--format markdown] [--output <path>]
```
Export a digest to a file.

### Publishing

```
digest publish <digest_id> [--blog <name>] [--dry-run]
```
Publish a digest to a blog.
- `--blog`: Override linked blog
- `--dry-run`: Show what would be published without actually publishing

## Examples

### Setup a topic with sources

```
digest topic add "chennai-transit" --desc "Chennai Metro and urban mobility news"
digest source add "chennai-transit" "https://cmrl.in/category/news/feed/" --type rss
digest source add "chennai-transit" "https://metrorailchennai.in/feed/" --type rss
```

### Link to a blog

```
digest blog add "transit-blog" "local" --config '{"path": "/home/ubuntu/.nanobot/workspace/transit-blog/_posts"}'
digest blog link "chennai-transit" "transit-blog" --category "transit" --slug-prefix "digest/"
```

### Fetch and generate digest

```
digest fetch "chennai-transit" --days 7
digest generate "chennai-transit" "weekly"
digest view <digest_id>
```

### Publish digest

```
digest publish <digest_id>
# Or test first
digest publish <digest_id> --dry-run
```

## Turso Setup

1. Sign up at https://turso.tech (free tier available)
2. Create a database
3. Get database URL and auth token
4. Set environment variables:
   ```bash
   export TURSO_DATABASE_URL="libsql://your-db.turso.io"
   export TURSO_AUTH_TOKEN="your-auth-token"
   ```

## Source Types

| Type | Description | Example |
|------|-------------|---------|
| `rss` | RSS/Atom feeds | `https://example.com/feed.xml` |
| `web` | Single web page | `https://example.com/article` |

## Blog Types

| Type | Description | Config Example |
|------|-------------|----------------|
| `local` | Local directory | `{"path": "/path/to/_posts"}` |

## Notes

- The CLI stores all data in Turso (SQLite-compatible database)
- Articles are deduplicated by URL
- Digests are formatted for WhatsApp by default (with emojis and bold text)
- Published digests are marked in the database to avoid re-publishing
