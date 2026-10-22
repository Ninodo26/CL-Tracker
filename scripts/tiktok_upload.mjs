import fs from 'fs';
import path from 'path';
import os from 'os';
import puppeteer from 'puppeteer-core';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '..');

const PROFILE_DIR = path.join(os.homedir(), '.cl_tiktok_chrome_profile');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const executablePath = fs.existsSync(chromePath) ? chromePath : edgePath;

async function uploadToTikTok(videoPath, captionText) {
  if (!fs.existsSync(PROFILE_DIR)) {
    console.error('❌ TikTok profile not found!');
    console.error('Please run `node scripts/tiktok_login.mjs` once to authenticate your account.');
    process.exit(1);
  }

  if (!fs.existsSync(videoPath)) {
    console.error(`❌ Video file not found: ${videoPath}`);
    process.exit(1);
  }

  console.log('===================================================');
  console.log('🚀 AUTOMATED TIKTOK STUDIO UPLOADER');
  console.log('===================================================');
  console.log(`Video: ${videoPath}`);
  console.log('Opening TikTok Studio in background...');

  const browser = await puppeteer.launch({
    executablePath,
    userDataDir: PROFILE_DIR,
    headless: false, // Run visible or headless: 'new'
    defaultViewport: { width: 1280, height: 900 },
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();
    await page.goto('https://www.tiktok.com/tiktokstudio/upload', {
      waitUntil: 'networkidle2',
      timeout: 60000
    });

    // Check if redirected to login
    if (page.url().includes('/login')) {
      console.error('❌ Session expired or not logged in.');
      console.error('Please run `node scripts/tiktok_login.mjs` to refresh login.');
      await browser.close();
      process.exit(1);
    }

    console.log('Selecting video file for upload...');
    // TikTok Studio upload input (often in an iframe or main page)
    const fileInput = await page.waitForSelector('input[type="file"][accept*="video"], input[type="file"]', {
      timeout: 30000
    });

    await fileInput.uploadFile(videoPath);
    console.log('File submitted, waiting for upload processing...');

    // Wait for the caption field to become active (indicates file is uploading/uploaded)
    await page.waitForSelector('[contenteditable="true"], .DraftEditor-editorContainer, textarea', {
      timeout: 45000
    });
    await new Promise(r => setTimeout(r, 4000));

    console.log('Entering video caption and hashtags...');
    // Find editable caption container
    const captionEl = await page.$('[contenteditable="true"], .DraftEditor-editorContainer div[role="textbox"]');
    if (captionEl) {
      await captionEl.click();
      // Select all existing text and backspace
      await page.keyboard.down('Control');
      await page.keyboard.press('A');
      await page.keyboard.up('Control');
      await page.keyboard.press('Backspace');
      await page.keyboard.type(captionText, { delay: 20 });
    }

    console.log('Waiting for video processing to complete...');
    // Wait until upload percentage finishes or "Upload complete" text appears
    await new Promise(r => setTimeout(r, 6000));

    // Find the Post button
    const postButton = await page.waitForSelector('button:has-text("Post"), .btn-post, button[type="submit"]', {
      timeout: 30000
    });

    console.log('Publishing video to TikTok...');
    await postButton.click();

    // Wait for success modal or redirect
    await new Promise(r => setTimeout(r, 8000));
    console.log('🎉 Successfully published to TikTok!');

    await browser.close();
  } catch (err) {
    console.error('❌ Upload error:', err.message);
    await browser.close();
    process.exit(1);
  }
}

const metaPath = path.join(rootDir, 'output', 'tiktok_post.json');
if (fs.existsSync(metaPath)) {
  const meta = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
  uploadToTikTok(meta.video_path, meta.description);
} else {
  const defaultVideo = path.join(rootDir, 'output', 'cl_tiktok_video.mp4');
  const defaultCaption = 'UEFA Champions League simulation breakdown! #UCL #ChampionsLeague #Football #Predictions';
  uploadToTikTok(defaultVideo, defaultCaption);
}
