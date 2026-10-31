"""Create focused native PBIP reports beside the original portfolio versions."""
from pathlib import Path
import copy,csv,hashlib,json,shutil,sqlite3

ROOT=Path(__file__).resolve().parent
BASE='https://developer.microsoft.com/json-schemas/fabric/item/report/definition/'
PAPER,WHITE,INK,MUTED,TEAL,CORAL,GOLD='#F6F5F0','#FFFFFF','#203B43','#61777D','#147D80','#BE5D50','#BA852D'

def put(path,value):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
def lit(v):return {'expr':{'Literal':{'Value':str(v).lower() if isinstance(v,bool) else str(v)+'D' if isinstance(v,(int,float)) else "'"+v.replace("'","''")+"'"}}}
def color(v):return {'solid':{'color':lit(v)}}
def field(table,name,measure=False):return {'field':{'Measure' if measure else 'Column':{'Expression':{'SourceRef':{'Entity':table}},'Property':name}},'queryRef':table+'.'+name,'nativeQueryRef':name}

class Report:
    def __init__(self,root,name):
        self.root,self.name=root,name;self.report=root/(name+'.Report');self.model=root/(name+'.SemanticModel')
        original=json.loads((ROOT/'report-template.json').read_text())
        original['themeCollection']['customTheme']['name']='Fieldnotes'
        original['resourcePackages'][1]['items']=[{'name':'Fieldnotes','path':'Fieldnotes.json','type':'CustomTheme'}]
        put(self.report/'definition/report.json',original)
        put(self.report/'StaticResources/RegisteredResources/Fieldnotes.json',{'name':'Fieldnotes / Decision reports','dataColors':[TEAL,CORAL,GOLD,'#667C91','#9BAEAA'],'background':WHITE,'foreground':INK,'tableAccent':TEAL,'textClasses':{'title':{'fontFace':'Segoe UI Semibold','fontSize':13,'color':INK},'label':{'fontFace':'Segoe UI','fontSize':11,'color':MUTED},'callout':{'fontFace':'Segoe UI','color':INK}}})
        put(self.root/(name+'.pbip'),{'version':'1.0','artifacts':[{'report':{'path':name+'.Report'}}]})
        put(self.report/'definition.pbir',{'$schema':'https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json','version':'4.0','datasetReference':{'byPath':{'path':'../'+name+'.SemanticModel'}}})
        put(self.report/'definition/version.json',{'$schema':BASE+'versionMetadata/1.0.0/schema.json','version':'2.0.0'})
        put(self.model/'definition.pbism',{'version':'1.0'});self.pages=[]
    def page(self,key,title):
        self.pages.append(key)
        put(self.report/f'definition/pages/{key}/page.json',{'$schema':BASE+'page/2.0.0/schema.json','name':key,'displayName':title,'displayOption':'FitToPage','height':1000,'width':1440,'objects':{'background':[{'properties':{'color':color(PAPER),'transparency':lit(0)}}]}})
        put(self.report/'definition/pages/pages.json',{'$schema':BASE+'pagesMetadata/1.0.0/schema.json','pageOrder':self.pages,'activePageName':self.pages[0]})
    def visual(self,page,key,kind,pos,title='',roles=None,objects=None,sort=None,bg=WHITE):
        v={'visualType':kind,'drillFilterOtherVisuals':True,'visualContainerObjects':{'background':[{'properties':{'show':lit(True),'color':color(bg),'transparency':lit(0)}}],'border':[{'properties':{'show':lit(False)}}],'title':[{'properties':{'show':lit(bool(title)),'text':lit(title),'fontColor':color(INK),'fontSize':lit(13),'fontFamily':lit('Segoe UI Semibold')}}]}}
        if roles:v['query']={'queryState':{role:{'projections':[field(*f) for f in fields]} for role,fields in roles.items()}}
        if sort:v['query']['sortDefinition']={'sort':[{'field':field(*sort[:3])['field'],'direction':sort[3]}],'isDefaultSort':False}
        if objects:v['objects']=objects
        x,y,w,h=pos
        put(self.report/f'definition/pages/{page}/visuals/{key}/visual.json',{'$schema':BASE+'visualContainer/2.0.0/schema.json','name':key,'position':{'x':x,'y':y,'width':w,'height':h,'z':0,'tabOrder':int(y*10+x)},'visual':v})
    def text(self,page,key,text,pos,size=12,ink=MUTED,bg=PAPER):
        self.visual(page,key,'textbox',pos,objects={'general':[{'properties':{'paragraphs':[{'textRuns':[{'value':part,'textStyle':{'fontFamily':'Segoe UI','fontSize':str(size)+'pt','color':ink}}]} for part in text.split('\n')]}}]},bg=bg)
    def card(self,page,key,table,measure,title,pos,precision=0):
        self.visual(page,key,'card',pos,title,{'Values':[(table,measure,True)]},{'labels':[{'properties':{'color':color(INK),'fontSize':lit(30),'labelDisplayUnits':lit(1),'precision':lit(precision)}}],'categoryLabels':[{'properties':{'show':lit(False)}}]})
    def slicer(self,page,key,table,column,title,pos):
        self.visual(page,key,'slicer',pos,title,{'Values':[(table,column)]},{'data':[{'properties':{'mode':lit('Dropdown')}}],'header':[{'properties':{'show':lit(False)}}],'items':[{'properties':{'fontColor':color(INK),'background':color(WHITE),'textSize':lit(11)}}],'selection':[{'properties':{'singleSelect':lit(False),'selectAllCheckboxEnabled':lit(True)}}]})
    def chart(self,page,key,table,category,measure,title,pos,extra=(),rate=False):
        o={'categoryAxis':[{'properties':{'labelColor':color(MUTED),'fontSize':lit(11),'showAxisTitle':lit(False)}}],'valueAxis':[{'properties':{'labelColor':color(MUTED),'fontSize':lit(10),'showAxisTitle':lit(False),'gridlineColor':color('#E3E8E5'),'labelDisplayUnits':lit(1)}}],'legend':[{'properties':{'show':lit(False)}}],'labels':[{'properties':{'show':lit(True),'color':color(INK),'fontSize':lit(10),'labelDisplayUnits':lit(1),'labelPrecision':lit(1 if rate else 0)}}],'dataPoint':[{'properties':{'defaultColor':color(CORAL if rate else TEAL)}}]}
        roles={'Category':[(table,category)],'Y':[(table,measure,True)]}
        if extra:roles['Tooltips']=[(table,m,True) for m in extra]
        self.visual(page,key,'clusteredBarChart',pos,title,roles,o,(table,measure,True,'Descending'))
    def table(self,page,key,columns,title,pos):self.visual(page,key,'tableEx',pos,title,{'Values':columns},{'grid':[{'properties':{'gridVertical':lit(False),'gridHorizontal':lit(True),'rowPadding':lit(5),'textSize':lit(11)}}],'columnHeaders':[{'properties':{'fontColor':color(INK),'backColor':color('#EDF1ED'),'fontSize':lit(11)}}],'values':[{'properties':{'fontColorPrimary':color(INK),'backColorPrimary':color(WHITE),'fontSize':lit(11)}}]})
    def model_file(self,model):put(self.model/'model.bim',model)