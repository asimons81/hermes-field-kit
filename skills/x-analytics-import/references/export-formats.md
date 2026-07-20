# Export Formats

The importer recognizes three X Analytics export families.

## Overview

Typical required columns:

```text
Date, Impressions, Likes, Engagements, Bookmarks, Shares,
New follows, Unfollows, Replies, Reposts, Profile visits
```

Additional known fields include post creation, video views, and media views.

## Content

Typical required columns:

```text
Post id, Date, Post text, Post Link, Impressions, Likes,
Engagements, Bookmarks, Shares, New follows, Replies,
Reposts, Profile visits
```

Additional click and expansion fields are accepted.

Content dates identify when posts were published. Their metric values are not assumed to equal account overview totals for that calendar day.

## Video

Video exports may begin with a title row followed by the real header:

```text
Video overview
Date, Views, Watch Time (ms), Completion Rate,
Average Watch Time (ms), Estimated Revenue
```

Some files append a separate `Your videos` table after the daily overview rows. The importer stops at that section boundary.

Revenue fields are sensitive and excluded from public-safe output.

## Header normalization

The parser handles:

- UTF-8 BOMs
- case and spacing differences
- common singular/plural aliases
- percentages
- currency markers
- comma-formatted numbers
- multiple supported date formats

Unknown columns warn by default. Set `fail_on_unknown_columns` only when strict schema locking is required.
