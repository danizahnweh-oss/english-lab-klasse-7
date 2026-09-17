"""Transcribe teacher-supplied original tests. Keep source PDFs unchanged."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TEXT=ROOT/'content/source-text'
E={}
def free(id,label,key,points=1):return dict(id=id,label=label,key=key,type='text',points=points)
def choice(id,label,options,correct):return dict(id=id,label=label,options=options,correct=correct,type='choice',points=len(correct))
def tf(id,label,yes):return choice(id,label,['true','false'],[0 if yes else 1])
def group(title,*items,image=None,alt=None):
 d=dict(title=title,items=list(items))
 if image:d.update(image='material/'+image,alt=alt)
 return d
L={
2021:[
 group('Part A · 1. Complete the sentence.',free('1a','Mr Schneider, the new English teacher, is … (first adjective)','young / friendly'),free('1b','… and … (second adjective)','friendly / young. Beide Eigenschaften nennen, keine doppelte Wertung.')),
 group('2. Why didn’t the students like sightseeing in their holidays?',choice('2','Tick the correct answer.',['They weren’t interested in new places.','They didn’t want to learn new things about old places.','They already knew a lot about the places from school trips.','They had to walk around for a long time, which was often boring.'],[3])),
 group('3. What do the students like to do in the holidays?',choice('3','Tick the correct picture.',['A · Kino','B · Burg besichtigen','C · Videospiele','D · Musik hören'],[2]),image='2021-listening.webp',alt='Originalbilder von links nach rechts: Kino mit Popcorn, Burg, Spielecontroller, Kopfhörer.'),
 group('4. How does Mr Schneider want to start the new school year?',free('4a','Mr Schneider doesn’t want to talk about last year’s grammar and he doesn’t like the idea of beginning with the …','(new) book'),free('4b','His idea is to start the new school year with …','presentations'),free('4c','… but first he has to look for …','an interesting topic / a topic / good ideas')),
 group('Part B · 5. Mr Schneider’s instructions for the project.',free('5a','Get into groups of … students.','four / 4'),free('5b','Choose … museums from the list.','two or three / 2 or 3'),free('5c','Look at the … they offer.','online tours')),
 group('6. The Smithsonian Museum',free('6a','Where is it?','Washington (D.C.) / capital of the USA'),free('6b','What is special about the museum? First aspect.','one of the largest museums (in the world) / a very large museum; many online tours. Nur „the largest museum“: 0 BE.'),free('6c','What is special about the museum? Second aspect.','Der andere Aspekt: many online tours ODER one of the largest / a very large museum. Keine doppelte Wertung.')),
 group('7. The British Museum. Select tour 1 or tour 2.',*[choice('7'+str(i+1),label,['1','2'],[a]) for i,(label,a) in enumerate([('It is the perfect tour for young people.',1),('The tour takes too much of their time.',0),('You get great details about everything in the museum.',0),('Max and the others have problems to understand everything.',0)])]),
 group('8. Give three reasons why the students think online tours are great.',free('8','Write three different reasons.','Drei verschiedene Gründe: auf dem Sofa bleiben; schneller als ein Besuch; anhalten und zurückgehen; Zeit für interessante Dinge; Langweiliges überspringen; kostenlos; nicht in den Ferien nötig. Pro richtigem Aspekt 1 BE.',3))],
2022:[
 group('Part A · 1. Fill in the information.',free('1a','Number of German towns/cities with a British partner:','553'),free('1b','Why twinning is a good idea:','People from different countries can meet / make friends.')),
 group('2. Which city is it?',*[choice('2'+str(i+1),label,['L · London','M · Munich','O · Oxford'],[a]) for i,(label,a) in enumerate([('The city where Mr Black shows a film:',1),('The city where Mr Black lives:',2),('The city where lots of international students met:',0),('The city where the partner school is going to be:',2)])]),
 group('3. Tick the correct answer.',choice('3','Some students stayed at home and joined the project online because …',['it was too expensive to go there.','they didn’t have time to travel there.','there were too many students there already.'],[0])),
 group('4. Write down Sarah’s idea.',free('4','What to do on Saturdays and Sundays:','go and visit places (with families)')),
 group('Part B · 5. The German students’ time at their English partner school.',free('5a','The lessons ended at …','(a) quarter to four (in the afternoon) / 3.45 pm / 15:45'),free('5b','The clubs they went to were the chess club and the …','yearbook / drama club')),
 group('6. Tick the correct answer.',choice('6','The English students knew they were German visitors because …',['they spoke German.','they asked lots of questions.','they didn’t wear school uniforms.'],[2])),
 group('7. Finish the sentence.',free('7','Paul remembers that the families they stayed with were friendly and …','asked a lot of questions about what they do at home; the German students learnt lots about life in England.')),
 group('8. What did Sarah get on Easter Sunday?',choice('8','Tick the correct picture.',['A · Hase','B · Eier','C · Schaf'],[1]),image='2022-listening.webp',alt='Originalbilder von links nach rechts: Schokoladenhase, verpackte Ostereier, Schokoladenschaf.'),
 group('9. Tick the correct answer.',choice('9','Choose one statement.',['They ate the painted eggs on top of the hill.','They had a picnic before they went up the hill.','They had lovely food when they arrived at the top of the hill.'],[2])),
 group('10. Complete the text.',free('10a','Egg rolling is … in England.','an old Easter tradition / a tradition / a competition'),free('10b','This is how it works: Each person takes one egg. All the eggs have … Then they start at the top and roll them down the hill.','a different colour / different colours')),
 group('11. Who?',*[choice('11'+str(i+1),label,['J · John','L · Lucy','S · Sarah'],[a]) for i,(label,a) in enumerate([('… won the second round.',1),('… won more rounds than the others.',0),('… had the fastest egg in round one.',2),('… had the egg that went the longest way in round two.',1)])])],
2023:[
 group('Part A · 1. Schools in the last fifty years.',free('1','One aspect that has changed:','interactive whiteboards / computers / tablets / internet')),
 group('2. Tick the correct statement.',choice('2','Alice Springs is …',['in the west of Australia.','six hours away from Julie’s home.','a village where only a few people live.'],[1])),
 group('3. Information on Julie and her school.',free('3a','Name of the school: Alice Springs …','School of the Air'),free('3b','Age at which Julie became a student:','three and a half / 3.5 / 3½ (auch 3,5)'),free('3c','The month when the school year starts:','February'),free('3d','Age of the school:','70 years old')),
 group('4. Typical school days. True or false?',tf('4a','Julie gets her worksheets by e-mail every week.',False),tf('4b','Lessons start at quarter to nine.',True),tf('4c','Ms Baker is their teacher.',False),tf('4d','The class always celebrates birthdays on Fridays.',False)),
 group('5. Complete the sentences.',free('5a','In her class, there are … other students and Julie.','12 / twelve'),free('5b','She finds it good to be in such a small class because … and everybody can be active during lessons every day.','she gets lots of chances to ask questions / she can ask lots of questions')),
 group('Part B · 6. At high school.',free('6','Fifteen: number of …','lessons (a week)')),
 group('7. Tick the two correct statements.',choice('7','Her year’s website is important for Julie and the other students because they can …',['read stories.','write to their teachers.','chat with their classmates.','do worksheets and get feedback.','watch some of their lessons again.'],[3,4])),
 group('8. Julie’s afternoons.',choice('8','Tick the picture which shows what she often does.',['A · Reiten','B · Schwimmen','C · Radfahren'],[0]),image='2023-listening.webp',alt='Originalbilder von links nach rechts: Reiten, Schwimmbad, Radfahren.'),
 group('9. Complete the sentence.',free('9a','For Julie, the get-together week is the … in the school year.','most exciting time / best week (ever)'),free('9b','… because …','the students and teachers meet at a camp / the students see each other face-to-face')),
 group('10. Complete.',free('10a','Julie’s best friend is Noah. His school room is on …','wheels'),free('10b','He travels around with his parents because they work in …','different places'))],
2024:[
 group('Part A · 1. King’s School in Canterbury.',free('1','Number of students at King’s School:','400 / four hundred')),
 group('2. What’s special about King’s School?',free('2a','King’s School has a partner school which is “Down Under”. This is what people from Australia say when they speak about their …','country'),free('2b','British students travel to meet their partners face-to-face in the month of …','December'),free('2c','… because it’s … there.','summer / summertime / warm / hot')),
 group('3. What British students do in Australia.',choice('3','Tick the correct picture.',['A · Unterricht','B · Strand','C · Zoo','D · Kino'],[1]),image='2024-listening.webp',alt='Originalbilder von links nach rechts: Klassenzimmer, Strand, Zoo, Kino.'),
 group('4. The project.',choice('4','Tick the correct statement.',['The kids meet on the Internet one day every week.','Students from class 8JT take part with their partners from Down Under.','Liz and Noah are preparing presentations on their last holidays.'],[0])),
 group('5. British Bank Holidays.',free('5a','In Britain almost all Bank Holidays are on a …','Monday'),free('5b','People often go away to cool places like …, zoos, or fun parks.','museums'),free('5c','Only one group of people is not happy about Bank Holidays: the …','shop assistants')),
 group('6. Liz’s last Bank Holiday.',choice('6','Liz and her family …',['travelled to the sea by car.','spent a day at the beach and had fish and chips there.','went on some rides at the fun park but not everybody loved them.'],[2])),
 group('7. Dreamland.',free('7','An attraction at Dreamland is the oldest roller coaster in the country. It’s also special because it’s …','made of wood / wooden')),
 group('8. The history of Bank Holidays.',free('8a','When they started:','(about) 150 years ago'),free('8b','Where the name comes from:','(just the) banks closed'),free('8c','Why people in Northern Ireland are lucky:','ten / 10 Bank Holidays / highest number of Bank Holidays in the UK / they have more Bank Holidays')),
 group('Part B · 9. A regatta on Todd River.',free('9a','Usually, a regatta is a boat race. The regatta on Todd River is different: this river in fact isn’t really a river because there is …','just sand / no water'),free('9b','The first regatta on Todd River took place in the year …','1962'),free('9c','… because some people wanted to …','raise money for charity / raise money')),
 group('10. The Henley-on-Todd Regatta.',choice('10','Tick the correct statement.',['Everybody can join in the regatta for free.','The event starts with a team competition.','The regatta is always on the same day in August.'],[2])),
 group('11. The Battle of the Boats.',free('11a','There are three teams. All of them wear …','crazy costumes'),free('11b','Their boats aren’t real boats because …','the teams can’t sit in them / have to carry them'))],
2025:[
 group('Part A · 1. Complete the sentences.',free('1a','The Council of Europe is like a …','big club'),free('1b','Most of the … are in it.','countries in Europe / European countries'),free('1c','Their mission is to make Europe …','a better place (to grow up in / for kids)')),
 group('2. The Council of Europe.',free('2a','Year in which it began:','1949'),free('2b','City where it began:','London'),free('2c','Number of people who live in its member states:','(almost) 700 million / 700m / 700,000,000; auch abweichende deutsche Zahlenschreibung zulässig.')),
 group('3. Languages. True or false?',tf('3a','People speak a lot more languages than there are states.',True),tf('3b','Each country has just one national language.',False),tf('3c','Some people in Spain and Italy speak the oldest European language.',False)),
 group('4. What do governments do to save special languages?',choice('4','Tick the two correct aspects.',['teach them at schools','have films in these languages','sell books in these languages','have special language camps'],[0,3])),
 group('5. Complete the sentences.',free('5a','Ms Smith says that learning new languages is good for our brains because it …','trains the way we think / makes us smarter'),free('5b','It also changes the way we see others because it helps us to …','become more open / understand other cultures better / communicate')),
 group('6. Complete the sentences.',free('6a','The first European Day of Languages was in the year 2001. Since then, it has always been on the same date:','26 September'),free('6b','On this day, there are events where people can …','try out / get interested in learning new languages. Nicht nur: learn new languages.')),
 group('Part B · 7. The European Day of Languages in class 7A.',free('7a','The students can get ideas from the … of the European Day of Languages. These ideas should not be too hard.','website / homepage. Nicht: Internet.'),free('7b','One student’s idea is to find out …','which countries his classmates’ families come from / how many languages the students in 7A speak in their families')),
 group('8. The big challenge. True or false?',tf('8a','One group chooses a place somewhere in the world and the other group must find it.',False),tf('8b','When the students find the place, they type in its name.',False)),
 group('9. Answer the question.',free('9','What exactly gives the players tips about the places?','(the language of) street signs / posters'))]
}
# The underlined erroneous spans in document order, official answers, and grammar topic.
C={
2021:[('heared','heard','perfect'),('don’t','haven’t|have not','questions'),('what','which|that','relatives'),('foots','feet','plural'),('didn’t knew','didn’t know|did not know','past'),('who’s','whose','relatives'),('has become','became','past'),('hurted','hurt','past'),('must','had to','modals'),('Than','Then|And','connectors'),('so fast like','as fast as|as fast as a','comparison'),('can’t','weren’t allowed to|were not allowed to|couldn’t|could not|weren’t able to|were not able to','modals'),('much','lots of|a lot of|many','quantifiers'),('ever did','has ever done','perfect'),('lucky','happy','words'),('their','there','pronouns'),('needn’t','don’t need|do not need|needn’t have|need not have','modals'),('childrens','children|kids','plural'),('that you','you to','words'),('bored','boring','words')],
2022:[('australian','Australian','words'),('now','know','words'),('Peoples','People','plural'),('an','her','pronouns'),('buyed','bought','past'),('makes','is','words'),('so lazy like','as lazy as','comparison'),('already saw','has already seen','perfect'),('their','they are|they’re','pronouns'),('familys','family’s','pronouns'),('stands up','gets up|wakes up','words'),('lucky','happy|healthy','words'),('At','In','prepositions'),('run not','don’t run|do not run|can’t run|cannot run|won’t run|will not run','present'),('most good','best','comparison'),('called she','did she call','questions'),('while','because','connectors'),('If','When','connectors'),('it gives','there are|they have','pronouns'),('much','many|a lot of|lots of|more','quantifiers')],
2023:[('The most','Most|Most of the','quantifiers'),('has started','started','past'),('while','during|because of','connectors'),('opens','open','modals'),('australian','Australian','words'),('at','in','prepositions'),('gived','gave','past'),('more good','better','comparison'),('thinks','thought','past'),('much','many','quantifiers'),('didn’t saw','didn’t see|did not see','past'),('wasn’t allowed','wasn’t able|was not able','modals'),('musted','had to','modals'),('exciting','excited','words'),('peoples','people','plural'),('am o’clock','am|a.m.','prepositions'),('popularest','most popular','comparison'),('go','goes','present'),('a lots','a lot|lots','quantifiers'),('was never','have never been','perfect')],
2024:[('heared','heard','perfect'),('has gone','went','past'),('interesting','interested','words'),('famousest','most famous','comparison'),('who','which|that','relatives'),('five','fifth|5th','words'),('from','of','prepositions'),('did he','did he do','questions'),('become','became|were becoming|got|were getting','past'),('much','many','quantifiers'),('tryed','tried','past')],
2025:[('there','their','pronouns'),('didn’t have','weren’t allowed|were not allowed','modals'),('choosed','chose|decided','past'),('more easy','easier|much easier','comparison'),('kids','kids’|children’s','pronouns'),('who','which','relatives'),('Smith’s','Smiths’','pronouns'),('played she','did she play','questions'),('like','as','comparison'),('see','watch','words')]
}
# Extract continuous original text, remove only answer lines and print layout whitespace.
starts={2021:'You have already',2022:'When you meet Izzy',2023:'The most',2024:'Have you ever',2025:'Not an easy task!'}
ends={2021:'_____ / 20 BE',2022:'From:',2023:'From:',2024:'=== PAGE 5 ===',2025:'=== PAGE 5 ==='}
for y in range(2021,2026):
 text=(TEXT/f'JA7_GY_E_{y}_Aufg.txt').read_text();s=text[text.index(starts[y]):];s=s[:s.index(ends[y])];s=re.sub(r'_+','',s);s=re.sub(r'\s+',' ',s).strip();s=re.sub(r' [46]$','',s)
 # Repair extraction-only spacing; preserve original wording and intentional errors.
 for a,b in {'COVID -19':'COVID-19','spe cial':'special','lo ves':'loves','fi ve':'five','w hole':'whole','tr yed':'tryed','p layed':'played','W e':'We','teenage boy':'teenage boy'}.items():s=s.replace(a,b)
 s=re.sub(r'\bth e\b','the',s)
 cursor=0;parts=[];items=[]
 for i,(bad,ans,t) in enumerate(C[y],1):
  m=re.search(r'(?<!\w)'+re.escape(bad)+r'(?!\w)',s[cursor:]);assert m,(y,bad,s[cursor:])
  at=cursor+m.start();parts.append(s[cursor:at]);parts.append('{{'+str(i)+'}}');cursor=at+len(bad)
  items.append(dict(id=str(i),type='correction',original=bad,answers=ans.split('|'),topic=t,caseSensitive=bad=='australian',points=1))
 parts.append(s[cursor:]);passages=[dict(title='Part A · Fehler verbessern' if y>=2024 else 'Fehler verbessern',kind='correction',text=''.join(parts),ids=[q['id'] for q in items])]
 E[y]=dict(year=y,listening=L[y],grammar=items,passages=passages)
# Original Part B word boxes: each box is used once; a single common bank preserves the task.
B={
2024:("Harvey had lots of energy, {{12}} he? He was still able to play games when they camped in the evenings {{13}} he walked long distances every day. He never {{14}} too tired at the end of the day.\nOther young children have also done the trail, but Harvey is several months younger {{15}} “Buddy Backpacker”, the youngest hiker on the trail before Harvey.\nAnother hiker, {{16}} name is Dale “Greybeard” Sanders, is very proud of {{17}} trip. He said: “Harvey is {{18}} adult hikers. This trip is going to change his and his parents’ {{19}} forever.” One thing is sure for Harvey: If he gets the chance, he {{20}} the Appalachian Trail again.",[
('didn’t',['hadn’t','didn’t','hasn’t'],'questions'),('although',['but','although','so'],'connectors'),('felt',['felt','fell','feel'],'past'),('than',['than','then','like'],'comparison'),('whose',["who’s",'which','whose'],'relatives'),('Harvey’s',['Harvey’s','Harveys’','Harveys'],'pronouns'),('as strong as',['as strong as','as strong like','strong as'],'comparison'),('lives',['living','lives','life'],'plural'),('will hike',['hiked','will hike','is hiking'],'future')]),
2025:("My friend's name is Cathy and she's 27. She doesn't have a smartphone {{11}} she needs smartphone skills in her job. I asked her why not.\n“Well, {{12}} I said goodbye to smartphones, I had one,” she said, “but I didn't like it. I had so many messages on my phone that I didn’t want to answer right away.” This was too much for Cathy. All her friends {{13}} write back really fast. But who can do that?\nMany don’t understand why the digital detox trend {{14}} faster yet. It is true that we all use technology {{15}}. People are always on their {{16}}, even when they're with friends or family. Being without a smartphone can {{17}} us a lot: We can practise how to {{18}} the best route on our own, for example.\nCathy’s life without a mobile phone can be an example for more people to {{19}} non-smartphone users and find more useful ways to spend their time. Try to be without your phone for {{20}} five hours a day for a start!",[
('although',['so that','because','although'],'connectors'),('before',['before','while','after'],'connectors'),('wanted her to',['she wanted to','wanted that she','wanted her to'],'words'),('hasn’t grown',['doesn’t grow','hasn’t grown','didn’t grow'],'perfect'),('too often',['too often','too many','too strong'],'words'),('phones',['phone’s','phones','phones’'],'plural'),('teach',['learn','teach','make'],'words'),('look for',['look for','look after','look at'],'words'),('become',['get','keep','become'],'words'),('at least',['not less','at least','a few'],'words')])}
for y,(text,rows) in B.items():
 offset=len(E[y]['grammar']);ids=[]
 for i,(answer,options,topic) in enumerate(rows,offset+1):
  ids.append(str(i));E[y]['grammar'].append(dict(id=str(i),type='bank',answers=[answer],topic=topic,points=1))
 # Keep box order from the source, not gap order.
 order=[6,7,1,4,8,0,3,5,2] if y==2024 else [3,0,9,2,1,4,8,7,5,6]
 E[y]['passages'].append(dict(title='Part B · Wortboxen' if y==2024 else 'Part B · Being offline',kind='bank',text=text,ids=ids,boxes=[rows[i][1] for i in order]))
for y,e in E.items():
 assert len(e['grammar'])==20
 assert sum(i['points'] for g in e['listening'] for i in g['items'])==20,(y,'listening points')
 e.update(title={2021:'On foot or online?',2022:'School Twinning',2023:'A special school in Australia',2024:'Holidays and festivals',2025:'The European Day of Languages'}[y],writingTitle={2021:'Englischcamp am See',2022:'Fahrradmarathon',2023:'Besuch in London',2024:'Museum Kunterbunt',2025:'Keltenfestival'}[y],writingPage={2021:5,2022:7,2023:5,2024:6,2025:6}[y],duration=50,words=140)
 text=(TEXT/f'JA7_GY_E_{y}_Aufg.txt').read_text().split(f"=== PAGE {e['writingPage']} ===")[1]
 text=text[text.index('Part III:'):];text=text.split('(Inhalt')[0]
 text=re.sub(r'Part III: Text\s*[Pp]roduction\s*20 BE','',text).strip()
 e['writingSource']=text
 e['writingImage']=f'material/{y}-writing.webp'
 e['writingAlt']='Originalmaterial zur Schreibaufgabe. Die Textfassung steht oberhalb; zusätzliche Bildinformationen stehen darunter.'
 e['files']={k:f'JA7_GY_E_{y}_{v}' for k,v in [('task','Aufg.pdf'),('solution','Loes.pdf'),('audio','Hoerverst.m4a')]}
details={
2021:"Camp-Pinnwand: 7.15 am wake-up call; 7.30 am sports at the lake; 8.15 am breakfast; 9.30 am Fun with English (English lessons in small groups); 12.00 am lunch (so im Original); 2.30 pm activity time, eine Aktivität für die ganze Woche; 6.30 pm dinner; 8.15 pm evening events; 10.30 pm good night. Activities: ball games, drama group, nature explorers, mountain biking. Evening events: MON get together around the campfire; TUES ghost story contest – Who can tell the scariest ghost story?; WED surprise; THUR Last night of the camp show.",
2022:"Fahrradmarathon – Radeln für den guten Zweck! Der Fahrradladen Maier spendet für jeden gefahrenen Kilometer 5 € an die Organisation Wir helfen Tieren. Wer: Jeder, der Spaß am Radfahren hat und gerne Gutes tut. Sportler oder Fitnessmuffel – jeder kann mitmachen! Wann: Samstag, 08. Okt, Start 10.00 Uhr. Treffpunkt: Am Luisenpark gegenüber der Schule. Die drei schnellsten Radfahrer gewinnen je zwei Kinokarten. Veranstalter: Fahrradladen Maier.\nKarte: Das Haus von Dylans Tante liegt an der Sonnenstraße östlich der Wallnerstraße. Nördlich der Sonnenstraße liegt die Schulstraße. Sie führt von der Wallnerstraße nach Osten zwischen Luisenpark im Norden und Schule im Süden. Der Treffpunkt ist im Park gegenüber der Schule markiert. Westlich der Wallnerstraße liegen Franz-Joseph-Straße und Kreuzstraße. Die Schillerstraße verläuft im Norden nach Westen über eine Brücke; die Blumenstraße liegt im Südwesten. spenden = to donate.",
2023:"Ideen für London: Ausstellung Roman London im Museum of London besuchen; Sportveranstaltung besuchen; Einkaufstour; Stadtbesichtigung.\nFlugticket: Alex Kramer; Economy; Munich → London Gatwick; 30/10/2023; departure 10:05; arrival 11:55; flight ZRX 382; seat 6 C; boarding time 20 minutes before departure.",
2024:"Museum Kunterbunt: Kunst-Workshops für Jugendliche, jeden Samstagnachmittag von 14–17 Uhr, 20 Euro. Bilder malen, Skulpturen schaffen oder in die Stadt gehen, um Fotos zu machen. Feedback: Die Workshops machen Spaß; tolle Workshop-Leiter; viel gelernt.",
2025:"Keltenfestival, Freitag, 17. Oktober 2025. Kochen wie die Kelten: Keltenbrot oder Keltenwürstchen mit einfachen Zutaten aus der Natur, zubereitet und probiert am offenen Feuer. Keltische Kostüme: magische und farbenfrohe Kleider aus der Vergangenheit gestalten. Preis für das schönste Kostüm: ein Tag für dich und deine Familie im Keltenmuseum. Word bank: die Kelten = the Celts; keltisch = Celtic."
}
for y,e in E.items():
 e['writingDetails']=details[y]
 # Repair character-spacing artifacts of the PDF extractor in displayed German text.
 for a,b in {'W örter':'Wörter','W etter':'Wetter','W orkshops':'Workshops','W orkshop':'Workshop','W ord':'Word','Arz t':'Arzt','p lanst':'planst','E -Mail':'E-Mail'}.items():e['writingSource']=e['writingSource'].replace(a,b)
(ROOT/'content/exams.json').write_text(json.dumps(E,ensure_ascii=False,indent=2))
(ROOT/'dist/exams-data.js').write_text('window.EXAMS = '+json.dumps(E,ensure_ascii=False,separators=(',',':'))+';\n')
print('Built 5 exams: 100 grammar items and 100 listening points.')
