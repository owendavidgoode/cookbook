# Cover Design Brief: "You Can Just Do Things"

## CRITICAL REQUIREMENTS

1. **Photo-realistic screenshot** — must look like a real Emacs window
2. **Crisp, clean, no grain** — sharp pixel-perfect text
3. **2100 x 3000 pixels** (7" x 10" at 300 DPI)
4. **PURE BLACK background (#0d0d0d)** — NOT gray, NOT charcoal, BLACK
5. **Clean monospace font** — Menlo, SF Mono, or Consolas. NOT italic. NOT stylized.

---

## THE TITLE — THIS IS THE MOST IMPORTANT PART

### DO NOT use ASCII art. Use plain bold monospace text:

```
YOU CAN
JUST DO
THINGS
```

### Title specifications:
- **Font**: Bold monospace (Menlo, SF Mono, or Consolas)
- **Color**: Cyan (#87ceeb)
- **Size**: VERY LARGE — the title should fill the **top 35-40%** of the image
- **Must be readable from across a room / as a tiny thumbnail**
- Each word group on its own line
- Generous vertical spacing between lines (at least 1.5x line height)

### Visual reference for title size:
```
┌─────────────────────────────────┐
│ File Edit Options Buffers Tools │  ← thin menu bar
├─────────────────────────────────┤
│                                 │
│         YOU CAN                 │  ← HUGE text
│                                 │
│         JUST DO                 │  ← HUGE text
│                                 │
│         THINGS                  │  ← HUGE text
│                                 │
│ ;; A Data Portrait of John...  │  ← small subtitle
├─────────────────────────────────┤
│ grep results here...            │  ← medium text
│                                 │
│ stats here...                   │
│                                 │
│ ;; Author: Owen D. Goode        │
├─────────────────────────────────┤
│ mode line                       │  ← thin bar
└─────────────────────────────────┘
```

The title takes up roughly **1/3 of the total height**.

---

## LAYOUT (Top to Bottom)

### 1. Menu Bar
Thin gray bar (#3a3a3a), 2-3% of image height:
```
File  Edit  Options  Buffers  Tools  Help
```
White text, small font.

### 2. Title Area (35-40% of image)
Plain bold monospace text, centered:
```
YOU CAN
JUST DO
THINGS
```
- Cyan (#87ceeb)
- LARGE font size
- Lots of vertical padding above and below

### 3. Subtitle
Small green text (#98fb98):
```
;; A Data Portrait of John D. Cook's Blog
```

### 4. Grep Section Header
```
-*- mode: grep; default-directory: "~/code/" -*-
grep -rn "johndcook.com" .
```
Orange (#ffa500) for the mode line, white for the command.

### 5. Grep Results (5-6 results max)
**Important: Add a blank line between EACH result.**

```
./pandas/_libs/groupby.pyx:128:# johndcook.com/blog/skewness_kurtosis/

./OnlineStats.jl/src/stats.jl:85:# johndcook.com/blog/standard_deviation/

./boost/accumulators/variance.hpp:204:// johndcook.com/blog/skewness_kurtosis/

./scipy/special/_loggamma.pxd:46:# johndcook.com/blog/gamma_function/

./numpy/random/_common.pyx:313:# johndcook.com/blog/ziggurat/
```

Colors:
- File paths: Light blue (#add8e6)
- Line numbers: Coral red (#ff6347)
- "johndcook.com": **Bright yellow (#ffff00)** — highlighted search match
- Everything else: White (#ffffff)

### 6. Match Count
Green (#98fb98):
```
Grep finished with 847 matches found
```

### 7. Stats (Emacs Lisp)
```
(setq blog-stats
      '((posts . 5233)
        (years . 17)
        (words . "1.8M")))
```
- `setq`: Cyan
- Numbers: Red/coral
- Strings: Orange

### 8. Author
Green (#98fb98):
```
;; Author: Owen D. Goode
```

### 9. Mode Line
Thin gray bar at bottom:
```
-UUU:%%--  *grep*      Bot L847   (Grep)
```

---

## COLOR PALETTE

| Element | Hex |
|---------|-----|
| Background | #1c1c1c |
| Menu/mode bars | #3a3a3a |
| Title | #87ceeb |
| Comments/green | #98fb98 |
| File paths | #add8e6 |
| Line numbers | #ff6347 |
| Search match | #ffff00 |
| Strings | #ffa500 |
| Normal text | #ffffff |
| Dim/muted | #6a6a6a |

---

## SPACING RULES

- **Double-space** between the three title lines
- **Blank line** between each grep result
- **Generous padding** above and below the title block
- The image should feel **airy, not cramped**

---

## WHAT TO AVOID

- ❌ Complex ASCII art fonts (they become illegible)
- ❌ Dense, cramped text
- ❌ Grainy or noisy texture
- ❌ Small title that doesn't stand out
- ❌ Gradients or glows
- ❌ Any non-monospace fonts

---

## CONTEXT

John D. Cook's blog (johndcook.com/blog, 2008-2024) published 5,233 posts about math and computing. His articles are cited in the source code of pandas, scipy, numpy, boost, Julia, TensorFlow, and hundreds of other projects. This cover visualizes that hidden influence: a grep search revealing his name everywhere in open-source code.
