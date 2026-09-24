#!/usr/bin/env python3
"""Generates every quiz page + the hub from the QUIZZES table. Run: python3 build.py  (then node --check is run by test.sh)."""
import os, pathlib, html
ROOT = pathlib.Path(__file__).parent
LOGO = "https://s43932.pcdn.co/wp-content/uploads/sites/190/2024/02/Flat-Horizontal-VVIS.png"
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&family=Barlow+Semi+Condensed:wght@400;500;600&display=swap" rel="stylesheet">'
FOOTER = '<footer>Vascular &amp; Vein Institute of the South &middot; <a href="tel:+19013902930">901-390-2930</a> &middot; <a href="https://vascularandveininstitute.com/locations/">14 locations in Tennessee, Mississippi and Arkansas</a><br>These tools are educational and do not replace an examination by a physician.</footer>'

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Vascular &amp; Vein Institute of the South</title>
<meta name="description" content="{description}">{canonical}
{fonts}
<link rel="stylesheet" href="../assets/quiz.css">
</head>
<body>
<header><div class="wrap top"><a href="https://vascularandveininstitute.com/"><img src="{logo}" alt="Vascular &amp; Vein Institute of the South"></a><a class="back" href="../">All self-check quizzes &rarr;</a></div></header>
<main class="wrap">
<h1>{title}</h1>
<p class="lead">{lead}</p>
<div id="vvis-quiz" class="vq" role="region" aria-label="{title}"><div class="vq-card"><div class="vq-progress" aria-hidden="true"><div class="vq-bar"></div></div><div class="vq-body"></div></div></div>
</main>
{footer}
<script>
{config}
</script>
<script src="../assets/quiz.js"></script>
</body>
</html>
"""

QUIZZES = [
dict(slug="pad", title="Peripheral Artery Disease Risk Quiz", hub="Peripheral artery disease (PAD)", blurb="Leg pain when walking, slow-healing sores, cold feet. Ten questions.",
 lead="Ten quick questions about your legs and your health. Your answers stay on your device — nothing is collected or stored.",
 description="Ten-question peripheral artery disease (PAD) risk self-check from the vascular surgeons of Vascular & Vein Institute of the South. Instant result, no personal information collected.",
 canonical=os.environ.get("PAD_CANONICAL",""),
 config=r"""window.VVIS_QUIZ={id:'pad_quiz',questions:[
 {q:'How old are you?',help:'Risk rises with age, especially after 65.',opts:[['Under 50',0],['50 to 64',1],['65 or older',2]]},
 {q:'Do you smoke, or have you smoked in the past?',help:'Smoking is the single strongest risk factor for PAD.',opts:[['Never smoked',0],['Former smoker',1],['Current smoker',3]]},
 {q:'Have you been diagnosed with diabetes?',help:'',opts:[['No',0],['Yes',2]]},
 {q:'Do you have high blood pressure or high cholesterol?',help:'Either one counts.',opts:[['Neither',0],['One of them',1],['Both',2]]},
 {q:'Have you had a heart attack, stroke, heart stents or bypass, or been told you have kidney disease?',help:'Artery disease in one part of the body often means it is present elsewhere.',opts:[['No',0],['Yes',2]]},
 {q:'Do your legs, calves, thighs or buttocks ache, cramp, or feel tired when you walk — and feel better after a few minutes of rest?',help:'This pattern is called claudication and is the classic sign of PAD.',opts:[['No',0],['Sometimes',2],['Often, or it limits how far I walk',3]]},
 {q:'Do you have pain in your feet or toes while resting or lying down, especially at night?',help:'',opts:[['No',0],['Yes',4]],flag:'Rest pain in the feet can mean severely reduced blood flow.'},
 {q:'Do you have a sore or wound on your foot, toe or lower leg that has not healed in more than two weeks?',help:'',opts:[['No',0],['Yes',4]],flag:'A wound that will not heal needs a circulation check promptly.'},
 {q:'Is one foot or leg colder, paler or more discolored than the other, or do you have numbness or hair loss on your lower legs?',help:'',opts:[['No',0],['Yes',2]]},
 {q:'Has a parent or sibling had PAD, an aneurysm, a heart attack or a stroke before age 65?',help:'',opts:[['No or not sure',0],['Yes',1]]}
],result:function(r){
 if(r.flags.length||r.score>=7) return {tier:'high',label:'Higher likelihood of PAD',text:'Your answers include signs that are commonly linked to reduced blood flow in the legs. This is worth evaluating soon rather than watching. The first test is simple and painless — a blood-pressure comparison between your arm and ankle (an ankle-brachial index) plus an ultrasound in our office.',flags:r.flags,urgent:r.flags.length?'Please call us today at '+r.PHONE+' so we can see you quickly.':null};
 if(r.score>=3) return {tier:'mod',label:'Some risk factors present',text:'You have risk factors that make PAD more likely, even if you have few symptoms today. A short vascular evaluation can tell you where you stand and what to do about it — often before any damage is done.'};
 return {tier:'low',label:'Lower likelihood of PAD',text:'Your answers suggest a lower likelihood of PAD right now. Keep it that way: stay active, avoid tobacco, and manage blood pressure, cholesterol and blood sugar. If you develop leg pain when walking, sores on your feet that will not heal, or a cold or discolored foot, get checked.'};
},disclaimer:'This quiz is an educational screening tool, not a diagnosis. Only an examination can confirm or rule out peripheral artery disease. If you have sudden severe leg pain, a cold pale leg, or chest pain, call 911.'};"""),

dict(slug="vein", title="Vein Health Check", hub="Vein health", blurb="Varicose veins, aching or swollen legs, skin changes. Ten questions.",
 lead="Ten quick questions about your legs. Your answers stay on your device — nothing is collected or stored.",
 description="Ten-question vein health self-check: varicose veins, aching or swollen legs, skin changes and ulcers. Instant result, no personal information collected.",
 config=r"""window.VVIS_QUIZ={id:'vein_quiz',questions:[
 {q:'Can you see veins on your legs?',help:'',opts:[['No visible veins',0],['Small web-like or spider veins',1],['Bulging, rope-like varicose veins',2]]},
 {q:'Do your legs ache, feel heavy or tired, especially by the end of the day or after standing?',help:'',opts:[['No',0],['Sometimes',1],['Most days',2]]},
 {q:'Do your ankles or lower legs swell by evening?',help:'',opts:[['No',0],['Sometimes',1],['Most days',2]]},
 {q:'Do you get night-time leg cramps or restless, jumpy legs?',help:'',opts:[['No',0],['Yes',1]]},
 {q:'Do you have itching or burning over the veins, or has the skin around your ankles turned darker, thicker or shiny?',help:'Skin changes are a sign the vein problem has been present for a while.',opts:[['No',0],['Itching or burning',1],['Skin has changed color or texture',2]]},
 {q:'Do you have, or have you had, an open sore near the ankle that was slow to heal?',help:'',opts:[['No',0],['Yes',4]],flag:'A slow-healing sore near the ankle is often a vein problem and should be seen promptly.'},
 {q:'Have you ever had a blood clot in a leg vein (DVT) or a painful, red, hard vein?',help:'',opts:[['No',0],['Yes',2]]},
 {q:'Does your work keep you standing or sitting in one place for long hours?',help:'',opts:[['No',0],['Yes',1]]},
 {q:'Have you had one or more pregnancies, or do close family members have varicose veins?',help:'',opts:[['Neither',0],['One of these',1],['Both',2]]},
 {q:'Have you tried compression stockings or elevating your legs without lasting relief?',help:'',opts:[['Have not tried',0],['Tried, and it helps',0],['Tried, not enough relief',1]]}
],result:function(r){
 if(r.flags.length||r.score>=7) return {tier:'high',label:'Vein disease is likely',text:'Your answers point to chronic venous insufficiency — vein valves that no longer close properly, letting blood pool in the legs. A painless ultrasound (venous duplex) confirms it and maps which veins are involved. Modern treatment is done in the office in under an hour with no downtime, and is usually covered by insurance when symptoms are present.',flags:r.flags,urgent:r.flags.length?'Please call us at '+r.PHONE+' so we can see you soon.':null};
 if(r.score>=3) return {tier:'mod',label:'Symptoms worth checking',text:'You have several signs that often come from vein disease. Left alone, these tend to progress slowly; treated early, they are simple to fix. A vein ultrasound in our office takes about 30 minutes and tells us exactly what is going on.'};
 return {tier:'low',label:'Lower likelihood of vein disease',text:'Your legs are not showing much sign of vein trouble. Staying active, avoiding long stretches of standing still, and elevating your legs when they are tired all help. If bulging veins, swelling or skin changes develop, come see us.'};
},disclaimer:'This quiz is an educational screening tool, not a diagnosis. A venous ultrasound is needed to confirm vein disease.'};"""),

dict(slug="ufe", title="Fibroids: Is UFE Right for Me?", hub="Fibroids &mdash; is UFE right for me?", blurb="Heavy periods, pelvic pressure, avoiding surgery. Six questions.",
 lead="Six questions about your symptoms and situation. Your answers stay on your device — nothing is collected or stored.",
 description="Six-question self-check on whether uterine fibroid embolization (UFE), a non-surgical fibroid treatment, may be an option. Instant result, no personal information collected.",
 config=r"""window.VVIS_QUIZ={id:'ufe_quiz',questions:[
 {q:'Have you been told you have uterine fibroids?',help:'',opts:[['Yes, diagnosed by ultrasound or MRI',2],['Not sure, but I have symptoms',1],['No',0]]},
 {q:'Which of these do you experience? Choose all that apply.',help:'',multi:true,opts:[['Heavy periods (soaking through pads or passing clots)',2],['Periods lasting more than 7 days',1],['Pelvic pressure, fullness or a growing belly',1],['Needing to urinate often, or trouble emptying',1],['Pain during sex, or lower back and leg pain',1],['Fatigue or anemia from blood loss',2],['None of these',0,'none']]},
 {q:'Are you pregnant now, or hoping to become pregnant in the next year?',help:'',opts:[['No',0],['Yes',0]]},
 {q:'Have you gone through menopause?',help:'',opts:[['No',0],['Yes',0]]},
 {q:'What treatments have you tried for fibroid symptoms?',help:'',opts:[['None yet',0],['Medication or a hormonal IUD, without enough relief',1],['I have been offered surgery (hysterectomy or myomectomy)',2]]},
 {q:'How important is it to you to avoid surgery and keep your uterus?',help:'',opts:[['Very important',1],['Somewhat',0],['Not a priority',0]]}
],result:function(r){
 var preg=r.chosen(2,'Yes'), meno=r.chosen(3,'Yes'), dx=r.value(0), sym=r.value(1);
 if(preg) return {tier:'info',label:'Talk with us before choosing a fibroid treatment',text:'UFE is generally not recommended for women who are pregnant or planning a pregnancy soon, because its effect on future fertility is still being studied. There are other fibroid options, and the right one depends on your goals — a consultation can lay them out.'};
 if(meno&&sym>0) return {tier:'info',label:'New symptoms after menopause need a prompt evaluation',text:'Fibroids usually shrink after menopause, so new bleeding or pelvic symptoms should be evaluated by a physician promptly to rule out other causes before any fibroid treatment is considered.'};
 if(dx===2&&sym>=2) return {tier:'high',label:'You may be a good candidate for UFE',text:'You have diagnosed fibroids with the kind of symptoms UFE treats well. UFE is a non-surgical, outpatient procedure: a tiny catheter blocks the arteries feeding the fibroids, which then shrink over the following months. Most women go home the same day and keep their uterus. A consultation with imaging confirms whether your fibroids are suited to it.'};
 if(sym>=2) return {tier:'mod',label:'Worth an evaluation',text:'Your symptoms are typical of fibroids. The next step is a pelvic ultrasound or MRI to confirm the diagnosis and measure the fibroids — then we can tell you whether UFE, medication or surgery fits best.'};
 return {tier:'low',label:'UFE is probably not the first step right now',text:'Without a fibroid diagnosis or significant symptoms, there is nothing to treat yet. If heavy periods, pelvic pressure or urinary changes develop, an ultrasound is the place to start.'};
},disclaimer:'This quiz is an educational screening tool, not a diagnosis. Imaging and a consultation determine whether UFE is appropriate.'};"""),

dict(slug="aaa", title="Aortic Aneurysm Screening: Do I Qualify?", hub="Aortic aneurysm screening", blurb="Do you qualify for a one-time screening ultrasound? Five questions.",
 lead="Five questions. A one-time screening ultrasound is quick, painless and covered by Medicare for people who qualify.",
 description="Five-question check on whether you meet the recommendation for a one-time abdominal aortic aneurysm (AAA) screening ultrasound. Instant result, no personal information collected.",
 config=r"""window.VVIS_QUIZ={id:'aaa_quiz',questions:[
 {q:'How old are you?',help:'',opts:[['Under 60',0],['60 to 64',1],['65 to 75',2],['Over 75',1]]},
 {q:'What was your sex at birth?',help:'Screening recommendations differ for men and women.',opts:[['Male',1],['Female',0]]},
 {q:'Have you smoked at least 100 cigarettes in your lifetime?',help:'Even if you quit long ago.',opts:[['No',0],['Yes',2]]},
 {q:'Has a parent, brother or sister had an aortic aneurysm?',help:'',opts:[['No or not sure',0],['Yes',3]]},
 {q:'Do you have high blood pressure, or known artery disease (PAD, carotid disease or heart disease)?',help:'',opts:[['No',0],['Yes',1]]}
],result:function(r){
 var a60=r.chosen(0,'60 to 64'), a65=r.chosen(0,'65 to 75'), a75=r.chosen(0,'Over 75'), male=r.chosen(1,'Male'), smoked=r.chosen(2,'Yes'), fam=r.chosen(3,'Yes');
 if(male&&a65&&smoked) return {tier:'high',label:'You meet the standard screening recommendation',text:'Men aged 65 to 75 who have ever smoked are recommended to have a one-time abdominal ultrasound to check for an aortic aneurysm. It takes about 15 minutes, uses no needles or radiation, and Medicare covers a one-time screening with a physician referral. Most people who are screened are reassured; the few who are not are watched or treated before the aneurysm becomes dangerous.',cta1:'Schedule a screening'};
 if(fam&&(a65||a75)) return {tier:'high',label:'Screening is recommended because of your family history',text:'A parent or sibling with an aortic aneurysm raises your own risk, and a one-time screening ultrasound is recommended for close relatives aged 65 and older regardless of smoking history. It is quick and painless, and Medicare covers it for people with a family history.',cta1:'Schedule a screening'};
 if(fam) return {tier:'mod',label:'Plan on screening — your family history matters',text:'Close relatives of someone with an aortic aneurysm should have a one-time ultrasound at 65, or earlier if your physician advises it. Tell your physician about the family history now so it is not missed.'};
 if(a65&&smoked) return {tier:'mod',label:'Screening is worth discussing',text:'For women aged 65 to 75 who have smoked, national guidelines leave the decision to you and your physician, while the Society for Vascular Surgery does recommend a one-time ultrasound. If you also have high blood pressure or other artery disease, screening is reasonable — let us talk it through with you.'};
 if(male&&a65) return {tier:'mod',label:'Screening is optional for you',text:'For men aged 65 to 75 who never smoked, guidelines suggest offering screening selectively. It is reasonable if you have high blood pressure or other artery disease, or simply want the reassurance — a 15-minute ultrasound answers the question for good.'};
 if(a75&&smoked) return {tier:'mod',label:'A one-time scan may still be reasonable',text:'If you have never had an abdominal ultrasound and are in good health, a one-time screening can still be worthwhile after 75 for people who have smoked. Ask us or your physician.'};
 if(a60&&smoked) return {tier:'mod',label:'You will reach screening age soon',text:'The standard recommendation begins at 65 for people who have ever smoked. Plan on a one-time ultrasound then — or sooner if a family history comes to light or you develop unexplained abdominal or back pain.'};
 return {tier:'low',label:'Routine screening is not recommended for you right now',text:'Based on your answers, guidelines do not call for AAA screening at this time. That can change with age or a new family history, so revisit this check periodically. Sudden severe abdominal or back pain with dizziness is an emergency — call 911.'};
},disclaimer:'This quiz reflects general screening guidelines (U.S. Preventive Services Task Force and the Society for Vascular Surgery) and Medicare coverage rules; it is not a diagnosis.'};"""),

dict(slug="gae", title="Knee Pain: Could Genicular Artery Embolization Help?", hub="Knee pain &mdash; could GAE help?", blurb="Osteoarthritis knee pain when other treatments have not done enough. Seven questions.",
 lead="Seven questions about your knee. Your answers stay on your device — nothing is collected or stored.",
 description="Seven-question check on whether genicular artery embolization (GAE), a minimally invasive treatment for knee osteoarthritis pain, may be an option. Instant result, no personal information collected.",
 config=r"""window.VVIS_QUIZ={id:'gae_quiz',questions:[
 {q:'Has a doctor told you that you have osteoarthritis (wear-and-tear arthritis) in this knee?',help:'Usually confirmed on an X-ray or MRI.',opts:[['Yes',2],['Not sure',1],['No',0]]},
 {q:'How long has the knee hurt?',help:'',opts:[['Less than 3 months',0],['3 to 6 months',1],['More than 6 months',2]]},
 {q:'On most days, how bad is the pain?',help:'',opts:[['Mild',0],['Moderate — limits some activities',1],['Severe — limits walking, stairs or sleep',2]]},
 {q:'What have you already tried? Choose all that apply.',help:'',multi:true,opts:[['Physical therapy or exercise program',1],['Anti-inflammatory medicines',1],['Steroid or gel (hyaluronic acid) injections',1],['Weight loss, bracing or activity changes',0],['Nothing yet',0,'none']]},
 {q:'Where do things stand with knee replacement?',help:'',opts:[['I have already had a replacement on this knee',0],['It has been recommended, but I want to avoid or delay it',2],['I am not a candidate for surgery',2],['It has not been discussed',1]]},
 {q:'Do you have a known allergy to X-ray contrast dye, or severe kidney disease?',help:'These affect how the procedure is planned, not necessarily whether it can be done.',opts:[['No',0],['Yes',0]]},
 {q:'Is the knee red, hot and swollen right now, or have you had a fever with it?',help:'',opts:[['No',0],['Yes',0]]}
],result:function(r){
 var replaced=r.chosen(4,'I have already had a replacement on this knee'), infect=r.chosen(6,'Yes'), oa=r.value(0), dur=r.value(1), tried=r.value(3), contrast=r.chosen(5,'Yes');
 if(infect) return {tier:'info',label:'A hot, swollen knee needs prompt medical attention',text:'Redness, heat and swelling — especially with fever — can mean infection or an inflammatory flare rather than arthritis wear. Please see a physician promptly before considering any elective procedure.'};
 if(replaced) return {tier:'info',label:'GAE is not designed for a replaced knee',text:'Genicular artery embolization treats pain from the inflamed lining of an arthritic knee joint. Pain after a knee replacement has different causes and should be evaluated by your orthopedic surgeon.'};
 if(oa===2&&dur>=1&&tried>=1) return {tier:'high',label:'You may be a candidate for GAE',text:'You have diagnosed knee osteoarthritis, lasting pain, and have already tried conservative care — the situation GAE was developed for. GAE is a newer, minimally invasive outpatient procedure that reduces blood flow to the inflamed joint lining. Early studies report pain relief for many patients, but results in controlled trials have been mixed and it is not right for everyone. A consultation reviews your imaging and whether it fits your knee.'+(contrast?' Your contrast allergy or kidney history will be part of that planning.':'')};
 if(oa>=1&&dur>=1) return {tier:'mod',label:'Worth a conversation',text:'Your knee pain has lasted long enough to take seriously. If osteoarthritis is confirmed on imaging, the usual path is physical therapy, medication or injections first; GAE is an option to discuss when those have not done enough. We can help you sort the sequence.'};
 return {tier:'low',label:'GAE is probably not the next step yet',text:'Knee pain of short duration, or without an arthritis diagnosis, should start with a primary care or orthopedic evaluation and conservative treatment. If the pain persists beyond a few months despite that, come back to this check.'};
},disclaimer:'This quiz is an educational screening tool, not a diagnosis. GAE is a newer treatment; suitability is decided in consultation after imaging review.'};"""),

dict(slug="carotid", title="Carotid Artery & Stroke Risk Check", hub="Carotid artery &amp; stroke risk", blurb="Risk factors and warning signs for carotid narrowing. Nine questions.",
 lead="Nine quick questions. Your answers stay on your device — nothing is collected or stored.",
 description="Nine-question carotid artery disease and stroke risk self-check. Instant result, no personal information collected.",
 config=r"""window.VVIS_QUIZ={id:'carotid_quiz',questions:[
 {q:'How old are you?',help:'',opts:[['Under 55',0],['55 to 64',1],['65 or older',2]]},
 {q:'Do you have high blood pressure?',help:'',opts:[['No',0],['Yes, controlled with treatment',1],['Yes, and not well controlled',2]]},
 {q:'Do you have high cholesterol or diabetes?',help:'',opts:[['Neither',0],['One of them',1],['Both',2]]},
 {q:'Do you smoke, or have you smoked in the past?',help:'',opts:[['Never',0],['Former smoker',1],['Current smoker',2]]},
 {q:'Have you had a heart attack, an irregular heartbeat (atrial fibrillation), or artery disease in your legs?',help:'',opts:[['No',0],['Yes',2]]},
 {q:'Has a doctor ever told you there is a whooshing sound (bruit) over your neck artery, or that you have narrowing in a neck artery?',help:'',opts:[['No',0],['Yes',3]]},
 {q:'Has a parent or sibling had a stroke or mini-stroke?',help:'',opts:[['No or not sure',0],['Yes',1]]},
 {q:'Have you ever had a brief episode of weakness or numbness on one side, slurred speech, or a curtain-like loss of vision in one eye that went away?',help:'These can be warning strokes (TIAs).',opts:[['No',0],['Yes',4]],flag:'Temporary stroke-like symptoms are a warning sign that needs urgent evaluation, even if they resolved.'},
 {q:'Have you had a stroke before?',help:'',opts:[['No',0],['Yes',3]]}
],result:function(r){
 if(r.flags.length) return {tier:'high',label:'Urgent evaluation recommended',text:'Symptoms that come and go — one-sided weakness, slurred speech, or losing vision in one eye — can be warning strokes. If it is happening now, call 911. If it happened before, you need a carotid ultrasound and a physician visit within days, not weeks.',flags:r.flags,urgent:'Please call us today at '+r.PHONE+'.'};
 if(r.score>=7) return {tier:'high',label:'Higher risk — a carotid ultrasound is worth doing',text:'Several of your answers are linked to narrowing of the carotid arteries, the main vessels that feed the brain. A carotid duplex ultrasound is quick, painless and shows whether plaque is building up. Knowing early lets us lower your stroke risk with medication, lifestyle changes and, when needed, a procedure.'};
 if(r.score>=3) return {tier:'mod',label:'Some risk factors present',text:'You have risk factors for carotid disease and stroke. Controlling blood pressure, cholesterol and blood sugar and staying tobacco-free matter most. Whether a screening ultrasound makes sense depends on how many risk factors you carry — ask us.'};
 return {tier:'low',label:'Lower risk right now',text:'Your answers suggest a lower likelihood of carotid disease. Keep blood pressure and cholesterol in check and stay active. Learn the stroke warning signs — face drooping, arm weakness, speech difficulty — and call 911 immediately if they appear.'};
},disclaimer:'This quiz is an educational screening tool, not a diagnosis. A carotid ultrasound is needed to detect artery narrowing.'};"""),
]

for q in QUIZZES:
    d = ROOT / q["slug"]; d.mkdir(exist_ok=True)
    can = f'\n<link rel="canonical" href="{q["canonical"]}">' if q.get("canonical") else ""
    (d / "index.html").write_text(PAGE.format(title=html.escape(q["title"], quote=False).replace("&amp;", "&amp;"), description=html.escape(q["description"], quote=True), canonical=can, fonts=FONTS, logo=LOGO, lead=q["lead"], config=q["config"], footer=FOOTER), encoding="utf8")

cards = "\n".join(f'<a href="{q["slug"]}/"><h3>{q["hub"]}</h3><p>{q["blurb"]}</p></a>' for q in QUIZZES)
HUB = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Self-Check Quizzes — Vascular &amp; Vein Institute of the South</title>
<meta name="description" content="Free two-minute self-checks from the vascular surgeons of Vascular &amp; Vein Institute of the South: PAD, vein health, fibroids/UFE, aortic aneurysm screening, knee pain/GAE, carotid and stroke risk. No personal information collected.">
{FONTS}
<link rel="stylesheet" href="assets/quiz.css">
</head>
<body>
<header><div class="wrap top"><a href="https://vascularandveininstitute.com/"><img src="{LOGO}" alt="Vascular &amp; Vein Institute of the South"></a><a class="back" href="https://vascularandveininstitute.com/">Back to our website &rarr;</a></div></header>
<main class="wrap">
<h1>Two-minute self-checks</h1>
<p class="lead">Quick, private screening tools from our vascular surgeons. Each takes about two minutes, gives you an instant result and a recommended next step, and collects no personal information.</p>
<div class="hub">
{cards}
</div>
<p class="lead">Ready to be seen? <a href="https://phreesia.me/SelfSchedulingVascular">Schedule online</a> or call <a href="tel:+19013902930">901-390-2930</a>.</p>
</main>
{FOOTER}
</body>
</html>
"""
(ROOT / "index.html").write_text(HUB, encoding="utf8")
print("built", len(QUIZZES), "quizzes + hub")
