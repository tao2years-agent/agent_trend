import net from 'node:net';
net.Socket.prototype.connect = function() { throw Error('offline probe'); };
globalThis.fetch = async () => { throw Error('offline probe'); };
import { registerHooks } from 'node:module';
import { pathToFileURL } from 'node:url';
const [equalsPath, normalizePath] = process.argv.slice(2);
registerHooks({resolve(specifier, context, next) {
  if (specifier === './normalize') return {url: pathToFileURL(normalizePath).href,shortCircuit:true};
  return next(specifier,context);
}});
const {handleEquals} = await import(pathToFileURL(equalsPath));
let raw='';for await (const piece of process.stdin)raw+=piece;
const rows=JSON.parse(raw);const scored=[];
for(const r of rows){
 const result=await handleEquals({assertion:{type:'equals'},renderedValue:r.expected,outputString:r.answer,inverse:false});
 scored.push([r.id,r.variant,result.score]);
}
process.stdout.write(JSON.stringify(scored));
