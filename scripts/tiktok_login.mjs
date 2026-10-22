import fs from 'fs';
import path from 'path';
import os from 'os';
import readline from 'readline';
import puppeteer from 'puppeteer-core';

const PROFILE_DIR = path.join(os.homedir(), '.cl_tiktok_chrome_profile');

const chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const executablePath = fs.existsSync(chromePath) ? chromePath : edgePath;

console.log('===================================================');
console.log('🔐 TIKTOK ONE-TIME ACCOUNT LOGIN SETUP');
console.log('===================================================');
console.log(`Profile Directory: ${PROFILE_DIR}`);
console.log('Launching browser window...');

const browser = await puppeteer.launch({
  executablePath,
  userDataDir: PROFILE_DIR,
  headless: false,
  defaultViewport: null,
  args: ['--start-maximized', '--no-sandbox']
});

const pages = await browser.pages();
const page = pages.length > 0 ? pages[0] : await browser.newPage();

await page.goto('https://www.tiktok.com/login', { waitUntil: 'networkidle2' });

console.log('\n👉 Instructions:');
console.log('1. Log into your TikTok account in the opened browser window.');
console.log('2. Once you are logged in and see your account profile/feed, come back here.');
console.log('3. Press ENTER in this terminal to save your login session.\n');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('Press [ENTER] after logging in to save session... ', async () => {
  console.log('\n✅ Session saved in profile directory!');
  console.log('Your automated TikTok uploader is now authenticated.');
  rl.close();
  await browser.close();
  process.exit(0);
});
