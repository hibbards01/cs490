#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import json
import time
from datetime import date, datetime, timedelta
import mysql.connector
import re
import sys
from twitter_credentials import *
import string
import naive_bayes

def get_all_tweets(screen_name):

	global consumer_key
	global consumer_secret
	global access_token
	global access_token_secret
	

	print "Getting tweets from %s" % (screen_name)
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	new_tweets = []

	try:
		#make initial request for most recent tweets (200 is the maximum allowed count)
		new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	except:
		print "Error retrieving data"
	
	#save most recent tweets
	if len(new_tweets) > 0:
		alltweets.extend(new_tweets)
		#print (len(new_tweets))

		#save the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		#keep grabbing tweets until there are no tweets left to grab
		while len(new_tweets) > 0:
			#print ("getting tweets before ", oldest)
			
			#all subsiquent requests use the max_id param to prevent duplicates
			new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
			
			#save most recent tweets
			alltweets.extend(new_tweets)
			
			#update the id of the oldest tweet less one
			oldest = alltweets[-1].id - 1
			
			print "%s...tweets downloaded so far" % (len(alltweets))
		
		myWords = {}

		for item in alltweets:
			keywords = string.split(item.text)
			for keyword in keywords:
				key = keyword.encode('unicode_escape')
				key = key.decode("utf-8")
				if key in myWords:
					myWords[key] += 1
				else:
					myWords[key] = 1

		result = calculateRisk(myWords)
		
		print result

		if result > 0.157:
			print "High risk "
		elif result > 0.1461:
			print "Median risk"
		else:
			print "Low risk"

	else:
		print "No tweets found for this account"

def calculateRisk(keywords):

	global table
	#table = naive_bayes.getTable()
	table = {'IT': 0.11405259827238287, 'not': 0.16379424025710113, 'too': 0.17573806745684142, 'ago': 0.1229611682014305, 'dont': 0.25524293253153274, 'characters': 0.34246286173486035, 'THAT': 0.12412144648584515, 'parents': 0.13992475414078845, 'I`m': 0.21332605401476207, '-': 0.04127320875319675, 'it?': 0.14715108670583438, 'every': 0.16418461262277712, 'front': 0.13362476624284453, 'until': 0.1289315705185386, 'attention': 0.23275167604492336, 'account': 0.13138175667882943, 'And': 0.16544275232734235, '|': 0.03828594156249837, 'Donald': 0.0676883900110477, 'makeup': 0.1763591016142828, 'drive': 0.13246825764178372, 'followed': 0.2594293562117103, 'coming': 0.08929638876112668, 'all': 0.14299220078923794, 'Being': 0.16861505053745773, 'these': 0.11642102560906885, 'put': 0.1676948746460243, 'before': 0.1395472642363211, 'WHY': 0.18085564826683465, 'feels': 0.19529881325664564, 'should': 0.1394916422826286, 'w/': 0.10596609984003137, 'b': 0.17677381967726302, ':3': 0.8959721466782393, '❤️': 0.1115732470427526, 'mood': 0.1368835383134667, 'dream': 0.1742654085442321, 'LOVE': 0.16405920812689662, 'kid': 0.1400139127586982, 'stay': 0.1644666912290178, 'team': 0.04350752360501627, 'news': 0.08712970103173388, 'me.': 0.6946491757023836, 'anymore': 0.1966404458977271, 'lose': 0.10747190523053465, 'exactly': 0.16202381338772845, 'lives': 0.12937118931557748, '.': 0.06548368450245286, 'lovely': 0.2321040774444665, 'Yes': 0.13955886673623075, 'stop': 0.17923968244569524, 'which': 0.19704493657919817, 'black': 0.14870693280390723, 'close': 0.11190731656541598, 'bed': 0.17810516908024365, 'human': 0.141529656438504, 'watching': 0.1257129229501305, '100%': 0.1655973512360024, 'another': 0.11708412974753253, 'ass': 0.1977473895204032, 'New': 0.05254298015380199, 'ya': 0.10182204922234943, 'usually': 0.2375225402879421, 'ask': 0.16451131185542547, 'AND': 0.10952810212170991, 'When': 0.10610689707999638, 'wine': 0.3371556344858662, 'miss': 0.11745688089485856, 'bc': 0.3925754275683123, '2016': 0.03693642103550565, 'JUST': 0.11208700025813627, 'goes': 0.10778970295484282, 'Great': 0.05938163046370621, 'knows': 0.17542754362476426, 'mental': 0.3944680969719003, 'Man': 0.11284155788903798, 'fun': 0.13374148281338885, '"I': 0.15103209764353073, 'wonder': 0.17813648434505427, 'She': 0.18460733696591716, 'important': 0.17439452245058118, 'when': 0.15671726205285635, 'The': 0.05991419265366666, 'holy': 0.29276694122478786, 'kiss': 0.23403765911066107, 'everything': 0.14529375947749962, 'could': 0.16450632564174825, 'Good': 0.12703969315185848, 'through': 0.12569542898470112, 'Niggas': 0.26007303061242104, 'looks': 0.16970526509468312, 'deep': 0.17287153491998966, 'name': 0.20941605554741488, 'DO': 0.14267570016173697, 'album': 0.06083590484936451, 'already': 0.13857217158994478, 'hehe': 0.8125734764944565, 'About': 0.15560643395088508, 'become': 0.15724988957057168, 'Can': 0.11300092740482863, 'relationship': 0.17678559137053285, 'keep': 0.15015710714870611, 'seeing': 0.1485459581421384, 'Watch': 0.06370025771982359, 'Even': 0.14615949875890907, 'those': 0.1578610528065734, 'next': 0.10711381930529836, 'sure': 0.14743557647164998, 'fact': 0.153884430447644, 'also': 0.23835536078670408, 'future': 0.10718974468294844, 'summer': 0.07049106634484592, 'Birthday': 0.1336551266113818, 'hard': 0.1672247758604221, 'All': 0.12321777531065242, 'its': 0.17379443763629818, 'hand': 0.17638651278846496, 'didn`t': 0.16990368470876935, 'stand': 0.09324213690637316, 'IS': 0.11251046444689722, 'anyone': 0.18014217753999046, 'suck': 0.24246717621372285, 'going': 0.1360930192270575, 'cant': 0.26344982590428473, 'ever': 0.15345793912797787, 'together': 0.14504655413288386, 'Out': 0.17072768427649132, 'Trump': 0.06604844978173209, 'young': 0.15382999887750476, 'both': 0.17882092717670683, 'crazy': 0.09468156735923453, 'we`re': 0.13124017468937038, 'This': 0.09209530774704325, 'two': 0.1324934011354987, 'isn`t': 0.1710429162684145, 'whole': 0.1475680470983796, 'OMG': 0.16886764095240384, 'way': 0.14117369672365365, 'out': 0.11494060266224641, 'Some': 0.21968134794553015, 'DM': 0.08734409143925519, 'Fuck': 0.2936561976838586, 'joke': 0.17383265697071182, 'hope': 0.17039212765788453, 'without': 0.14073743390929447, 'Time': 0.09524345705126082, 'it!': 0.12772352394686134, 'stopped': 0.20531736246731394, 'crying': 0.23671780431284173, 'TO': 0.07635985973317985, 'Where': 0.14348497560647627, 'LIKE': 0.09442283178030568, 'THIS': 0.11397204569613693, 'fight': 0.1224802843692473, 'others': 0.1224127949253285, 'life': 0.15490300052953968, 'Damn': 0.09549167028257309, 'ppl': 0.1621301414766637, 'left': 0.11134844151675843, 'depression': 0.69727750740053, 'you': 0.15322145868495604, 'hair': 0.17583374382588687, 'just': 0.16736362638480548, 'IM': 0.23503575542882774, 'As': 0.0952523222592586, 'for': 0.11454377854602642, 'long': 0.16128559582015362, 'let': 0.1385373524633649, 'THE': 0.055275884460457385, 'short': 0.13680133925770774, 'pls': 0.16073561400943998, '@Ashton5SOS': 0.6645295192848771, 'rn': 0.08172131468669849, 'beat': 0.13155140382790415, 'does': 0.17097809975056658, 'Going': 0.17736350331987424, 'sleep': 0.18318277260016969, 'gone': 0.11026236779773985, 'our': 0.07127356570681324, 'old': 0.17351075404061372, 'mouth': 0.2059689484485927, 'little': 0.1712240193974878, 'so': 0.17775629844708637, 'gives': 0.15285930988245186, 'that`s': 0.19209856898962693, 'probably': 0.20558948161155183, 'i`m': 0.38222134205043407, 'take': 0.134261877203111, 'Your': 0.10327468797621689, 'called': 0.16708541050975817, 'woman': 0.19860481405221345, 'chill': 0.1289499827371877, 'enjoy': 0.13548610053514207, 'dark': 0.23006406686022585, 'big': 0.15877546723357602, 'die': 0.27335325710967673, '@Calum5SOS': 0.7896793269852677, 'women': 0.17463426709369023, 'luck': 0.12116699082124294, 'OH': 0.175404294298475, 'we': 0.08733294624150181, 'Have': 0.13097853262646827, 'played': 0.16179238087722433, 'new': 0.11732301945689023, 'Thank': 0.11355625624254954, 'each': 0.14605602398187867, 'more': 0.15012035432020185, 'died': 0.17185724493181143, 'me': 0.21363530735803116, 'WITH': 0.0845384023101477, 'guys': 0.16051054298359702, 'These': 0.09149076077727585, 'vote': 0.07326258214179648, 'taken': 0.16331283508667072, 'picture': 0.18808499279221896, 'deal': 0.10979482603361701, 'go': 0.12540201914071405, 'respect': 0.12367795754173737, 'can': 0.1334105362976882, 'ain`t': 0.08473994226630241, 'Everyone': 0.16004726269460764, 'least': 0.15204595724242334, 'happened': 0.1304155010199902, 'goodnight': 0.3680118594436796, '#GOPDebate': 0.37132068816478814, 'saying': 0.1834521762753201, 'Don`t': 0.15140774056430453, 'Now': 0.05657373236740893, 'thank': 0.1945866474452679, '????': 0.059607338207698646, 'smile': 0.2257028466863175, 'NOT': 0.12824947304146472, 'asking': 0.20116835156283688, 'us': 0.07297595642784395, 'kind': 0.2218263441794023, 'him': 0.13512845133343024, 'taste': 0.21048660386562826, 'pick': 0.12096569520700237, 'learn': 0.11164307640000774, 'couldn`t': 0.1407281542530305, 'online': 0.19643168059740057, 'birthday': 0.08995665983199978, 'your': 0.1352007082084347, 'send': 0.12324152677711145, 'open': 0.1433749580259536, 'blood': 0.18782170219366903, 'Oh': 0.14397594647222964, '4': 0.07814050804215779, 'word': 0.1794623234945363, 'hours': 0.14599820116627604, 'happy': 0.1440511405070138, 'pictures': 0.17356547954047596, 'middle': 0.15845833017598882, 'tho': 0.12224206114000424, 'meant': 0.15565831944002168, 'turned': 0.14779707310633042, 'eh': 0.1962041400870387, 'niggas': 0.1703711138098837, 'here': 0.11820424379147437, 'say': 0.15139086033153934, '—': 0.22014267098144333, 'wouldn`t': 0.18357330229598026, 'Let`s': 0.07455157322595236, 'fall': 0.13356555482303312, 'person': 0.21477192478358736, 'awful': 0.3164173898478477, 'baby': 0.17068879607416507, '(': 0.22518905037126813, 'talk': 0.1820625427672858, 'sexual': 0.4505635058637047, 'WHAT': 0.13188592068358843, 'my': 0.2115582042546026, 'HAPPY': 0.1242187597121619, 'is': 0.13541954174594736, 'wasn`t': 0.1478638301672649, 'bye': 0.20213762730213558, 'alone': 0.19770994685349655, 'almost': 0.1711119196094475, 'Prince': 0.12974780344494663, 'place': 0.1530825497377956, '1st': 0.08016807101222878, 'may': 0.09511671030203868, 'got': 0.13118458790431806, 'thanks': 0.21535503680504234, 'Sometimes': 0.19267888641561862, 'want': 0.17188694905984206, 'ok': 0.23822497896776973, '5sos': 0.87977262670637, 'found': 0.18304419754681753, 'ha': 0.3488287342271275, 'problem': 0.12860210361981314, 'lil': 0.13924097591870666, 'Idk': 0.17846962013317436, 'wanted': 0.14696952622599058, 'most': 0.14011718561486103, 'where': 0.16490848726160093, 'deserve': 0.19235401245454398, 'didnt': 0.20757445089242102, 'hold': 0.14148465712486927, 'oh': 0.25627381264526383, 'y`all': 0.08925538920349108, 'body': 0.23835037616550797, 'vs': 0.05159049269915019, 'Hope': 0.12239966587930914, 'Then': 0.15817503714657777, 'r': 0.06587506041549822, 'seriously': 0.16251690698425134, 'meet': 0.13047076711344976, 'asked': 0.20282108582061312, 'she': 0.18371966849986268, 'i': 0.33472139281456814, 'episode': 0.1199596660555458, 'made': 0.16929420282758467, 'Was': 0.15488800227167102, 'world': 0.11301769813547309, 'but': 0.18447629375094374, 'Go': 0.1211454130825728, 'fuck': 0.2761381949546609, 'looking': 0.15131963224019057, 'cares': 0.2280064297973569, 'yesterday': 0.12233084381366603, 'face': 0.1908241956028489, 'are': 0.14584472898410591, 'I`ve': 0.2054690071540409, 'twitter': 0.3092707505657266, 'friends': 0.16960310249645283, '&lt;3': 0.5384218736296862, 'drunk': 0.30791242478135233, 'number': 0.15567392011071868, 'seen': 0.14647613145341312, '20': 0.10383117537606007, 'different': 0.1617848902512859, 'media': 0.0881327556744589, 'forever': 0.15440409968169216, 'same': 0.17244929590446229, 'gay': 0.3277124602810967, 'wake': 0.18613947679191936, 'lol': 0.09726579881619912, 'completely': 0.2289272847709541, 'Me': 0.20588514947743303, 'choice': 0.1520459572424233, 'Well': 0.14479179115800594, 'find': 0.14501895691714034, 'clean': 0.3260998537271765, 'past': 0.10356087835762914, 'forgot': 0.21545621682653884, 'you.': 0.5288202095759701, 'video': 0.17899266650464019, 'type': 0.13798069016610126, 'point': 0.13168574092417087, 'question': 0.12481563401034292, '@': 0.07949269403243282, 'weird': 0.26621791928381, 'voice': 0.1728769687873388, 'bit': 0.16185652755192714, 'wants': 0.11823181875558661, 'work': 0.10670590307185517, 'sometimes': 0.2107844036814907, 'tired': 0.18529186733395833, 'How': 0.09092136177633425, 'Her': 0.13457324746941662, 'Goodnight': 0.37262517117339305, 'game': 0.04331383307572282, 'strong': 0.24152921402676028, 'Follow': 0.18477882921393682, 'single': 0.12047756095832791, 'lot': 0.17967355572537586, 'fuckin': 0.2724211287277489, 'dog': 0.23283824064079678, 'me?': 0.2577825835513341, 'boy': 0.1968250925264928, 'song': 0.1005784991142974, 'job': 0.11895969170916743, '?': 0.0, 'because': 0.23629762946111105, 'pizza': 0.20937894580464833, 'funny': 0.19353090744024137, 'text': 0.1513688823358652, 'make': 0.12920477652132042, 'Life': 0.13411342874283758, 'sense': 0.1432961644424169, 'reading': 0.18327710490051596, 'sad': 0.20245474624025372, 'watched': 0.17077363593755895, 'songs': 0.13031678648250086, 'white': 0.18877498356992028, 'haha': 0.10482473970391837, 'weekend': 0.05955396809295544, 'Hey': 0.09681110071025055, 'bought': 0.17057503798607762, 'case': 0.1603468144107976, 'bad': 0.20353925504226736, 'People': 0.17543023348440567, 'nobody': 0.17109408831079417, 'either': 0.15169231407292208, 'aren`t': 0.17258883103809763, 'beautiful': 0.1855100150715104, 'Am': 0.28998466944518303, 'yall': 0.10956200557933961, 'i`ve': 0.4228561440378021, 'telling': 0.18655375010065206, 'used': 0.176561549923408, 'throw': 0.1328135873095997, 'and': 0.16302276502836746, 'amazing': 0.12880696360368768, 'remember': 0.17359770770338878, 'list': 0.13869978679500505, '15': 0.09196004644216015, 'best': 0.1102851760125306, 'games': 0.06657240902932951, 'gets': 0.1284375654409516, 'That`s': 0.12614527401875772, 'n': 0.12454902200313493, 'around': 0.1404178224526467, 'over': 0.11449414210922514, 'line': 0.10986816247348881, 'UP': 0.09972542558963897, 'it': 0.16631496293794157, 'in': 0.11250527269451127, 'FUCKING': 0.20552695014219144, 'saw': 0.18529770277393323, 'sick': 0.20092130623787346, 'For': 0.1031953127220081, 'guy': 0.19130606931264976, 'it.': 0.4592419949144561, 'Christmas': 0.10661448338093482, 'victim': 0.3797739817303947, 'act': 0.13023075568143178, 'tumblr': 0.6301858110210435, 'things': 0.15310786097453458, 'once': 0.1915060067508447, 'pics': 0.19593370786878586, 'beer': 0.30176514952461125, 'men': 0.2007548762042594, 'Need': 0.11265289044578794, 'Not': 0.1355157968356304, 'Are': 0.11794659470628206, 'clothes': 0.21277437441365535, 'season': 0.07089343585225648, 'eat': 0.24854199387134124, 'literally': 0.2067694407335029, 'yo': 0.10461425720812134, '...': 0.7051004620553062, 'abuse': 0.610512144249193, 'how': 0.15734987083542223, 'ugly': 0.2325342529525604, 'you`ve': 0.183305994167497, 'she`s': 0.19454160931414374, 'turn': 0.14025237854332934, 'via': 0.10445125977737323, 'My': 0.22746575221433254, 'hear': 0.11909902164302386, 'follow': 0.23525626710968733, 'don’t': 0.27357053152581423, 'What': 0.08377341381705719, 'have': 0.16244124725289172, 'tweeting': 0.19498660377227378, 'ones': 0.16791322213619822, 'needs': 0.11992336934605836, '"': 0.06629190793660927, '!!': 0.09540850546289645, 'videos': 0.1745415324744066, 'support': 0.10574460845598843, 'quick': 0.13360081389489833, 'low': 0.21010557200771293, 'Got': 0.19573267678147968, 'on': 0.11669195942336125, 'hit': 0.11976352163498062, 'i`ll': 0.36048075298069693, 'entire': 0.09208646088127322, 'know': 0.1547893744142423, 'side': 0.12460251826216058, 'She`s': 0.16682995708643567, 'Ass': 0.6454817483150198, 'Just': 0.13207365688589875, 'home': 0.11100588281908078, 'haven`t': 0.14952123454460378, 'One': 0.1929043554874161, 'Is': 0.1375443542519208, 'full': 0.13385318892832726, 'do': 0.15507460430395448, 'BE': 0.07527609086796509, 'public': 0.11836010368705158, 'times': 0.15696985757690265, 'making': 0.16723975432182775, 'waiting': 0.1375907926890591, 'appreciate': 0.15135905913646333, 'HAVE': 0.10359222167254863, 'Sorry': 0.14342102029968543, 'shut': 0.20537933702358804, 'bro': 0.0742296517533118, 'alive': 0.19279058382163552, 'win': 0.03382790792875955, 'Twitter': 0.18122342264712155, 'SHIT': 0.19561271035985198, 'sex': 0.36679022801099376, 'will': 0.11753176061216841, 'wanna': 0.1374251665444334, 'trying': 0.16693661775027185, 'show': 0.12182633252325475, 'Shit': 0.3779694447788675, 'cause': 0.15477441326177457, 'idk': 0.21906071305165964, 'hurt': 0.21442417920869786, 'yourself': 0.15681097992715745, 'since': 0.10805066217914387, 'Ok': 0.19008870806697817, 'of': 0.12898675831518314, 'by': 0.07213956470743096, 'write': 0.15917770663662092, 'last': 0.09905765948271619, ':D': 0.2539695713451429, 'brother': 0.1555756151135866, 'pretty': 0.18080174209853564, 'ur': 0.15078829274719557, 'wear': 0.2052002326759522, 'something': 0.17111051350781423, 'matter': 0.12592506675558032, 'some': 0.14172972636118025, 'own': 0.1554234179126697, 'or': 0.16163265528742804, 'Drake': 0.12671263372983205, 'bout': 0.08235876512956601, 'doesn`t': 0.15011434732123793, 'speak': 0.1586071666850851, 'time': 0.1345025351491612, 'her': 0.16432558513164822, 'loves': 0.19010729489516592, 'always': 0.15999743199772595, 'a': 0.15317747014560076, 'can`t': 0.1512533918823253, 'dm': 0.291185589167286, 'an': 0.12586497552474615, 'https:/…': 0.04035297157700567, 'cute': 0.23748099789216892, 'course': 0.12795706400401077, '&amp': 0.08888508147612237, 'girlfriend': 0.2128472043435731, 'skin': 0.2002025835578466, 'girl': 0.18047172137275672, 'still': 0.14433846109638315, 'children': 0.2139431299819058, 'hate': 0.2029529885135762, 'cuz': 0.20567953239001968, 'second': 0.12410286703510201, 'trust': 0.15849458829250324, '@5SOS': 0.522509338933621, 'fan': 0.13140929891508826, 'the': 0.11312710132038926, 'use': 0.1747151323794352, 'Or': 0.16701759467810617, 'live': 0.1374152367881377, 'lmao': 0.08668693320065536, 'loved': 0.17494522782201025, '10': 0.08191090651212612, 'thought': 0.16777969920024025, 'worst': 0.16914346370339178, 'drink': 0.32309747709245457, 'piece': 0.1437983444661309, 'look': 0.14593796976586493, '1': 0.1183310634423518, 'tomorrow': 0.08038560487052415, 'from': 0.08342196166158357, 'nothing': 0.1448394105587396, 'CUTE': 0.2988446270990262, 'self': 0.22153104912268948, 'Wow': 0.09520923415371993, 'More': 0.045930156870446825, 'Let': 0.11307618613657004, 'tonight': 0.08133746847441033, 'being': 0.19720997353000402, 'thoughts': 0.18631005099854597, 'TV': 0.09713909168583648, 'mean': 0.21083085369639942, 'they': 0.15441902138410388, 'Always': 0.11140803243625273, 'art': 0.2592662137038901, 'country': 0.058228852233062754, 'was': 0.15189294916851945, 'wish': 0.19439373954685427, '…': 0.0654767561204088, 'Stop': 0.15241937702246033, 'till': 0.13009478576111094, 'OK': 0.27481347614733925, 'you`ll': 0.17910933235794402, 'yes': 0.17446425556351727, 'even': 0.17212264237255975, 'right': 0.12052069120778774, 'great': 0.10259541183729366, 'years': 0.12313990544433619, 'ill': 0.2578067585247701, 'money': 0.107946507535826, 'cold': 0.1525719411378024, 'went': 0.14842628003396105, 'followers': 0.45084901014508083, 'feel': 0.21257795613620406, 'dick': 0.34344388790063823, 'school': 0.15078957040157484, 'soon': 0.1176768725717632, 'he`s': 0.17392033367774776, 'Maybe': 0.15763085358152704, 'ARE': 0.12800006520809837, 'morning': 0.14978717609628223, 'feelings': 0.16955845207336315, 'happens': 0.13345506794461445, 'mess': 0.21886703688069806, 'brain': 0.24405422685986866, 'means': 0.16314512379961094, 'using': 0.12877878546884008, 'music': 0.07301814123850144, 'ice': 0.13957199817274235, 'seem': 0.22416955497956148, 'Keep': 0.13874460924257262, 'thinking': 0.18409487530494137, 'LIVE': 0.19658927912538274, 'IN': 0.06806512146397001, 'room': 0.15693204774217534, 'coffee': 0.24161443982678762, 'bitches': 0.21556927712736978, 'any': 0.1395714042361331, 'feeling': 0.15408878660987418, 'Today': 0.31861010746363666, 'must': 0.10363679544364321, 'lost': 0.08137202885553627, 'far': 0.13483647738412222, 'normal': 0.3207157021575383, 'wait': 0.09347663062653622, 'Please': 0.0710713220892336, '@YouTube': 0.42449065294676136, 'ng': 0.15072810748257248, 'He`s': 0.09047868743875939, 'If': 0.15092422270178768, 'wife': 0.22669273292540476, 'YOU': 0.1058200966266901, 'read': 0.15818038300117696, 'handle': 0.19011951105374142, 'stats': 0.7847732178195616, 'super': 0.2515576337894602, 'though': 0.13400386065667413, 'gave': 0.13803627597497575, '+': 0.10588438327633487, 'mom': 0.16186952206246422, 'answer': 0.14571913326862806, 'started': 0.14431358065429975, 'looked': 0.1297035742877149, 'water': 0.13575864840987306, 'help': 0.11173649560972183, 'terrible': 0.16130953959342717, 'movie': 0.13028481250590232, 'seems': 0.15796405998932703, 'get': 0.14498168890360474, 'god': 0.2728221111397598, 'sweet': 0.18863304040574072, '??': 0.06460384148668462, 'Look': 0.0988260825857361, 'w': 0.14393197672545238, 'crush': 0.23937180730143032, 'Still': 0.08227029058857169, 'tried': 0.21144772725887892, 'shows': 0.1202176512339846, 'I`d': 0.20012086100202348, 'We`re': 0.0796967738521265, 'knew': 0.12598436688820167, 'fell': 0.23194646053507492, 'Know': 0.21494719680644903, 'BUT': 0.12710265542415505, 'horrible': 0.29260035470021567, 'hi': 0.2203184425624587, 'tweet': 0.21960032314265246, 'less': 0.14888959241330252, 'dude': 0.18719669670951491, 'Be': 0.17596890582674035, 'what': 0.1594450042049952, 'police': 0.20249637978992024, 'https:…': 0.046380599789535876, 'who': 0.1717202768272402, 'wearing': 0.1716082523433557, 'spend': 0.13569263976791024, 'fucked': 0.297613881789003, 'yet': 0.13138905919945973, 'Back': 0.2212928240808303, 'now.': 0.369585976953058, 'into': 0.1575909003197653, 'hell': 0.18131684600921302, 'giving': 0.1354185361928764, 'post': 0.19245295144015923, 'eye': 0.17330927485336567, 'Y`all': 0.08611554551578339, 'reason': 0.20224078566856243, '!': 0.11123098717235753, 'year': 0.09858665852383873, 'Its': 0.1495521800045517, 'change': 0.06412464052303254, 'down': 0.12298245797178337, 'few': 0.17488031297872497, 'daddy': 0.21078440368149068, 'fat': 0.3752401150022534, 'Happy': 0.0697827718347029, 'At': 0.13470262098868194, 'one': 0.14818101596795655, 'might': 0.14453925719145297, 'you`re': 0.19513786751346607, 'done': 0.12733607731608623, 'Can`t': 0.10167262537707887, 'inside': 0.1596689322294506, 'promise': 0.2504177745538074, 'WAS': 0.11454406380108911, 'cool': 0.1698710315968131, 'totally': 0.19253988622693188, 'his': 0.10776193376959545, 'did': 0.13905538454457833, 'why': 0.17729728612589568, 'FUCK': 0.24436533337109706, 'true': 0.18930854036610933, 'From': 0.059627570821937564, 'against': 0.05627532116707948, 'fine': 0.20952448138361124, '7': 0.05828761766357942, '@Michael5SOS': 1.0, 'following': 0.17418144849522343, 'NO': 0.09882938934368612, 'early': 0.10122009278725948, 'ALL': 0.08882938621028466, 'Who': 0.11153030442303513, 'They': 0.1024576332796542, 'himself': 0.14296176225320556, 'mind': 0.15853494877603672, 'someone': 0.1925164926246868, 'often': 0.17350427858464154, 'idea': 0.19213704046623686, 'whatever': 0.1903977886275059, 'SO': 0.15165312049872257, 'between': 0.11611963384095193, 'well': 0.17139722591870124, 'control': 0.12341789633725335, 'pay': 0.1315727018069634, ';)': 0.17499367597600513, 'wrong': 0.15279960580893662, 'eyes': 0.2087822704577801, 'mother': 0.20160459127138933, 'there': 0.1371604842755402, 'Big': 0.12091267353730076, 'food': 0.14947212860346576, 'hey': 0.216679996301381, 'straight': 0.16199282044857044, 'again': 0.15766293230615605, 'thing': 0.17232107579772896, 'favorite': 0.1500224871387153, 'death': 0.18506474988929078, 'three': 0.12643837308841974, 'top': 0.10734706195481265, 'met': 0.1867084706933846, 'pussy': 0.24338672248775758, 'okay': 0.19604331279630166, 'u': 0.15702394822208643, 'care': 0.20636575529061232, 'you!': 0.091430777929462, 'Like': 0.1807832319228054, 'ive': 0.47470949048954647, 'Lol': 0.06356269108225236, 'listen': 0.1510788889698205, 'health': 0.22143074709857163, 'dead': 0.17734343410172743, 'leave': 0.13841622121348468, 'anything': 0.16327466269972873, 'group': 0.11629362507063074, 'need': 0.1487135169461076, 'truly': 0.22332085879218386, 'Michael': 0.24577238674232013, 'DONT': 0.17923968244569527, 'at': 0.10473586987767569, 'man': 0.11810637309343174, 'set': 0.10505223350296546, 'Take': 0.08005356907468775, 'https…': 0.035943717195571476, '&lt': 0.6992636898769697, 'ME': 0.14219511651688616, 'smh': 0.08847281413344392, 'never': 0.18103367009436208, 'party': 0.0986145294391257, 'think': 0.18960873287111446, 'behind': 0.111089657674558, 'easy': 0.11771520182529659, 'minutes': 0.12206487520581605, 'says': 0.11909340774490827, 'lit': 0.09643029308981153, 'would': 0.16136265168319855, 'hour': 0.14773388128545292, 'enough': 0.177152226969715, 'Love': 0.12180004079245581, 'watch': 0.13373481581082922, 'sitting': 0.19870344661246264, 'boys': 0.1795863277340007, 'But': 0.19961258151562883, 'took': 0.13901624913293006, 'Here': 0.08451381896727465, 'having': 0.17732588136653615, 'Bitch': 0.38066048443491357, 'sounds': 0.18171538561960646, 'So': 0.13823891510113215, 'break': 0.12574154034985302, 'sunshine': 0.6990477397062379, 'buy': 0.13791149815347606, 'I’m': 0.22278314793378823, 'right?': 0.17603082287170918, 'Someone': 0.17133720837577748, 'me!': 0.21509466417423603, 'thinks': 0.1540770762021935, 'hoes': 0.16100341427112275, ')': 0.19438403131575238, ':/': 0.20268534488567447, 'family': 0.1374935531223582, 'yeah': 0.1305722272514287, 'ON': 0.0967881793570861, 'gotta': 0.1433051169985145, 'had': 0.15180466080752106, 'internet': 0.24363884390852497, 'killed': 0.11722739789891419, 'definitely': 0.13172806483485536, 'been': 0.14277572891244555, 'huge': 0.179743467919977, 'running': 0.09117066376707857, 'very': 0.18543331961784099, 'heard': 0.13541923239406695, 'ITS': 0.19017857771294688, 'moment': 0.1058105813468159, 'able': 0.13547819484576684, 'sit': 0.15130975469081462, 'shower': 0.2622254513848176, 'liked': 0.5626373271050187, 'shit': 0.19599673034804063, 'girls': 0.18063271575574316, 'play': 0.09491371584837417, 'other': 0.14829467490779985, 'Too': 0.13324353579375103, 'red': 0.17446158496439093, 'he': 0.1255662690596038, 'positive': 0.2049215862803447, 'only': 0.16064515660492043, 'Boy': 0.20270210108737163, 'victims': 0.2891284880636742, 'many': 0.14569538468606683, 'sexy': 0.1545320961382164, 'follower': 0.6549544301145456, '//': 0.07685648939125488, 'try': 0.18219749667240173, 'real': 0.15373527262183379, 'likes': 0.2024087838603605, 'x': 0.23542612437331403, 'this': 0.13006848534770185, 'HOW': 0.13358926756451195, 'taking': 0.1368835383134667, 'I`M': 0.15795159205301232, 'later': 0.11962635238387538, 'It': 0.14498302669977492, 'cut': 0.17108393102612354, 'em': 0.10976793591011785, 'LOL': 0.18939221831072053, 'understand': 0.18544880162565247, '&': 0.6329669874622871, 'sorry': 0.26986655371658036, 'thats': 0.26088484329128336, 'delete': 0.2891324943212765, 'To': 0.156019781133666, 'no': 0.15858716553855598, 'What`s': 0.12630009138227416, 'doing': 0.14231561993789335, 'Day': 0.10207990520560963, 'special': 0.1346079809558252, 'Bernie': 0.06403006640638334, 'free': 0.10381106145692627, 'ready': 0.08674156507105106, 'myself': 0.30281947606134135, 'damn': 0.1575237405835327, 'rest': 0.1466650337221688, 'like': 0.18983517484056098, 'Think': 0.23120616256333848, 'sucks': 0.23633562788248494, 'calls': 0.1224291196042499, 'you?': 0.16913113121520953, 'omg': 0.18717749641009335, 'Girls': 0.20320606508379815, 'mine': 0.1701920137774105, '@Luke5SOS': 0.866137147044257, '30': 0.07593808301493622, '??????': 0.0790562255370057, 'Come': 0.05975691688490637, 'chance': 0.07983437965139491, 'laugh': 0.17221651809508418, 'I': 0.20193041198400505, ':)': 0.1514377742565828, 'about': 0.16454807667244042, 'kill': 0.26696494383071556, 'playing': 0.10357820136530335, '5': 0.09120123317852073, 'annoying': 0.1771943362158342, 'run': 0.08399513326548012, 'bring': 0.08870884047149878, 'cat': 0.25750154458555047, 'good': 0.15735346425704244, 'there`s': 0.2024454426779976, 'really': 0.19198124433799427, 'save': 0.11771876202450304, 'Up': 0.09757840060411797, '3': 0.08457924898378213, 'ex': 0.21667387025264181, 'photo': 0.12129633859550795, 'scared': 0.21937692494330796, 'won`t': 0.13446652972392112, 'AT': 0.06962865077922178, 'basically': 0.30868796374811447, 'killing': 0.17087205862691376, 'as': 0.1263863149040729, 'supposed': 0.22385211762303409, 'tweets': 0.2460417747380575, 'that.': 0.46502544050730454, 'getting': 0.1337371199551231, '#Periscope': 0.370479554937705, 'drinking': 0.342547760805172, 'OUT': 0.09141041289886447, 'that': 0.1471460678397836, 'much': 0.16998825270798643, 'instead': 0.18711148940049654, 'starting': 0.1171420233208853, 'lie': 0.11970765561711925, 'You': 0.1387391911203511, 'Every': 0.11970765561711928, 'end': 0.12806610831793344, 'worry': 0.1573746540974725, 'glad': 0.1779962785564929, 'Girl': 0.14617927582369208, 'mad': 0.15363424075507695, 'Get': 0.043328297425611326, 'You`re': 0.20207283818321323, 'teacher': 0.15771580728174087, 'key': 0.16346732182779755, 'to': 0.1277371326089665, 'months': 0.13284513489229424, 'hot': 0.19665238860260903, 'simply': 0.2580613863132738, 'stupid': 0.19152713682517938, '?????': 0.061432856219122756, 'jokes': 0.24873176635623465, 'walk': 0.1366775034253389, 'car': 0.1476429929706316, 'their': 0.12932411688228862, 'hands': 0.13018579556869608, 'sa': 0.1562879063235273, 'see': 0.10996629282117935, 'imagine': 0.16485462893973826, 'af': 0.11643305023250444, 'shot': 0.08404850228526053, 'rock': 0.16726820217342211, 'wow': 0.16798768820836127, 'worth': 0.17147331979337407, 'rather': 0.15218600122235296, 'pain': 0.2622765221693332, 'whenever': 0.27954610795327955, 'while': 0.15458669649455306, 'child': 0.24839541746263138, 'dumb': 0.18211213222710051, 'keeps': 0.16505972362095067, 'head': 0.1605453788245716, 'tell': 0.19112910590338042, 'gonna': 0.16846339140492186, 'Would': 0.1857211368871126, 'pic': 0.16916849160139633, 'perfect': 0.14929414026917656, 'With': 0.11118699274327787, 'felt': 0.20982310856482425, 'it`s': 0.20230670920603452, 'then': 0.15730579619621407, 'today': 0.10109781783409579, 'nigga': 0.13060675539952812, 'eating': 0.200637235474588, 'asleep': 0.17360669651073182, 'talking': 0.1538568057207262, 'check': 0.09875693875254338, 'finally': 0.12658150574639584, 'U': 0.17908021924091871, 'yea': 0.18852063769248936, 'Stay': 0.1967902212323448, 'GOD': 0.06880272260463914, 'agree': 0.14302293751570244, 'dogs': 0.2337064919724821, 'outside': 0.13007114371284617, 'kids': 0.13248786876100022, 'story': 0.11189640897348545, 'poor': 0.15547588449213787, 'boyfriend': 0.20616359490671599, 'shouldn`t': 0.1851578071377206, 'people': 0.1838520623049472, 'A': 0.11174280009289195, 'book': 0.07164965108789298, 'days': 0.15242889264384596, 'off': 0.1361406758631024, 'That': 0.12677108449515362, 'He': 0.10221470541385436, 'suicide': 0.4126978133157846, 'ang': 0.23089801665187162, 'opinion': 0.2134239929584529, 'house': 0.15802309766965789, 'told': 0.17419976063309683, 'Jesus': 0.14053348413291564, 'Really': 0.12547984527282943, 'phone': 0.16197577523246756, 'No': 0.1733875822914442, 'working': 0.08606639607969105, 'half': 0.09939097504659081, 'awesome': 0.09690681137316, 'character': 0.24303841450720337, 'actually': 0.21219122714119043, 'such': 0.1733840755097093, 'week': 0.07001289005941876, 'cry': 0.21670954448199756, 'than': 0.13607265018381162, 'social': 0.16511682169321515, '=': 0.10172199530766533, 'sign': 0.14412038415397443, 'na': 0.13703658249436496, 'God': 0.08037197371962664, 'up': 0.1344520236225406, 'don`t': 0.18165124262958832, 'page': 0.16119869461563419, 'excited': 0.09945192942547257, 'night': 0.11622347751001318, 'kinda': 0.1697970912905049, 'they`re': 0.2273468969615846, 'wtf': 0.19658927912538274, 'http…': 0.047031348473502155, 'soul': 0.13821739922425727, 'under': 0.12937118931557748, 'back': 0.12417825622313787, 'away': 0.1208267532601746, 'makes': 0.20088507595450855, '8': 0.07717006611749475, 'In': 0.12407449291763453, 'start': 0.12499852504453932, 'Will': 0.07308528816799384, 'im': 0.3167983879982809, 'share': 0.0728021896574809, 'please': 0.1618879799768732, 'give': 0.16103223834617278, 'maybe': 0.20943105494203124, 'RT': 0.08885623233952758, 'I`ll': 0.18663430917910412, 'am': 0.25848148137403454, '..': 0.3159153793520398, 'Of': 0.13098695208077088, 'extremely': 0.3866805123115239, 'said': 0.13436636010411068, 'serious': 0.12588973656311417, 'Thanks': 0.13001707296310527, 'first': 0.11469981686200625, 'actual': 0.22234081444630038, 'Black': 0.06964430809504599, '9': 0.10572698422503411, 'fans': 0.060914985193576195, 'Did': 0.13668157833560649, 'realize': 0.17005255783000414, 'It`s': 0.14813284648122654, 'believe': 0.14184812571840086, 'listening': 0.13946590349621407, 'son': 0.09378003543436332, 'dying': 0.2724665787514846, 'Do': 0.177443943935855, 'who`s': 0.1571629961342601, 'trash': 0.15040514148508788, 'friend': 0.17176585143394635, 'absolutely': 0.24014692159891945, 'everyone': 0.19088711137286848, 'MY': 0.1188190387981694, 'high': 0.16419005780374238, 'dad': 0.22810601824151852, 'heart': 0.14620519751202216, 'came': 0.14363883137140165, 'Why': 0.13063445892059028, 'proud': 0.1360145960637372, 'happen': 0.12023742976877554, 'takes': 0.11502027981043411, 'nice': 0.1944455682338499, 'after': 0.10971972377897773, 'Never': 0.11635308015352396, 'them': 0.169758173038666, '2': 0.1261461859610227, 'guess': 0.21695356731473742, 'words': 0.16346732182779755, 'See': 0.08330683263895147, 'forget': 0.13352016349792287, 'were': 0.1435987413406885, 'broken': 0.237534010257071, 'block': 0.1745189709260954, 'everyday': 0.14978056261391937, 'small': 0.15922091704605584, 'Only': 0.10761922724781639, '6': 0.07560224717618759, 'May': 0.07980876989059779, 'call': 0.1495521800045517, 'date': 0.3042114989742419, 'shirt': 0.2200521672654567, 'IF': 0.0955789052153059, 'hurts': 0.2882952551120586, 'stuff': 0.20887645683255146, 'catch': 0.10993218353936045, 'xx': 0.43167439067653623, 'sister': 0.1905811101272161, 'Want': 0.14253861254635636, 'smoke': 0.2606541175825541, 'id': 0.3950780745688578, 'racist': 0.22143074709857163, 'comes': 0.1204469902429176, 'now': 0.127536051376106, 'late': 0.08728682004335157, 'fake': 0.180595457279631, 'part': 0.14099134959314416, 'anxiety': 0.4823586228566574, 'come': 0.12338768565609601, 'day': 0.13382806963425867, 'smart': 0.20649050479441178, 'dress': 0.19040862680669457, 'broke': 0.15574322901926976, 'There': 0.11255371338281084, 'band': 0.272855335781077, 'FOR': 0.02542579887878282, 'We': 0.06585332131299612, 'fucking': 0.2928954980712939, 'Yeah': 0.13361003655330558, 'OF': 0.07775076424163686, 'Because': 0.21094294937645838, 'honestly': 0.2295045764511736, 'htt…': 0.04878742734417173, 'fire': 0.11891240465084281, 'move': 0.10948617616145519, 'let`s': 0.10622210226373129, 'if': 0.15636288275624974, 'worse': 0.21116531042271003, 'blocked': 0.3266416702791364, 'Remember': 0.16316865674846853, 'There`s': 0.12355111687942563, 'couple': 0.10130785344924308, 'better': 0.11966654957433709, 'class': 0.10238380315730777, 'what`s': 0.18454371833612804, 'On': 0.13313132355524288, 'living': 0.15986710907806, 'bitch': 0.24255120429087543, 'anime': 0.6703948390042538, 'during': 0.09742213897641264, '???': 0.06697305881642783, 'swear': 0.13293876069346347, 'be': 0.13716329264385668, 'else': 0.17630609239641448, ':(': 0.20044814793675186, 'Im': 0.3058096176521306, 'calling': 0.15137901624473726, 'Best': 0.05341498891877247, 'with': 0.12211505998960025, 'safe': 0.14592736907168716, 'sound': 0.13637147979770492, 'has': 0.10913492388244199, 'love': 0.16506522731378415, 'woke': 0.22489699844366773}

	wordsSum = 0
	total = sum(keywords.values())

	for key, value in keywords.items():
		word = key.decode("utf-8")
		try:
			wordsSum += table[word] * value
		except:
			total -= value

	if not total:
		return 0

	return wordsSum / total

if __name__ == '__main__':

	#pass in the username of the account you want to download
	get_all_tweets(sys.argv[1])


