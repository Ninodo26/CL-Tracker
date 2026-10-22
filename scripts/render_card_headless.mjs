import http from 'http';
import fs from 'fs';
import path from 'path';
import puppeteer from 'puppeteer-core';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '..');

function startServer(port = 8765) {
  const mimeTypes = {
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.svg': 'image/svg+xml'
  };

  const server = http.createServer((req, res) => {
    let reqPath = decodeURI(req.url.split('?')[0]);
    if (reqPath === '/' || reqPath === '') reqPath = '/index.html';
    const filePath = path.join(rootDir, reqPath);

    if (!fs.existsSync(filePath)) {
      res.writeHead(404);
      res.end('Not found');
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = mimeTypes[ext] || 'application/octet-stream';
    res.writeHead(200, { 'Content-Type': contentType, 'Access-Control-Allow-Origin': '*' });
    fs.createReadStream(filePath).pipe(res);
  });

  return new Promise((resolve) => {
    server.listen(port, () => resolve(server));
  });
}

async function renderBatch(scenesJsonPath, outputDir) {
  if (!fs.existsSync(scenesJsonPath)) {
    console.error(`Scenes file not found: ${scenesJsonPath}`);
    process.exit(1);
  }

  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const raw = JSON.parse(fs.readFileSync(scenesJsonPath, 'utf8'));
  const scenes = Array.isArray(raw) ? raw : (raw.scenes || []);
  const server = await startServer(8765);

  const candidates = [
    process.env.PUPPETEER_EXECUTABLE_PATH,
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium-browser',
    '/usr/bin/chromium'
  ].filter(Boolean);
  const executablePath = candidates.find(p => fs.existsSync(p));

  const browser = await puppeteer.launch({
    executablePath,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  await page.goto('http://localhost:8765/index.html', { waitUntil: 'networkidle0' });

  for (let i = 0; i < scenes.length; i++) {
    const scene = scenes[i];
    const outPath = path.join(outputDir, `${scene.id || `scene_${i + 1}`}.png`);

    await page.evaluate((cType, cPayload) => {
      window.openTikTokCard(cType, cPayload);
      window.setTikTokFormat('story');
      window.renderTikTokCanvas();
    }, scene.type || 'standings', scene.payload || {});

    await new Promise(r => setTimeout(r, 500));

    const dataUrl = await page.evaluate(() => {
      const canvas = document.getElementById('tiktok-canvas');
      return canvas ? canvas.toDataURL('image/png') : null;
    });

    if (dataUrl) {
      fs.writeFileSync(outPath, dataUrl.replace(/^data:image\/png;base64,/, ''), 'base64');
      console.log(`[RENDERED] ${scene.id} -> ${outPath}`);
    } else {
      console.error(`Failed to capture canvas for ${scene.id}`);
    }
  }

  await browser.close();
  server.close();
}

const args = process.argv.slice(2);
const scenesPath = args[0] || path.join(rootDir, 'output', 'scenes.json');
const outDir = args[1] || path.join(rootDir, 'output', 'frames');

renderBatch(scenesPath, outDir).catch(err => {
  console.error('Render batch error:', err);
  process.exit(1);
});
