# Part E — Test Report

Corpus size N = 100, vocabulary size M = 127.

## Part E.1 — Free-text VSM (lnc.ltc) queries

### Query: `cotton shirt`

| docID | Category | Title | Cosine score |
|---|---|---|---|
| D001 | T-Shirt | Men's Cotton Crew Neck T-Shirt - Black | 0.2428 |
| D041 | T-Shirt | Men's Cotton Crew Neck T-Shirt - Maroon | 0.2428 |
| D061 | T-Shirt | Men's Cotton Crew Neck T-Shirt - White | 0.2428 |
| D081 | T-Shirt | Men's Cotton Crew Neck T-Shirt - Mustard | 0.2402 |
| D022 | Shirt | Men's Checked Cotton Shirt - White | 0.2364 |
| D082 | Shirt | Men's Checked Cotton Shirt - Blue | 0.2364 |
| D021 | T-Shirt | Men's Cotton Crew Neck T-Shirt - Sky Blue | 0.2360 |
| D042 | Shirt | Men's Checked Cotton Shirt - Maroon | 0.2347 |
| D002 | Shirt | Men's Checked Cotton Shirt - Black | 0.2321 |
| D062 | Shirt | Men's Checked Cotton Shirt - Olive | 0.2321 |

### Query: `winter jacket`

| docID | Category | Title | Cosine score |
|---|---|---|---|
| D058 | Jacket | Women's Quilted Winter Jacket - Black | 0.2845 |
| D018 | Jacket | Women's Quilted Winter Jacket - Beige | 0.2824 |
| D078 | Jacket | Women's Quilted Winter Jacket - Beige | 0.2824 |
| D038 | Jacket | Women's Quilted Winter Jacket - Olive | 0.2790 |
| D098 | Jacket | Women's Quilted Winter Jacket - Olive | 0.2790 |
| D028 | Jacket | Women's Casual Puffer Jacket - Black | 0.2543 |
| D088 | Jacket | Women's Casual Puffer Jacket - Black | 0.2543 |
| D048 | Jacket | Women's Casual Puffer Jacket - Beige | 0.2525 |
| D008 | Jacket | Women's Casual Puffer Jacket - Olive | 0.2495 |
| D068 | Jacket | Women's Casual Puffer Jacket - Olive | 0.2495 |

### Query: `regular fit kurta`

| docID | Category | Title | Cosine score |
|---|---|---|---|
| D004 | Kurta | Men's Regular Fit Kurta - Pink | 0.2554 |
| D064 | Kurta | Men's Regular Fit Kurta - White | 0.2554 |
| D024 | Kurta | Men's Regular Fit Kurta - Teal | 0.2529 |
| D084 | Kurta | Men's Regular Fit Kurta - Beige | 0.2529 |
| D044 | Kurta | Men's Regular Fit Kurta - Navy Blue | 0.2461 |
| D034 | Kurta | Women's Printed Straight Kurta - Maroon | 0.2384 |
| D094 | Kurta | Women's Printed Straight Kurta - Teal | 0.2384 |
| D054 | Kurta | Women's Printed Straight Kurta - Mustard | 0.2361 |
| D014 | Kurta | Women's Printed Straight Kurta - Beige | 0.2343 |
| D074 | Kurta | Women's Printed Straight Kurta - Pink | 0.2343 |

### Query: `high waist leggings`

| docID | Category | Title | Cosine score |
|---|---|---|---|
| D029 | Leggings | Women's High Waist Stretch Leggings - Grey | 0.3415 |
| D049 | Leggings | Women's High Waist Stretch Leggings - Black | 0.3415 |
| D089 | Leggings | Women's High Waist Stretch Leggings - Grey | 0.3415 |
| D009 | Leggings | Women's High Waist Stretch Leggings - Olive Green | 0.3314 |
| D069 | Leggings | Women's High Waist Stretch Leggings - Olive Green | 0.3314 |
| D019 | Leggings | Women's Printed Active Leggings - Black | 0.2891 |
| D059 | Leggings | Women's Printed Active Leggings - Grey | 0.2891 |
| D079 | Leggings | Women's Printed Active Leggings - Black | 0.2891 |
| D039 | Leggings | Women's Printed Active Leggings - Olive Green | 0.2805 |
| D099 | Leggings | Women's Printed Active Leggings - Olive Green | 0.2805 |

### Query: `festive saree`

| docID | Category | Title | Cosine score |
|---|---|---|---|
| D035 | Saree | Women's Cotton Handloom Saree - Yellow | 0.2004 |
| D055 | Saree | Women's Cotton Handloom Saree - Pink | 0.2004 |
| D095 | Saree | Women's Cotton Handloom Saree - Maroon | 0.2004 |
| D005 | Saree | Women's Printed Daily Wear Saree - Blue | 0.2000 |
| D025 | Saree | Women's Printed Daily Wear Saree - Maroon | 0.2000 |
| D065 | Saree | Women's Printed Daily Wear Saree - Green | 0.2000 |
| D085 | Saree | Women's Printed Daily Wear Saree - Red | 0.2000 |
| D015 | Saree | Women's Cotton Handloom Saree - Red | 0.1980 |
| D075 | Saree | Women's Cotton Handloom Saree - Blue | 0.1980 |
| D045 | Saree | Women's Printed Daily Wear Saree - Purple | 0.1976 |

### Query: `breathable fabric t-shirt`

| docID | Category | Title | Cosine score |
|---|---|---|---|
| D011 | T-Shirt | Men's Oversized Graphic T-Shirt - Mustard | 0.3306 |
| D071 | T-Shirt | Men's Oversized Graphic T-Shirt - Black | 0.3306 |
| D001 | T-Shirt | Men's Cotton Crew Neck T-Shirt - Black | 0.3281 |
| D041 | T-Shirt | Men's Cotton Crew Neck T-Shirt - Maroon | 0.3281 |
| D061 | T-Shirt | Men's Cotton Crew Neck T-Shirt - White | 0.3281 |
| D031 | T-Shirt | Men's Oversized Graphic T-Shirt - Olive Green | 0.3247 |
| D091 | T-Shirt | Men's Oversized Graphic T-Shirt - Sky Blue | 0.3247 |
| D081 | T-Shirt | Men's Cotton Crew Neck T-Shirt - Mustard | 0.3247 |
| D051 | T-Shirt | Men's Oversized Graphic T-Shirt - Navy Blue | 0.3213 |
| D021 | T-Shirt | Men's Cotton Crew Neck T-Shirt - Sky Blue | 0.3190 |

### Query: `stretch denim jeans`

| docID | Category | Title | Cosine score |
|---|---|---|---|
| D013 | Jeans | Men's Slim Fit Stretch Jeans - Grey | 0.3132 |
| D073 | Jeans | Men's Slim Fit Stretch Jeans - Grey | 0.3132 |
| D043 | Jeans | Men's Regular Fit Denim Jeans - Grey | 0.3124 |
| D033 | Jeans | Men's Slim Fit Stretch Jeans - Grey | 0.3074 |
| D093 | Jeans | Men's Slim Fit Stretch Jeans - Grey | 0.3074 |
| D003 | Jeans | Men's Regular Fit Denim Jeans - Grey | 0.3066 |
| D063 | Jeans | Men's Regular Fit Denim Jeans - Grey | 0.3066 |
| D053 | Jeans | Men's Slim Fit Stretch Jeans - Grey | 0.2887 |
| D023 | Jeans | Men's Regular Fit Denim Jeans - Grey | 0.2291 |
| D083 | Jeans | Men's Regular Fit Denim Jeans - Grey | 0.2291 |

### Query: `warm fleece hoodie`

| docID | Category | Title | Cosine score |
|---|---|---|---|
| D037 | Hoodie | Unisex Fleece Pullover Hoodie - Black | 0.3202 |
| D097 | Hoodie | Unisex Fleece Pullover Hoodie - Black | 0.3202 |
| D057 | Hoodie | Unisex Fleece Pullover Hoodie - Wine | 0.3165 |
| D017 | Hoodie | Unisex Fleece Pullover Hoodie - Navy Blue | 0.3140 |
| D077 | Hoodie | Unisex Fleece Pullover Hoodie - Navy Blue | 0.3140 |
| D007 | Hoodie | Women's Oversized Fleece Hoodie - Black | 0.2899 |
| D067 | Hoodie | Women's Oversized Fleece Hoodie - Black | 0.2899 |
| D027 | Hoodie | Women's Oversized Fleece Hoodie - Wine | 0.2867 |
| D087 | Hoodie | Women's Oversized Fleece Hoodie - Wine | 0.2867 |
| D047 | Hoodie | Women's Oversized Fleece Hoodie - Navy Blue | 0.2845 |

### Query: `printed dress`

| docID | Category | Title | Cosine score |
|---|---|---|---|
| D076 | Dress | Women's Casual Fit Dress - Green | 0.1665 |
| D036 | Dress | Women's Casual Fit Dress - Black | 0.1648 |
| D046 | Dress | Women's Solid Midi Dress - Lavender | 0.1633 |
| D016 | Dress | Women's Casual Fit Dress - Floral Pink | 0.1631 |
| D056 | Dress | Women's Casual Fit Dress - Yellow | 0.1629 |
| D006 | Dress | Women's Solid Midi Dress - Green | 0.1617 |
| D066 | Dress | Women's Solid Midi Dress - Maroon | 0.1617 |
| D096 | Dress | Women's Casual Fit Dress - Navy Blue | 0.1616 |
| D026 | Dress | Women's Solid Midi Dress - Navy Blue | 0.1570 |
| D086 | Dress | Women's Solid Midi Dress - Floral Pink | 0.1570 |

### Query: `zip closure jacket`

| docID | Category | Title | Cosine score |
|---|---|---|---|
| D058 | Jacket | Women's Quilted Winter Jacket - Black | 0.1180 |
| D018 | Jacket | Women's Quilted Winter Jacket - Beige | 0.1171 |
| D078 | Jacket | Women's Quilted Winter Jacket - Beige | 0.1171 |
| D028 | Jacket | Women's Casual Puffer Jacket - Black | 0.1165 |
| D088 | Jacket | Women's Casual Puffer Jacket - Black | 0.1165 |
| D038 | Jacket | Women's Quilted Winter Jacket - Olive | 0.1157 |
| D048 | Jacket | Women's Casual Puffer Jacket - Beige | 0.1157 |
| D098 | Jacket | Women's Quilted Winter Jacket - Olive | 0.1157 |
| D008 | Jacket | Women's Casual Puffer Jacket - Olive | 0.1143 |
| D068 | Jacket | Women's Casual Puffer Jacket - Olive | 0.1143 |

### Query: `waterproof rain trench coat`

_No matching documents (all query terms are out-of-vocabulary — this is the required OOV test case)._

## Part E.2 — Exact phrase queries

_First 3 are from the assignment's suggested list (kept for direct traceability); the remaining 5 are phrases we constructed ourselves from the corpus, including 3-to-5-word phrases specifically to verify that phrase search genuinely works beyond 2 words, not just for the given 2-word examples._

### Phrase: `"cotton shirt"` (assignment-suggested)

| docID | Category | Title | Start position(s) |
|---|---|---|---|
| D002 | Shirt | Men's Checked Cotton Shirt - Black | [3] |
| D022 | Shirt | Men's Checked Cotton Shirt - White | [3] |
| D042 | Shirt | Men's Checked Cotton Shirt - Maroon | [3] |
| D062 | Shirt | Men's Checked Cotton Shirt - Olive | [3] |
| D082 | Shirt | Men's Checked Cotton Shirt - Blue | [3] |

### Phrase: `"stretch denim"` (assignment-suggested)

| docID | Category | Title | Start position(s) |
|---|---|---|---|
| D003 | Jeans | Men's Regular Fit Denim Jeans - Grey | [10] |
| D013 | Jeans | Men's Slim Fit Stretch Jeans - Grey | [9] |
| D033 | Jeans | Men's Slim Fit Stretch Jeans - Grey | [10] |
| D043 | Jeans | Men's Regular Fit Denim Jeans - Grey | [9] |
| D063 | Jeans | Men's Regular Fit Denim Jeans - Grey | [10] |
| D073 | Jeans | Men's Slim Fit Stretch Jeans - Grey | [9] |
| D093 | Jeans | Men's Slim Fit Stretch Jeans - Grey | [10] |

### Phrase: `"high waist"` (assignment-suggested)

| docID | Category | Title | Start position(s) |
|---|---|---|---|
| D009 | Leggings | Women's High Waist Stretch Leggings - Olive Green | [2, 24] |
| D019 | Leggings | Women's Printed Active Leggings - Black | [22] |
| D029 | Leggings | Women's High Waist Stretch Leggings - Grey | [2, 23] |
| D039 | Leggings | Women's Printed Active Leggings - Olive Green | [23] |
| D049 | Leggings | Women's High Waist Stretch Leggings - Black | [2, 23] |
| D059 | Leggings | Women's Printed Active Leggings - Grey | [22] |
| D069 | Leggings | Women's High Waist Stretch Leggings - Olive Green | [2, 24] |
| D079 | Leggings | Women's Printed Active Leggings - Black | [22] |
| D089 | Leggings | Women's High Waist Stretch Leggings - Grey | [2, 23] |
| D099 | Leggings | Women's Printed Active Leggings - Olive Green | [23] |

### Phrase: `"printed straight kurta"` (original)

| docID | Category | Title | Start position(s) |
|---|---|---|---|
| D014 | Kurta | Women's Printed Straight Kurta - Beige | [2] |
| D034 | Kurta | Women's Printed Straight Kurta - Maroon | [2] |
| D054 | Kurta | Women's Printed Straight Kurta - Mustard | [2] |
| D074 | Kurta | Women's Printed Straight Kurta - Pink | [2] |
| D094 | Kurta | Women's Printed Straight Kurta - Teal | [2] |

### Phrase: `"oversized graphic t shirt"` (original)

| docID | Category | Title | Start position(s) |
|---|---|---|---|
| D011 | T-Shirt | Men's Oversized Graphic T-Shirt - Mustard | [2] |
| D031 | T-Shirt | Men's Oversized Graphic T-Shirt - Olive Green | [2] |
| D051 | T-Shirt | Men's Oversized Graphic T-Shirt - Navy Blue | [2] |
| D071 | T-Shirt | Men's Oversized Graphic T-Shirt - Black | [2] |
| D091 | T-Shirt | Men's Oversized Graphic T-Shirt - Sky Blue | [2] |

### Phrase: `"slim fit stretch jeans"` (original)

| docID | Category | Title | Start position(s) |
|---|---|---|---|
| D013 | Jeans | Men's Slim Fit Stretch Jeans - Grey | [2] |
| D033 | Jeans | Men's Slim Fit Stretch Jeans - Grey | [2] |
| D053 | Jeans | Men's Slim Fit Stretch Jeans - Grey | [2] |
| D073 | Jeans | Men's Slim Fit Stretch Jeans - Grey | [2] |
| D093 | Jeans | Men's Slim Fit Stretch Jeans - Grey | [2] |

### Phrase: `"quilted winter jacket"` (original)

| docID | Category | Title | Start position(s) |
|---|---|---|---|
| D018 | Jacket | Women's Quilted Winter Jacket - Beige | [2] |
| D038 | Jacket | Women's Quilted Winter Jacket - Olive | [2] |
| D058 | Jacket | Women's Quilted Winter Jacket - Black | [2] |
| D078 | Jacket | Women's Quilted Winter Jacket - Beige | [2] |
| D098 | Jacket | Women's Quilted Winter Jacket - Olive | [2] |

### Phrase: `"women high waist stretch leggings"` (original)

| docID | Category | Title | Start position(s) |
|---|---|---|---|
| D009 | Leggings | Women's High Waist Stretch Leggings - Olive Green | [1] |
| D029 | Leggings | Women's High Waist Stretch Leggings - Grey | [1] |
| D049 | Leggings | Women's High Waist Stretch Leggings - Black | [1] |
| D069 | Leggings | Women's High Waist Stretch Leggings - Olive Green | [1] |
| D089 | Leggings | Women's High Waist Stretch Leggings - Grey | [1] |

## Part E.3 — Ordered proximity queries (WITHIN/k)

_First 2 are from the assignment's sample list; the remaining 6 are original, chosen to cover different k values, different term pairs, and — in the case of `men WITHIN/3 jacket` — a deliberate negative case that should and does return zero matches (all Jacket-category items in this corpus are Women's), to demonstrate the system discriminates rather than matching everything._

### `cotton WITHIN/3 shirt` (assignment-suggested)

| docID | Category | Title | Matching (pos1, pos2) pairs |
|---|---|---|---|
| D001 | T-Shirt | Men's Cotton Crew Neck T-Shirt - Black | [(11, 14)] |
| D002 | Shirt | Men's Checked Cotton Shirt - Black | [(3, 4)] |
| D021 | T-Shirt | Men's Cotton Crew Neck T-Shirt - Sky Blue | [(12, 15)] |
| D022 | Shirt | Men's Checked Cotton Shirt - White | [(3, 4)] |
| D041 | T-Shirt | Men's Cotton Crew Neck T-Shirt - Maroon | [(11, 14)] |
| D042 | Shirt | Men's Checked Cotton Shirt - Maroon | [(3, 4)] |
| D061 | T-Shirt | Men's Cotton Crew Neck T-Shirt - White | [(11, 14)] |
| D062 | Shirt | Men's Checked Cotton Shirt - Olive | [(3, 4)] |
| D081 | T-Shirt | Men's Cotton Crew Neck T-Shirt - Mustard | [(11, 14)] |
| D082 | Shirt | Men's Checked Cotton Shirt - Blue | [(3, 4)] |

### `festive WITHIN/4 kurta` (assignment-suggested)

_No document satisfies this proximity constraint._

### `printed WITHIN/3 kurta` (original)

| docID | Category | Title | Matching (pos1, pos2) pairs |
|---|---|---|---|
| D014 | Kurta | Women's Printed Straight Kurta - Beige | [(2, 4)] |
| D034 | Kurta | Women's Printed Straight Kurta - Maroon | [(2, 4)] |
| D054 | Kurta | Women's Printed Straight Kurta - Mustard | [(2, 4)] |
| D074 | Kurta | Women's Printed Straight Kurta - Pink | [(2, 4)] |
| D094 | Kurta | Women's Printed Straight Kurta - Teal | [(2, 4)] |

### `slim WITHIN/2 fit` (original)

| docID | Category | Title | Matching (pos1, pos2) pairs |
|---|---|---|---|
| D002 | Shirt | Men's Checked Cotton Shirt - Black | [(22, 23)] |
| D012 | Shirt | Women's Striped Casual Shirt - Blue | [(22, 23)] |
| D013 | Jeans | Men's Slim Fit Stretch Jeans - Grey | [(2, 3)] |
| D022 | Shirt | Men's Checked Cotton Shirt - White | [(22, 23)] |
| D032 | Shirt | Women's Striped Casual Shirt - Light Pink | [(23, 24)] |
| D033 | Jeans | Men's Slim Fit Stretch Jeans - Grey | [(2, 3)] |
| D042 | Shirt | Men's Checked Cotton Shirt - Maroon | [(22, 23)] |
| D052 | Shirt | Women's Striped Casual Shirt - Beige | [(22, 23)] |
| D053 | Jeans | Men's Slim Fit Stretch Jeans - Grey | [(2, 3)] |
| D062 | Shirt | Men's Checked Cotton Shirt - Olive | [(22, 23)] |
| D072 | Shirt | Women's Striped Casual Shirt - Black | [(22, 23)] |
| D073 | Jeans | Men's Slim Fit Stretch Jeans - Grey | [(2, 3)] |
| D082 | Shirt | Men's Checked Cotton Shirt - Blue | [(22, 23)] |
| D092 | Shirt | Women's Striped Casual Shirt - White | [(22, 23)] |
| D093 | Jeans | Men's Slim Fit Stretch Jeans - Grey | [(2, 3)] |

### `zip WITHIN/3 fly` (original)

| docID | Category | Title | Matching (pos1, pos2) pairs |
|---|---|---|---|
| D003 | Jeans | Men's Regular Fit Denim Jeans - Grey | [(22, 23)] |
| D013 | Jeans | Men's Slim Fit Stretch Jeans - Grey | [(21, 22)] |
| D023 | Jeans | Men's Regular Fit Denim Jeans - Grey | [(21, 22)] |
| D033 | Jeans | Men's Slim Fit Stretch Jeans - Grey | [(22, 23)] |
| D043 | Jeans | Men's Regular Fit Denim Jeans - Grey | [(21, 22)] |
| D053 | Jeans | Men's Slim Fit Stretch Jeans - Grey | [(21, 22)] |
| D063 | Jeans | Men's Regular Fit Denim Jeans - Grey | [(22, 23)] |
| D073 | Jeans | Men's Slim Fit Stretch Jeans - Grey | [(21, 22)] |
| D083 | Jeans | Men's Regular Fit Denim Jeans - Grey | [(21, 22)] |
| D093 | Jeans | Men's Slim Fit Stretch Jeans - Grey | [(22, 23)] |

### `quilted WITHIN/4 jacket` (original)

| docID | Category | Title | Matching (pos1, pos2) pairs |
|---|---|---|---|
| D008 | Jacket | Women's Casual Puffer Jacket - Olive | [(8, 11)] |
| D018 | Jacket | Women's Quilted Winter Jacket - Beige | [(2, 4)] |
| D028 | Jacket | Women's Casual Puffer Jacket - Black | [(8, 11)] |
| D038 | Jacket | Women's Quilted Winter Jacket - Olive | [(2, 4)] |
| D048 | Jacket | Women's Casual Puffer Jacket - Beige | [(8, 11)] |
| D058 | Jacket | Women's Quilted Winter Jacket - Black | [(2, 4)] |
| D068 | Jacket | Women's Casual Puffer Jacket - Olive | [(8, 11)] |
| D078 | Jacket | Women's Quilted Winter Jacket - Beige | [(2, 4)] |
| D088 | Jacket | Women's Casual Puffer Jacket - Black | [(8, 11)] |
| D098 | Jacket | Women's Quilted Winter Jacket - Olive | [(2, 4)] |

### `women WITHIN/6 saree` (original)

| docID | Category | Title | Matching (pos1, pos2) pairs |
|---|---|---|---|
| D005 | Saree | Women's Printed Daily Wear Saree - Blue | [(1, 5)] |
| D015 | Saree | Women's Cotton Handloom Saree - Red | [(1, 4)] |
| D025 | Saree | Women's Printed Daily Wear Saree - Maroon | [(1, 5)] |
| D035 | Saree | Women's Cotton Handloom Saree - Yellow | [(1, 4)] |
| D045 | Saree | Women's Printed Daily Wear Saree - Purple | [(1, 5)] |
| D055 | Saree | Women's Cotton Handloom Saree - Pink | [(1, 4)] |
| D065 | Saree | Women's Printed Daily Wear Saree - Green | [(1, 5)] |
| D075 | Saree | Women's Cotton Handloom Saree - Blue | [(1, 4)] |
| D085 | Saree | Women's Printed Daily Wear Saree - Red | [(1, 5)] |
| D095 | Saree | Women's Cotton Handloom Saree - Maroon | [(1, 4)] |

### `men WITHIN/3 jacket` (original)

_No document satisfies this proximity constraint._

## Part E.4 — Where positional information changes the result

### Case 1: `cotton shirt` — VSM ranks a document the exact phrase search rejects

- Top VSM result: **D001** (score 0.2428), a *T-Shirt* whose text is "...Made from 100% cotton, this t-shirt is designed..." — 'cotton' and 'shirt' both occur, but 3 tokens apart, not adjacent.
- Exact phrase `"cotton shirt"` matches only ['D002', 'D022', 'D042', 'D062', 'D082'] — documents whose *title* literally reads "...Cotton Shirt..." (e.g. D002: "Checked Cotton Shirt"), where the two words are truly adjacent (position gap = 1).
- **D001 is NOT in the phrase-match set at all** — i.e. positional information doesn't just re-order the results here, it changes membership in the result set entirely: bag-of-words VSM cannot distinguish 'made from cotton, this...shirt' from 'cotton shirt', but the positional index can.

### Case 2: `festive kurta` — idf silently zeroes out a query term in VSM, and word ORDER (invisible to VSM) rules out every document in proximity search

- `df('festiv') = 100` out of N = 100 documents — the word 'festive' occurs in the closing boilerplate sentence of *every single document* ("...works well for casual, office, travel, or festive styling..."). Its idf is therefore `log10(100/100) = 0`, so under ltc query weighting 'festive' contributes **exactly zero** to the VSM score, however many times it's repeated. The VSM ranking for `festive kurta` shown below is, in effect, identical to ranking on 'kurta' alone:
| docID | Category | Title | Cosine score |
|---|---|---|---|
| D004 | Kurta | Men's Regular Fit Kurta - Pink | 0.2007 |
| D064 | Kurta | Men's Regular Fit Kurta - White | 0.2007 |
| D034 | Kurta | Women's Printed Straight Kurta - Maroon | 0.1992 |
| D094 | Kurta | Women's Printed Straight Kurta - Teal | 0.1992 |
| D024 | Kurta | Men's Regular Fit Kurta - Teal | 0.1988 |

- Now consider `festive WITHIN/k kurta` for ANY k (we tried k as large as 10): it matches **zero** documents — {}. Inspecting raw positions explains why: in this template-generated corpus, 'kurta' always appears early (it comes from the title-derived opening sentence, e.g. position 4 or 11 in D004), while 'festive' always appears late (from the closing boilerplate, e.g. position 37 in D004) — 'kurta' *always* precedes 'festive', never the other way round, in every single document. Since our proximity search is explicitly **ordered** (term1 must occur before term2), `festive WITHIN/k kurta` can never match, for any k, in any document.
- This is a case positional information doesn't just refine VSM's ranking — it reveals a **structural fact about word order** (kurta-then-festive, never festive-then-kurta) that a bag-of-words model like VSM cannot represent even in principle, since VSM has no notion of sequence at all.

## Novelty — BM25 vs. lnc.ltc VSM comparison

Both models are given the exact same free-text queries. We report the top-5 docIDs from each and flag whether the *ranking* (not just the score scale, which is not comparable across models) differs.

| Query | lnc.ltc top-5 (docID order) | BM25 top-5 (docID order) | Same order? |
|---|---|---|---|
| cotton shirt | ['D001', 'D041', 'D061', 'D081', 'D022'] | ['D001', 'D041', 'D061', 'D081', 'D021'] | No |
| winter jacket | ['D058', 'D018', 'D078', 'D038', 'D098'] | ['D018', 'D058', 'D078', 'D038', 'D098'] | No |
| regular fit kurta | ['D004', 'D064', 'D024', 'D084', 'D044'] | ['D004', 'D024', 'D064', 'D084', 'D044'] | No |
| high waist leggings | ['D029', 'D049', 'D089', 'D009', 'D069'] | ['D029', 'D049', 'D089', 'D009', 'D069'] | Yes |
| festive saree | ['D035', 'D055', 'D095', 'D005', 'D025'] | ['D035', 'D055', 'D095', 'D005', 'D015'] | No |
| breathable fabric t-shirt | ['D011', 'D071', 'D001', 'D041', 'D061'] | ['D011', 'D071', 'D001', 'D041', 'D061'] | Yes |
| stretch denim jeans | ['D013', 'D073', 'D043', 'D033', 'D093'] | ['D013', 'D073', 'D043', 'D033', 'D093'] | Yes |
| warm fleece hoodie | ['D037', 'D097', 'D057', 'D017', 'D077'] | ['D037', 'D097', 'D057', 'D017', 'D077'] | Yes |
| printed dress | ['D076', 'D036', 'D046', 'D016', 'D056'] | ['D036', 'D076', 'D006', 'D046', 'D056'] | No |
| zip closure jacket | ['D058', 'D018', 'D078', 'D028', 'D088'] | ['D018', 'D058', 'D078', 'D028', 'D038'] | No |
