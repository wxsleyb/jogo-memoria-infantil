'use strict';
/* Jogo da Memória Infantil. Não acessa Pixabay em tempo de execução.
 * Ilustrações previamente aprovadas são arquivos locais, sempre em pares idênticos.
 */
const $ = (s) => document.querySelector(s);
const ui = {
  board: $('#game-board'), stage: $('#board-stage'), hint: $('#board-hint'),
  input: $('#numPairs'), presets: [...document.querySelectorAll('.preset')],
  themes: [...document.querySelectorAll('.theme')], start: $('#start-button'),
  startLabel: $('#start-button-label'), previewStart: $('#preview-start'), status: $('#setup-message'),
  time: $('#time-value'), attempts: $('#attempts-value'), pairs: $('#pairs-value'),
  level: $('#level-label'), progress: $('#progress-fill'), progressText: $('#progress-text'),
  progressTrack: $('#progress-track'), best: $('#best-record'),
  pause: $('#pause-button'), pauseOverlay: $('#pause-overlay'), resume: $('#resume-button'),
  zoomIn: $('#zoom-in'), zoomOut: $('#zoom-out'), zoomLabel: $('#zoom-label'),
  sound: $('#sound-toggle'), soundIcon: $('#sound-icon'),
  dialog: $('#win-dialog'), closeWin: $('#close-win'), playAgain: $('#play-again'),
  winTime: $('#win-time'), winAttempts: $('#win-attempts'), winPairs: $('#win-pairs'),
  winStars: $('#win-stars'), winRecord: $('#win-record')
};

const game = {
  theme: 'animais', pairs: 6, matches: 0, attempts: 0,
  first: null, second: null, locked: false, state: 'ready',
  elapsed: 0, resumeAt: 0, tick: null, flipTimeout: null,
  version: 0, zoom: 1, sound: false
};
const THEME_NAMES = {animais:'BICHINHOS',frutas:'FRUTINHAS',transportes:'VEÍCULOS',todos:'TODOS'};

function shuffle(items) {
  const list = [...items];
  for (let i=list.length-1;i>0;i--) {
    const j=Math.floor(Math.random()*(i+1));[list[i],list[j]]=[list[j],list[i]];
  }
  return list;
}
function readPairs(){const n=Number(ui.input.value);return Number.isInteger(n)&&n>=2&&n<=32?n:null;}
function selectedTheme(){return ui.themes.find((b)=>b.classList.contains('is-selected'))?.dataset.theme||'animais';}
function selectedPairs(){return readPairs()??game.pairs;}
function difficulty(p){return p===6?'CASUAL':p===12?'INTERMEDIÁRIO':p===16?'INSANO':'PERSONALIZADO';}
function message(text,error=false){ui.status.textContent=text;ui.status.classList.toggle('is-error',error);}
function labelFor(p,theme){ui.level.textContent=`${difficulty(p)} · ${p} PARES · ${THEME_NAMES[theme]}`;}
function updatePreset(){const p=readPairs();ui.presets.forEach(b=>{const on=Number(b.dataset.pairs)===p;b.classList.toggle('is-selected',on);b.setAttribute('aria-pressed',String(on));});if(game.state==='ready'){updateReadyPreview();}}
function changeTheme(theme){if(!THEME_NAMES[theme])return;ui.themes.forEach(b=>{const on=b.dataset.theme===theme;b.classList.toggle('is-selected',on);b.setAttribute('aria-pressed',String(on));});if(game.state==='ready')updateReadyPreview();else message('O novo tema será usado quando você iniciar outra partida.');}
function updateBoardColumns(p,preview=false){
  const count=preview?12:p*2, columns=preview?4:count<=16?4:count<=24?6:8;
  ui.board.style.setProperty('--cols-desktop',columns);
  ui.board.style.setProperty('--cols-tablet',Math.min(columns,6));
  ui.board.style.setProperty('--cols-mobile',Math.min(columns,4));
  ui.board.style.setProperty('--board-base-width',`${columns*108+(columns-1)*11}px`);
  ui.board.style.setProperty('--board-scale',game.zoom);
}
function previewBoard(){
  ui.board.classList.add('is-preview');ui.board.replaceChildren();updateBoardColumns(readPairs()||6,true);
  const fragment=document.createDocumentFragment();
  for(let i=0;i<12;i++){const el=document.createElement('div');el.className='preview-card';fragment.appendChild(el);}
  ui.board.appendChild(fragment);ui.hint.hidden=false;
}
function updateReadyPreview(){const p=readPairs();if(!p){message('Escolha entre 2 e 32 pares.',true);return;}game.pairs=p;game.theme=selectedTheme();game.matches=0;game.attempts=0;previewBoard();labelFor(p,game.theme);updateStats();updateRecord();message('Escolha um tema e comece a brincadeira!');}
function formatTime(ms){const sec=Math.floor(ms/1000);return `${String(Math.floor(sec/60)).padStart(2,'0')}:${String(sec%60).padStart(2,'0')}`;}
function elapsed(){return game.elapsed+(game.state==='playing'?performance.now()-game.resumeAt:0);}
function updateStats(){ui.time.textContent=formatTime(elapsed());ui.attempts.textContent=String(game.attempts);ui.pairs.innerHTML=`${game.matches} <em>/ ${game.pairs}</em>`;const pct=Math.round(game.matches/game.pairs*100);ui.progress.style.width=`${pct}%`;ui.progressText.textContent=`${pct}% concluído`;ui.progressTrack.setAttribute('aria-valuemax',game.pairs);ui.progressTrack.setAttribute('aria-valuenow',game.matches);}
function recordKey(theme=game.theme,pairs=game.pairs){return `memoria-infantil-${theme}-${pairs}`;}
function readRecord(){try{const r=JSON.parse(localStorage.getItem(recordKey())||'null');return r&&Number.isInteger(r.attempts)&&Number.isFinite(r.time)?r:null;}catch(_){return null;}}
function saveRecord(){const r=readRecord(),time=Math.round(elapsed());const better=!r||game.attempts<r.attempts||(game.attempts===r.attempts&&time<r.time);if(better){try{localStorage.setItem(recordKey(),JSON.stringify({attempts:game.attempts,time}));}catch(_){} }return better;}
function updateRecord(){const r=readRecord();ui.best.textContent=r?`${r.attempts} tent. · ${formatTime(r.time)}`:'—';}
function endTimers(){clearInterval(game.tick);clearTimeout(game.flipTimeout);game.tick=null;game.flipTimeout=null;}
let audioContext;
function playSound(type){if(!game.sound)return;try{audioContext ||= new (window.AudioContext||window.webkitAudioContext)();if(audioContext.state==='suspended')audioContext.resume();const notes=type==='win'?[523,659,784]:type==='match'?[540,740]:type==='miss'?[270,220]:[500];notes.forEach((hz,i)=>{const osc=audioContext.createOscillator(),gain=audioContext.createGain(),at=audioContext.currentTime+i*.09;osc.frequency.value=hz;osc.type='sine';gain.gain.setValueAtTime(.0001,at);gain.gain.exponentialRampToValueAtTime(.075,at+.015);gain.gain.exponentialRampToValueAtTime(.0001,at+.13);osc.connect(gain).connect(audioContext.destination);osc.start(at);osc.stop(at+.14);});}catch(_){} }
function library(theme){
  const local=window.BIBLIOTECA_LOCAL||{},pixabay=window.BIBLIOTECA_PIXABAY||{};
  const categories=theme==='todos'?['animais','frutas','transportes']:[theme];
  const pool=[];const seen=new Set();
  // Primeiro imagens importadas da Pixabay e aprovadas manualmente; depois ilustrações locais de demonstração.
  for(const category of categories){
    for(const source of [pixabay,local])for(const item of source[category]||[]){
      if(!item||typeof item.nome!=='string'||typeof item.src!=='string')continue;
      const key=`${category}:${item.nome.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase()}`;
      if(seen.has(key))continue;seen.add(key);pool.push({...item,category});
    }
  }
  return pool;
}
function imageReady(src){
  return new Promise(resolve=>{
    const img=new Image();let done=false;
    const finish=ok=>{if(done)return;done=true;clearTimeout(timeout);resolve(ok);};
    const timeout=setTimeout(()=>finish(false),7000);
    img.onload=()=>finish(img.naturalWidth>0);img.onerror=()=>finish(false);img.src=src;
    if(img.complete)finish(img.naturalWidth>0);
  });
}
async function chooseImages(p,theme){
  const pool=shuffle(library(theme));if(pool.length<p)throw new Error(`Biblioteca insuficiente para ${p} pares.`);
  let selected=pool.slice(0,p),errors=[];
  const checks=await Promise.all(selected.map(i=>imageReady(i.src)));
  for(let k=0;k<selected.length;k++)if(!checks[k])errors.push(k);
  if(errors.length){
    const available=pool.slice(p);const used=new Set(selected.filter((_,i)=>checks[i]).map(i=>i.src));
    for(const index of errors){let replacement=null;while(available.length){const a=available.shift();if(used.has(a.src))continue;if(await imageReady(a.src)){replacement=a;break;}}if(!replacement)throw new Error('Algumas imagens não estão disponíveis. Confira os arquivos da pasta img.');selected[index]=replacement;used.add(replacement.src);}
  }
  return selected;
}
function createCard(item,index,pairId,version){
  const btn=document.createElement('button');btn.type='button';btn.className='card';btn.dataset.pair=String(pairId);btn.setAttribute('aria-label',`Carta ${index+1}, virada para baixo`);btn.setAttribute('aria-pressed','false');
  const inner=document.createElement('span');inner.className='card-inner';
  const back=document.createElement('span');back.className='card-face card-back';
  const front=document.createElement('span');front.className='card-face card-front';
  const img=document.createElement('img');img.className='front-image';img.alt='';img.loading='eager';img.decoding='async';img.src=item.src;
  front.appendChild(img);inner.append(back,front);btn.appendChild(inner);
  btn.addEventListener('click',()=>flipCard(btn,item,index,version));return btn;
}
function flipCard(btn,item,index,version){
  if(version!==game.version||game.state!=='playing'||game.locked||btn.disabled||btn.classList.contains('is-flipped'))return;
  btn.classList.add('is-flipped');btn.setAttribute('aria-pressed','true');btn.setAttribute('aria-label',`Carta ${index+1}: ${item.nome}`);playSound('flip');
  if(!game.first){game.first=btn;return;}
  game.second=btn;game.locked=true;game.attempts++;updateStats();
  const a=game.first,b=game.second;
  if(a.dataset.pair===b.dataset.pair){
    a.classList.add('is-matched');b.classList.add('is-matched');a.disabled=b.disabled=true;
    game.matches++;playSound('match');updateStats();game.first=game.second=null;game.locked=false;
    if(game.matches===game.pairs){game.flipTimeout=setTimeout(()=>{if(version===game.version)finishGame();},650);}else message('Muito bem! Você encontrou um par!');
  }else{
    a.classList.add('is-wrong');b.classList.add('is-wrong');playSound('miss');
    game.flipTimeout=setTimeout(()=>{
      if(version!==game.version)return;
      for(const c of [a,b]){c.classList.remove('is-flipped','is-wrong');c.setAttribute('aria-pressed','false');c.setAttribute('aria-label',`Carta ${Number(c.dataset.pos)+1}, virada para baixo`);}
      game.first=game.second=null;game.locked=false;
    },980);
  }
}
async function startGame(){
  const p=readPairs();if(p===null){message('Por favor, escolha um número inteiro entre 2 e 32.',true);ui.input.focus();return;}
  const theme=selectedTheme();const version=++game.version;
  endTimers();if(ui.dialog.open)ui.dialog.close();game.state='loading';game.locked=true;game.matches=0;game.attempts=0;game.pairs=p;game.theme=theme;game.first=game.second=null;game.elapsed=0;
  ui.pause.disabled=true;ui.pauseOverlay.hidden=true;ui.hint.hidden=true;ui.start.disabled=true;ui.startLabel.textContent='Carregando imagens...';
  labelFor(p,theme);updateStats();updateRecord();message('Preparando as ilustrações...');
  try{
    const images=await chooseImages(p,theme);if(version!==game.version)return;
    const cards=shuffle(images.flatMap((item,id)=>[{item,id},{item,id}]));
    const frag=document.createDocumentFragment();
    cards.forEach(({item,id},index)=>{const el=createCard(item,index,id,version);el.dataset.pos=String(index);frag.appendChild(el);});
    ui.board.classList.remove('is-preview');ui.board.replaceChildren(frag);updateBoardColumns(p);
    game.state='playing';game.locked=false;game.elapsed=0;game.resumeAt=performance.now();game.tick=setInterval(()=>{if(version===game.version)updateStats();},200);
    ui.pause.disabled=false;ui.pause.textContent='Ⅱ Pausar';ui.startLabel.textContent='Nova partida';message('Encontre duas figuras iguais!');updateStats();
  }catch(e){if(version!==game.version)return;game.state='ready';game.locked=false;ui.startLabel.textContent='Iniciar partida';previewBoard();message(e.message||'Não foi possível carregar as ilustrações.',true);}
  finally{if(version===game.version)ui.start.disabled=false;}
}
function togglePause(){
  if(game.state==='playing'){
    game.elapsed=elapsed();game.state='paused';clearInterval(game.tick);game.tick=null;ui.pauseOverlay.hidden=false;ui.pause.textContent='▶ Continuar';message('Partida pausada.');
  }else if(game.state==='paused')resume();
}
function resume(){if(game.state!=='paused')return;game.state='playing';game.resumeAt=performance.now();ui.pauseOverlay.hidden=true;ui.pause.textContent='Ⅱ Pausar';game.tick=setInterval(updateStats,200);message('Vamos continuar!');}
function finishGame(){if(game.state!=='playing')return;game.elapsed=elapsed();game.state='won';endTimers();ui.pause.disabled=true;updateStats();const better=saveRecord();updateRecord();ui.winTime.textContent=formatTime(game.elapsed);ui.winAttempts.textContent=String(game.attempts);ui.winPairs.textContent=String(game.pairs);const stars=game.attempts<=game.pairs*1.5?3:game.attempts<=game.pairs*2.5?2:1;ui.winStars.textContent='★'.repeat(stars)+'☆'.repeat(3-stars);ui.winStars.setAttribute('aria-label',`${stars} de 3 estrelas`);ui.winRecord.textContent=better?'Novo recorde!':'Você completou mais uma partida!';ui.startLabel.textContent='Jogar novamente';message('Parabéns! Todos os pares encontrados!');playSound('win');if(typeof ui.dialog.showModal==='function')ui.dialog.showModal();}
function zoom(delta){game.zoom=Math.max(.65,Math.min(1.3,Math.round((game.zoom+delta)*100)/100));ui.board.style.setProperty('--board-scale',game.zoom);ui.zoomLabel.textContent=`${Math.round(game.zoom*100)}%`;ui.zoomOut.disabled=game.zoom<=.65;ui.zoomIn.disabled=game.zoom>=1.3;}

ui.presets.forEach(button=>button.addEventListener('click',()=>{ui.input.value=button.dataset.pairs;updatePreset();}));
ui.input.addEventListener('input',updatePreset);
ui.themes.forEach(button=>button.addEventListener('click',()=>changeTheme(button.dataset.theme)));
ui.start.addEventListener('click',startGame);ui.previewStart.addEventListener('click',startGame);
ui.pause.addEventListener('click',togglePause);ui.resume.addEventListener('click',resume);
ui.zoomIn.addEventListener('click',()=>zoom(.1));ui.zoomOut.addEventListener('click',()=>zoom(-.1));
ui.sound.addEventListener('click',()=>{game.sound=!game.sound;ui.sound.setAttribute('aria-pressed',String(game.sound));ui.sound.setAttribute('aria-label',game.sound?'Desativar sons':'Ativar sons');ui.sound.querySelector('.sound-label').textContent=game.sound?'Som ligado':'Som desligado';});
ui.closeWin.addEventListener('click',()=>ui.dialog.close());ui.playAgain.addEventListener('click',startGame);
ui.dialog.addEventListener('close',()=>{if(game.state==='won')ui.start.focus();});
previewBoard();updateReadyPreview();
