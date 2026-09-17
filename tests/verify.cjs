const {JSDOM}=require('jsdom'),fs=require('fs'),path=require('path'),assert=require('assert/strict');
const base=path.resolve(__dirname,'../dist'),html=fs.readFileSync(base+'/index.html','utf8');
const source=['data.js','exams-data.js','online-exams.js','app.js'].map(f=>fs.readFileSync(base+'/'+f,'utf8')).join('\n');
let tools={};
function load(saved){const dom=new JSDOM(html,{url:'https://example.org/',runScripts:'outside-only',pretendToBeVisual:true}),w=dom.window;w.scrollTo=()=>{};w.HTMLElement.prototype.scrollIntoView=()=>{};w.confirm=()=>true;w.document.modelContext={registerTool(t){tools[t.name]=t;}};if(saved)w.localStorage.setItem('english-lab-klasse-7-v1',saved);w.eval(source+'\nwindow.testEval=s=>eval(s);');return dom;}
let dom=load(),w=dom.window;const ev=s=>w.testEval(s);function route(s){w.location.hash=s;ev('render(false)');}function click(s){w.document.querySelector(s).click();}function input(el,v){el.value=v;el.dispatchEvent(new w.Event('input',{bubbles:true}));}
(async()=>{
const D=w.LAB_DATA,EX=w.EXAMS;assert.equal(D.questions.length,196);assert.equal(D.grammar.length,14);assert.equal(new Set(D.questions.map(q=>q.id)).size,196);
assert.equal(D.curriculum.scope,'Bayern · Gymnasium · Englisch als 1. Fremdsprache · Lernstand Ende Klasse 6');
for(const item of [...D.questions,...D.grammar])assert(item.curriculumGrades.length&&item.curriculumGrades.every(g=>g===5||g===6));
assert.equal(D.questions.filter(q=>q.id.endsWith('-lp56')).length,14);
assert(!D.questions.some(q=>/myself|yours|\bours\b|I have lived here|We have waited/.test(q.prompt)));
assert(!D.grammar.some(t=>t.forms.some(f=>/myself|ourselves|since Monday|when she arrives|mine, yours/i.test(f))));
assert(D.questions.some(q=>q.prompt.includes('timetable')));

for(const q of D.questions){assert(q.year===0);for(const a of q.answers)assert(ev(`matchAnswer(D.questions.find(q=>q.id===${JSON.stringify(q.id)}),${JSON.stringify(a)})`));ev(`state.session={kind:'topic',ids:[${JSON.stringify(q.id)}],index:0,responses:{}}`);route('quiz');assert(w.document.querySelector('#answer-form'));}
for(const t of D.grammar){assert.equal(D.questions.filter(q=>q.topic===t.id).length,14);for(const l of ['basic','apply','transfer'])assert.equal(ev(`questionSet('topic','${t.id}','${l}').length`),l==='transfer'?6:4);}
assert.equal(ev("questionSet('diagnostic').length"),12);for(let i=0;i<10;i++){const topics=ev("questionSet('mixed').map(q=>q.topic)");assert.equal(new Set(topics).size,12);}
ev('state.session=null');
for(const r of ['home','practice','grammar',...D.grammar.map(t=>'grammar/'+t.id),'exams',...Object.keys(EX).map(y=>'exam/'+y),'progress','writing','listening']){
 route(r);const doc=w.document;assert(doc.querySelector('h1'),r);assert(!doc.querySelector('main').innerHTML.includes('undefined'),r);const ids=[...doc.querySelectorAll('[id]')].map(x=>x.id);assert.equal(ids.length,new Set(ids).size,r+' unique IDs');
 for(const el of doc.querySelectorAll('input,textarea,select'))assert(el.id&&doc.querySelector(`label[for="${el.id}"]`)||el.closest('label')||el.getAttribute('aria-label'),r+' labelled form');
 for(const el of doc.querySelectorAll('[src],a[href]')){const url=el.getAttribute('src')||el.getAttribute('href');if(!url||url.startsWith('#')||url.startsWith('http'))continue;assert(fs.existsSync(path.join(base,decodeURIComponent(url.split('#')[0]))),url);}
 if(!r.startsWith('exam/')&&r!=='exams')assert(!doc.querySelector('audio,[data-exam-listen],[data-exam-field]'),r+' no prior test content');
}
assert(!w.document.querySelector('[data-nav="writing"],[data-nav="listening"]'));route('home');assert.equal(w.document.querySelectorAll('.plan-row').length,11);assert(!/\d{2}\.\d{2}\./.test([...w.document.querySelectorAll('.plan-row')].map(e=>e.textContent).join('')));let box=w.document.querySelector('[data-plan="0"]');box.checked=true;box.dispatchEvent(new w.Event('change',{bubbles:true}));assert.equal(w.document.querySelector('#plan-count').textContent,'1 / 11 Einheiten');
ev("startSession('diagnostic');render(false)");input(w.document.querySelector('#answer'),'unsubmitted');route('grammar/present');route('quiz');assert.equal(w.document.querySelector('#answer').value,'unsubmitted');ev("checkAnswer('wrong')");assert.equal(ev('stats().attempted'),1);ev("checkAnswer('wrong')");assert.equal(ev('state.answers[state.session.ids[0]].attempts'),1);assert(w.document.querySelector('#answer-feedback').textContent.includes('Passende Antwort'));
for(const [y,e] of Object.entries(EX)){
 assert.equal(e.grammar.length,20);assert.equal(e.listening.flatMap(g=>g.items).reduce((n,i)=>n+i.points,0),20);assert.equal(new Set(e.listening.flatMap(g=>g.items).map(i=>i.id)).size,e.listening.flatMap(g=>g.items).length);
 assert.equal(e.passages.flatMap(p=>[...p.text.matchAll(/\{\{(\d+)\}\}/g)].map(m=>m[1])).length,20);
 for(const g of e.grammar){assert(D.grammar.some(t=>t.id===g.topic));for(const a of g.answers)assert(ev(`examGrammarCorrect(EX[${y}].grammar.find(g=>g.id==='${g.id}'),${JSON.stringify(a)})`));}
 route('exam/'+y);assert.equal(w.document.querySelectorAll('[data-exam-grammar]').length,20);assert.equal(w.document.querySelector(`[data-exam-timer="${y}"]`).textContent,'50:00');assert(!w.document.querySelector('[data-exam-self]'));
 input(w.document.querySelector('[data-exam-listen]'),'saved answer');input(w.document.querySelector('[data-exam-grammar]'),'grammar draft');input(w.document.querySelector('#exam-writing-text'),'A message to my friend.');assert.equal(w.document.querySelector('#exam-word-count').textContent,'5 Wörter');route('home');route('exam/'+y);assert.equal(w.document.querySelector('[data-exam-listen]').value,'saved answer');assert.equal(w.document.querySelector('[data-exam-grammar]').value,'grammar draft');
 click(`[data-action="exam-timer:${y}"]`);assert(ev(`examState(${y}).timer.running`));click(`[data-action="exam-timer:${y}"]`);assert(!ev(`examState(${y}).timer.running`));
 ev(`(()=>{let s=examState(${y});for(const g of EX[${y}].grammar)s.grammar[g.id]=g.answers[0];for(const i of EX[${y}].listening.flatMap(g=>g.items)){if(i.type==='choice')s.listening[i.id]=[...i.correct];else s.listening[i.id]=i.key;}})()`);route('exam/'+y);click(`[data-action="exam-submit:${y}"]`);assert(ev(`examState(${y}).submitted`));assert.equal(ev(`examScore(${y}).grammar`),20);assert.equal(ev(`examScore(${y}).total`),null);assert(w.document.querySelector('[data-exam-grammar]').disabled);assert(w.document.querySelector('#exam-writing-text').disabled);
 for(const el of w.document.querySelectorAll('[data-exam-self]')){el.value=[...el.options].at(-1).value;el.dispatchEvent(new w.Event('change',{bubbles:true}));}assert.equal(ev(`examScore(${y}).total`),60,y+' perfect total');
 const answerBefore=ev(`examState(${y}).grammar['1']`);input(w.document.querySelector('[data-exam-grammar]'),'tampered');assert.equal(ev(`examState(${y}).grammar['1']`),answerBefore);
 ev(`examState(${y}).grammar['1']='wrong'`);assert.equal(ev(`examScore(${y}).total`),59);
 click(`[data-action="exam-edit:${y}"]`);assert.equal(ev(`Object.keys(examState(${y}).self).length`),0);assert.equal(w.document.querySelector('#exam-writing-text').value,'A message to my friend.');
}
route('exam/2021');ev('examState(2021).submitted=true');route('exam/2021');let select=w.document.querySelector('[data-exam-self="l:8"]');assert([...select.options].some(o=>o.value==='3'));select.value='2.5';select.dispatchEvent(new w.Event('change',{bubbles:true}));assert.equal(ev("examState(2021).self['l:8']"),'2.5');
assert(ev("!examGrammarCorrect(EX[2022].grammar[0],'australian')"));assert(ev("!matchAnswer(D.questions.find(q=>q.id==='n-words-07'),'british')"));
const before=ev('JSON.stringify(state)');assert.throws(()=>tools.start_grammar_practice.execute({topic:'not-real'}));assert.equal(ev('JSON.stringify(state)'),before);tools.start_grammar_practice.execute({topic:'past'});assert.equal(ev('state.session.ids.length'),12);
ev('save()');const saved=w.localStorage.getItem('english-lab-klasse-7-v1');dom.window.close();dom=load(saved);w=dom.window;assert.equal(ev('examState(2025).writing'),'A message to my friend.');assert.equal(ev('state.plan[0]'),true);
// Missions reward actual answers; skipping and replaying cannot inflate the best score.
ev('state=defaults()');
for(const id of ['time','detective','workshop']){const qs=ev(`questionSet('mission','${id}')`);assert.equal(qs.length,5);assert.equal(new Set(qs.map(q=>q.id)).size,5);assert(qs.every(q=>ev(`MISSIONS.find(m=>m.id==='${id}').topics.includes('${q.topic}')`)));}
assert.equal(ev("questionSet('mission','invalid').length"),0);
for(const [correct,stars] of [[0,0],[1,1],[2,1],[3,2],[4,2],[5,3]])assert.equal(ev(`missionStars(${correct})`),stars);
ev("startSession('mission','time');render(false)");
assert.equal(w.document.querySelectorAll('.mission-trail li').length,5);
ev("checkAnswer('incorrect')");click('[data-action="next"]');
for(let i=1;i<5;i++){ev('checkAnswer(D.questions.find(q=>q.id===state.session.ids[state.session.index]).answers[0])');click('[data-action="next"]');}
assert.equal(ev("bestStars('time')"),2);assert(w.document.querySelector('.mission-finish').textContent.includes('2 von 3 Sternen'));assert(ev('earnedBadges()[0].earned'));
const wrong=ev('state.session.ids[0]');ev(`state.session={kind:'mistakes',ids:['${wrong}'],index:0,responses:{}};render(false);checkAnswer(D.questions.find(q=>q.id==='${wrong}').answers[0])`);assert(ev('earnedBadges()[2].earned'));
ev("startSession('mission','time');render(false)");for(let i=0;i<5;i++)click('[data-action="skip"]');assert.equal(ev("bestStars('time')"),2);assert(w.document.querySelector('.mission-finish').textContent.includes('0 von 3 Sternen'));
for(const id of ['time','detective','workshop']){ev(`startSession('mission','${id}');render(false)`);for(let i=0;i<5;i++){ev('checkAnswer(D.questions.find(q=>q.id===state.session.ids[state.session.index]).answers[0])');click('[data-action="next"]');}assert.equal(ev(`bestStars('${id}')`),3);}
assert(ev('earnedBadges()[3].earned'));route('exam/2025');assert(!w.document.querySelector('.mission-board,.mission-trail,.badge-shelf,.mission-finish'));
ev('save()');const missionSaved=w.localStorage.getItem('english-lab-klasse-7-v1');dom.window.close();dom=load(missionSaved);w=dom.window;assert.equal(ev("bestStars('time')"),3);assert(ev('earnedBadges()[2].earned'));assert(ev('earnedBadges()[3].earned'));
const legacy=JSON.parse(missionSaved);delete legacy.data.missions;legacy.data.plan[0]=true;dom.window.close();dom=load(JSON.stringify(legacy));w=dom.window;assert.equal(ev("bestStars('time')"),0);assert.equal(ev('state.plan[0]'),true);assert(ev('stats().attempted>0'));dom.window.close();
// Exercise controls: real selection, submission, saved drafts and immutable feedback.
dom=load();w=dom.window;
const submit=()=>w.document.querySelector('#answer-form').dispatchEvent(new w.Event('submit',{bubbles:true,cancelable:true}));
const openQuestion=id=>{ev(`state.session={kind:'topic',ids:[${JSON.stringify(id)}],index:0,responses:{}}`);route('quiz');};
const choiceQ=w.LAB_DATA.questions.find(q=>q.type==='choice');
openQuestion(choiceQ.id);let incorrect=[...w.document.querySelectorAll('[data-exercise-option]')].find(el=>!ev(`matchAnswer(D.questions.find(q=>q.id==='${choiceQ.id}'),${JSON.stringify(el.value)})`));incorrect.click();submit();assert(!ev(`state.answers['${choiceQ.id}'].correct`));
openQuestion(choiceQ.id);let right=[...w.document.querySelectorAll('[data-exercise-option]')].find(el=>ev(`matchAnswer(D.questions.find(q=>q.id==='${choiceQ.id}'),${JSON.stringify(el.value)})`));right.click();route('grammar/present');route('quiz');assert(w.document.querySelector('[data-exercise-option]:checked'));
const choiceSaved=w.localStorage.getItem('english-lab-klasse-7-v1');dom.window.close();dom=load(choiceSaved);w=dom.window;route('quiz');assert(w.document.querySelector('[data-exercise-option]:checked'));submit();assert(ev(`state.answers['${choiceQ.id}'].correct`));assert(w.document.querySelector('[data-exercise-option]').disabled);
const orderQ=w.LAB_DATA.questions.find(q=>q.type==='order');openQuestion(orderQ.id);click('[data-action="puzzle-add:0"]');submit();assert(!ev(`state.session.responses['${orderQ.id}']`));route('grammar/present');route('quiz');assert.equal(ev('state.session.exerciseUI[state.session.ids[0]].picked.length'),1);
const puzzleSaved=w.localStorage.getItem('english-lab-klasse-7-v1');dom.window.close();dom=load(puzzleSaved);w=dom.window;route('quiz');assert.equal(w.document.querySelectorAll('.puzzle-answer button').length,1);click('[data-action="puzzle-remove:0"]');assert.equal(w.document.querySelectorAll('.puzzle-answer button').length,0);click('[data-action="puzzle-add:0"]');click('[data-action="puzzle-clear"]');assert.equal(ev('state.session.exerciseUI[state.session.ids[0]].picked.length'),0);
for(let i=orderQ.parts.length-1;i>=0;i--)click(`[data-action="puzzle-add:${i}"]`);submit();assert(!ev(`state.answers['${orderQ.id}'].correct`));
for(const q of w.LAB_DATA.questions.filter(q=>q.type==='order')){openQuestion(q.id);for(let i=0;i<q.parts.length;i++)click(`[data-action="puzzle-add:${i}"]`);submit();assert(ev(`state.answers['${q.id}'].correct`),q.id);const before=ev('JSON.stringify(state.session)');ev("exerciseAction('puzzle-clear')");assert.equal(ev('JSON.stringify(state.session)'),before);}
for(const q of w.LAB_DATA.questions.filter(q=>q.type==='error')){openQuestion(q.id);const index=q.parts.indexOf(q.answers[0]);assert(index>=0);click(`[data-action="error-pick:${(index+1)%q.parts.length}"]`);submit();assert(!ev(`state.answers['${q.id}'].correct`));openQuestion(q.id);click(`[data-action="error-pick:${index}"]`);submit();assert(ev(`state.answers['${q.id}'].correct`));assert(w.document.querySelector('#answer-feedback').textContent.includes(q.correctedSentence));}
for(const q of w.LAB_DATA.questions.filter(q=>q.type==='choice'))assert.equal(q.options.filter(a=>ev(`matchAnswer(D.questions.find(q=>q.id==='${q.id}'),${JSON.stringify(a)})`)).length,1);
for(const kind of ['input','choice','order','error']){ev(`startSession('format','${kind}');render(false)`);assert.equal(ev('state.session.ids.length'),12);assert(ev(`state.session.ids.every(id=>D.questions.find(q=>q.id===id).type==='${kind}')`));}
// Stars are based on distinct mastered tasks, including corrected errors; never farmed or lost.
ev('state=defaults()');const presentQs=w.LAB_DATA.questions.filter(q=>q.topic==='present');
for(let i=0;i<presentQs.length;i++){const q=presentQs[i];openQuestion(q.id);if(i===0){ev("checkAnswer('wrong')");openQuestion(q.id);}ev(`checkAnswer(${JSON.stringify(q.answers[0])})`);assert.equal(ev("topicProgress('present').stars"),i+1>=14?3:i+1>=10?2:i+1>=5?1:0);if(i===4)assert(w.document.querySelector('.new-star'));}
const mastered=ev("topicProgress('present').correct");openQuestion(presentQs[0].id);ev("checkAnswer('wrong again')");assert.equal(ev("topicProgress('present').correct"),mastered);assert.equal(ev("topicProgress('present').stars"),3);openQuestion(presentQs[0].id);ev(`checkAnswer(${JSON.stringify(presentQs[0].answers[0])})`);assert.equal(ev("topicProgress('present').correct"),mastered);
ev('save()');const starsSaved=w.localStorage.getItem('english-lab-klasse-7-v1');dom.window.close();dom=load(starsSaved);w=dom.window;assert.equal(ev("topicProgress('present').stars"),3);dom.window.close();

const oldContent={version:1,data:{answers:{'n-perfect-05':{correct:true,answer:'since'},'n-present-01':{correct:true,answer:'walks'}},session:{kind:'diagnostic',ids:['n-perfect-05'],index:0,responses:{}},plan:{0:true},exams:{2025:{writing:'Keep this original test draft.'}}}};
dom=load(JSON.stringify(oldContent));w=dom.window;assert.equal(ev('state.session'),null);assert.equal(ev('stats().correct'),1);assert.equal(ev("state.answers['n-perfect-05'].answer"),'since');assert.equal(ev("state.answers['n-perfect-05-lp56']"),undefined);assert.equal(ev('state.plan[0]'),true);assert.equal(ev('examState(2025).writing'),'Keep this original test draft.');dom.window.close();
console.log('PASS: curriculum metadata, revised-question isolation and preserved legacy progress, five-question missions, honest persistent stars, earned badges, legacy data migration, 196 independent answer keys, all four exercise controls, saved puzzles, permanent topic stars, all topic levels, 100 original grammar keys, five 60-point exams, hidden solutions, 50-minute timers, score limits, saved drafts, navigation, asset links and labelled forms. Emulated DOM, no browser visual QA.');
})().catch(e=>{console.error(e);dom.window.close();process.exitCode=1;});
