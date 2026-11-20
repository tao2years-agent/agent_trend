'use strict';
const assert = require('node:assert/strict');
const path = require('node:path');
const fs = require('node:fs');
const { createRequire } = require('node:module');
const local = createRequire(path.join(process.cwd(),'package.json'));
const diagnosis = { stages: [], warnings: [], versions: {}, passed: false };
const stderr = console.error;
const warn = console.warn;
const capture = (...args) => diagnosis.warnings.push(args.map(String).join(' '));
console.error = console.warn = capture;
let stage = 'environment';
let window;
try {
  const { JSDOM } = local('jsdom');
  const dom = new JSDOM('<!doctype html><html><body></body></html>', {url: 'https://local.invalid/', pretendToBeVisual: true});
  window = dom.window;
  for (const key of ['window','document','navigator','HTMLElement','Node','MutationObserver','Event']) {
    Object.defineProperty(globalThis,key,{ value:key==='window'?window:window[key], configurable:true });
  }
  globalThis.IS_REACT_ACT_ENVIRONMENT = true;
  const fromRTL = createRequire(local.resolve('@testing-library/react'));
  const readPkg = (req, name) => {
    let here = path.dirname(req.resolve(name));
    for (;;) {
      const pkg=path.join(here,'package.json');
      if (fs.existsSync(pkg)) {
        const obj=JSON.parse(fs.readFileSync(pkg,'utf8'));
        if (obj.name===name) return obj.version;
      }
      const parent=path.dirname(here);
      if (parent===here) throw new Error('package metadata missing for '+name);
      here=parent;
    }
  };
  for (const pkg of ['react','react-dom','@testing-library/react','@testing-library/dom','jsdom']) diagnosis.versions[pkg]=readPkg(local,pkg);
  diagnosis.versions.dom_seen_by_RTL=readPkg(fromRTL,'@testing-library/dom');
  diagnosis.stages.push(stage);
  stage='import';
  const React=local('react');
  const { render, screen, fireEvent, cleanup }=local('@testing-library/react');
  diagnosis.stages.push(stage);
  const h=React.createElement;
  let mounts=0, disposals=0;
  function Draft({heading}) {
    const [text,setText]=React.useState('');
    const [items,setItems]=React.useState([]);
    React.useEffect(()=>{mounts++;return ()=>{disposals++};},[]);
    function submit(e) {
      e.preventDefault();
      if (text.trim()) {setItems([...items,text.trim()]);setText('');}
    }
    return h('section',null,h('h1',null,heading),h('form',{onSubmit:submit},
      h('label',null,'Task name',h('input',{value:text,onChange:e=>setText(e.target.value)})),
      h('button',{type:'submit'},'Add task')),h('ul',null,...items.map(i=>h('li',{key:i},i))),
      h('button',{type:'button',onClick:()=>setItems([])},'Clear tasks'));
  }
  stage='render';const root=render(h(Draft,{heading:'Work queue'}));
  assert.equal(screen.getByRole('heading',{name:'Work queue'}).textContent,'Work queue');assert.equal(mounts,1);diagnosis.stages.push(stage);
  stage='change_submit';const field=screen.getByRole('textbox',{name:'Task name'});fireEvent.change(field,{target:{value:' verify migration '}});
  assert.equal(field.value,' verify migration ');fireEvent.click(screen.getByRole('button',{name:'Add task'}));
  assert.equal(screen.getByRole('listitem').textContent,'verify migration');assert.equal(field.value,'');diagnosis.stages.push(stage);
  stage='rerender';root.rerender(h(Draft,{heading:'Current work'}));assert.ok(screen.getByRole('heading',{name:'Current work'}));assert.equal(screen.getByRole('listitem').textContent,'verify migration');assert.equal(mounts,1);diagnosis.stages.push(stage);
  stage='clear';fireEvent.click(screen.getByRole('button',{name:'Clear tasks'}));assert.equal(screen.queryAllByRole('listitem').length,0);diagnosis.stages.push(stage);
  stage='unmount_cleanup';root.unmount();assert.equal(disposals,1);assert.equal(screen.queryByRole('heading'),null);cleanup();assert.equal(document.body.children.length,0);assert.equal(disposals,1);diagnosis.stages.push(stage);
  diagnosis.passed=true;
} catch(e) {
  diagnosis.failure={stage,code:e.code||null,message:String(e.message).split('\nRequire stack:')[0],frames:String(e.stack).split('\n').filter(l=>l.trim().startsWith('at ')).slice(0,4).map(l=>l.replaceAll(process.cwd(),'<project>'))};
} finally {
  if(window)window.close();
  console.error=stderr;console.warn=warn;
}
diagnosis.open_handle_types_before_exit = process.getActiveResourcesInfo();
process.stdout.write(JSON.stringify(diagnosis)+'\n',()=>process.exit(diagnosis.passed?0:1));
