"use strict";

/* ==========================================================
   EXPENSE TRACKER V3 - script.js
   Used by BOTH index.html (dashboard) and expenses.html.
   Sections:
   1. Constants & sample data     6. Toasts
   2. Small helpers               7. Dialog helpers
   3. Storage (localStorage)      8. Dashboard page
   4. Theme (dark mode)           9. Expenses page
   5. Mobile menu                 10. Start the app
   ========================================================== */


/* ---------- 1. CONSTANTS & SAMPLE DATA ---------- */
const STORAGE_KEY = "expenseTracker.expenses";
const THEME_KEY = "expenseTracker.theme";
const TOAST_DURATION = 3500; // milliseconds

// Keys match the CSS class names (category-food) and the <option> values
const CATEGORIES = {
  food: "Food & Beverages",
  transport: "Transport",
  bills: "Bills",
  entertainment: "Entertainment",
  others: "Others",
};

// Used only the very first time the app runs (when nothing is saved yet)
const SAMPLE_EXPENSES = [
  { id: "1", date: "2026-10-22", category: "food", description: "Lunch", amount: 15 },
  { id: "2", date: "2026-10-21", category: "transport", description: "Grab", amount: 12 },
  { id: "3", date: "2026-10-20", category: "bills", description: "Internet", amount: 89 },
  { id: "4", date: "2026-10-18", category: "entertainment", description: "Cinema", amount: 32 },
  { id: "5", date: "2026-10-15", category: "food", description: "Groceries", amount: 180 },
  { id: "6", date: "2026-10-10", category: "others", description: "Birthday gift", amount: 45 },
  { id: "7", date: "2026-09-28", category: "bills", description: "Electricity", amount: 120 },
  { id: "8", date: "2026-09-20", category: "food", description: "Dinner", amount: 48 },
  { id: "9", date: "2026-09-12", category: "transport", description: "Petrol", amount: 60 },
  { id: "10", date: "2026-09-05", category: "entertainment", description: "Concert ticket", amount: 150 },
  { id: "11", date: "2026-08-25", category: "bills", description: "Phone plan", amount: 65 },
  { id: "12", date: "2026-08-14", category: "food", description: "Brunch", amount: 38 },
];


/* ---------- 2. SMALL HELPERS ---------- */

// Shortcut for document.querySelector
const $ = (selector, parent = document) => parent.querySelector(selector);

// Create an element, optionally with a class and text.
// textContent is used (not innerHTML), so user input can never inject HTML.
function createElement(tag, className, text) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text !== undefined) element.textContent = text;
  return element;
}

function formatCurrency(amount) {
  return "RM " + amount.toLocaleString("en-MY", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

// "2026-10-22" -> "22/10/2026" (string split avoids time zone surprises)
function formatDate(isoDate) {
  const [year, month, day] = isoDate.split("-");
  return `${day}/${month}/${year}`;
}

// "2026-10" -> "October 2026"
function formatMonth(monthKey) {
  const [year, month] = monthKey.split("-");
  return new Date(Number(year), Number(month) - 1, 1).toLocaleDateString("en-GB", {
    month: "long",
    year: "numeric",
  });
}

// Today's date as "YYYY-MM-DD" in the user's local time
function getTodayISO() {
  const now = new Date();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `${now.getFullYear()}-${month}-${day}`;
}

// "YYYY-MM" for the current month
function getCurrentMonthKey() {
  return getTodayISO().slice(0, 7);
}

function createId() {
  if (typeof crypto !== "undefined" && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return Date.now().toString() + Math.random().toString(16).slice(2);
}

function sumAmounts(expenses) {
  return expenses.reduce((total, expense) => total + expense.amount, 0);
}


/* ---------- 3. STORAGE (localStorage) ---------- */
function loadExpenses() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);

    // Nothing saved yet: start with the sample data
    if (saved === null) {
      const samples = SAMPLE_EXPENSES.map((expense) => ({ ...expense }));
      saveExpenses(samples);
      return samples;
    }

    const parsed = JSON.parse(saved);
    return Array.isArray(parsed) ? parsed : [];
  } catch (error) {
    console.error("Could not load expenses:", error);
    return [];
  }
}

function saveExpenses(expenses) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(expenses));
  } catch (error) {
    console.error("Could not save expenses:", error);
    showToast("error", "Could not save your data.");
  }
}


/* ---------- 4. THEME (DARK MODE) ---------- */
function applyTheme(theme) {
  const isDark = theme === "dark";
  document.body.classList.toggle("dark-mode", isDark);

  const button = $("#theme-toggle");
  if (button) {
    button.textContent = isDark ? "Light mode" : "Dark mode";
    button.setAttribute("aria-pressed", String(isDark));
  }
}

function initTheme() {
  let savedTheme = null;
  try {
    savedTheme = localStorage.getItem(THEME_KEY);
  } catch (error) {
    console.error("Could not read theme:", error);
  }

  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  applyTheme(savedTheme || (prefersDark ? "dark" : "light"));

  const button = $("#theme-toggle");
  if (!button) return;

  button.addEventListener("click", () => {
    const nextTheme = document.body.classList.contains("dark-mode") ? "light" : "dark";
    applyTheme(nextTheme);
    try {
      localStorage.setItem(THEME_KEY, nextTheme);
    } catch (error) {
      console.error("Could not save theme:", error);
    }
  });
}


/* ---------- 5. MOBILE MENU ---------- */
function initMobileMenu() {
  const sidebar = $("#sidebar");
  const toggle = $("#menu-toggle");
  if (!sidebar || !toggle) return;

  function setOpen(isOpen) {
    sidebar.classList.toggle("is-open", isOpen);
    toggle.setAttribute("aria-expanded", String(isOpen));
  }

  toggle.addEventListener("click", () => {
    setOpen(!sidebar.classList.contains("is-open"));
  });

  // Close with the Escape key
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") setOpen(false);
  });

  // Close when clicking anywhere outside the sidebar
  document.addEventListener("click", (event) => {
    if (!sidebar.contains(event.target) && !toggle.contains(event.target)) {
      setOpen(false);
    }
  });
}


/* ---------- 6. TOASTS ---------- */
const toastTimers = {}; // one timer per toast type

// type is "success", "error" or "warning" (matches #toast-success etc.)
function showToast(type, message) {
  const toast = $(`#toast-${type}`);
  if (!toast) return;

  if (message) $(".toast-message", toast).textContent = message;
  toast.hidden = false;

  clearTimeout(toastTimers[type]); // restart the timer if it is already visible
  toastTimers[type] = setTimeout(() => {
    toast.hidden = true;
  }, TOAST_DURATION);
}

function initToasts() {
  const container = $("#toast-container");
  if (!container) return;

  // One listener on the container handles all three close buttons
  container.addEventListener("click", (event) => {
    const closeButton = event.target.closest(".toast-close");
    if (closeButton) closeButton.closest(".toast").hidden = true;
  });
}


/* ---------- 7. DIALOG HELPERS ---------- */
function initDialogs() {
  // Every Cancel button closes the dialog it sits in
  document.querySelectorAll(".cancel-btn").forEach((button) => {
    button.addEventListener("click", () => button.closest("dialog").close());
  });

  // Clicking the dark backdrop (outside the box) closes the dialog
  document.querySelectorAll("dialog.modal").forEach((dialog) => {
    dialog.addEventListener("click", (event) => {
      if (event.target !== dialog) return; // click was on something inside
      const box = dialog.getBoundingClientRect();
      const clickedOutside =
        event.clientX < box.left ||
        event.clientX > box.right ||
        event.clientY < box.top ||
        event.clientY > box.bottom;
      if (clickedOutside) dialog.close();
    });
  });
}


/* ---------- 8. DASHBOARD PAGE (index.html) ---------- */
function initDashboard() {
  const expenses = loadExpenses();
  renderSummary(expenses);
  renderChart(expenses);
}

function renderSummary(expenses) {
  const monthKey = getCurrentMonthKey();
  const thisMonth = expenses.filter((expense) => expense.date.startsWith(monthKey));
  const highest = expenses.reduce((max, expense) => Math.max(max, expense.amount), 0);

  $("#total-expenses").textContent = formatCurrency(sumAmounts(expenses));
  $("#monthly-expenses").textContent = formatCurrency(sumAmounts(thisMonth));
  $("#expense-count").textContent = expenses.length;
  $("#highest-expense").textContent = formatCurrency(highest);
}

function renderChart(expenses) {
  const list = $("#expense-chart");
  const monthKey = getCurrentMonthKey();
  const thisMonth = expenses.filter((expense) => expense.date.startsWith(monthKey));
  const monthTotal = sumAmounts(thisMonth);

  // Total per category, biggest first
  const categoryTotals = Object.keys(CATEGORIES)
    .map((key) => ({
      key,
      total: sumAmounts(thisMonth.filter((expense) => expense.category === key)),
    }))
    .sort((a, b) => b.total - a.total);

  categoryTotals.forEach(({ key, total }) => {
    const percent = monthTotal > 0 ? Math.round((total / monthTotal) * 100) : 0;

    const bar = $(`#chart-${key}`);
    bar.value = percent;
    bar.textContent = `${percent}%`;
    $(`#chart-${key}-amount`).textContent = formatCurrency(total);

    // Appending an element that is already in the list moves it,
    // so the rows end up sorted from biggest to smallest.
    list.appendChild($(`.chart-row[data-category="${key}"]`));
  });
}


/* ---------- 9. EXPENSES PAGE (expenses.html) ---------- */

// Elements (they are null on the dashboard, so we only use them on this page)
const ui = {
  tableBody: $("#expense-table-body"),
  tableWrapper: $("#table-wrapper"),
  emptyState: $("#empty-state"),
  search: $("#expense-search"),
  categoryFilter: $("#category-filter"),
  monthFilter: $("#date-filter"),
  sortFilter: $("#sort-filter"),
  addModal: $("#add-expense-modal"),
  addForm: $("#add-expense-form"),
  editModal: $("#edit-expense-modal"),
  editForm: $("#edit-expense-form"),
  deleteModal: $("#delete-confirmation"),
};

// Everything the page needs to remember while it is open
const state = {
  expenses: [],
  search: "",
  category: "all",
  month: "all",
  sort: "newest",
  deletingId: null,
};

function initExpensesPage() {
  state.expenses = loadExpenses();

  // Dashboard search sends us here as expenses.html?q=something
  const query = new URLSearchParams(window.location.search).get("q");
  if (query) {
    ui.search.value = query;
    state.search = query.trim().toLowerCase();
  }

  populateMonthFilter();
  renderExpenses();
  bindExpenseEvents();
}

/* ----- Filtering, sorting and rendering ----- */
function getVisibleExpenses() {
  const visible = state.expenses.filter((expense) => {
    const matchesSearch = expense.description.toLowerCase().includes(state.search);
    const matchesCategory = state.category === "all" || expense.category === state.category;
    const matchesMonth = state.month === "all" || expense.date.startsWith(state.month);
    return matchesSearch && matchesCategory && matchesMonth;
  });

  // ISO dates ("2026-10-22") sort correctly as plain text
  const sorters = {
    newest: (a, b) => b.date.localeCompare(a.date),
    oldest: (a, b) => a.date.localeCompare(b.date),
    highest: (a, b) => b.amount - a.amount,
    lowest: (a, b) => a.amount - b.amount,
  };
  return visible.sort(sorters[state.sort]);
}

function renderExpenses() {
  const visible = getVisibleExpenses();
  ui.tableBody.replaceChildren(...visible.map(createExpenseRow));

  const isEmpty = visible.length === 0;
  ui.tableWrapper.hidden = isEmpty;
  ui.emptyState.hidden = !isEmpty;
  if (isEmpty) updateEmptyState(state.expenses.length === 0);
}

// Two kinds of "empty": no expenses at all, or no expenses match the filters
function updateEmptyState(hasNoExpenses) {
  $(".empty-state-title", ui.emptyState).textContent = hasNoExpenses
    ? "No expenses yet"
    : "No matching expenses";
  $(".empty-state-text", ui.emptyState).textContent = hasNoExpenses
    ? "Start tracking your spending by adding your first expense."
    : "Try changing your search or filters.";
  $("#empty-add-expense-btn").hidden = !hasNoExpenses;
}

// Rebuild the month dropdown from the months that exist in the data
function populateMonthFilter() {
  const months = [...new Set(state.expenses.map((expense) => expense.date.slice(0, 7)))]
    .sort()
    .reverse();
  const previous = ui.monthFilter.value;

  ui.monthFilter.replaceChildren(
    new Option("All Months", "all"),
    ...months.map((month) => new Option(formatMonth(month), month))
  );

  ui.monthFilter.value = months.includes(previous) ? previous : "all";
  state.month = ui.monthFilter.value;
}

/* ----- Building table rows (same HTML structure as expenses.html) ----- */
function createCell(label, className) {
  const cell = createElement("td", className);
  cell.dataset.label = label; // used by the mobile card layout in CSS
  return cell;
}

function createActionButton(text, className, ariaLabel) {
  const button = createElement("button", className, text);
  button.type = "button";
  button.setAttribute("aria-label", ariaLabel);
  return button;
}

function createExpenseRow(expense) {
  const row = createElement("tr", "expense-row");
  row.dataset.expenseId = expense.id;

  const dateCell = createCell("Date");
  const time = createElement("time", "", formatDate(expense.date));
  time.dateTime = expense.date;
  dateCell.appendChild(time);

  const categoryCell = createCell("Category");
  categoryCell.appendChild(
    createElement(
      "span",
      `category-badge category-${expense.category}`,
      CATEGORIES[expense.category] || expense.category
    )
  );

  const descriptionCell = createCell("Description");
  descriptionCell.textContent = expense.description;

  const amountCell = createCell("Amount", "amount");
  amountCell.textContent = formatCurrency(expense.amount);

  const actionsCell = createCell("Actions", "actions");
  actionsCell.append(
    createActionButton(
      "Edit",
      "btn btn-secondary edit-expense-btn",
      `Edit ${expense.description} expense`
    ),
    createActionButton(
      "Delete",
      "btn btn-danger delete-expense-btn",
      `Delete ${expense.description} expense`
    )
  );

  row.append(dateCell, categoryCell, descriptionCell, amountCell, actionsCell);
  return row;
}

/* ----- Add, edit and delete ----- */

// Read and validate a form. Returns an expense object, or null if invalid.
function readExpenseForm(form) {
  const data = new FormData(form);
  const expense = {
    date: data.get("date"),
    category: data.get("category"),
    description: String(data.get("description")).trim(), // "   " is not valid
    amount: Number.parseFloat(data.get("amount")),
  };

  const isValid =
    expense.date &&
    CATEGORIES[expense.category] &&
    expense.description &&
    expense.amount > 0;

  if (!isValid) {
    showToast("warning", "Please check your input and try again.");
    return null;
  }

  expense.amount = Math.round(expense.amount * 100) / 100; // 2 decimal places
  return expense;
}

// Save, then refresh everything that depends on the data
function saveAndRefresh(message) {
  saveExpenses(state.expenses);
  populateMonthFilter();
  renderExpenses();
  showToast("success", message);
}

function openAddModal() {
  ui.addForm.reset();
  $("#add-date").value = getTodayISO();
  ui.addModal.showModal();
}

function openEditModal(id) {
  const expense = state.expenses.find((item) => item.id === id);
  if (!expense) return;

  $("#edit-id").value = expense.id;
  $("#edit-date").value = expense.date;
  $("#edit-category").value = expense.category;
  $("#edit-description").value = expense.description;
  $("#edit-amount").value = expense.amount;
  ui.editModal.showModal();
}

function openDeleteModal(id) {
  state.deletingId = id;
  ui.deleteModal.showModal();
}

function handleAddSubmit(event) {
  event.preventDefault();
  const data = readExpenseForm(ui.addForm);
  if (!data) return;

  state.expenses.push({ id: createId(), ...data });
  ui.addModal.close();
  saveAndRefresh("Expense added successfully");
}

function handleEditSubmit(event) {
  event.preventDefault();
  const data = readExpenseForm(ui.editForm);
  if (!data) return;

  const expense = state.expenses.find((item) => item.id === $("#edit-id").value);
  if (!expense) {
    showToast("error", "Could not find that expense.");
    return;
  }

  Object.assign(expense, data); // copies the new values onto the existing object
  ui.editModal.close();
  saveAndRefresh("Expense updated successfully");
}

function handleConfirmDelete() {
  if (state.deletingId === null) return;

  state.expenses = state.expenses.filter((item) => item.id !== state.deletingId);
  ui.deleteModal.close();
  saveAndRefresh("Expense deleted successfully");
}

/* ----- Event listeners for this page ----- */
function bindExpenseEvents() {
  // Filters, search and sort
  ui.search.addEventListener("input", () => {
    state.search = ui.search.value.trim().toLowerCase();
    renderExpenses();
  });
  ui.categoryFilter.addEventListener("change", () => {
    state.category = ui.categoryFilter.value;
    renderExpenses();
  });
  ui.monthFilter.addEventListener("change", () => {
    state.month = ui.monthFilter.value;
    renderExpenses();
  });
  ui.sortFilter.addEventListener("change", () => {
    state.sort = ui.sortFilter.value;
    renderExpenses();
  });

  // Add buttons (the normal one and the one inside the empty state)
  $("#add-expense-btn").addEventListener("click", openAddModal);
  $("#empty-add-expense-btn").addEventListener("click", openAddModal);

  // Edit and Delete buttons live inside rows that are rebuilt often,
  // so we listen once on the table body (event delegation).
  ui.tableBody.addEventListener("click", (event) => {
    const row = event.target.closest(".expense-row");
    if (!row) return;
    const id = row.dataset.expenseId;

    if (event.target.closest(".edit-expense-btn")) openEditModal(id);
    if (event.target.closest(".delete-expense-btn")) openDeleteModal(id);
  });

  // Forms and delete confirmation
  ui.addForm.addEventListener("submit", handleAddSubmit);
  ui.editForm.addEventListener("submit", handleEditSubmit);
  $("#confirm-delete-btn").addEventListener("click", handleConfirmDelete);

  // Forget which expense was being deleted if the dialog closes any way
  ui.deleteModal.addEventListener("close", () => {
    state.deletingId = null;
  });
}


/* ---------- 10. START THE APP ---------- */
function init() {
  // Runs on every page
  initTheme();
  initMobileMenu();
  initToasts();
  initDialogs();

  // Runs only on the page that has these elements
  if ($("#expense-chart")) initDashboard();
  if (ui.tableBody) initExpensesPage();
}

init();