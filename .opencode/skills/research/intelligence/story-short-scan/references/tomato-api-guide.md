
# Tomato Novel Internal API Guide

## Overview
Tomato Novel (fanqienovel.com) is a SPA that offers internal JSON APIs for book listing and filtering. This guide covers the relevant endpoints, category mappings, and pitfalls encountered during automated short-story scanning.

## Key Endpoints

### Category List
`GET https://fanqienovel.com/api/author/book/category_list/v0/?gender={0|1|2}`
- `gender=0` returns all categories. `1` for male, `2` for female.
- Response: `{ "code": 0, "data": [ { "category_id": ..., "name": "...", "label": "..." } ] }`

### Book List (with filters)
`GET https://fanqienovel.com/api/author/library/book_list/v0/`
Parameters:
- `page_count` (int, e.g., 30)
- `page_index` (int, default 0)
- `gender` (1=male, 2=female)
- `category_id` (int, -1 for all)
- `creation_status` (0=all, 1=ongoing)
- `word_count` (0=all, 1=<300k words, 2=300k-1M, 3=>1M)
- `book_type` (-1=all)
- `sort` (0=hottest)
Response: `{ "code": 0, "data": { "book_list": [...], "has_more": bool, "total_count": int } }`

### Book Page (for real titles/abstracts)
`https://fanqienovel.com/page/{book_id}`
- The page HTML contains the true visible title, abstract, and word count, but the API `book_list` data has font-obfuscated `title` and `abstract` fields (garbled when read programmatically via `requests`).

## Category Mapping for 14 Common Short-Story Genres

The platform's internal categories are labeled differently from the user's requested genres. The following mapping was derived empirically:

| User Category | Platform Category Name | Category ID | Gender |
|---------------|------------------------|-------------|--------|
| 悬疑惊悚 | 女频悬疑 | 747 | 2 |
| 宫斗宅斗 | 古风世情 | 1139 | 2 |
| 现言甜宠 | 青春甜宠 | 749 | 2 |
| 古言甜宠 | 古风世情 | 1139 | 2 |
| 民国旧影 | 民国言情 | 1017 | 2 |
| 年代 | 年代 | 79 | 2 |
| 女性成长 | 女强 | 86 | 2 |
| 玄幻仙侠 | 玄幻言情 | 248 | 1 |
| 男生生活 | 都市日常 | 261 | 1 |
| 男生情感 | 悬疑恋爱 | 1169 | 1 |
| 男频脑洞 | 悬疑脑洞 | 539 | 1 |
| 女频脑洞 | 女频悬疑 | 747 | 2 |
| 历史古代 | 古代 | 758 | 1 |
| 都市日常 | 校园 | 4 | 2 |

**Note**: These mappings are approximate. Some categories overlap (e.g., 古风世情 used for both 宫斗宅斗 and 古言甜宠). Always verify with the actual category list API for the latest IDs. If a precise match isn't available, fall back to fetching all short stories and filtering by keyword in the title/abstract.

## Font Obfuscation Pitfall
- The `title` and `abstract` fields in the book list API response are encoded with a custom font mapping. Direct HTTP requests (e.g., via `requests.get`) will return garbled text.
- **Workaround**: Use a browser-based method (e.g., `browser_navigate` to the book page, or `browser_console` to execute `document.querySelector('h1').innerText`). The browser renders the correct text because it applies the font mapping.
- For batch processing: first obtain `book_id` from the API, then navigate to each `/page/{book_id}` to extract the real title and abstract.

## Word Count Filter Inaccuracy
- The `word_count=1` parameter is intended to filter books under 300k characters, but some results exceed this threshold (e.g., 40.6万字). Always verify the actual word count from the book page before treating it as a short story.

## Complete Workflow for Multi-Category Short-Story Scan
1. **Get category list** via API for `gender=0` (or separately for 1,2) and build name->ID mapping.
2. **Match user categories** to platform category IDs using the table above as a starting point. Fall back to keyword matching in category names.
3. **Fetch book lists** for each matched category with parameters: `gender=appropriate`, `category_id=...`, `word_count=1`, `creation_status=1`, `sort=0`, `page_count=5` (or up to 30).
4. **Extract true metadata**: For each book, use a browser to open `https://fanqienovel.com/page/{book_id}` and extract the heading text, word count, and abstract from the rendered DOM. Store results.
5. **Filter by word count**: Discard any book with actual word count > 30万字.
6. **Analyze** each surviving short story using `story-short-ana` (or perform surface-level analysis from the abstract and chapter structure if full text not accessible).

## Example Code Snippet (Python + requests)
```python
def fetch_category_map(gender=0):
    url = "https://fanqienovel.com/api/author/book/category_list/v0/"
    params = {"gender": gender}
    resp = requests.get(url, params=params, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://fanqienovel.com/library"})
    data = resp.json()['data']
    return {cat['name']: cat['category_id'] for cat in data}
```

## Known Issues
- The platform's `/short-story` path does not exist. Short stories must be accessed via the library filter.
- The API may return duplicate books across categories (e.g., same book appears in both 悬疑惊悚 and 女频脑洞 because the underlying category is the same).
- Browser automation may be rate-limited or require login session. Using an existing logged-in browser context preserves the session cookie.
