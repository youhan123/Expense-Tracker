# Expense Tracker V3

A responsive expense tracking dashboard built with plain **HTML, CSS and JavaScript**: no frameworks, no libraries, no build step. This is the third version of a learning project, built to practise frontend fundamentals.

## Features

**Dashboard**
- Summary cards: total expenses, this month, number of transactions, highest expense
- Expense Overview: a bar chart of this month's spending by category, sorted from largest to smallest

**Expenses page**
- Add, edit and delete expenses (with a delete confirmation dialog)
- Search by description
- Filter by category and by month
- Sort by newest, oldest, highest or lowest amount
- Empty states for "no expenses yet" and "no matching results"

**General**
- Dark mode, remembered between visits and between pages
- Responsive layout: full sidebar on desktop, icon-only sidebar on tablet, slide-out menu and card-style table on mobile
- Toast notifications for success, error and warning messages
- Data saved in the browser with `localStorage`
- Semantic HTML and accessible form labels, dialogs and buttons

## Tech Stack

| Layer | Technology |
|---|---|
| Structure | HTML5 (semantic elements, `<dialog>`, `<progress>`, `<table>`) |
| Styling | CSS3 (custom properties, Grid, Flexbox, media queries) |
| Logic | Vanilla JavaScript (ES6+) |
| Storage | `localStorage` |

## Project Structure

```
expense-tracker-v3/
├── index.html      # Dashboard page
├── expenses.html   # Expenses page (table, filters, modals)
├── style.css       # All styles, including dark mode and responsive rules
├── script.js       # All logic, shared by both pages
└── README.md
```

## Getting Started

No installation is needed. You only need a modern browser.

Because the two pages share data through `localStorage`, run the project with a local server instead of opening the files directly (some browsers do not share `localStorage` between separate `file://` pages).

**Option 1: VS Code Live Server**
1. Install the **Live Server** extension.
2. Right-click `index.html` and choose **Open with Live Server**.

**Option 2: Python**
```bash
python -m http.server 8000
```
Then open <http://localhost:8000> in your browser.

## How It Works

- **Data:** each expense is an object with `id`, `date` (`YYYY-MM-DD`), `category`, `description` and `amount`. The list is saved in `localStorage` under the key `expenseTracker.expenses`, and the theme under `expenseTracker.theme`.
- **First run:** the app loads 12 sample expenses so the pages are not empty.
- **Rendering:** the Expenses page keeps its filter values in a `state` object. Any change updates `state` and calls `renderExpenses()`, which redraws the table.
- **Two pages, one script:** `script.js` checks which elements exist on the current page and only runs the code for that page.
- **Dashboard search:** the header search is a plain HTML form that opens `expenses.html?q=your-search`. The Expenses page reads `q` and fills the search box.

## Resetting the Data

Open the browser console and run:

```js
localStorage.clear();
```

Then reload the page to get the sample data back.

## Known Limitations

- Data lives only in one browser on one device. Clearing browser data deletes it.
- The Reports and Settings links are placeholders; those pages do not exist yet.
- "This Month" uses today's date, so it shows RM 0.00 if no expenses are dated in the current month.
- Currency is fixed to Malaysian Ringgit (RM).
- There are no automated tests yet.

## Version History

| Version | Stack | Status |
|---|---|---|
| V1 | Python + JSON | Done |
| V2 | Python + SQLite | Done |
| **V3** | **HTML + CSS + JavaScript** | **This project** |
| V4 (planned) | FastAPI + PostgreSQL + React | Planned |

## Ideas for Future Improvements

- Reports page with monthly and yearly charts
- Settings page (currency, default category, name)
- Export expenses to CSV
- Monthly budget with a warning when it is exceeded
- Total of the currently filtered expenses
- Custom categories
- Connect to the FastAPI backend in the next version

## What I Learned

- Writing semantic, accessible HTML
- Building a responsive layout with CSS Grid, Flexbox and custom properties
- Implementing dark mode by swapping CSS variables
- Managing application state and re-rendering in plain JavaScript
- Using event delegation, `localStorage` and the native `<dialog>` element
- Structuring a multi-page app that shares one script

