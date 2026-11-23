"""Build the interactive web version of the marketing campaign review.

Reads data/processed/comparison-cells.csv, controls.json and the outcome
comparison in deliverables/outcome-comparison, and writes report/index.html,
a self-contained page for GitHub Pages. Standard library only.

    python tools/build_web_report.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from web_report_shell import page

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
COMPARISON = ROOT / "deliverables" / "outcome-comparison"
OUT = ROOT / "report" / "index.html"


def num(v: str):
    return None if v == "" else float(v)


def load() -> dict:
    cube = []
    with open(PROCESSED / "comparison-cells.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cube.append([r["month"], r["channel"], r["previous_outcome"], r["contact_band"],
                         int(r["records"]), int(r["subscriptions"]), int(r["recorded_contacts"])])
    matched = []
    with open(COMPARISON / "matched-cells.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            matched.append({
                "month": r["month"], "order": int(r["month_order"]), "channel": r["channel"],
                "all": int(r["all_records"]),
                "sr": int(r["success_records"]), "ss": int(r["success_subscriptions"]),
                "fr": int(r["failure_records"]), "fs": int(r["failure_subscriptions"]),
                "srate": num(r["success_rate"]), "frate": num(r["failure_rate"]),
                "other": int(r["other_outcome_records"]), "note": r["population_note"],
            })
    controls = json.loads((PROCESSED / "controls.json").read_text(encoding="utf-8"))
    totals = [sum(c[i] for c in cube) for i in (4, 5, 6)]
    expected = [controls["all"][k] for k in ("records", "subscriptions", "recorded_contacts")]
    if totals != expected:
        raise SystemExit(f"cube totals {totals} do not reconcile to controls {expected}")
    return {"cube": cube, "matched": matched, "controls": controls}


BODY = r"""
<div class="controls" aria-label="Report filters">
  <div class="control"><span>CHANNEL</span><div class="seg" id="f-channel"></div></div>
  <div class="control"><label for="f-month"><span class="eyebrow">MONTH (YEARS POOLED)</span></label><select id="f-month"></select></div>
</div>
<section class="overview" id="overview">
  <div class="headline">
    <div class="eyebrow"><span class="num">01</span>THE SELECTION STORY</div>
    <h1>High rates.<br><span>Small, selected groups.</span></h1>
    <p class="standfirst">Records with a previous success convert far more often, but they are a small, self-selected group. Their rate describes who they are; it doesn't estimate what another contact would achieve.</p>
    <div class="big-label">SUBSCRIPTION RATE <span id="scope-label"></span></div>
    <div class="big" id="k-rate">—</div>
    <div class="context"><span class="pill" id="k-subs">—</span><span>subscriptions among <b id="k-rec">—</b> records</span></div>
    <div class="kpis">
      <div><span>RECORDED CONTACTS</span><strong id="k-contacts">—</strong><small id="k-cpr"></small></div>
      <div><span>SUBSCRIPTIONS PER 100 CONTACTS</span><strong id="k-p100">—</strong><small>output per unit of workload</small></div>
      <div><span>PRIOR-SUCCESS RECORDS</span><strong id="k-ps">—</strong><small id="k-ps-n"></small></div>
      <div><span>SIX OR MORE CONTACTS</span><strong id="k-six">—</strong><small id="k-six-n"></small></div>
    </div>
  </div>
  <section class="card" aria-labelledby="cmp-title">
    <div class="card-head"><div><div class="eyebrow">SAME MONTH AND CHANNEL / 20 OBSERVED CELLS</div><h2 id="cmp-title">Prior success versus prior failure</h2></div></div>
    <div class="legend"><span><i style="background:var(--orange)"></i>Prior success rate</span><span><i style="background:var(--prior)"></i>Prior failure rate</span><span>Select a row to see its counts</span></div>
    <div id="cmp" class="chart"></div>
    <div class="detail" aria-live="polite"><span>Cell <b id="d-cell">—</b></span><span>Prior success <b id="d-s">—</b></span><span>Prior failure <b id="d-f">—</b></span><span>Other outcomes <b id="d-o">—</b></span></div>
    <p class="note" id="d-note"></p>
  </section>
</section>
<section id="groups">
  <div class="section-intro"><div><div class="eyebrow"><span class="num">02</span>RATE VERSUS WORKLOAD</div><h2>Who converts, and what it costs in contacts</h2></div>
  <div class="control"><span>SIZE BARS BY</span><div class="seg" id="f-measure"></div></div></div>
  <div class="panels">
    <section class="panel"><div class="panel-title"><h3>Previous outcome</h3><span id="u1"></span></div><div id="b-outcome"></div></section>
    <section class="panel"><div class="panel-title"><h3>Contacts in this campaign</h3><span id="u2"></span></div><div id="b-band"></div></section>
  </div>
  <p class="note">Contact count is the final count for each record. Unsuccessful records can keep receiving attempts, so a falling rate with more contacts doesn't show that stopping earlier would improve results.</p>
</section>
<section class="decision" id="decision" style="margin-top:28px"><div class="decision-index">03<span>THE NEXT CHECK</span></div>
  <div><h2>Test one standardized follow-up, prospectively.</h2><p>The gap holds within every observed month and channel, which makes it worth investigating. A randomized trial that offers one extra follow-up after an unsuccessful first contact, measured over 30 days with a workload guardrail, would show whether follow-up changes outcomes.</p></div>
  <div class="decision-note">A proposed experiment.<br><b>No trial has run, and no lift is claimed.</b></div></section>
<nav class="links" aria-label="Project links"><a href="https://github.com/ZakJRademacher/marketing-campaign-performance">Project repository</a><a href="https://github.com/ZakJRademacher/marketing-campaign-performance/blob/main/docs/OUTCOME_COMPARISON.md">Outcome comparison</a><a href="https://github.com/ZakJRademacher/marketing-campaign-performance/blob/main/docs/EXPERIMENT_PROPOSAL.md">Experiment proposal</a><a href="https://github.com/ZakJRademacher/marketing-campaign-performance/raw/main/deliverables/Marketing%20Campaign%20Review.pbix">Power BI report (.pbix)</a></nav>
<footer><span id="foot-totals"></span><span>Independent portfolio analysis of historical public data</span>
<p>Source: Moro, Cortez &amp; Rita (2014), UCI Bank Marketing dataset, DOI 10.24432/C5K306, CC BY 4.0; adapted into grouped reporting tables. Full attribution is in <a href="https://github.com/ZakJRademacher/marketing-campaign-performance/blob/main/docs/SOURCES.md">docs/SOURCES.md</a>. Month names pool years because the file has no year column. The source has no durable client ID or contact-by-contact history, so no causal effect, targeting rule or ROI is inferred. Figures are computed in the browser from the project's published tables and reconcile to its control totals.</p></footer>
"""

SCRIPT = r"""
const MONTH_ORDER=['mar','apr','may','jun','jul','aug','sep','oct','nov','dec'];
const MLABEL={mar:'Mar',apr:'Apr',may:'May',jun:'Jun',jul:'Jul',aug:'Aug',sep:'Sep',oct:'Oct',nov:'Nov',dec:'Dec'};
const OLABEL={success:'Previous success',failure:'Previous failure',nonexistent:'No previous campaign'};
const cube=DATA.cube.map(([m,c,o,b,r,s,n])=>({m,c,o,b,r,s,n}));
const state={channel:'all',month:'all',measure:'rate',cell:'may|cellular'};
const inScope=x=>(state.channel==='all'||x.c===state.channel)&&(state.month==='all'||x.m===state.month);
const sum=rows=>rows.reduce((a,x)=>(a.r+=x.r,a.s+=x.s,a.n+=x.n,a),{r:0,s:0,n:0});
function group(rows,key){const g=new Map();for(const x of rows){const a=g.get(x[key])||{key:x[key],r:0,s:0,n:0};a.r+=x.r;a.s+=x.s;a.n+=x.n;g.set(x[key],a);}return[...g.values()];}
function scopeName(){return(state.channel==='all'?'All channels':state.channel[0].toUpperCase()+state.channel.slice(1))+(state.month==='all'?', all months':', '+MLABEL[state.month]);}
const sel=$('f-month');sel.innerHTML='<option value="all">All months</option>'+MONTH_ORDER.map(m=>`<option value="${m}">${MLABEL[m]}</option>`).join('');
sel.addEventListener('change',()=>{state.month=sel.value;syncCell();render();});
function syncCell(){const ok=DATA.matched.filter(r=>(state.channel==='all'||r.channel===state.channel)&&(state.month==='all'||r.month===state.month));if(ok.length&&!ok.some(r=>r.month+'|'+r.channel===state.cell))state.cell=ok[0].month+'|'+ok[0].channel;}
function kpis(){
  const rows=cube.filter(inScope),t=sum(rows);
  $('scope-label').textContent=scopeName();$('k-rate').textContent=pct(t.r?t.s/t.r:null);$('k-subs').textContent=int(t.s);$('k-rec').textContent=int(t.r);
  $('k-contacts').textContent=int(t.n);$('k-cpr').textContent=t.r?(t.n/t.r).toFixed(2)+' per record':'';$('k-p100').textContent=t.n?(100*t.s/t.n).toFixed(1):'—';
  const ps=sum(rows.filter(x=>x.o==='success'));$('k-ps').textContent=pct(ps.r?ps.s/ps.r:null);$('k-ps-n').textContent=`${int(ps.s)} of ${int(ps.r)} · ${pct(t.r?ps.r/t.r:null)} of records`;
  const six=sum(rows.filter(x=>x.b.startsWith('05')));$('k-six').textContent=pct(six.r?six.s/six.r:null);$('k-six-n').textContent=`${int(six.s)} of ${int(six.r)} · ${int(six.n)} contacts`;
}
function comparison(){
  const rows=[...DATA.matched].sort((a,b)=>a.order-b.order||a.channel.localeCompare(b.channel));
  const W=720,rowH=24,T=26,L=118,R=56,H=T+rows.length*rowH+30,x=v=>L+v*(W-L-R);
  let s=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Subscription rates for prior-success and prior-failure records in each of 20 month and channel cells">`;
  for(let k=0;k<=4;k++){s+=`<line class="grid-line" x1="${x(k/4)}" x2="${x(k/4)}" y1="${T-8}" y2="${H-26}"/><text class="axis" x="${x(k/4)}" y="${H-8}" text-anchor="middle">${k*25}%</text>`;}
  rows.forEach((r,i)=>{const y=T+i*rowH+rowH/2,id=r.month+'|'+r.channel,inFilter=(state.channel==='all'||r.channel===state.channel)&&(state.month==='all'||r.month===state.month),on=id===state.cell;
    const small=r.sr<100||r.fr<100;
    s+=`<g class="bar-mark${inFilter?'':' dim'}" data-id="${id}" tabindex="0" role="button" aria-label="${MLABEL[r.month]} ${r.channel}: prior success ${pct(r.srate)}, prior failure ${pct(r.frate)}">`;
    if(on)s+=`<rect x="4" y="${y-rowH/2+1}" width="${W-8}" height="${rowH-2}" rx="6" fill="var(--soft)"/>`;
    s+=`<text class="axis" x="${L-14}" y="${y+4}" text-anchor="end" ${on?'style="fill:var(--ink)"':''}>${MLABEL[r.month]} · ${r.channel}</text>`;
    if(r.srate!=null&&r.frate!=null)s+=`<line x1="${x(r.frate)}" x2="${x(r.srate)}" y1="${y}" y2="${y}" stroke="var(--line)" stroke-width="4" stroke-linecap="round"/>`;
    if(r.frate!=null)s+=`<circle cx="${x(r.frate)}" cy="${y}" r="5.5" fill="var(--prior)"/>`;
    if(r.srate!=null)s+=`<circle cx="${x(r.srate)}" cy="${y}" r="6.5" fill="${small?'var(--card)':'var(--orange)'}" stroke="var(--orange)" stroke-width="2.5"/>`;
    s+=`<rect x="0" y="${y-rowH/2}" width="${W}" height="${rowH}" fill="transparent"/></g>`;});
  $('cmp').innerHTML=s+'</svg>';
  $('cmp').querySelectorAll('[data-id]').forEach(g=>{const pick=()=>{state.cell=g.dataset.id;comparison();};g.addEventListener('click',pick);g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();pick();}});});
  const c=DATA.matched.find(r=>r.month+'|'+r.channel===state.cell);
  $('d-cell').textContent=MLABEL[c.month]+' · '+c.channel;$('d-s').textContent=`${int(c.ss)}/${int(c.sr)} (${pct(c.srate)})`;$('d-f').textContent=`${int(c.fs)}/${int(c.fr)} (${pct(c.frate)})`;$('d-o').textContent=int(c.other)+' records';
  $('d-note').textContent=c.note+'. Hollow markers have fewer than 100 prior-success or prior-failure records. Years are pooled.';
}
function panels(){
  const rows=cube.filter(inScope),byRate=state.measure==='rate';
  const unit=byRate?'SUBSCRIPTION RATE':'RECORDED CONTACTS';$('u1').textContent=unit;$('u2').textContent=unit;
  const opt={value:r=>byRate?(r.r?r.s/r.r:0):r.n,max:byRate?1:undefined,right:r=>byRate?pct(r.r?r.s/r.r:null):int(r.n),cls:r=>byRate?'alt':'',meta:r=>`${int(r.s)} of ${int(r.r)} records · ${int(r.n)} contacts · ${(r.n?100*r.s/r.n:0).toFixed(1)} per 100 contacts`};
  const outs=group(rows,'o').sort((a,b)=>['success','failure','nonexistent'].indexOf(a.key)-['success','failure','nonexistent'].indexOf(b.key));
  $('b-outcome').innerHTML=bars(outs,{...opt,label:r=>OLABEL[r.key]||r.key});
  $('b-band').innerHTML=bars(group(rows,'b').sort((a,b)=>a.key.localeCompare(b.key)),{...opt,label:r=>r.key.slice(4)});
}
function render(){kpis();comparison();panels();}
seg('f-channel',[['all','All'],['cellular','Cellular'],['telephone','Telephone']],state.channel,v=>{state.channel=v;syncCell();render();});
seg('f-measure',[['rate','Subscription rate'],['contacts','Contacts']],state.measure,v=>{state.measure=v;panels();});
const ct=DATA.controls.all;$('foot-totals').textContent=`${int(ct.records)} campaign records · ${int(ct.subscriptions)} subscriptions · ${int(ct.recorded_contacts)} recorded contacts`;
render();watchSections(['overview','groups','decision']);
"""


def main() -> None:
    data = load()
    html_text = page(
        url="https://zakjrademacher.github.io/marketing-campaign-performance/report/",
        image="https://zakjrademacher.github.io/marketing-campaign-performance/deliverables/portfolio-cover-wide.png",
        title="Marketing Campaign Review",
        description="Interactive review of bank marketing outcomes: selected high-rate groups, matched month and channel comparisons, and contact workload.",
        rail_name="Campaign<br>Review",
        nav=[("overview", "Overview"), ("groups", "Rate vs workload"), ("decision", "Next check")],
        window_label="OBSERVATIONS",
        window_value="<strong>41,188 records</strong>Mar–Dec, years pooled",
        credit="HISTORICAL REVIEW<br>Portuguese bank campaigns<br>Zak Rademacher",
        identity="MARKETING / CAMPAIGN REVIEW",
        period="2008–2010 SOURCE <span>/</span> HISTORICAL PUBLIC DATA",
        body=BODY,
        data=data,
        script=SCRIPT,
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html_text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(html_text):,} bytes)")


if __name__ == "__main__":
    main()
