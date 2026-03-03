// Unidades disponibles por categoria
const units = {
    temperatura: ["celsius", "fahrenheit", "kelvin"],
    longitud: ["m", "km", "mi", "ft"],
    peso: ["kg", "lb", "g"],
    velocidad: ["kmh", "mph", "ms"],
};

// Etiquetas legibles para mostrar en UI
const labels = {
    temperatura: { celsius: "°C", fahrenheit: "°F", kelvin: "K" },
    longitud: { m: "m", km: "km", mi: "mi", ft: "ft" },
    peso: { kg: "kg", lb: "lb", g: "g" },
    velocidad: { kmh: "km/h", mph: "mph", ms: "m/s" },
};

let currentCat = "temperatura";
let history = [];
const THEME_KEY = "themeMode";
const systemThemeQuery = window.matchMedia("(prefers-color-scheme: dark)");

function resolveTheme(mode) {
    if (mode === "auto") return systemThemeQuery.matches ? "dark" : "light";
    return mode;
}

function applyTheme(mode) {
    const resolvedTheme = resolveTheme(mode);
    document.documentElement.setAttribute("data-theme", resolvedTheme);
}

function initThemeMode() {
    const themeSelect = document.getElementById("theme-mode");
    if (!themeSelect) return;

    const savedMode = localStorage.getItem(THEME_KEY) || "auto";
    themeSelect.value = savedMode;
    applyTheme(savedMode);

    themeSelect.addEventListener("change", () => {
        const selectedMode = themeSelect.value;
        localStorage.setItem(THEME_KEY, selectedMode);
        applyTheme(selectedMode);
    });

    systemThemeQuery.addEventListener("change", () => {
        const currentMode = localStorage.getItem(THEME_KEY) || "auto";
        if (currentMode === "auto") applyTheme("auto");
    });
}


/**
 * LOGICA DE CONVERSION (llamada al servidor Flask)
 * El servidor Flask comunica con ICE en puerto 10000
 */
async function convert(cat, valor, desde, hasta) {
    if (desde === hasta) return valor;

    try {
        const response = await fetch('/api/convert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                categoria: cat,
                valor: valor,
                desde: desde,
                hasta: hasta
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error en la conversión');
        }

        const data = await response.json();
        return data.resultado;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}


//UI: poblar selects al cambiar categoria

function populateSelects(cat) {
    const desdeEl = document.getElementById("desde");
    const hastaEl = document.getElementById("hasta");
    const opts = units[cat];

    desdeEl.innerHTML = opts.map(u =>
        `<option value="${u}">${labels[cat][u] || u}</option>`
    ).join("");

    hastaEl.innerHTML = opts.map(u =>
        `<option value="${u}">${labels[cat][u] || u}</option>`
    ).join("");

    if (opts.length > 1) hastaEl.value = opts[1];
}

/**
 * UI: ejecutar conversion y mostrar resultado
 */
async function doConvert() {
    const valor = parseFloat(document.getElementById("valor").value);
    const desde = document.getElementById("desde").value;
    const hasta = document.getElementById("hasta").value;
    const resEl = document.getElementById("result");
    const unitEl = document.getElementById("result-unit");

    if (isNaN(valor)) {
        resEl.className = "screen-value error";
        resEl.textContent = "Ingresa un valor";
        unitEl.textContent = "";
        return;
    }

    // Mostrar indicador de carga
    resEl.className = "screen-value loading";
    resEl.textContent = "...";

    try {
        const res = await convert(currentCat, valor, desde, hasta);
        const formatted = parseFloat(res.toFixed(6)).toString();

        resEl.className = "screen-value result-animate";
        resEl.textContent = formatted;
        unitEl.textContent = labels[currentCat][hasta] || hasta;

        addHistory(valor, desde, formatted, hasta);
    } catch (error) {
        resEl.className = "screen-value error";
        resEl.textContent = "Error";
        unitEl.textContent = "(sin conexión)";
        console.error(error);
    }
}

/**
 * HISTORIAL
 */
function addHistory(val, desde, res, hasta) {
    history.unshift({ val, desde, res, hasta, cat: currentCat });
    if (history.length > 5) history.pop();
    renderHistory();
}

function renderHistory() {
    const list = document.getElementById("history-list");
    if (!history.length) {
        list.innerHTML = `<div class="empty-history">Sin conversiones aun</div>`;
        return;
    }

    list.innerHTML = history.map((h, i) => {
        const lab = labels[h.cat];
        return `<div class="history-item" onclick="loadHistory(${i})">
        <span>${h.val} ${lab[h.desde] || h.desde}</span>
        <span class="history-result">${h.res} ${lab[h.hasta] || h.hasta}</span>
        </div>`;
    }).join("");
}

function loadHistory(i) {
    const h = history[i];
    document.querySelectorAll(".tab").forEach(t =>
        t.classList.toggle("active", t.dataset.cat === h.cat)
    );
    currentCat = h.cat;
    populateSelects(h.cat);
    document.getElementById("valor").value = h.val;
    document.getElementById("desde").value = h.desde;
    document.getElementById("hasta").value = h.hasta;
    doConvert();
}

/**
 * EVENTOS
 */

// Cambio de categoria
document.querySelectorAll(".tab").forEach(tab => {
    tab.addEventListener("click", () => {
        document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
        tab.classList.add("active");
        currentCat = tab.dataset.cat;
        populateSelects(currentCat);

        // Limpiar campo de valor al cambiar categoría
        document.getElementById("valor").value = '';

        const resEl = document.getElementById("result");
        resEl.className = "screen-value placeholder";
        resEl.textContent = "—";
        document.getElementById("result-unit").textContent = "";
    });
});

// Swap de unidades
document.getElementById("swap-btn").addEventListener("click", () => {
    const desdeEl = document.getElementById("desde");
    const hastaEl = document.getElementById("hasta");
    [desdeEl.value, hastaEl.value] = [hastaEl.value, desdeEl.value];
    if (document.getElementById("valor").value) doConvert();
});

// Conversion en tiempo real
document.getElementById("valor").addEventListener("input", () => {
    if (document.getElementById("valor").value) doConvert();
});

document.getElementById("desde").addEventListener("change", () => {
    if (document.getElementById("valor").value) doConvert();
});

document.getElementById("hasta").addEventListener("change", () => {
    if (document.getElementById("valor").value) doConvert();
});

document.getElementById("convert-btn").addEventListener("click", doConvert);

document.getElementById("valor").addEventListener("keydown", e => {
    if (e.key === "Enter") doConvert();
});

/**
 * INIT
 */
initThemeMode();
populateSelects(currentCat);