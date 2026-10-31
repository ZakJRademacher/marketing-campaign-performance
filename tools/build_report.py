"""Build the editable Power BI project from validated reporting CSVs."""
from pathlib import Path
import json
from report_builder import Report,field,put,INK,MUTED,TEAL

P=Path(__file__).resolve().parents[1]

def build():
    r=Report(P/'powerbi','CampaignReview')
    specs={'Campaigns':[('Source Row','int64'),('Month','string'),('Month Order','int64'),('Channel','string'),('Previous Outcome','string'),('Contacts','int64'),('Contact Band','string'),('Subscribed','int64')], 'Months':[('Month','string'),('Month Order','int64')], 'Channels':[('Channel','string')], 'Outcomes':[('Previous Outcome','string')], 'ContactBands':[('Contact Band','string')]}
    tables=[]
    for name,columns in specs.items():
        cols=[{'name':c,'dataType':t,'sourceColumn':c,'summarizeBy':'none'} for c,t in columns]
        if name=='Months':cols[0]['sortByColumn']='Month Order'
        convert=', '.join('{"'+c+'", '+('Int64.Type' if t=='int64' else 'type text')+'}' for c,t in columns)
        expression=['let',f' Source = Csv.Document(File.Contents(DataFolder & "/{name}.csv"),[Delimiter=",",Encoding=65001,QuoteStyle=QuoteStyle.Csv]),',' Headers = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),',f' Typed = Table.TransformColumnTypes(Headers, {{{convert}}}, "en-US")','in',' Typed']
        tables.append({'name':name,'columns':cols,'partitions':[{'name':name,'mode':'import','source':{'type':'m','expression':expression}}]})
    measures=[('Records',"COUNTROWS('Campaigns')",'#,0'),('Subscriptions',"SUM('Campaigns'[Subscribed])",'#,0'),('Subscription Rate','DIVIDE([Subscriptions],[Records])','0.0%'),('Recorded Contacts',"SUM('Campaigns'[Contacts])",'#,0'),('Contacts per Record','DIVIDE([Recorded Contacts],[Records])','0.00'),('Subscriptions per 100 Contacts','100 * DIVIDE([Subscriptions],[Recorded Contacts])','0.00'),('Group Size','IF([Records] < 100, "Small sample: N < 100", "N >= 100; descriptive comparison")',''),('Selection Finding','VAR N=[Records] RETURN IF(ISBLANK(N), "No records match this selection.", FORMAT(N,"#,0") & " records; " & FORMAT([Subscriptions],"#,0") & " subscriptions (" & FORMAT([Subscription Rate],"0.0%") & "). Recorded contacts: " & FORMAT([Recorded Contacts],"#,0") & ". Compare like months and channels before choosing a trial.")','')]
    tables[0]['measures']=[{'name':n,'expression':e,'formatString':fmt} for n,e,fmt in measures]
    rels=[]
    for dim,col in [('Months','Month'),('Channels','Channel'),('Outcomes','Previous Outcome'),('ContactBands','Contact Band')]:
        rels.append({'name':'Campaigns_'+dim,'fromTable':'Campaigns','fromColumn':col,'toTable':dim,'toColumn':col,'fromCardinality':'many','toCardinality':'one','crossFilteringBehavior':'oneDirection'})
    r.model_file({'name':'CampaignReview','compatibilityLevel':1600,'model':{'culture':'en-US','defaultPowerBIDataSourceVersion':'powerBI_V3','expressions':[{'name':'DataFolder','kind':'m','expression':'"'+(P/'data/processed').as_posix()+'" meta [IsParameterQuery=true,Type="Text",IsParameterQueryRequired=true]'}],'tables':tables,'relationships':rels}})
    def filters(page):
        for i,(t,c,title) in enumerate([('Months','Month','Observed month of year'),('Channels','Channel','Contact channel'),('Outcomes','Previous Outcome','Previous campaign outcome')]):r.slicer(page,'filter'+str(i),t,c,title,(24+i*472,150,448,68))
    def chart(page,key,dim,col,measure,title,pos,rate=False):
        r.chart(page,key,dim,col,measure,title,pos,extra=('Records','Subscriptions','Recorded Contacts','Group Size'),rate=rate)
        p=r.report/f'definition/pages/{page}/visuals/{key}/visual.json';v=json.loads(p.read_text());q=v['visual']['query'];q['queryState']['Y']['projections']=[field('Campaigns',measure,True)];q['queryState']['Tooltips']['projections']=[field('Campaigns',m,True) for m in ['Records','Subscriptions','Recorded Contacts','Group Size']];q['sortDefinition']['sort'][0]['field']=field('Campaigns',measure,True)['field'];put(p,v)
    r.page('decision','01  Campaign review')
    r.text('decision','eyebrow','FIELDNOTES / MARKETING OPERATIONS',(24,10,1392,28),10,TEAL)
    r.text('decision','title','Where should the next follow-up experiment focus?',(24,44,1392,58),26,INK)
    r.text('decision','sub','Compare observed subscriptions with contact workload. Historical records are not a randomized contact experiment.',(24,107,1392,36),12)
    filters('decision')
    for i,(m,title,prec) in enumerate([('Records','Campaign records',0),('Subscriptions','Subscriptions',0),('Subscription Rate','Observed subscription rate',1),('Recorded Contacts','Recorded campaign contacts',0)]):r.card('decision','kpi'+str(i),'Campaigns',m,title,(24+i*354,238,330,112),prec)
    chart('decision','outcomes','Outcomes','Previous Outcome','Subscription Rate','01  Prior outcome and subscription rate',(24,370,680,290),True)
    chart('decision','workload','ContactBands','Contact Band','Recorded Contacts','02  Contact workload by final contact count',(728,370,688,290))
    r.visual('decision','finding','multiRowCard',(24,682,1392,90),roles={'Values':[('Campaigns','Selection Finding',True)]})
    r.text('decision','action','NEXT ACTION / Test a follow-up protocol within comparable month and channel groups. Track subscription rate and contacts per record in randomized groups. Success-history records are an investigation lead, not proof of a treatment effect.',(24,793,1392,95),13,INK)
    r.text('decision','footer','UCI Bank Marketing / Moro et al. / CC BY 4.0 / 41,188 historical records / No cost or ROI claim / Zak Rademacher',(24,946,1392,38),10)
    r.page('investigation','02  Compare like groups')
    r.text('investigation','title','Does the pattern hold within the same channel and month?',(24,28,1392,65),25,INK)
    r.text('investigation','sub','Filters on this page are independent. Use the same selections to compare pages. Months pool observations across source years.',(24,104,1392,38),12)
    filters('investigation')
    chart('investigation','bands','ContactBands','Contact Band','Subscription Rate','Subscription rate by final contact-count band',(24,246,680,330),True)
    r.table('investigation','evidence',[('Outcomes','Previous Outcome'),('Campaigns','Records',True),('Campaigns','Subscriptions',True),('Campaigns','Subscription Rate',True),('Campaigns','Contacts per Record',True),('Campaigns','Group Size',True)],'Previous-outcome evidence in this selection',(728,246,688,330))
    r.text('investigation','definitions','READ THE MEASURES\nOne record is one source client-campaign observation, not a phone-call event. Recorded contacts sum campaign contact counts, including the last contact. Rates divide observed subscriptions by records in the same selection. Source row numbers provide lineage, not reusable customer identities.\n\nWHY THIS IS NOT A STOPPING RULE\nNonresponders may receive more attempts; final contact count is partly a result of the process. Call duration is post-contact and excluded. The source lacks costs and a randomized untreated group. Do not infer ROI, incremental lift or a causal effect of contact frequency.',(24,604,1392,240),14,INK)
    r.text('investigation','small','SMALL GROUPS / Counts below 100 are flagged in tooltips and the table. This display convention is not a statistical significance test. Unknown and nonexistent prior outcomes remain separate observed categories.',(24,860,1392,90),12)
    print(P/'powerbi/CampaignReview.pbip')

if __name__=='__main__':build()
