/* Shared browser/Node validation for whether a snapshot can support the
 * league-phase odds and simulator. Missing legacy flags are derived from the
 * actual schedule; an explicit false always disables those features. */
(function (root) {
  function hasCompleteLeaguePhaseSchedule(snapshot) {
    if (!snapshot || typeof snapshot !== "object") return false;
    if (snapshot.schedule_complete === false) return false;
    if (snapshot.schedule_complete !== undefined && typeof snapshot.schedule_complete !== "boolean") return false;

    const teams = snapshot.teams;
    const matches = snapshot.matches;
    if (!Array.isArray(teams) || teams.length !== 36 || !Array.isArray(matches) || matches.length !== 144) return false;

    const names = new Set();
    for (const team of teams) {
      if (!team || typeof team.name !== "string" || !team.name.trim() || names.has(team.name)) return false;
      if (![team.elo, team.points, team.gd].every(Number.isFinite)) return false;
      names.add(team.name);
    }

    const appearances = new Map([...names].map(name => [name, {total: 0, home: 0, away: 0}]));
    const pairs = new Set();
    for (const match of matches) {
      if (!match || typeof match.home !== "string" || typeof match.away !== "string" ||
          !names.has(match.home) || !names.has(match.away) || match.home === match.away ||
          typeof match.played !== "boolean") return false;
      const pair = JSON.stringify([match.home, match.away].sort());
      if (pairs.has(pair)) return false;
      pairs.add(pair);
      appearances.get(match.home).home += 1;
      appearances.get(match.away).away += 1;
      appearances.get(match.home).total += 1;
      appearances.get(match.away).total += 1;
    }
    return [...appearances.values()].every(c => c.total === 8 && c.home === 4 && c.away === 4);
  }

  function hasValidQualificationOdds(snapshot) {
    if (!hasCompleteLeaguePhaseSchedule(snapshot)) return false;
    const teams = snapshot.teams;
    if (!teams.every(t => Number.isFinite(t.prob_top8) && Number.isFinite(t.prob_top24) &&
        t.prob_top8 >= 0 && t.prob_top8 <= t.prob_top24 && t.prob_top24 <= 1)) return false;
    const top8 = teams.reduce((sum, t) => sum + t.prob_top8, 0);
    const top24 = teams.reduce((sum, t) => sum + t.prob_top24, 0);
    return Math.abs(top8 - 8) <= 0.04 && Math.abs(top24 - 24) <= 0.04;
  }

  root.hasCompleteLeaguePhaseSchedule = hasCompleteLeaguePhaseSchedule;
  root.hasValidQualificationOdds = hasValidQualificationOdds;
  if (typeof module !== "undefined" && module.exports) {
    module.exports = {hasCompleteLeaguePhaseSchedule, hasValidQualificationOdds};
  }
})(typeof globalThis !== "undefined" ? globalThis : this);
