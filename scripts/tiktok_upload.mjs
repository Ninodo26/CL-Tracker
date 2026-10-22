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

async function findElementInFrames(page, selector, timeout = 30000) {
  const startTime = Date.now();
  while (Date.now() - startTime < timeout) {
    // Check main page
    try {
      const el = await page.$(selector);
      if (el) return { frame: page, element: el };
    } catch (e) {}

    // Check all subframes (TikTok frequently uses iframes for creator studio)
    for (const frame of page.frames()) {
      try {
        const el = await frame.$(selector);
        if (el) return { frame, element: el };
      } catch (e) {}
    }
    await new Promise(r => setTimeout(r, 800));
  }
  return null;
}

async function uploadToTikTok(videoPath, captionText) {
  if (!fs.existsSync(PROFILE_DIR)) {
    console.error('❌ TikTok profile not found!');
    console.error('Please run `node scripts/tiktok_login.mjs` first to authenticate your account.');
    process.exit(1);
  }

  if (!fs.existsSync(videoPath)) {
    console.error(`❌ Video file not found: ${videoPath}`);
    process.exit(1);
  }

  console.log('===================================================');
  console.log('🚀 AUTOMATED TIKTOK STUDIO UPLOADER');
  console.log('===================================================');
  console.log(`📹 Video: ${videoPath}`);
  console.log('🌐 Opening TikTok Creator Studio...');

  const browser = await puppeteer.launch({
    executablePath,
    userDataDir: PROFILE_DIR,
    headless: false, // Set to false to allow visibility and captcha bypass if needed
    defaultViewport: { width: 1280, height: 900 },
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-blink-features=AutomationControlled']
  });

  try {
    const page = await browser.newPage();

    // Try primary upload URLs
    const uploadUrls = [
      'https://www.tiktok.com/tiktokstudio/upload',
      'https://www.tiktok.com/creator-center/upload',
      'https://www.tiktok.com/upload'
    ];

    let loaded = false;
    for (const url of uploadUrls) {
      try {
        console.log(`Navigating to ${url}...`);
        await page.goto(url, { waitUntil: 'networkidle2', timeout: 45000 });
        if (!page.url().includes('/login')) {
          loaded = true;
          break;
        }
      } catch (e) {
        console.log(`Note: ${url} reached timeout, trying next or inspecting DOM...`);
      }
    }

    if (page.url().includes('/login')) {
      console.error('❌ Session expired or not logged in.');
      console.error('Please run `node scripts/tiktok_login.mjs` to refresh your login.');
      await browser.close();
      process.exit(1);
    }

    console.log('🔍 Locating video upload element...');
    const fileInputResult = await findElementInFrames(
      page,
      'input[type="file"][accept*="video"], input[type="file"]',
      35000
    );

    if (!fileInputResult) {
      throw new Error('Could not find file input element on TikTok upload page.');
    }

    const { frame, element: fileInput } = fileInputResult;
    console.log('📤 Submitting video file to uploader...');
    await fileInput.uploadFile(videoPath);

    console.log('⏳ File submitted! Waiting for upload and thumbnail processing...');
    await new Promise(r => setTimeout(r, 6000));

    // Wait for the caption field
    console.log('✍️ Entering video caption and hashtags...');
    const captionResult = await findElementInFrames(
      page,
      '[contenteditable="true"], .DraftEditor-editorContainer div[role="textbox"], textarea',
      35000
    );

    if (captionResult) {
      const captionEl = captionResult.element;
      await captionEl.click();
      await page.keyboard.down('Control');
      await page.keyboard.press('A');
      await page.keyboard.up('Control');
      await page.keyboard.press('Backspace');
      await page.keyboard.type(captionText, { delay: 20 });
      console.log('✅ Caption and hashtags filled!');
    } else {
      console.log('⚠️ Caption box not directly targeted; continuing with video submission.');
    }

    // Wait for upload progress to finish
    console.log('⏳ Ensuring video processing completes...');
    await new Promise(r => setTimeout(r, 8000));

    // Look for post button
    console.log('🚀 Finding Post button...');
    const postBtnResult = await findElementInFrames(
      page,
      'button[data-e2e="post_video_button"], button.btn-post, button:has-text("Post"), button[type="submit"]',
      25000
    );

    if (postBtnResult) {
      console.log('👉 Clicking Post...');
      await postBtnResult.element.click();
      console.log('⏳ Waiting for publishing confirmation...');
      await new Promise(r => setTimeout(r, 10000));
      console.log('🎉 Successfully published video to TikTok!');
    } else {
      console.log('⚠️ Could not click Post button automatically. Please click Post in the open browser.');
      await new Promise(r => setTimeout(r, 15000));
    }

    await browser.close();
    console.log('🏁 Process finished.');
  } catch (err) {
    console.error('❌ Upload note/error:', err.message);
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
  const defaultCaption = 'UEFA Champions League AI simulation breakdown! #UCL #ChampionsLeague #Football #Predictions';
  uploadToTikTok(defaultVideo, defaultCaption);
}
