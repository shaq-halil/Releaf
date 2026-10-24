const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const root = path.resolve(__dirname, '..');
const prefix = '/repository/';
const mime = {'.html':'text/html','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.webp':'image/webp','.woff2':'font/woff2','.jpg':'image/jpeg'};
const server = http.createServer((req,res)=>{
 const pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
 if(!pathname.startsWith(prefix)){res.writeHead(404).end();return;}
 let file=path.resolve(root,pathname.slice(prefix.length));
 if(file!==root&&!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}
 if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
 if(!fs.existsSync(file)){res.writeHead(404).end();return;}
 res.setHeader('Content-Type',mime[path.extname(file)]||'text/plain');res.end(fs.readFileSync(file));
});
(async()=>{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const base=`http://127.0.0.1:${server.address().port}${prefix}`;
 const browser=await chromium.launch({args:['--no-sandbox']});const page=await browser.newPage();const failed=[];
 page.on('response',response=>{if(response.status()>=400)failed.push(response.url());});
 for(const route of ['', 'our-story/']){
  assert.equal((await page.goto(base+route,{waitUntil:'networkidle'})).status(),200);
  await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(image=>{image.loading='eager';return image.decode()}));});
  assert.equal(await page.evaluate(()=>getComputedStyle(document.body).fontFamily.includes('DM Sans')),true);
 }
 await page.getByRole('navigation').getByRole('link',{name:'Home',exact:true}).click();assert.equal(page.url(),base);
 await page.getByRole('navigation').getByRole('link',{name:'Our story',exact:true}).click();assert.equal(page.url(),base+'our-story/');
 assert.deepEqual(failed,[]);
 const result={passed:true,prefix,checks:['direct root and nested page loads','relative CSS, fonts and images','cross-page Home and Our Story navigation'],failedRequests:failed};
 fs.writeFileSync(path.join(__dirname,'subpath-check.json'),JSON.stringify(result,null,2));console.log(result);
 await browser.close();server.close();
})().catch(error=>{console.error(error);server.close();process.exit(1)});
