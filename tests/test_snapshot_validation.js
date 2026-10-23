const test = require("node:test");
const assert = require("node:assert/strict");
const {hasCompleteLeaguePhaseSchedule, hasValidQualificationOdds} = require("../scripts/snapshot_validation.js");

function completeSnapshot() {
  const teams = Array.from({length: 36}, (_, i) => ({
    name: `Club ${i}`, elo: 1500, points: 0, gd: 0,
    prob_top8: 8 / 36, prob_top24: 24 / 36,
  }));
  const matches = [];
  for (let i = 0; i < 36; i++) {
    for (let d = 1; d <= 4; d++) {
      const j = (i + d) % 36;
      matches.push({home: teams[i].name, away: teams[j].name, played: false});
    }
  }
  return {teams, matches};
}

test("complete legacy snapshot without schedule_complete derives a complete schedule", () => {
  const snapshot = completeSnapshot();
  assert.equal(hasCompleteLeaguePhaseSchedule(snapshot), true);
  assert.equal(hasValidQualificationOdds(snapshot), true);
});

test("genuinely incomplete schedule is rejected", () => {
  const snapshot = completeSnapshot();
  snapshot.matches.pop();
  assert.equal(hasCompleteLeaguePhaseSchedule(snapshot), false);
  assert.equal(hasValidQualificationOdds(snapshot), false);
});

test("explicitly incomplete schedule overrides otherwise complete contents", () => {
  const snapshot = {...completeSnapshot(), schedule_complete: false};
  assert.equal(hasCompleteLeaguePhaseSchedule(snapshot), false);
  assert.equal(hasValidQualificationOdds(snapshot), false);
});

test("missing or malformed data is rejected", () => {
  assert.equal(hasCompleteLeaguePhaseSchedule(null), false);
  assert.equal(hasCompleteLeaguePhaseSchedule({teams: [], matches: []}), false);
  const malformed = completeSnapshot();
  malformed.matches[0].home = "Unknown team";
  assert.equal(hasCompleteLeaguePhaseSchedule(malformed), false);
  const badOdds = completeSnapshot();
  badOdds.teams[0].prob_top24 = NaN;
  assert.equal(hasValidQualificationOdds(badOdds), false);
  const malformedFlag = {...completeSnapshot(), schedule_complete: "true"};
  assert.equal(hasCompleteLeaguePhaseSchedule(malformedFlag), false);
});


test("index.html renderAll, What-If predictor, and single-season simulation execute without runtime errors", () => {
  const fs = require("node:fs");
  const path = require("node:path");
  const vm = require("node:vm");

  const html = fs.readFileSync(path.join(__dirname, "..", "index.html"), "utf8");
  const scriptMatches = [...html.matchAll(/<script(?![^>]*type=["']text\/template["'])[^>]*>([\s\S]*?)<\/script>/g)];
  assert.ok(scriptMatches.length >= 2, "Expected executable inline scripts in index.html");
  const mainScript = scriptMatches.map(m => m[1]).join("\n");
  const standingsData = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "data", "standings.json"), "utf8"));

  const elements = {};
  function getEl(id) {
    if (!elements[id]) {
      elements[id] = {
        id,
        innerHTML: "",
        textContent: "",
        value: "",
        style: {},
        dataset: {},
        classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
        querySelector() { return getEl(id + "_child"); },
        querySelectorAll() { return []; },
        appendChild() {},
        setAttribute() {},
        scrollIntoView() {},
      };
    }
    return elements[id];
  }

  const sandbox = {
    console,
    Math,
    Date,
    Set,
    Map,
    Array,
    Object,
    String,
    Number,
    Boolean,
    JSON,
    Promise,
    setTimeout: () => 0,
    clearTimeout: () => {},
    requestAnimationFrame: (cb) => cb(),
    window: { location: { search: "", hash: "" }, scrollTo() {}, addEventListener() {} },
    localStorage: { getItem: () => null, setItem: () => {}, removeItem: () => {} },
    navigator: { clipboard: { writeText: async () => {} } },
    document: {
      getElementById: (id) => getEl(id),
      querySelector: () => getEl("qs"),
      querySelectorAll: () => [],
      createElement: (tag) => getEl("created_" + tag),
      body: getEl("body"),
      addEventListener: () => {},
    },
    fetch: () => new Promise(() => {}),
  };
  sandbox.window.document = sandbox.document;
  vm.createContext(sandbox);
  vm.runInContext(mainScript, sandbox);

  vm.runInContext(`STANDINGS = ${JSON.stringify(standingsData)}; renderAll();`, sandbox);
  assert.ok(elements["standings-content"].innerHTML.includes("standings-row"), "Standings rows must render");
  assert.ok(elements["matches-content"].innerHTML.includes("match-row"), "Match rows must render");

  vm.runInContext(`setWhatIfPick('Arsenal', 'Bayern Munich', 'H');`, sandbox);
  assert.equal(elements["whatif-floating-bar"].style.display, "flex");
  assert.ok(elements["standings-content"].innerHTML.includes("standings-row"), "What-If standings rows must render");

  vm.runInContext(`clearAllWhatIfPicks();`, sandbox);
  assert.equal(elements["whatif-floating-bar"].style.display, "none");

  vm.runInContext(`runSimulation();`, sandbox);
  assert.ok(elements["standings-content"].innerHTML.includes("Simulated Tournament Champion"), "Simulation banner must render");
  vm.runInContext(`clearSimulation();`, sandbox);
});
