"""Gera ilustrações vetoriais ORIGINAIS de demonstração (não provenientes da Pixabay).
Para integrar imagens da Pixabay, veja importar_pixabay.py e README.md.
"""
from pathlib import Path
from html import escape
import colorsys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'img'/'ilustracoes'

animals=[
 ('Gato','#F39B52','cat'),('Cachorro','#C58A5B','dog'),('Coelho','#E6C5D5','rabbit'),('Urso','#AA7A55','bear'),
 ('Raposa','#EC824D','fox'),('Leão','#E5AF4F','lion'),('Panda','#F6F0E8','panda'),('Porquinho','#F9A1B5','pig'),
 ('Sapo','#76C877','frog'),('Pinguim','#4E6680','penguin'),('Coruja','#AF7B56','owl'),('Macaco','#BA8351','monkey'),
 ('Elefante','#8799B4','elephant'),('Zebra','#F6F1E8','zebra'),('Vaquinha','#F4EEE9','cow'),('Ovelha','#F6EDE8','sheep'),
 ('Tigre','#F3A74E','tiger'),('Girafa','#F7C869','giraffe'),('Hipopótamo','#9C9AC4','hippo'),('Jacaré','#6DBF85','crocodile'),
 ('Tartaruga','#75BA8E','turtle'),('Baleia','#69AEE1','whale'),('Golfinho','#86BDDF','dolphin'),('Polvo','#B38CE4','octopus'),
 ('Caranguejo','#F4847B','crab'),('Abelhinha','#F6CA56','bee'),('Borboleta','#D5A0F0','butterfly'),('Joaninha','#ED7474','ladybug'),
 ('Passarinho','#80B9EE','bird'),('Dinossauro','#83C69A','dino'),('Esquilo','#C88A62','squirrel'),('Rena','#BA9277','reindeer'),
]

fruits=[
 ('Maçã','#F27779','apple'),('Banana','#F7D56C','banana'),('Pera','#ACD784','pear'),('Morango','#F07180','strawberry'),
 ('Uva','#B294E8','grapes'),('Melancia','#EA7382','watermelon'),('Laranja','#F8AC5C','orange'),('Limão','#E8D861','lemon'),
 ('Abacaxi','#F2C55B','pineapple'),('Cereja','#D9677B','cherry'),('Coco','#AD8C6B','coconut'),('Manga','#F9B85E','mango'),
 ('Kiwi','#A9D174','kiwi'),('Pêssego','#F2A17B','peach'),('Ameixa','#9B83BC','plum'),('Framboesa','#E16B8A','raspberry'),
 ('Mirtilo','#7C98D9','blueberry'),('Mamão','#F6AE6B','papaya'),('Maracujá','#E9BF65','passionfruit'),('Abacate','#A1C686','avocado'),
 ('Figo','#B18CC3','fig'),('Romã','#DF7689','pomegranate'),('Goiaba','#9BCC77','guava'),('Carambola','#F1CD72','starfruit'),
 ('Pitaya','#EF8EBD','dragonfruit'),('Melão','#E6CB85','melon'),('Tangerina','#F7A66E','tangerine'),('Caqui','#EEA16A','persimmon'),
 ('Amora','#947CBD','blackberry'),('Groselha','#DF779A','currant'),('Jambo','#DE7285','roseapple'),('Lichia','#EB9F9E','lychee'),
]

vehicles=[
 ('Carro','#75ACF1','car'),('Caminhão','#EBA16E','truck'),('Ônibus','#F2C65F','bus'),('Bicicleta','#9DBDE8','bike'),
 ('Moto','#E68C9D','moto'),('Trem','#A897DD','train'),('Barco','#77BDE3','boat'),('Avião','#8BBFE0','plane'),
 ('Helicóptero','#9ACDAA','helicopter'),('Foguete','#EF91A5','rocket'),('Trator','#A9C96E','tractor'),('Ambulância','#E7E9EF','ambulance'),
 ('Bombeiros','#F27A76','firetruck'),('Polícia','#86ACDB','police'),('Táxi','#EFC95F','taxi'),('Escolar','#F7D96C','schoolbus'),
 ('Patinete','#B69DDF','scooter'),('Skate','#EAA6A4','skate'),('Balão','#EBA5BA','balloon'),('Submarino','#8E9EE3','submarine'),
 ('Escavadeira','#EEC16A','excavator'),('Sorvete','#F8B9CC','icecreamtruck'),('Van','#85C6C1','van'),('Bondinho','#C994D7','tram'),
 ('Veleiro','#82BBDD','sailboat'),('Navio','#739FCA','ship'),('Jipe','#8CB69E','jeep'),('Corrida','#E98488','racecar'),
 ('Trem-bala','#B1C8D4','bullettrain'),('Basculante','#E6B469','dumptruck'),('Caminhonete','#BA9DD3','pickup'),('Dirigível','#D6A6DE','airship'),
]

def shape(tag, **p):
 attrs=' '.join(f'{k.replace("_","-")}="{escape(str(v),quote=True)}"' for k,v in p.items())
 return f'<{tag} {attrs}/>'

def ellipse(cx,cy,rx,ry,fill,stroke='none',sw=0):return shape('ellipse',cx=cx,cy=cy,rx=rx,ry=ry,fill=fill,stroke=stroke,stroke_width=sw)
def rect(x,y,w,h,fill,rx=0,stroke='none',sw=0):return shape('rect',x=x,y=y,width=w,height=h,rx=rx,fill=fill,stroke=stroke,stroke_width=sw)
def circle(cx,cy,r,fill):return shape('circle',cx=cx,cy=cy,r=r,fill=fill)
def path(d,fill,stroke='none',sw=0):return shape('path',d=d,fill=fill,stroke=stroke,stroke_width=sw,stroke_linecap='round',stroke_linejoin='round')

def face(y=201, eyes=33):
 return ''.join([ellipse(180-eyes,y,8,10,'#26324A'),ellipse(180+eyes,y,8,10,'#26324A'),circle(180-eyes-2,y-3,2.7,'#FFFFFF'),circle(180+eyes-2,y-3,2.7,'#FFFFFF'),circle(133,y+25,8,'#F5A4AA'),circle(227,y+25,8,'#F5A4AA'),path(f'M166 {y+32} Q180 {y+47} 194 {y+32}','none','#4E4B58',4)])

def animal_art(kind,color,i):
 s=''
 # base body
 s+=ellipse(180,275,76,73,color)
 # eyes/body template
 special_ears = {
 'cat':path('M103 165 L102 91 L150 131 Z',color)+path('M210 131 L258 91 L258 165 Z',color),
 'fox':path('M97 168 L105 95 L160 129 Z',color)+path('M200 129 L255 95 L263 168 Z',color),
 'rabbit':ellipse(135,114,24,78,color)+ellipse(225,114,24,78,color)+ellipse(135,112,10,52,'#F5A9C6')+ellipse(225,112,10,52,'#F5A9C6'),
 'dog':ellipse(97,173,31,66,'#936545')+ellipse(263,173,31,66,'#936545'),
 'bear':circle(108,145,31,color)+circle(252,145,31,color),
 'panda':circle(108,145,29,'#33465A')+circle(252,145,29,'#33465A'),
 'lion':''.join(circle(180+96*__import__('math').cos(j*__import__('math').pi/7),191+94*__import__('math').sin(j*__import__('math').pi/7),39,'#E5A04C') for j in range(14)),
 'pig':ellipse(108,143,30,28,color)+ellipse(252,143,30,28,color),
 'frog':circle(128,145,25,color)+circle(232,145,25,color),
 'penguin':'',
 'owl':path('M94 168 L94 117 L137 143 M223 143 L266 117 L266 168',color),
 'monkey':circle(100,207,30,color)+circle(260,207,30,color),
 'elephant':ellipse(100,195,32,53,color)+ellipse(260,195,32,53,color),
 'zebra':ellipse(109,145,23,34,color)+ellipse(251,145,23,34,color),
 'cow':path('M124 145 L113 116 L138 134 Z', '#BDB6A9')+path('M222 134 L247 116 L236 145 Z','#BDB6A9'),
 'sheep':''.join(circle(112+j*23,147+(j%2)*-9,21,'#FFF') for j in range(7)),
 'tiger':path('M102 165 L104 107 L155 140 Z',color)+path('M205 140 L256 107 L258 165 Z',color),
 'giraffe':path('M116 151 L119 104 L144 143 Z',color)+path('M216 143 L241 104 L244 151 Z',color),
 'hippo':circle(112,143,24,color)+circle(248,143,24,color),
 'crocodile':ellipse(113,149,22,18,color)+ellipse(247,149,22,18,color),
 'turtle':'', 'whale':'','dolphin':'','octopus':'','crab':'','bee':'','butterfly':'','ladybug':'',
 'bird':'','dino':'','squirrel':'','reindeer':path('M126 159 Q105 124 94 103 M94 103 L81 84 M101 114 L113 95 M234 159 Q255 124 266 103 M266 103 L279 84 M259 114 L247 95','none','#987356',10)
 }
 if kind in ['butterfly']:
  s=ellipse(123,190,66,73,'#D69BFA')+ellipse(237,190,66,73,'#F3B2D7')+ellipse(123,249,53,45,'#B28BE3')+ellipse(237,249,53,45,'#ED91C4')+ellipse(180,223,25,85,'#8A669D')+face(186,9)
 elif kind in ['bee']:
  s=ellipse(130,157,50,40,'#F3F6FB')+ellipse(230,157,50,40,'#F3F6FB')+ellipse(180,217,80,97,'#F7D65E')+rect(106,211,148,18,'#5F5360',8)+rect(121,259,118,17,'#5F5360',8)+face(174)
 elif kind in ['ladybug']:
  s=ellipse(180,220,93,94,'#E76670')+rect(176,142,8,156,'#613A52',4)+''.join(circle(x,y,12,'#653B52') for x,y in [(136,177),(224,177),(133,240),(227,240)])+face(185)
 elif kind in ['octopus']:
  s=''.join(path(f'M{120+j*24} 246 Q{88+j*25} 309 {93+j*29} 314','none',color,24) for j in range(6))+ellipse(180,190,92,79,color)+face(184)
 elif kind in ['crab']:
  s=ellipse(180,221,93,64,color)+path('M103 201 L55 173 L55 143 M257 201 L305 173 L305 143','none',color,18)+ellipse(55,142,22,31,color)+ellipse(305,142,22,31,color)+face(210)
 elif kind in ['whale','dolphin']:
  s=ellipse(185,220,100,68,color)+path('M90 211 Q40 152 50 250 Q62 260 98 245',color)+circle(160,205,8,'#26324A')+path('M171 228 Q183 240 195 228','none','#26324A',4)+path('M183 159 Q196 125 209 155',color)+circle(148,235,10,'#DCA1B0')
 elif kind in ['turtle']:
  s=circle(180,208,91,'#5AAB83')+ellipse(180,223,72,68,'#83D2A5')+ellipse(180,182,43,24,'#66B58D')+ellipse(180,264,45,22,'#66B58D')+circle(180,224,41,'#73C79B')+face(195)
 else:
  s+=special_ears.get(kind,'')
  s+=ellipse(180,204,91,83,color,'#FFFFFF',3)
  if kind in ['panda']:
   s+=ellipse(146,198,26,31,'#34495E')+ellipse(214,198,26,31,'#34495E')
  if kind in ['penguin']:
   s+=ellipse(180,246,65,96,'#F9F7F2')
  if kind in ['cow']:
   s+=ellipse(143,179,24,17,'#5A6176')+ellipse(231,226,19,20,'#5A6176')
  if kind in ['zebra','tiger']:
   s+=path('M141 128 L164 163 L153 173 M219 128 L196 163 L207 173 M94 189 L121 206 M266 189 L239 206','none','#6D5F4D',10)
  if kind in ['giraffe']:
   s+=circle(131,183,12,'#C99252')+circle(229,241,11,'#C99252')+circle(225,169,9,'#C99252')
  if kind in ['dog']:
   s+=ellipse(180,233,43,33,'#F7E4D2')
  if kind in ['elephant']:
   s+=path('M175 227 Q166 276 191 284 Q209 276 199 263','none',color,27)
  if kind in ['pig','hippo']:
   s+=ellipse(180,236,46,29,'#EFA2B3' if kind=='pig' else '#AAB0C9')+circle(162,236,5,'#916A80')+circle(198,236,5,'#916A80')
  if kind in ['crocodile']:
   s+=ellipse(180,236,84,22,'#9FDB99')+path('M109 244 L129 256 L150 244 L171 256 L192 244 L213 256 L234 244','none','#FDFCF6',5)
  if kind in ['squirrel']:
   s+=path('M260 269 Q331 278 294 174 Q314 220 271 239','#B9774F')
  if kind in ['bird','owl']:
   s+=ellipse(112,234,32,49,'#A9C7D7')+ellipse(248,234,32,49,'#A9C7D7')+path('M164 223 L196 223 L180 240 Z','#EAB35F')
  if kind in ['dino']:
   s+=path('M91 182 L78 166 L107 156 L97 142 L128 147 L133 127 L156 139', '#639E89')
  if kind in ['lion']:
   s+=ellipse(180,229,36,25,'#F8D994')
  s+=face(197)
  if kind in ['cat','fox','lion','tiger','dog','bear']:
   s+=path('M168 226 L192 226 L180 237 Z','#665151')
 return s

def fruit_art(kind,color,i):
 s=''
 if kind=='banana':
  s+=path('M90 167 Q154 300 275 155 Q276 275 183 294 Q115 306 90 167 Z',color,'#D0A74C',4)
 elif kind=='watermelon':
  s+=path('M88 180 Q181 328 272 180 Z','#F27B8D')+path('M88 180 Q181 327 272 180','none','#6DBD80',18)+''.join(ellipse(x,y,4,9,'#433A50') for x,y in [(150,205),(180,225),(210,205),(167,252),(194,257)])
 elif kind=='grapes':
  s+=''.join(circle(x,y,29,'#A184D1') for x,y in [(150,166),(207,166),(126,206),(180,206),(233,206),(152,246),(206,246),(179,278)])
 elif kind=='cherry':
  s+=path('M178 131 Q157 169 139 225 M178 131 Q209 168 230 225','none','#659970',8)+circle(135,241,47,'#DA526A')+circle(236,241,47,'#EA6881')
 elif kind=='pineapple':
  s+=path('M166 157 L142 89 L180 126 L204 89 L198 154 L230 113 L215 175 Z','#72B68A')+ellipse(180,226,80,101,color)+path('M125 179 L230 284 M125 274 L230 180 M111 212 L219 305 M151 163 L247 263','none','#CF9D48',5)
 elif kind in ['strawberry','raspberry','blackberry','blueberry','currant']:
  s+=path('M180 143 C285 136 261 261 181 296 C89 261 77 139 180 143 Z',color)
  if kind!='strawberry':
   s+=''.join(circle(x,y,14,'#B25B81' if kind=='raspberry' else '#745DAB' if kind in ['blackberry','blueberry'] else '#D85277') for x,y in [(153,182),(180,170),(205,185),(137,212),(168,215),(196,219),(220,213),(154,245),(185,254),(206,244)])
  else:s+=''.join(ellipse(x,y,3,6,'#FFE5A8') for x,y in [(147,187),(181,194),(210,187),(164,227),(199,238),(181,267)])
 elif kind in ['pear','avocado','fig']:
  s+=path('M180 140 C205 140 209 187 227 207 C292 283 227 307 180 305 C126 308 76 275 126 208 C145 179 154 141 180 140 Z',color)
  if kind=='avocado':s+=ellipse(180,255,27,38,'#95664B')
 elif kind in ['orange','lemon','kiwi','coconut','passionfruit','guava','melon','tangerine']:
  s+=ellipse(180,226,91,89,color)
  if kind in ['orange','tangerine','lemon']:
   s+=''.join(path(f'M180 224 L{180+67*__import__("math").cos(j*__import__("math").pi/4)} {224+65*__import__("math").sin(j*__import__("math").pi/4)}','none','#FFF0C5',3) for j in range(8))
  if kind=='kiwi':s+=ellipse(180,227,50,48,'#D5E3A4')+''.join(circle(180+35*__import__('math').cos(j*__import__('math').pi/8),227+34*__import__('math').sin(j*__import__('math').pi/8),4,'#475549') for j in range(16))
  if kind=='coconut':s+=circle(165,207,8,'#78604D')+circle(199,207,8,'#78604D')+circle(181,235,8,'#78604D')
 elif kind=='starfruit':
  s+=path('M180 112 L204 175 L271 179 L220 220 L238 286 L180 247 L122 286 L140 220 L89 179 L156 175 Z',color)
 elif kind=='dragonfruit':
  s+=ellipse(180,222,84,95,color)+path('M120 146 L110 113 L154 149 M218 151 L253 125 L245 181 M140 281 L122 309 L167 288','#8DC594')
 else:
  s+=path('M180 141 C279 121 281 272 189 299 C98 306 79 206 113 168 C131 148 148 144 180 141 Z',color)
 # stems / leaves
 if kind not in ['banana','watermelon','grapes','cherry','pineapple','starfruit']:
  s+=path('M177 152 Q173 122 184 111','none','#7A8461',9)+path('M184 129 Q228 96 244 136 Q216 160 184 129','#7ABB80')
 if kind in ['apple','peach','mango','plum','pomegranate','roseapple','persimmon','lychee']:
  s+=ellipse(145,202,17,28,'#FFFFFF55')
 # playful face
 s+=ellipse(156,225,6,8,'#394050')+ellipse(204,225,6,8,'#394050')+path('M168 243 Q180 255 192 243','none','#394050',3.7)+circle(137,241,7,'#F5A1A8')+circle(224,241,7,'#F5A1A8')
 return s

def transport_art(kind,color,i):
 s=''
 if kind in ['plane','rocket','helicopter','balloon','airship']:
  if kind=='plane':
   s+=path('M180 102 Q203 162 194 212 L268 254 L268 274 L193 250 L189 306 L171 306 L167 250 L92 274 L92 254 L166 212 Q157 162 180 102 Z',color)
  elif kind=='rocket':
   s+=path('M180 100 Q246 157 211 281 L149 281 Q114 157 180 100 Z',color)+path('M148 228 L117 277 L149 269 M212 228 L243 277 L212 269','#F4BA81')+circle(180,191,25,'#BDEDF8')+path('M158 280 L202 280 L180 318 Z','#F9C55F')
  elif kind=='helicopter':
   s+=ellipse(176,231,94,56,color)+rect(88,216,34,17,color,8)+rect(252,234,47,16,color,8)+path('M125 172 L236 172 M181 173 L181 202','none','#6A7184',10)+path('M118 279 L255 279','none','#6A7184',9)+ellipse(170,229,41,30,'#C3EBF3')
  elif kind=='balloon':
   s+=ellipse(180,164,75,93,color)+rect(151,265,58,40,'#B38664',8)+path('M142 224 L157 265 M218 224 L203 265','none','#B38664',5)+path('M180 75 L180 251','none','#FFFFFF66',12)
  else:
   s+=ellipse(175,192,120,64,color)+path('M244 189 L287 182 L281 224 L232 227',color)+rect(149,252,57,31,'#CDA77E',9)+path('M159 254 L150 233 M195 254 L204 233','none','#9C8790',4)
 elif kind in ['boat','sailboat','ship','submarine']:
  if kind=='submarine':
   s+=ellipse(180,226,113,61,color)+rect(159,139,49,44,color,7)+circle(150,218,22,'#C9ECF5')+circle(205,218,22,'#C9ECF5')+path('M292 208 L313 188 L313 264 L292 240',color)
  else:
   s+=path('M77 234 L283 234 L255 301 L113 301 Z',color)
   if kind=='boat':s+=rect(142,190,84,47,'#F7F4EF',9)+rect(167,205,35,20,'#94C9E3',7)
   elif kind=='sailboat':s+=path('M179 100 L179 231 L102 231 Z','#FFFFFF')+path('M184 124 L249 231 L184 231 Z','#F6D27C')
   else:s+=rect(122,166,115,67,'#F7F4EF',8)+rect(138,182,28,22,'#90CFE1',5)+rect(180,182,28,22,'#90CFE1',5)
   s+=path('M87 306 Q115 290 141 306 Q169 291 195 306 Q229 292 255 306','none','#86C6E9',7)
 elif kind in ['bike','moto','scooter','skate']:
  if kind=='skate':
   s+=rect(87,225,189,27,color,14)+circle(124,265,15,'#465267')+circle(244,265,15,'#465267')
  else:
   s+=circle(115,274,35,'#52627C')+circle(247,274,35,'#52627C')+circle(115,274,23,'#EAF5FF')+circle(247,274,23,'#EAF5FF')
   if kind=='bike':s+=path('M115 274 L156 203 L208 274 L115 274 L182 225 L247 274','none',color,12)+path('M152 204 L143 185 M181 225 L181 184 L205 184','none','#52627C',8)
   elif kind=='scooter':s+=rect(128,242,116,14,color,7)+path('M231 247 L214 164 L244 164','none','#59627D',8)
   else:s+=path('M128 249 L177 209 L217 238 L250 248',color)+rect(164,192,63,32,'#5D627D',9)
 else:
  # land vehicles: silhouette + windows + wheels
  bus=kind in ['bus','schoolbus','tram','train','bullettrain']
  truck=kind in ['truck','firetruck','icecreamtruck','dumptruck','excavator','tractor','pickup','ambulance']
  if bus:
   s+=rect(74,171,215,103,color,22)
   for x in (102,157,212):s+=rect(x,187,44,38,'#CCF0F7',8)
   if kind=='tram':s+=path('M111 165 L180 121 L249 165','none','#7A78A0',7)
   if kind=='bullettrain':s+=path('M74 210 L107 168 L283 168 L283 268 L74 268 Z',color)
  elif truck:
   s+=rect(76,181,134,82,color,10)+path('M210 206 L254 206 L289 244 L289 266 L210 266 Z',color)
   s+=rect(228,216,36,29,'#B7E1F2',6)
   if kind=='firetruck':s+=path('M111 172 L176 172','none','#F5F2E8',11)+path('M125 187 L125 228','none','#F5F2E8',8)
   if kind=='ambulance':s+=rect(132,186,13,49,'#EF656B',1)+rect(114,204,50,13,'#EF656B',1)
   if kind=='excavator':s+=path('M97 192 Q52 105 82 105 L140 159','none','#E0B766',17)
   if kind=='icecreamtruck':s+=rect(110,190,66,22,'#F5F0FF',6)+circle(126,201,9,'#F6A3C6')+circle(145,201,9,'#F4D89B')
  else:
   s+=rect(91,214,184,58,color,17)+path('M123 215 L151 171 L230 171 L256 215 Z',color)
   s+=path('M162 185 L216 185 L233 213 L139 213 Z','#CAEAF3')
   if kind=='racecar':s+=path('M93 238 L276 238','none','#FFFFFF',8)
   if kind=='police':s+=rect(172,156,32,14,'#F67286',4)
   if kind=='taxi':s+=rect(165,157,34,16,'#F7E4B6',4)
  s+=circle(132,268,26,'#45566B')+circle(245,268,26,'#45566B')+circle(132,268,12,'#E8ECF2')+circle(245,268,12,'#E8ECF2')
  s+=circle(278,246,7,'#FFF0B0')
 return s

def generate(theme,entries,artist):
 for i,(name,color,kind) in enumerate(entries):
  bgs=['#F9EAF4','#EDF8FD','#FCF0DC','#EAF5E8','#F1EBFD','#FCEFE9','#E7F7F6','#FAEFF8']
  bg=bgs[i%len(bgs)]
  title=escape(name)
  content=artist(kind,color,i)
  # Illustrated card art, not an emoji: all shapes are handmade vector graphics.
  svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="360" height="420" viewBox="0 0 360 420" role="img" aria-label="Ilustração de {title}">
  <defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{bg}"/><stop offset="1" stop-color="#FFFFFF"/></linearGradient><filter id="shadow" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="9" stdDeviation="9" flood-color="#7D6C9C" flood-opacity=".20"/></filter></defs>
  <rect width="360" height="420" rx="24" fill="url(#bg)"/>
  {circle(63,84,28,'#FFFFFF99')}{circle(301,95,39,'#FFFFFF77')}{circle(282,318,19,'#FFFFFFB2')}
  <g filter="url(#shadow)">{content}</g>
  <rect x="44" y="352" width="272" height="48" rx="24" fill="#FFFFFFE9"/>
  <text x="180" y="383" font-family="Verdana,Arial,sans-serif" font-weight="bold" font-size="23" text-anchor="middle" fill="#55516B">{title}</text>
  </svg>'''
  namefile=f'{i+1:02d}-{kind}.svg'
  dest=OUT/theme/namefile;dest.write_text(svg,encoding='utf8')
  yield {'nome':name,'src':f'img/ilustracoes/{theme}/{namefile}','origem':'arte-original-inclusa'}

if __name__=='__main__':
 import json
 data={'animais':list(generate('animais',animals,animal_art)), 'frutas':list(generate('frutas',fruits,fruit_art)), 'transportes':list(generate('transportes',vehicles,transport_art))}
 (ROOT/'biblioteca-local.js').write_text('window.BIBLIOTECA_LOCAL = '+json.dumps(data,ensure_ascii=False,indent=2)+';\n',encoding='utf8')
 print('Ilustrações criadas:',sum(map(len,data.values())))
