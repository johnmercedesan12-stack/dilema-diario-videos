// Uso: node render.mjs out/video.mp4
import puppeteer from 'puppeteer-core'; import fs from 'fs'; import {spawn} from 'child_process';
const TL=JSON.parse(fs.readFileSync('work/timeline.json','utf8')), FPS=30, out=process.argv[2];
fs.writeFileSync('work/page.html', fs.readFileSync('comp.html','utf8').replace('__TIMELINE__',JSON.stringify(TL)).replace('node_modules/','../node_modules/'));
const b=await puppeteer.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox','--allow-file-access-from-files'],headless:true});
const p=await b.newPage(); await p.setViewport({width:1080,height:1920});
await p.goto('file://'+process.cwd()+'/work/page.html'); await p.evaluate(()=>window.ready);
const only=process.argv[3];
if(only){for(const t of only.split(',')){await p.evaluate(t=>window.seek(t),+t);await p.screenshot({path:`work/f_${t}.jpg`,type:'jpeg',quality:80});}await b.close();process.exit(0)}
const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',FPS,'-i','-','-i','work/audio.wav','-c:v','libx264','-preset','medium','-crf','23','-maxrate','650k','-bufsize','1300k','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-shortest','-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
const n=Math.ceil(TL.total*FPS);
for(let i=0;i<n;i++){await p.evaluate(t=>window.seek(t),i/FPS);const buf=await p.screenshot({type:'jpeg',quality:90});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));}
ff.stdin.end(); await new Promise(r=>ff.on('close',r)); await b.close(); console.log('ok',n,'frames');
