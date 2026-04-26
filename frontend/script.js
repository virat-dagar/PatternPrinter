const patternSelect = document.querySelector("#patternSelect");
const symbolInput = document.querySelector("#symbolInput");
const sizeInput = document.querySelector("#sizeInput");
const widthInput = document.querySelector("#widthInput");
const heightInput = document.querySelector("#heightInput");
const rectangleFields = document.querySelector(".rectangle-only");
const lineFields = document.querySelector(".line-only");
const categoryTabs = document.querySelector("#categoryTabs");
const activeCategoryLabel = document.querySelector("#activeCategory");
const dimensionMode = document.querySelector("#dimensionMode");
const patternCount = document.querySelector("#patternCount");
const categoryPill = document.querySelector("#categoryPill");
const shapePill = document.querySelector("#shapePill");
const detailTitle = document.querySelector("#detailTitle");
const description = document.querySelector("#patternDescription");
const previewTitle = document.querySelector("#previewTitle");
const output = document.querySelector("#patternOutput");
const rowCount = document.querySelector("#rowCount");
const charCount = document.querySelector("#charCount");
const copyButton = document.querySelector("#copyButton");

let patterns = [];
let activeCategory = "All";

async function loadPatterns() {
  const response = await fetch("/api/patterns");
  const data = await response.json();
  patterns = data.patterns;
  patternCount.textContent = patterns.length;

  renderCategoryTabs();
  syncPatternOptions("diamond-hollow");
  await render();
}

function renderCategoryTabs() {
  const categories = ["All", ...new Set(patterns.map((pattern) => pattern.category))];
  categoryTabs.innerHTML = categories
    .map((category) => {
      const count = category === "All" ? patterns.length : patterns.filter((pattern) => pattern.category === category).length;
      return `<button class="category-tab${category === activeCategory ? " is-active" : ""}" type="button" data-category="${category}">${category} ${count}</button>`;
    })
    .join("");

  categoryTabs.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", async () => {
      activeCategory = button.dataset.category;
      renderCategoryTabs();
      syncPatternOptions();
      await render();
    });
  });
}

function syncPatternOptions(preferredId = patternSelect.value) {
  const visiblePatterns = getVisiblePatterns();
  const selectedPattern = visiblePatterns.find((pattern) => pattern.id === preferredId) || visiblePatterns[0];

  patternSelect.innerHTML = visiblePatterns
    .map((pattern) => `<option value="${pattern.id}">${pattern.name}</option>`)
    .join("");

  patternSelect.value = selectedPattern.id;
  activeCategoryLabel.textContent = activeCategory;
}

function getVisiblePatterns() {
  if (activeCategory === "All") {
    return patterns;
  }
  return patterns.filter((pattern) => pattern.category === activeCategory);
}

async function render() {
  const pattern = patterns.find((item) => item.id === patternSelect.value);
  if (!pattern) return;

  setDimensionMode(pattern.requires_rectangle);
  categoryPill.textContent = pattern.category;
  shapePill.textContent = pattern.shape;
  detailTitle.textContent = pattern.name;
  description.textContent = pattern.description;
  previewTitle.textContent = pattern.name;

  const params = new URLSearchParams({
    pattern: pattern.id,
    symbol: symbolInput.value || "*",
  });

  if (pattern.requires_rectangle) {
    params.set("width", widthInput.value);
    params.set("height", heightInput.value);
  } else {
    params.set("size", sizeInput.value);
  }

  const response = await fetch(`/api/render?${params.toString()}`);
  const data = await response.json();
  const text = data.output || data.error || "Unable to render pattern.";

  output.textContent = text;
  updateOutputStats(text);
}

function setDimensionMode(isRectangle) {
  rectangleFields.hidden = !isRectangle;
  lineFields.hidden = isRectangle;
  widthInput.disabled = !isRectangle;
  heightInput.disabled = !isRectangle;
  sizeInput.disabled = isRectangle;
  dimensionMode.textContent = isRectangle ? "Width x Height" : "Lines";
}

function updateOutputStats(text) {
  const rows = text ? text.split("\n") : [];
  const chars = rows.join("").length;
  rowCount.textContent = `${rows.length} ${rows.length === 1 ? "row" : "rows"}`;
  charCount.textContent = `${chars} chars`;
}

async function copyPattern() {
  await navigator.clipboard.writeText(output.textContent);
  copyButton.textContent = "Copied";
  window.setTimeout(() => {
    copyButton.textContent = "Copy";
  }, 1200);
}

patternSelect.addEventListener("change", render);
[symbolInput, sizeInput, widthInput, heightInput].forEach((element) => {
  element.addEventListener("input", render);
});

copyButton.addEventListener("click", copyPattern);
loadPatterns();
