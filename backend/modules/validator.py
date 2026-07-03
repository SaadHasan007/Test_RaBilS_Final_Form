import re
import spacy
from nltk.corpus import wordnet as wn ,stopwords
import numpy as np
import torch
from sentence_transformers import SentenceTransformer, util
import pickle
from modules.nlp import parse_user_story

# rule based ambiguity detection using framework suggested in research papers
nlp = spacy.load("en_core_web_sm") #English nlp model
embedding_model = SentenceTransformer('models/all-MiniLM-L6-v2') #pre-trained AI model that understands sentence meaning
dataset_embeddings = torch.load("models/userstory_dataset_embeddings.pt") # Embed all stories (text,text,..) to [[0.3 ,0.34, 0.67],[0.3 ,0.34, 0.67]..]

VAGUE_WORDS = ['reliable-delivery', 'quick-payment', 'suitable-response', 'high-usability', 'responsive-layout', 'expected', 'robust', 'smooth-processing', 'appropriate-interface', 'low-complexity', 'rapid-processing', 'reliable', 'efficient-process', 'reasonable-security', 'powerful-control', 'optimized-navigation', 'excellent', 'improved', 'modern-layout', 'clear-navigation', 'high-risk', 'huge', 'specific', 'optimized-processing', 'many-options', 'professional-workflow', 'clean-validation', 'poor', 'automatic', 'safe-delivery', 'improved-security', 'minimal-processing', 'low-accuracy', 'various', 'safe-transactions', 'useful-monitoring', 'intelligent-monitoring', 'secure-access', 'flexible-validation', 'clean-layout', 'sufficient-security', 'future-proof', 'responsive-validation', 'convenient-search', 'proper-integration', 'convenient-reporting', 'reasonable-usage', 'clear-reporting', 'scalable-storage', 'shortly', 'maximum-efficiency', 'efficient-validation', 'minimal-errors', 'seamless', 'accessible', 'relevant-content', 'some', 'several', 'low-delay', 'powerful-security', 'reasonable-load', 'clean-monitoring', 'critical', 'appropriate-timeframe', 'complicated', 'reasonable-limit', 'dynamic-interface', 'meaningful-message', 'satisfactory-performance', 'quick-results', 'improved-response', 'helpful', 'efficient-reporting', 'good', 'relevant', 'acceptable-speed', 'modern-validation', 'smooth-operation', 'secure-storage', 'high-volume', 'flexible-workflow', 'seamless-processing', 'reasonable-size', 'relevant-monitoring', 'minimal-input', 'dynamic', 'minimal-delay', 'meaningful-notifications', 'best-in-class', 'simple-management', 'cutting-edge', 'clean', 'consistent', 'fast-navigation', 'robust-storage', 'improved-accessibility', 'instant-response', 'acceptable-availability', 'normal-behavior', 'reliable-storage', 'reliable-search', 'normal', 'effective-reporting', 'safely', 'proper-validation', 'advanced-validation', 'minimal-clicks', 'major', 'modern', 'interactive', 'partially-complete', 'intelligent-routing', 'normally', 'complete', 'stable-connection', 'sufficient-storage', 'responsive-navigation', 'intelligent', 'fast-loading', 'appropriate-format', 'rapid-verification', 'responsive', 'quick-access', 'friendly-navigation', 'enhanced', 'fast', 'secure-processing', 'secure', 'simple-process', 'state-of-the-art', 'desired-state', 'safe-navigation', 'adequate-security', 'friendly-interface', 'safe-validation', 'advanced-monitoring', 'recommended', 'easy-processing', 'friendly-monitoring', 'improved-experience', 'properly', 'professional-layout', 'meaningful-validation', 'better-visibility', 'flexible-layout', 'well-structured', 'intelligent-reporting', 'generic', 'suitable-integration', 'friendly-search', 'advanced-filtering', 'optimized-layout', 'complex', 'fault-tolerant', 'easy-registration', 'fast-monitoring', 'modern-workflow', 'sufficient-performance', 'professional-navigation', 'useful-alerts', 'feature-rich', 'low-speed', 'flexible-navigation', 'reasonable-quality', 'convenient', 'effective-navigation', 'smart-alerts', 'dynamic-content', 'acceptable-limit', 'appropriate-layout', 'safe-processing', 'timely', 'customized', 'high-priority', 'adaptable', 'optimized-access', 'adequate-visibility', 'easy-login', 'accurately', 'better-search', 'useful-validation', 'multiple', 'high-performance', 'optimized-interface', 'easily', 'intelligently', 'secure-validation', 'accurate', 'appropriate-speed', 'reliable-notifications', 'responsive-search', 'reasonable-retry', 'adequate-support', 'portable', 'strong-security', 'satisfactory-result', 'instant-loading', 'manual', 'optimized-experience', 'adequate', 'dynamically', 'safe-handling', 'proper-security', 'best-practice', 'enhanced-performance', 'robust-reporting', 'simple', 'friendly', 'sometimes', 'structured', 'higher', 'enhanced-accessibility', 'rapid-search', 'advanced', 'high-efficiency', 'smooth-loading', 'fully', 'scalable-monitoring', 'manageable', 'flexible', 'prioritized', 'easy-workflow', 'efficient-workflow', 'sufficient-monitoring', 'instant-update', 'suitable', 'proper-handling', 'easy-control', 'smart-search', 'clear-message', 'slowly', 'future-ready', 'significant-delay', 'reasonable-time', 'adequate-validation', 'stable-navigation', 'intelligent-alerts', 'convenient-validation', 'reliable-monitoring', 'effective-process', 'improved-workflow', 'professional-interface', 'advanced-features', 'friendly-processing', 'efficient', 'advanced-control', 'high-speed', 'industry-standard', 'engaging', 'acceptable-interface', 'automatically', 'perfect', 'convenient-checkout', 'production-ready', 'minimal-design', 'few', 'small', 'dynamic-behavior', 'efficient-routing', 'mission-critical', 'optimized', 'heavy-duty', 'quick-verification', 'clear-view', 'smart-validation', 'timely-response', 'advanced-security', 'advanced-search', 'improved-layout', 'high-load', 'powerful-validation', 'convenient-processing', 'appropriate-security', 'advanced-reporting', 'productive', 'robust-validation', 'instant-access', 'highly-available', 'bad', 'appropriate-content', 'appropriate-action', 'seamless-transition', 'large', 'stable', 'fast-validation', 'easy-management', 'meaningful-insights', 'quick-loading', 'acceptable-workflow', 'powerful-filtering', 'smart-filtering', 'rapid-access', 'seamless-workflow', 'trustworthy', 'easy', 'effective-processing', 'smart-routing', 'easy-configuration', 'robust-security', 'preferred', 'better-experience', 'sufficiently', 'better-system', 'recent', 'better-navigation', 'clean-navigation', 'correct-behavior', 'flexible-processing', 'organized', 'simple-navigation', 'stable-interface', 'smartly', 'timely-validation', 'smart-processing', 'reliable-processing', 'stable-system', 'minimal', 'scalable-processing', 'improved-navigation', 'quickly', 'improve', 'enhanced-visibility', 'flexible-reporting', 'reasonable', 'low-latency', 'low-resource', 'rapid-navigation', 'meaningful-reporting', 'sufficient-data', 'minimal-wait', 'professional', 'appropriate', 'business-critical', 'dynamic-navigation', 'useful-reporting', 'useful', 'reasonable-amount', 'next-generation', 'safe-storage', 'efficiently', 'irrelevant', 'transparent', 'robust-access', 'bad-quality', 'convenient-access', 'easy-validation', 'personalized', 'modern-navigation', 'appropriate-time', 'flexible-settings', 'modern-search', 'high-complexity', 'smart-navigation', 'world-class', 'adequately', 'reliable-service', 'partially', 'instant-results', 'useful-results', 'enough', 'desired-results', 'successfully', 'acceptable-quality', 'powerful-monitoring', 'professional-design', 'better-performance', 'simple-access', 'enterprise-grade', 'soon', 'stable-validation', 'easy-access', 'stable-search', 'high-security', 'tiny', 'best', 'reliable-payment', 'enhanced-security', 'scalable-reporting', 'better-processing', 'meaningful-processing', 'acceptable-performance', 'high-visibility', 'powerful', 'robust-processing', 'enhanced-monitoring', 'reasonable-speed', 'minimal-effort', 'acceptable-experience', 'minimal-overhead', 'rapid-response', 'instant-feedback', 'fastest', 'acceptable-delay', 'smooth-search', 'maximum-speed', 'significant', 'low', 'readable', 'better-control', 'maximum', 'safe', 'reasonable-accuracy', 'expected-behavior', 'fast-delivery', 'acceptable', 'timely-update', 'clean-storage', 'acceptable-security', 'powerful-reporting', 'effective-monitoring', 'quick-checkout', 'high-availability', 'scalable-navigation', 'secure-navigation', 'seamless-validation', 'appropriate-response', 'intelligent-search', 'rarely', 'far', 'better', 'unauthorized', 'clean-design', 'scalable', 'optimized-security', 'optimized-query', 'maximum-performance', 'good-quality', 'professional-processing', 'optimized-workflow', 'all', 'high', 'high-accuracy', 'acceptable-result', 'timely-delivery', 'simple-checkout', 'fast-filtering', 'intelligent-processing', 'seamless-navigation', 'effective', 'important', 'effective-validation', 'appropriate-message', 'quality-content', 'optimized-validation', 'better-speed', 'simple-settings', 'clear-layout', 'massive', 'efficient-storage', 'quick-processing', 'meaningful-feedback', 'friendly-validation', 'meaningful-alerts', 'acceptable-usage', 'quick', 'optimized-storage', 'easy-navigation', 'correct', 'adequate-speed', 'appropriate-size', 'useful-notifications', 'improved-monitoring', 'useful-feedback', 'easy-monitoring', 'optimized-search', 'optimized-loading', 'simple-processing', 'smart-recommendation', 'enhanced-navigation', 'effectively', 'user-friendly', 'helpful-message', 'clean-reporting', 'minor', 'seamless-access', 'better-layout', 'often', 'efficient-navigation', 'maintainable', 'appropriate-level', 'sensitive', 'quick-response', 'professional-validation', 'high-scalability', 'responsive-workflow', 'safe-integration', 'proper', 'timely-processing', 'satisfactory', 'incomplete', 'relevant-notifications', 'unexpected-behavior', 'better-security', 'responsive-filtering', 'performant', 'best-effort', 'clear-validation', 'correctly', 'heavy', 'easy-search', 'confidential', 'high-capacity', 'stable-performance', 'proper-monitoring', 'responsive-processing', 'instantly', 'improved-performance', 'rapidly', 'low-risk', 'convenient-management', 'powerful-processing', 'robust-monitoring', 'highly-secure', 'sufficient', 'tailored', 'low-bandwidth', 'securely', 'relevant-insights', 'proper-format', 'responsive-interface', 'clean-processing', 'intuitive', 'many', 'smart', 'easy-to-use', 'certain', 'good-visibility', 'good-monitoring', 'relevant-processing', 'adequate-storage', 'unsafe', 'robust-search', 'cleanly', 'powerful-search', 'sufficient-speed', 'lower', 'quick-validation', 'smart-monitoring', 'suitable-format', 'efficient-loading', 'authorized', 'maximum-security', 'reliable-connection', 'minimal-steps', 'enhancement', 'secure-transactions', 'smoothly', 'occasionally', 'suitable-option', 'secure-payment', 'sufficient-logging', 'fast-reporting', 'dynamic-validation', 'smooth-experience', 'stable-storage', 'secure-connections', 'modern-processing', 'smooth-workflow', 'dynamic-updates', 'high-quality', 'consistently', 'timely-notification', 'easy-interface', 'usable', 'appropriate-data', 'friendly-workflow', 'instant-validation', 'seamless-integration', 'common', 'low-maintenance', 'secure-reporting', 'smooth-validation', 'unusual', 'dynamic-filtering', 'optimized-system', 'enhanced-control', 'stable-processing', 'good-design', 'low-memory', 'simple-validation', 'relevant-feedback', 'clear-interface', 'high-reliability', 'optimized-performance', 'intuitive-interface', 'reasonable-performance', 'reliably', 'advanced-navigation', 'intelligent-validation', 'appropriate-workflow', 'clear-feedback', 'low-effort', 'effective-storage', 'appropriate-access', 'rapid-loading', 'understandable', 'clear-processing', 'reasonable-behavior', 'slow', 'simple-interface', 'real-time', 'clean-interface', 'low-priority', 'friendly-layout', 'advanced-processing', 'acceptable-design', 'smooth-navigation', 'flexible-search', 'lightweight', 'slower', 'near', 'scalable-search', 'optimized-results', 'clearly', 'flexible-filtering', 'appropriate-permissions', 'fast-processing', 'better-monitoring', 'better-usability', 'clear-visibility', 'acceptable-accuracy', 'convenient-navigation', 'sufficient-validation', 'improved-visibility', 'sufficient-capacity', 'safe-access', 'few-clicks', 'great', 'efficient-filtering', 'manageable-workload', 'high-flexibility', 'enhanced-usability', 'incompatible', 'modern-design', 'quick-search', 'clear', 'effective-search', 'relevant-alerts', 'flexibly', 'acceptable-output', 'effective-routing', 'efficient-processing', 'simple-layout', 'adequate-monitoring', 'intelligent-filtering', 'unexpected', 'simply', 'smooth-transition', 'scalable-validation', 'modern-interface', 'compatible', 'seamless-search', 'desired', 'efficient-search', 'adequate-performance', 'meaningful', 'reasonable-workflow', 'good-performance', 'suspicious', 'simple-search', 'timely-alert', 'rapid-validation', 'fast-search', 'trusted', 'timely-action', 'professional-reporting', 'quick-navigation', 'useful-processing', 'reasonable-response', 'low-performance', 'smooth', 'light', 'minimal-time', 'frequently', 'dynamic-layout', 'optimal', 'reliable-system', 'good-experience', 'instant-notification', 'rapid', 'relevant-results', 'reliable-validation', 'immediately', 'usually', 'better-interface', 'predictive', 'meaningful-results', 'low-overhead', 'scalable-workflow']
SAFE_WORDS = ['exchanged','trusted','initiated','previews','remain','resume','pickups','sharing',
'suspended','trends','edited','placements','selection','reflected','adding',
'acknowledge','misuse','spam','coordination','execution','log','arrivals',
'translated','alignment','timing','structure','irregularities','deliver',
'recommended','fee','live','integrate','acknowledgments','transitions',
'started','correspondence','acknowledged','protection','requested','standard',
'launch','registered','accessories','persistent','render','capabilities',
'oversight','responsibility','continues','coverage','screens','transferred',
'revised','expense','funds','peak','selections','operate','reported',
'training','measured','marked','persistence','corrections','fulfill','match',
'connection','indexing','testing','taxonomy','replacements','storage','parallel',
'tools','protected','requesting','destinations','focus','patterns','scoring',
'ranking','budgets','posture','modifications','typing','quality','timely',
'exposure','verify','contains','modify','merge','satisfaction','denied',
'duplicate','resolutions','automation','preparation','distributed','units',
'explanation','stream','communication','demand','task','normalize','inquiries',
'violate','pays','aligns','calculation','offerings','plan','breakdown',
'acceptance','avoid','contribution','register','reconcile','split','enter',
'commitments','decisions','clear','intake','warnings','approach',
'responsibilities','articles','improved','combine','handling','formatting',
'publication','scroll','freeze','input','performed','recovered','sequences',
'recorded','extend','affect','copy','answer','variants','points','point',
'corrected','accesses','stages','obligations','qualified','documented','fees',
'submission','managed','procedures','linked','grouped','specialized','link',
'program','basis','reserved','origin','stops','requires','registration',
'structured','blocking','premium','forecasting','revisions','activation',
'transmit','unresolved','contact','attach','identical','delayed','fail',
'apply','initiate','behavior','base','including','authority','expected',
'exchanges','disposal','devices','consumption','materials','official','trend',
'indicators','produced','implemented','sponsored','stocking','average',
'violations','logic','views','allowed','shipping','charge','classify',
'decision','resolved','critical','answered','place','markets','bundling',
'time','boost','granted','informed','rated','move','ships','guidelines',
'moderation','blocks','issues','unlock','transparent','spelling','containing',
'persists','organized','copies','streaming','partnerships','pricing','used',
'recommendations','prepare','determined','labeling','contacts','questions',
'collect','rounding','selling','usage','distributions','frequent','mistakes',
'suggestions','abandoned','discontinued','settled','redeem','communicate',
'earned','action','stopped','formatted','coordinated','cycles','competition',
'experiences','strengths','validity','transform','filing','separate',
'frequency','visualized','failures','launched','times','titles','correlation',
'arranged','retrieval','protocol','unique','specific','associated','approvals',
'additions','solutions','privilege','structures','push','resetting','returned',
'addressed','landing','differences','chats','bundled','retention','resets',
'delivered','explaining','operates','submissions','abuse','recovery',
'identities','charged','opened','color','sale','errors','dimensions','warning',
'scan','synchronized','integrated','waiting','cancelled','followers',
'supports','terms','offered','enforced','local','performing','accessible',
'journey','referral','reporting','sizes','reserve','monthly','disputes',
'statements','market','guidance','release','retrieve','measures','controls',
'segment','right','reflect','prepared','adoption','advanced','runs',
'provide','appear','constraints','include','backlog','preferred','visibility',
'attacks','money','promote','captures','consolidated','common','accounting',
'making','movements','preserve','models','restricted','balances','breaches',
'aligned','converted','operations','hours','conflicting','offsets','links',
'internal','identity','includes','developed','paths','vary','dispute',
'proceed','declarations','commissions','indicate','format','disputed',
'forms','directed','filings','operating','transparency','ordering',
'instructions','maintains','qualify','speed','start','rotate','ownership',
'complaint','consistent','incorrect','resolves','joined','moderated','define',
'known','determine','effect','altered','weight','error','standardized','find',
'communications','expand','choose','loyalty','blocked','findings','profit',
'movement','exchange','specifications','sets','issued','stage','respond',
'listed','packaging','performs','credits','shipped','fails','insights',
'mandatory','conversions','expired','close','run','begins','localized','lock',
'related','threats','end','keys','benefit','viewed','retrieved','assignment',
'pass','progress','expiring','perform','keep','entries','steps','tiers',
'assessment','approval','issue','recover','reflects','gift','confirmation',
'maintenance','connections','synchronization','rights','messaging','defaults',
'overall','finance','accepted','appears','localize','coordinate','packed',
'stays','rates','target','cost','registrations','read','matched',
'responsible','attempted','reduce','empty','expect','discard','success',
'delays','capacity','maintain','notice','help','declared','missing',
'responding','inquiry','reply','posting','secure','reward','replies','damage',
'streams','call','redemption','followed','authorities','manages','respected',
'job','increases','packing','branding','drop','duty','activated','pause',
'buying','marketing','placed','boosts','occurs','inspected','renewal','limits',
'costs','failure','planned','estimates','actions','modified','unusual','name',
'exemption','declined','actual','resolve','remaining','zone','programs',
'deletion','dynamic','encouraged','refined','planning','text','level',
'reorder','running','engine','route','commission','assessments','volume',
'ordered','editorial','translate','deducted','overrides','placing','drops',
'tests','reservations','destination','handled','investigating','flash',
'limitations','synchronize','launches','change','abnormal','case','risk',
'print','set','revoke','periods','logging','original','daily','connected',
'combined','pay','follows','withdrawal','guide','finished','routing',
'qualifies','signed','sensitive','uses','write','reaches','conflict',
'associate','embedded','clean','tier','captured','matches','capture',
'connects','observed','documentation','persist','replaced','suspend','mark',
'social','business','excluded','schemes','registers','competitive','charts',
'communicated','notes','arrival','segments','completes','length','redeemed',
'conducted','recurring','promoted','experience','variations','measure',
'targets','consider','declaration','subscribed','inactivity','mismatched',
'loss','upgrades','recommendation','manual','preserved','immediate','consume',
'deductions','visualize','expanded','replay','effective','calculations',
'anomalies','installments','block','commerce','lineage','voice','view','site',
'checks','convert','overload','expansion','intelligence','growth','scope',
'delivering','share','audiences','learn','issuing','expiration','savings',
'becomes','trails','closure','suppression','progresses','adjustments',
'attention','shared','engagement','delay','moved','friction','restrict',
'interpret','tracing','traffic','deals','using','broadcast','partial',
'explain','collection','community','confirming','screen','regular',
'prohibited','appropriate','distribute','require','easier','organize',
'understand','applied','certifications','spending','routed','rewards',
'starts','device','implement','aggregated','improvements','complete',
'reconciled','connect','design','adjusted','contain','subscribe','obtain',
'depth','solve','standards','highlight','grouping','behaviors','modification',
'finishes','control','transfer','evidence','external','transfers','inform',
'jobs','navigate','editing','supply','detail','attempts','applying','manage',
'risks','refine','severity','stability','registering','provides','begin',
'tasks','handle','rate','cash','suggested','complaints','dispatched','visits',
'question','cycle','replacement','repeat','navigation','correction',
'reliable','authorized','repeated','demonstrated','comparison','suggest',
'attached','agreements','increase','assist','recognize','plans','analysis',
'established','referrals','needed','placement','affiliate','acceptable',
'limited','withdrawals','returning','churn','damaged','retain','controlled',
'network','activate','balance','required','scale','preview','future','know',
'personalized','answers','changes','trust','formats','sold','calls','transit',
'posted','shopping','tailored','size','list','confirmations','decrease',
'notices','contents','forward','reach','canceled','included','protocols',
'stable','badges','based','select','reminder','single','guides','ends',
'follow','creation','performance','edit','involving','handles','names',
'cancel','detection','seasons','defective','interest','readiness','installment',
'remove','reset','removed','limit','defined','cleared','decline','default',
'collections','safety','credit','ready','consistency','visit','compatible',
'distribution','attempt','historical','adjust','viewing','acquisition',
'balanced','supported','faster','progression','discover','histories',
'alternative','interests','collected','maintained','indicated','locate',
'moderate','chat','respect','lists','browsing','transmitted','explore','stop',
'chosen','portal','assignments','legal','signals','popular','weekly',
'progressing','assessed','impact','initiating','found','picking','sell',
'focused','grant','align','automatic','conversion','decide','recommend',
'continue','traced','suspension','occurred','agreement','currencies',
'association','supporting','starting','inspect','sequence','international',
'bypass','resolution','conditions','breakdowns','matching','intervals',
'customs','incoming','reduced','flagged','operational','lawful','violation',
'gain','ship','taken','clearance','released','sales','duties','levels',
'timers','replace','confidence','charges','click','check','concerns','key',
'votes','fulfilled','benefits','digital','recording','written','requirements',
'presence','retained','picked','laws','period','detailed','happen','confirm',
'reasons','featured','dependent','confirmed','bulk','added','spikes','allows',
'possible','reminders','browse','checked','volumes','provided','mode','high',
'edits','combination','rapid','see', 'urgency', 'expires', 'expire', 'add', 'buy', 'items', 'successful', 'profiler', 'textarea', 'cpu', 'return', 'font', 'disabled', 'saving', 'captcha', 'ascii', 'operator', 'uuids', 'permission', 'private', 'cell', 'server', 'multiclass', 'source', 'checkpoint', 'archives', 'backend', 'crawlers', 'role', 'version', 'router', 'agent', 'encoders', 'directories', 'billing', 'callbacks', 'analyzing', 'create', 'viewport', 'optimizer', 'calculates', 'message', 'yaml', 'shown', 'admin', 'processor', 'handshake', 'attribute', 'taxes', 'domain', 'serializers', 'videos', 'metrics', 'assigning', 'invoiceid', 'histograms', 'icons', 'dropdown', 'toolbars', 'zip', 'inference', 'asset', 'receipts', 'platform', 'configured', 'aggregation', 'domains', 'shows', 'displaying', 'sorted', 'publishers', 'transformer', 'descriptions', 'tooltips', 'mappers', 'price', 'generate', 'priority', 'ports', 'metric', 'loaded', 'language', 'database', 'track', 'objects', 'reports', 'failover', 'rejected', 'reviewing', 'date', 'refreshing', 'index', 'endpoint', 'receipt', 'consumers', 'validates', 'collector', 'snapshots', 'pages', 'feedback', 'interpreter', 'deploymentid', 'platforms', 'regression', 'radio', 'update', 'online', 'scores', 'attachments', 'loads', 'compares', 'cursors', 'subscription', 'roles', 'validating', 'unavailable', 'certificates', 'allocator', 'syntax', 'servers', 'modules', 'comments', 'forecast', 'containers', 'existing', 'total', 'privacy', 'settings', 'moderators', 'registry', 'aggregator', 'popups', 'amounts', 'executors', 'load', 'identified', 'template', 'sent', 'campaigns', 'approves', 'reviewers', 'json', 'bytes', 'snapshot', 'calculated', 'open', 'functions', 'authentication', 'vector', 'folders', 'ssd', 'profilers', 'groups', 'totals', 'processed', 'localhost', 'sources', 'compilers', 'watchdog', 'benchmarks', 'consent', 'promotions', 'detected', 'extractor', 'port', 'validator', 'statuses', 'checkpointing', 'sidebar', 'vendor', 'workflows', 'inventory', 'reference', 'latest', 'quantities', 'data', 'document', 'toolbar', 'cookies', 'request', 'accordion', 'checkboxes', 'synchronizer', 'tracked', 'imported', 'sending', 'parameters', 'switches', 'products', 'states', 'payments', 'jpg', 'mock', 'brands', 'pipeline', 'observer', 'shopper', 'wallets', 'epoch', 'store', 'formatter', 'identifier', 'kernels', 'submit', 'generator', 'authorizers', 'tokenizers', 'item', 'login', 'records', 'tokenizer', 'service', 'parser', 'themes', 'compiler', 'zipcode', 'queues', 'storing', 'module', 'executor', 'function', 'extension', 'channels', 'numbers', 'paymentid', 'tree', 'components', 'registries', 'seller', 'shipments', 'application', 'threads', 'client', 'loader', 'fax', 'csv', 'closed', 'cookie', 'telephone', 'popup', 'normalization', 'classification', 'comparing', 'timezones', 'video', 'grids', 'baseline', 'classifier', 'emulators', 'code', 'libraries', 'xml', 'productid', 'footer', 'shipmentid', 'subscriptions', 'buildid', 'filtering', 'developer', 'connectors', 'pointer', 'challenges', 'builds', 'vendors', 'stylesheet', 'binary', 'scanners', 'hidden', 'option', 'enabled', 'serializer', 'validate', 'scheduling', 'overview', 'artifacts', 'container', 'deleting', 'replicas', 'credential', 'slider', 'details', 'messageid', 'app', 'analyze', 'payout', 'checkbox', 'android', 'displays', 'members', 'gender', 'buyer', 'browser', 'process', 'svg', 'configurations', 'featuremaps', 'histogram', 'postalcode', 'radios', 'playbook', 'marketplace', 'menus', 'translations', 'crawler', 'docker', 'carousels', 'encoder', 'javascript', 'sprites', 'developers', 'cards', 'build', 'filters', 'hook', 'group', 'resources', 'initializer', 'callback', 'buffer', 'pickup', 'notification', 'dashboard', 'gateway', 'batch', 'validated', 'observers', 'nickname', 'scanner', 'record', 'displayed', 'identifying', 'png', 'python', 'rollback', 'benchmark', 'latency', 'sdk', 'trackingid', 'stored', 'synchronizers', 'interfaces', 'exporting', 'uri', 'bio', 'statistics', 'creating', 'loading', 'checkpoints', 'keyword', 'react', 'system', 'subscriber', 'tls', 'flags', 'viewports', 'watchdogs', 'queries', 'saves', 'published', 'previous', 'triggers', 'middleware', 'biography', 'refreshed', 'sharding', 'mobile', 'listings', 'staff', 'stocks', 'tax', 'services', 'ipv4', 'optimizers', 'reviews', 'reactjs', 'routers', 'rollbacks', 'restore', 'employees', 'conversationid', 'menu', 'workspaces', 'deserialization', 'predictors', 'restriction', 'ratings', 'directory', 'sliders', 'compliance', 'analysts', 'information', 'socket', 'duration', 'frontends', 'description', 'brand', 'cart', 'temporary', 'updates', 'dialog', 'handler', 'snippets', 'localization', 'elements', 'telephones', 'generated', 'formatters', 'probability', 'regulation', 'thresholds', 'datasets', 'folder', 'workspaceid', 'environment', 'feed', 'patch', 'trees', 'governance', 'manifest', 'reviewed', 'address', 'layouts', 'avatar', 'events', 'usb', 'replica', 'administrator', 'tenant', 'event', 'breadcrumbs', 'comment', 'state', 'approve', 'vectorizers', 'merchant', 'requests', 'coupon', 'review', 'receives', 'gateways', 'locations', 'inferencing', 'merchants', 'publishes', 'serialization', 'tab', 'vectorizer', 'traceid', 'discount', 'public', 'daemons', 'refreshes', 'finetuning', 'aggregators', 'export', 'responses', 'preference', 'carousel', 'vms', 'widgets', 'middlename', 'catalogs', 'integrations', 'addons', 'carts', 'amount', 'thumbnail', 'barcodes', 'restores', 'processing', 'listener', 'rejects', 'clipboard', 'encryption', 'unsuccessful', 'status', 'offline', 'users', 'backups', 'frontend', 'unicode', 'extractors', 'saved', 'package', 'product', 'offer', 'session', 'clients', 'interface', 'payroll', 'library', 'autocomplete', 'repositories', 'resource', 'switch', 'configuration', 'pdf', 'buyers', 'buttons', 'summary', 'classifiers', 'guid', 'checksumid', 'firewalls', 'translation', 'grid', 'alerts', 'banners', 'fonts', 'buffers', 'nodes', 'renderers', 'markdown', 'api', 'alert', 'filtered', 'plugin', 'tenants', 'sandbox', 'region', 'nicknames', 'deployment', 'save', 'transactions', 'checksum', 'phone', 'matrices', 'barcode', 'mocks', 'settlement', 'operand', 'search', 'predictor', 'url', 'draft', 'notificationid', 'tenantkey', 'notifies', 'departments', 'spinners', 'file', 'sessions', 'detects', 'resolver', 'invoice', 'dataset', 'tag', 'thread', 'identifiers', 'team', 'policy', 'bundle', 'upload', 'instances', 'priorities', 'showing', 'migrations', 'proxies', 'filter', 'executing', 'offers', 'sends', 'notifying', 'pointers', 'orchestrators', 'downloads', 'webhook', 'segmentation', 'visible', 'partners', 'feature', 'proxy', 'restrictions', 'hash', 'lastname', 'fulfillment', 'prices', 'wishlist', 'cursor', 'throughput', 'validators', 'sellers', 'reject', 'transaction', 'assistants', 'notified', 'warehouses', 'labels', 'payment', 'tokens', 'urls', 'runtime', 'hostname', 'organizationid', 'indexes', 'publishing', 'dns', 'replication', 'publisher', 'sql', 'authorization', 'listeners', 'integration', 'order', 'method', 'query', 'pipelineid', 'html', 'messages', 'trace', 'downtime', 'notifications', 'counts', 'searches', 'websocket', 'ios', 'promotion', 'templates', 'spinner', 'partitions', 'matrix', 'cells', 'component', 'databases', 'executed', 'cron', 'ram', 'cluster', 'attachment', 'report', 'images', 'partner', 'exported', 'imports', 'detecting', 'verified', 'stylesheets', 'analyzes', 'probabilities', 'storefront', 'preprocessing', 'usernames', 'debugger', 'namespace', 'image', 'tokenization', 'currency', 'updated', 'codes', 'profiles', 'layout', 'gpu', 'type', 'guids', 'byte', 'sections', 'account', 'element', 'endpoints', 'configure', 'references', 'deletes', 'namespaces', 'editors', 'widget', 'webhooks', 'download', 'analyzed', 'vm', 'uuid', 'identify', 'refreshkey', 'discounts', 'extensions', 'apps', 'microservice', 'enrollment', 'send', 'announcement', 'response', 'threshold', 'assigned', 'heatmap', 'heatmaps', 'archiving', 'dispatch', 'artifact', 'publish', 'versions', 'settlements', 'pipelines', 'deployments', 'checksums', 'created', 'label', 'refresh', 'policies', 'editor', 'threadid', 'orders', 'available', 'sprite', 'final', 'password', 'regulations', 'results', 'teams', 'mapper', 'systems', 'captchas', 'backup', 'inactive', 'batching', 'analytics', 'calculating', 'options', 'migration', 'updating', 'sku', 'emulator', 'certificate', 'tags', 'generating', 'validation', 'rule', 'shoppers', 'lookups', 'debuggers', 'deliveries', 'footers', 'comparator', 'schemas', 'blueprints', 'comparators', 'pending', 'embeddings', 'firstname', 'requestid', 'scheduled', 'submitted', 'configures', 'organizations', 'importing', 'deleted', 'decryption', 'values', 'environments', 'microservices', 'queue', 'telemetries', 'countries', 'bandwidth', 'https', 'unassigned', 'manager', 'coordinator', 'methods', 'page', 'executes', 'summaries', 'lookup', 'profile', 'audit', 'count', 'parsers', 'adapter', 'dropdowns', 'stock', 'exceptions', 'tenantid', 'engineers', 'dashboards', 'windows', 'table', 'eventid', 'signing', 'monitors', 'tracking', 'show', 'selector', 'officer', 'backends', 'handlers', 'dispatcher', 'hooks', 'favicon', 'member', 'display', 'partition', 'graphql', 'import', 'feeds', 'responseid', 'forecasts', 'challenge', 'schedule', 'agents', 'fraud', 'calculate', 'mobiles', 'sockets', 'token', 'designations', 'refunds', 'category', 'timezone', 'releaseid', 'clustering', 'plugins', 'scraper', 'fullname', 'media', 'durations', 'selectors', 'languages', 'score', 'vectors', 'types', 'permissions', 'active', 'firewall', 'featuremap', 'current', 'icon', 'embedding', 'applications', 'breadcrumb', 'authorizer', 'avatars', 'logs', 'regions', 'cachekey', 'restoring', 'accesskey', 'downloading', 'moderator', 'analyst', 'channel', 'schedules', 'orchestrator', 'handshakes', 'checkout', 'headers', 'heartbeat', 'window', 'completed', 'warehouse', 'managers', 'apis', 'generates', 'notify', 'sessionid', 'jpeg', 'rules', 'carrier', 'controllers', 'gzip', 'documents', 'firmware', 'organization', 'assistant', 'multilabel', 'restored', 'execute', 'oauth', 'epochs', 'addon', 'blueprint', 'uml', 'reviewer', 'apikey', 'dependencies', 'detect', 'consumer', 'parameter', 'exports', 'assigns', 'payouts', 'processors', 'user', 'invoices', 'monitoring', 'suppliers', 'approved', 'uploading', 'assign', 'broadcasters', 'patches', 'tabs', 'tickets', 'monitored', 'initializers', 'cache', 'packages', 'stacks', 'heartbeats', 'delivery', 'userid', 'caches', 'received', 'resolvers', 'dispatchers', 'transformers', 'ticket', 'spanid', 'sidebars', 'receiving', 'fields', 'frameworks', 'configuring', 'bundles', 'receive', 'adapters', 'banner', 'features', 'shops', 'searched', 'snippet', 'stack', 'history', 'cms', 'searching', 'http', 'postprocessing', 'secretkey', 'clusters', 'sqlite', 'administrators', 'purchase', 'support', 'compared', 'deduplication', 'subscribers', 'submits', 'skus', 'refund', 'carriers', 'preferences', 'instance', 'exception', 'department', 'number', 'trigger', 'timestamp', 'batches', 'redis', 'archive', 'setting', 'files', 'dependency', 'manifests', 'operators', 'button', 'cachekeys', 'location', 'card', 'uploads', 'traces', 'transactionid', 'header', 'purchases', 'security', 'delete', 'kernel', 'interpreters', 'broadcaster', 'scheduler', 'quantity', 'attendance', 'ui', 'username', 'accounts', 'audits', 'workspace', 'controller', 'daemon', 'uploaded', 'downloaded', 'announcements', 'object', 'listing', 'monitor', 'schedulers', 'coupons', 'ipv6', 'result', 'timestamps', 'assets', 'loaders', 'campaign', 'telemetry', 'generators', 'engineer', 'sorts', 'locales', 'framework', 'hostnames', 'theme', 'orderid', 'schema', 'identifies', 'creates', 'tracks', 'signature', 'catalog', 'wallet', 'logout', 'failed', 'country', 'submitting', 'customers', 'uptime', 'tables', 'access', 'flag', 'operands', 'keywords', 'navbar', 'categories', 'shop', 'new', 'websockets', 'stores', 'supplier', 'compare', 'field', 'section', 'addresses', 'collectors', 'tooltip', 'hashes', 'archived', 'workflow', 'authenticators', 'thumbnails', 'rating', 'dates', 'activities', 'shipment', 'content', 'permanent', 'clientid', 'signatures', 'returns', 'activity', 'authenticator', 'verification', 'connector', 'attributes', 'designation', 'birthdate', 'credentials', 'phones', 'employee', 'decompression', 'playbooks', 'browsers', 'node', 'sorting', 'compression', 'scrapers', 'processes', 'customer', 'value', 'locale', 'renderer', 'dialogs', 'timeseries', 'sort', 'repository']

STOPWORDS = set(stopwords.words('english'))

def is_polysemous(userStory):
    doc = nlp(userStory.lower())

    poly_words = []

    for token in doc:
        word = token.text

        # Skip stopwords
        if word in STOPWORDS:
            continue

        # Skip safe words
        if word in SAFE_WORDS:
            continue

        # Only important POS
        if token.pos_ not in ["NOUN", "VERB", "ADJ"]:
            continue

        synsets = wn.synsets(word)

        # Strict threshold
        if len(synsets) >= 3:
            poly_words.append(word)

    return poly_words
def detect_missing_structure(userStory):
    issues = []

    # Pattern checks
    as_actor = re.search(r"\bas (a|an|the)\b", userStory, re.IGNORECASE)
    i_want = re.search(r"\bi want\b", userStory,re.IGNORECASE)
    so_that = re.search(r"\bso that\b", userStory, re.IGNORECASE)
    has_comma_after_actor = bool(re.search(r"\bas\s+(a|an|the)\s+[^,]+,\s*", userStory, re.IGNORECASE))
    ends_with_full_stop = userStory.strip().endswith(".")

    if not as_actor:
        issues.append("Missing 'As a' section")

    if not i_want:
        issues.append("Missing 'I want' section")

    if not so_that:
        issues.append("Missing 'So that' section")
        
    if not has_comma_after_actor:
        issues.append("Missing 'Comma'  after \" As a [role]\" section")

    if not ends_with_full_stop:
        issues.append("Missing 'full stop' at end")
    return {
        "missing_structure": len(issues) > 0,
        "issues": issues
    }
def detect_grammar_issues(userStory):
    doc = nlp(userStory)
    issues = []

    has_verb = any(token.dep_ == "ROOT" and token.pos_ == "VERB" for token in doc)
    has_subject = any(token.dep_ in ["nsubj", "nsubjpass"] for token in doc)
    has_object = any(token.dep_ in ["dobj", "pobj"] for token in doc)

    if not has_verb:
        issues.append("Missing main verb")

    if not has_subject:
        issues.append("Missing subject")

    if not has_object:
        issues.append("Missing object or target")

    if len(doc) < 5:
        issues.append("Sentence too short")

    return {
        "grammar_issues": len(issues) > 0,
        "issues": issues
    }

# level 1 : Lexical Level
def detect_vagueness(userStory):
    result = parse_user_story(userStory)
    goal = result["goal"] or " "
    benefit = result["benefit"] or " "
    words = goal +" "+ benefit
    words = words.lower().split()


    vague_found = [w for w in words if w in VAGUE_WORDS]
    poly_found = [w for w in words if is_polysemous(w)]

    detected = len(vague_found) > 0 or len(poly_found) > 0
    notes = []
   
    if vague_found and not poly_found:
        notes.append(f"User story contains vague word(s) : {vague_found}")
    elif poly_found and not vague_found:
        notes.append(f"User story contains polysemous word(s) : {poly_found}")
    elif vague_found and poly_found:
        notes.append(f"User story contains vague word(s) : {vague_found}")
        notes.append(f"User story contains polysemous word(s) : {poly_found}")

    return {
        "type": "vagueness",
        "detected": detected,
        "confidence": 0.1,
        "details": {
            "vague_words": vague_found,
            "polysemous_words": poly_found
        },
        "notes" : notes
    }
# level 2 : Syntactic Level
def syntactic_inconsistency_detector(userStory):
    structure = detect_missing_structure(userStory)
    grammar = detect_grammar_issues(userStory)

    notes = []
    detected = structure["missing_structure"] or grammar["grammar_issues"]
    if(detected):
        if(structure["missing_structure"]):
            for issue in structure["issues"]:
                notes.append(f"Syntax error(s) found in UserStory: {issue}")
        if(grammar["grammar_issues"]):
            for issue in grammar["issues"]:
                notes.append(f"Grammar issue(s) found in UserStory: {issue}")
    return {
        "type": "syntax",
        "detected": detected,
        "confidence": 0.1,
        "details": {
            "structure": structure,
            "grammar": grammar
        },
        "notes": notes 
    }
# level 3 : Semantic Level
def detect_insufficiency(target_story, threshold=0.35):
    target_emb = embedding_model.encode(target_story, convert_to_tensor=True)
    similarities = util.cos_sim(target_emb, dataset_embeddings)[0].cpu().numpy()

    max_sim = float(np.max(similarities))
    detected = False
    notes = []
    if(max_sim < threshold):
        detected = True
        confidence = 0.75
        notes.append(f"User story is not from e-commerce domain")
    return {
        "type": "insufficiency",
        "detected": detected,
        "confidence": 0.1,
        "details": {
            "max_similarity": max_sim
        },
        "notes" : notes
    }
# level 4 : Pragmatic Level
def detect_duplication(target_story, all_stories):
    embeddings = embedding_model.encode(all_stories, convert_to_tensor=True)
    target_emb = embedding_model.encode(target_story, convert_to_tensor=True)

    similarities = util.cos_sim(target_emb, embeddings)[0].cpu().numpy()

    max_sim = float(np.max(similarities))
    index = int(np.argmax(similarities))

    detected = False
    notes = []
    if(max_sim >= 0.75):
         detected = True
         notes.append(f"User story with same functionality already exists")

    return {
        "type": "duplication",
        "detected": detected,
        "confidence": 0.1,
        "details": {
            "similarity": max_sim,
            "matched_index": index
        },
        "notes": notes
    }
# fusion level
def rule_based_ambiguity_detection(target_story, all_stories=[]):
    notes = []
    results = [
        detect_vagueness(target_story),
        syntactic_inconsistency_detector(target_story),
        detect_insufficiency(target_story)
    ]

    if all_stories:
        results.append(detect_duplication(target_story, all_stories))

    for r in results:
        notes.extend(r["notes"])

    return {
        "type": "rule_based",
        "results": results,
        "confidence": 0.1,
        "notes" : notes
    }





# ML based ambuguity detection----------------

# Load model and vectorizer
with open("models/logistic_regression_model_ambiguty_detection/model.pkl", "rb") as f:
    model = pickle.load(f)
with open("models/logistic_regression_model_ambiguty_detection/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)
    
label_columns = [
    "ActorAmbiguity",
    "SemanticAmbiguity",
    "ScopeAmbiguity",
    "AcceptanceAmbiguity",
    "DependencyAmbiguity",
    "PriorityAmbiguity",
    "TechnicalAmbiguity"
]

#prediction using logistic regression
def ml_based_ambiguity_prediction(userStory):
    vec = vectorizer.transform([userStory.lower()])
    probs = model.predict_proba(vec)

    threshold = 0.3

    notes = []
    predictions = {
        label: int(p[0][1] > threshold)
        for label, p in zip(label_columns, probs)
    }

    #  "ActorAmbiguity",
    # "SemanticAmbiguity",
    # "ScopeAmbiguity",
    # "AcceptanceAmbiguity",
    # "DependencyAmbiguity",
    # "PriorityAmbiguity"
    # "TechnicalAmbiguity"
    if(predictions["ActorAmbiguity"]):
        notes.append("unclear which type of user and what access level")
    if(predictions["SemanticAmbiguity"]):
        notes.append("Contain Vague verbs")
    if(predictions["ScopeAmbiguity"]):
        notes.append("scope is too broad")
    if(predictions["AcceptanceAmbiguity"]):
        notes.append("Non measurable acceptance criteria")
    if(predictions["DependencyAmbiguity"]):
        notes.append("Unclear which system and what integration dependencies exist")
    if(predictions["PriorityAmbiguity"]):
        notes.append("No clear priority or urgency specified")
    if(predictions["TechnicalAmbiguity"]):
        notes.append("contain Technical requirement without specific metrics or implementation details")

    detected = any(predictions.values())

    return {
        "type": "ml_based",
        "detected": detected,
        "confidence": 0.65 if detected else 0.3,
        "details": predictions,
        "notes" : notes
    }

#fusion layer, combine all report
def generate_final_ambiguity_report(userStory, all_stories=[]):

    rule_report = rule_based_ambiguity_detection(userStory, all_stories)
    ml_report = ml_based_ambiguity_prediction(userStory)



    notes = list(rule_report.get("notes", []))
    notes.extend(ml_report.get("notes", []))
    # Combine detections
    combined_detected = (
        any(r["detected"] for r in rule_report["results"]) 
        or ml_report["detected"]
    )

    # Weighted confidence
    final_confidence = (
        0.6 * rule_report["confidence"] +
        0.4 * ml_report["confidence"]
    )

    return {
        "user_story": userStory,
        "ambiguity_detected": combined_detected,
        "confidence": round(final_confidence, 2),
        "analysis": {
            "rule_based": rule_report,
            "ml_based": ml_report
        },
        "notes" : notes 
    }

# #remove code below, it was for testing only
# def print_ambiguity_report(report):
#     print("\n" + "="*60)
#     print("USER STORY:")
#     print(report["user_story"])
#     print("="*60)

#     print(f"\nAmbiguity Detected: {report['ambiguity_detected']}")
#     print(f"Overall Confidence: {report['confidence']}")
#     print("-"*60)

#     # 🔵 RULE-BASED
#     print("\n[ RULE-BASED ANALYSIS ]")
#     rb = report["analysis"]["rule_based"]

#     for r in rb["results"]:
#         print(f"\n→ Notes: {r['notes']}")
#         print(f"\n→ Type: {r['type']}")
#         print(f"  Detected: {r['detected']}")
#         print(f"  Confidence: {r['confidence']}")

#         # Details (dynamic)
#         for key, value in r["details"].items():
#             print(f"  {key}: {value}")

#     print("-"*60)

#     # 🟣 ML-BASED
#     print("\n[ ML-BASED ANALYSIS ]")
#     ml = report["analysis"]["ml_based"]
#     print(f"\n→ Notes: {r['notes']}")
#     print(f"Detected: {ml['detected']}")
#     print(f"Confidence: {ml['confidence']}")

#     print("\nPredicted Ambiguities:")
#     for key, value in ml["details"].items():
#         print(f"  {key}: {value}")

#     print("="*60 + "\n")

# ts="As a user, I want  to access fast dashboard so that i can track delivery."
# ats=["As a store owner, I want to track order so that I have better find desired items",
#      "As a user, I want to open dashboard so that i can track delivery.",
#      "As a seller, I want to handle orders so that I can complete purchase"]
# print_ambiguity_report(generate_final_ambiguity_report(ts,ats))


#----------------------------------------------------------------------------------------------------------

