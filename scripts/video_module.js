
let isRecordingVideo = false;

async function recordTikTokVideo(){
  const canvas = document.getElementById('tiktok-canvas');
  const recordBtn = document.getElementById('tiktok-record-btn');
  const previewImg = document.getElementById('tiktok-preview-img');
  if (!canvas || isRecordingVideo) return;

  isRecordingVideo = true;
  setTikTokFormat('story'); // Ensure 9:16 vertical format
  canvas.style.display = 'block';
  if (previewImg) previewImg.style.display = 'none';

  if (recordBtn) {
    recordBtn.disabled = true;
    recordBtn.textContent = '⏳ Rendering Video (0%)...';
  }

  const stream = canvas.captureStream(30);
  let mimeType = 'video/webm;codecs=vp9';
  if (typeof MediaRecorder !== 'undefined') {
    if (MediaRecorder.isTypeSupported('video/mp4')) {
      mimeType = 'video/mp4';
    } else if (MediaRecorder.isTypeSupported('video/webm;codecs=h264')) {
      mimeType = 'video/webm;codecs=h264';
    } else if (MediaRecorder.isTypeSupported('video/webm')) {
      mimeType = 'video/webm';
    }
  }

  let recorder;
  try {
    recorder = new MediaRecorder(stream, { mimeType, videoBitsPerSecond: 6000000 });
  } catch(e) {
    recorder = new MediaRecorder(stream);
  }

  const chunks = [];
  recorder.ondataavailable = (e) => {
    if (e.data && e.data.size > 0) chunks.push(e.data);
  };

  recorder.onstop = () => {
    const blob = new Blob(chunks, { type: mimeType });
    const ext = mimeType.includes('mp4') ? 'mp4' : 'webm';
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `cl-tracker-tiktok-${currentTikTokType}-${Date.now()}.${ext}`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1500);

    isRecordingVideo = false;
    canvas.style.display = 'none';
    if (previewImg) previewImg.style.display = 'block';
    if (recordBtn) {
      recordBtn.disabled = false;
      recordBtn.textContent = '🎬 Export Animated Video (MP4)';
    }
    showTikTokToast(`✓ 9:16 Video Generated (${ext.toUpperCase()})! Ready to post on TikTok.`);
    renderTikTokCanvas();
  };

  recorder.start();

  const totalFrames = 240; // 8 seconds at 30 fps
  let frame = 0;

  function stepAnimation(){
    const progress = frame / totalFrames;
    renderTikTokAnimatedScene(progress);
    frame++;

    if (recordBtn && frame % 20 === 0) {
      const pct = Math.round(progress * 100);
      recordBtn.textContent = `⏳ Rendering Video (${pct}%)...`;
    }

    if (frame <= totalFrames) {
      requestAnimationFrame(stepAnimation);
    } else {
      recorder.stop();
    }
  }

  requestAnimationFrame(stepAnimation);
}

function renderTikTokAnimatedScene(progress){
  const canvas = document.getElementById('tiktok-canvas');
  if (!canvas) return;
  const W = 1080;
  const H = 1920;
  canvas.width = W;
  canvas.height = H;
  const ctx = canvas.getContext('2d');

  // Background gradient with gentle pulse
  const pulse = Math.sin(progress * Math.PI * 4) * 0.05;
  const bgGrad = ctx.createLinearGradient(0, 0, 0, H);
  bgGrad.addColorStop(0, '#030712');
  bgGrad.addColorStop(0.35, '#071830');
  bgGrad.addColorStop(0.7, '#040d1c');
  bgGrad.addColorStop(1, '#02040a');
  ctx.fillStyle = bgGrad;
  ctx.fillRect(0, 0, W, H);

  // Spotlight pulse
  const topGlow = ctx.createRadialGradient(W / 2, 0, 50, W / 2, 0, W * (0.75 + pulse));
  topGlow.addColorStop(0, 'rgba(30, 90, 180, 0.45)');
  topGlow.addColorStop(0.6, 'rgba(15, 45, 95, 0.18)');
  topGlow.addColorStop(1, 'rgba(0, 0, 0, 0)');
  ctx.fillStyle = topGlow;
  ctx.fillRect(0, 0, W, H);

  // Grid
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
  ctx.lineWidth = 1;
  for (let x = 60; x < W; x += 120){
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
  }
  for (let y = 60; y < H; y += 120){
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
  }

  const headerY = 120;
  ctx.fillStyle = '#d9b84a';
  ctx.font = '700 24px "IBM Plex Mono", monospace';
  ctx.textAlign = 'center';
  ctx.fillText('★ UEFA CHAMPIONS LEAGUE 2026/27 ★', W / 2, headerY);

  if (currentTikTokType === 'match'){
    renderAnimatedMatchScene(ctx, W, H, headerY, progress);
  } else if (currentTikTokType === 'team'){
    renderTikTokTeamCard(ctx, W, H, true, headerY);
  } else {
    renderTikTokStandingsCard(ctx, W, H, true, headerY);
  }

  // Animated progress bar at the very top of video
  ctx.fillStyle = '#d9b84a';
  ctx.fillRect(0, 0, W * progress, 8);

  // Footer
  ctx.textAlign = 'center';
  ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
  ctx.font = '18px "IBM Plex Mono", monospace';
  ctx.fillText('EVIDENCE-BASED AI & MONTE CARLO SIMULATOR • GITHUB.COM/NINODO26/CL-TRACKER', W / 2, H - 70);
}

function renderAnimatedMatchScene(ctx, W, H, headerY, progress){
  const m = currentTikTokPayload;
  const home = m.home || 'Real Madrid';
  const away = m.away || 'Paris Saint-Germain';
  const mdLabel = (m.matchday || 'Matchday 4').replace('League Stage - ', 'Matchday ').toUpperCase();

  ctx.fillStyle = '#ffffff';
  ctx.font = '700 64px "Anton", sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText(mdLabel + ' SHOWDOWN', W / 2, headerY + 70);

  ctx.fillStyle = '#8ea2c6';
  ctx.font = '22px "IBM Plex Mono", monospace';
  ctx.fillText('OFFICIAL AI WIN PROBABILITY & TACTICAL PREVIEW', W / 2, headerY + 110);

  const cardY = headerY + 145;
  const cardH = 820;
  const cardW = 920;
  const cardX = (W - cardW) / 2;

  ctx.fillStyle = 'rgba(7, 18, 38, 0.75)';
  ctx.strokeStyle = '#d9b84a';
  ctx.lineWidth = 2;
  drawRoundedRect(ctx, cardX, cardY, cardW, cardH, 20, true, true);

  const homeColor = teamColor(home);
  const awayColor = teamColor(away);
  const homeX = cardX + 180;
  const awayX = cardX + cardW - 180;
  const crestY = cardY + 160;

  // Home Badge
  ctx.save();
  ctx.fillStyle = homeColor;
  ctx.beginPath(); ctx.arc(homeX, crestY, 65, 0, Math.PI * 2); ctx.fill();
  ctx.lineWidth = 4; ctx.strokeStyle = '#ffffff'; ctx.stroke();
  ctx.restore();

  ctx.fillStyle = '#ffffff';
  ctx.font = '700 36px "Anton", sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText(initials(home), homeX, crestY + 12);

  // Away Badge
  ctx.save();
  ctx.fillStyle = awayColor;
  ctx.beginPath(); ctx.arc(awayX, crestY, 65, 0, Math.PI * 2); ctx.fill();
  ctx.lineWidth = 4; ctx.strokeStyle = '#ffffff'; ctx.stroke();
  ctx.restore();

  ctx.fillStyle = '#ffffff';
  ctx.font = '700 36px "Anton", sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText(initials(away), awayX, crestY + 12);

  // VS
  ctx.fillStyle = '#d9b84a';
  ctx.font = '700 44px "Anton", sans-serif';
  ctx.fillText('VS', W / 2, crestY + 14);

  // Team Names
  ctx.fillStyle = '#ffffff';
  ctx.font = '700 38px "Anton", sans-serif';
  ctx.fillText(home.toUpperCase(), homeX, crestY + 115);
  ctx.fillText(away.toUpperCase(), awayX, crestY + 115);

  const tHome = (STANDINGS && STANDINGS.teams || []).find(t => t.name === home);
  const tAway = (STANDINGS && STANDINGS.teams || []).find(t => t.name === away);
  ctx.font = '20px "IBM Plex Mono", monospace';
  ctx.fillStyle = '#8ea2c6';
  ctx.fillText(tHome ? `#${tHome.rank} In UCL • ${tHome.points} Pts` : 'Top Tier European Contender', homeX, crestY + 148);
  ctx.fillText(tAway ? `#${tAway.rank} In UCL • ${tAway.points} Pts` : 'Top Tier European Contender', awayX, crestY + 148);

  // Animated Probability Bar
  let pHome = 0.48, pDraw = 0.24, pAway = 0.28;
  if (m.odds){
    pHome = m.odds.home; pDraw = m.odds.draw; pAway = m.odds.away;
  } else if (tHome && tAway){
    [pHome, pDraw, pAway] = outcomeProbabilitiesJS(tHome.elo, tAway.elo);
  }

  // Animate bar filling up between progress 0.1 and 0.5
  const barAnimFactor = Math.min(1, Math.max(0, (progress - 0.1) * 3));
  const pctHome = Math.round(pHome * 100 * barAnimFactor);
  const pctDraw = Math.round(pDraw * 100 * barAnimFactor);
  const pctAway = Math.round(pAway * 100 * barAnimFactor);

  const barY = crestY + 210;
  const barW = 760;
  const barH = 50;
  const barX = (W - barW) / 2;

  ctx.fillStyle = '#11223e';
  drawRoundedRect(ctx, barX, barY, barW, barH, 12, true, false);

  const w1 = barW * (pctHome / 100);
  const w2 = barW * (pctDraw / 100);
  const w3 = Math.max(0, barW * barAnimFactor - w1 - w2);

  ctx.fillStyle = homeColor;
  drawRoundedRect(ctx, barX, barY, w1, barH, 10, true, false);
  ctx.fillStyle = '#64748b';
  drawRoundedRect(ctx, barX + w1, barY, w2, barH, 0, true, false);
  ctx.fillStyle = awayColor;
  drawRoundedRect(ctx, barX + w1 + w2, barY, w3, barH, 10, true, false);

  if (barAnimFactor > 0.3){
    ctx.fillStyle = '#ffffff';
    ctx.font = '700 22px "IBM Plex Mono", monospace';
    ctx.textAlign = 'center';
    ctx.fillText(`${pctHome}% ${home.split(' ').pop()}`, barX + w1 / 2, barY + 34);
    if (w2 > 50) ctx.fillText(`${pctDraw}% Draw`, barX + w1 + w2 / 2, barY + 34);
    if (w3 > 50) ctx.fillText(`${pctAway}% ${away.split(' ').pop()}`, barX + w1 + w2 + w3 / 2, barY + 34);
  }

  // Simulated Score Pop-in (after 0.4 progress)
  if (progress > 0.4){
    const scoreY = barY + 85;
    ctx.fillStyle = '#d9b84a';
    ctx.font = '700 28px "Anton", sans-serif';
    ctx.fillText(m.played ? `FINAL RESULT: ${m.score}` : `SIMULATED MOST LIKELY: 2 - 1`, W / 2, scoreY);
  }

  // Key Player Showdown
  const hLineup = (LINEUPS_DATA && LINEUPS_DATA[home]) || {};
  const aLineup = (LINEUPS_DATA && LINEUPS_DATA[away]) || {};
  const hStar = (hLineup.starting_xi && hLineup.starting_xi[hLineup.starting_xi.length - 1]) || {name: 'Primary Talisman'};
  const aStar = (aLineup.starting_xi && aLineup.starting_xi[aLineup.starting_xi.length - 1]) || {name: 'Primary Talisman'};

  const showdownY = cardY + 460;
  ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
  ctx.beginPath();
  ctx.moveTo(cardX + 40, showdownY); ctx.lineTo(cardX + cardW - 40, showdownY); ctx.stroke();

  ctx.fillStyle = '#d9b84a';
  ctx.font = '700 22px "Anton", sans-serif';
  ctx.fillText('KEY PLAYER HEAD-TO-HEAD', W / 2, showdownY + 36);

  ctx.fillStyle = '#ffffff';
  ctx.font = '700 26px "Anton", sans-serif';
  ctx.fillText(hStar.name.toUpperCase(), homeX, showdownY + 90);
  ctx.fillText(aStar.name.toUpperCase(), awayX, showdownY + 90);

  ctx.fillStyle = '#8ea2c6';
  ctx.font = '18px "IBM Plex Mono", monospace';
  ctx.fillText(`Manager: ${hLineup.manager || 'Elite Coach'}`, homeX, showdownY + 125);
  ctx.fillText(`Manager: ${aLineup.manager || 'Elite Coach'}`, awayX, showdownY + 125);

  // Bottom Viral Hook Card
  const viralY = cardY + cardH + 40;
  const viralH = 260;
  ctx.fillStyle = 'rgba(217, 184, 74, 0.08)';
  ctx.strokeStyle = '#d9b84a';
  ctx.lineWidth = 1.5;
  drawRoundedRect(ctx, cardX, viralY, cardW, viralH, 16, true, true);

  ctx.fillStyle = '#d9b84a';
  ctx.font = '700 24px "Anton", sans-serif';
  ctx.fillText('🚨 HIGH-STAKES QUALIFICATION SCENARIO', W / 2, viralY + 50);

  ctx.fillStyle = '#f4ede2';
  ctx.font = '22px "IBM Plex Mono", monospace';
  const hookText = `${home} and ${away} battle in an essential Matchday 4 fixture. 16 points guarantees direct Round of 16 qualification, while 10 points secures a playoff spot. Every goal swings Elo and qualification odds!`;
  wrapText(ctx, hookText, cardX + 45, viralY + 105, cardW - 90, 36, 4);
}
