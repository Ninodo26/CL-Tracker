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
