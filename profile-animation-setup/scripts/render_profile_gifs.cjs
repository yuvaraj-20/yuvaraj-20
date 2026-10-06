const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const {execFileSync} = require('node:child_process');
const {chromium} = require('playwright');

async function main() {
  const root = path.resolve(__dirname, '..');
  const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'yuva-profile-frames-'));
  const browser = await chromium.launch({headless: true});
  try {
    for (const [name, width, originalWidth, originalHeight] of [
      ['craftele-comic', 640, 1024, 1536],
      ['pixel-city', 960, 1180, 570],
    ]) {
      const source = fs.readFileSync(path.join(root, 'assets', name + '.svg'), 'utf8');
      if (name === 'pixel-city' && source.includes('DEMO DATA')) {
        throw new Error('Refusing to publish demo contributions. Generate the real city first.');
      }
      const height = Math.round(width * originalHeight / originalWidth);
      const page = await browser.newPage({viewport: {width, height}, deviceScaleFactor: 1, reducedMotion: 'no-preference'});
      await page.setContent('<style>html,body{margin:0;padding:0;background:#0d1117}svg{display:block;width:100%;height:auto}</style>' + source);
      await page.evaluate(() => document.fonts.ready);
      await page.waitForTimeout(300);
      const frames = path.join(temporary, name);
      fs.mkdirSync(frames);
      const frameCount = 80, fps = 10;
      const animationCount = await page.evaluate(() => document.getAnimations().length);
      if (!animationCount) throw new Error(name + ': no animations found');
      for (let frame = 0; frame < frameCount; frame++) {
        await page.evaluate(time => {
          document.getAnimations().forEach(animation => {animation.pause(); animation.currentTime = time;});
        }, frame * 1000 / fps);
        await page.screenshot({path: path.join(frames, String(frame).padStart(4, '0') + '.png')});
      }
      const input = path.join(frames, '%04d.png');
      const palette = path.join(frames, 'palette.png');
      const output = path.join(root, 'assets', name + '.gif');
      execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(fps), '-i', input,
        '-vf', 'palettegen=stats_mode=diff', '-frames:v', '1', '-update', '1', palette], {stdio:'inherit'});
      execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', String(fps), '-i', input,
        '-i', palette, '-lavfi', 'paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle',
        '-loop', '0', output], {stdio:'inherit'});
      console.log(name + ': 80 GIF frames written');
      await page.close();
    }
  } finally {
    await browser.close();
    fs.rmSync(temporary, {recursive:true, force:true});
  }
}
main().catch(error => {console.error(error.message); process.exitCode = 1;});
