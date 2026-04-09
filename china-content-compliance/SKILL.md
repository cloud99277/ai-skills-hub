---
name: china-content-compliance
description: Filters and rewrites content for China mainland public-distribution compliance, producing a publishable version with compliance annotations. Use when preparing content for mainland platforms, generating a public-safe version of internal material, or the user explicitly requests 公开版, 合规检查, 内容审查, or /china-compliance.
---

# China Content Compliance Filter (v2.0)

**Design Goal**: Build an independent content compliance processing module for China mainland platform distribution.

**Default scope**: This skill should default to general China mainland public-distribution compliance. Organization-specific, role-specific, or region-specific overlays should be layered separately rather than treated as the default baseline.

**Logic**:
```
Raw Data → Compliance_Filter (Clean/Rewrite) → Dual Output
```

**Platforms**: WeChat Official Account, Douyin, Bilibili, Xiaohongshu, Zhihu

---

## Core Functions

1. **Dual Output**
   - Personal Version: Complete content (Obsidian local)
   - Public Version: Compliance-filtered content (publishable)

2. **Three-Layer Filtering**
   - 🔴 **Hard Block (Red Rules)**: Direct deletion, no human confirmation
   - 🟠 **Soft Rewrite (Orange Rules)**: LLM rewrite, preserve information
   - 🟡 **Annotation (Yellow Rules)**: Add compliance labels

3. **Compliance Report**
   - Detailed record of all modifications
   - Risk level and triggered rules
   - Human review recommendations

---

## Usage

### Method 1: Auto-filter during report generation
```
Generate today's report, output public version
```

### Method 2: Check existing file
```
/china-compliance data/2026-02-08.md
```

### Method 3: Check text content
```
Check if the following content meets domestic publishing standards:
[paste content]
```

---

## Layer 1: Hard Block Rules (Red Rules)

**Action**: **Direct deletion**, no human confirmation, never publish.
**Reason**: Violates platform red lines, causes account suspension, ban, or legal risk.

### R-01: Cryptocurrency Trading

**Trigger Keywords**:
- `BTC`, `Bitcoin`, `ETH`, `Ethereum`, `USDT`, `Tether`
- `Virtual currency`, `Digital currency`, `Cryptocurrency`, `Token`
- `Mining`, `Mining machine`, `Mining pool`, `Hash power`
- `Airdrop`, `ICO`, `IEO`, `IDO`
- `Exchange`, `Binance`, `Coinbase`, `OKX`
- `DeFi`, `Decentralized finance`, `Liquidity mining`
- `NFT trading`, `NFT price`, `NFT speculation`

**Processing**:
- Delete entire news item
- Delete entire `Web3/Crypto` section

**Example**:
- ❌ Original: "Mistaken payment of $40B BTC causes market shock"
- ✅ Processing: **Direct deletion**

**Compliance Report**: `[R-01] Deleted: Cryptocurrency trading content`

---

### R-02: Domestic Product/Reputation Defamation

**Trigger Conditions**:
- `[Domestic Brand] + [Malware|Virus|Trojan|Backdoor|Spyware]`
- `[Domestic Brand] + [Scam|Run away|Bankruptcy|Collapse]`
- `[Domestic Brand] + [Theft|Steal|Leak|Sell user data]`

**Domestic Brand List**:
- AI: Kimi, Moonshot, Tongyi Qianwen, Wenxin Yiyan, Zhipu, DeepSeek, Baichuan, MiniMax, 01.AI
- Tech: Huawei, Xiaomi, OPPO, vivo, ByteDance, Tencent, Alibaba, Baidu, Meituan, Pinduoduo
- Security: Hikvision, Dahua, Uniview
- Auto: BYD, NIO, XPeng, Li Auto

**Processing**:
- Direct deletion of entire news item
- **Whitelist Exception**: Source is official notice (MIIT, Public Security, CAC, SAMR)
- Whitelist content still needs compliance report annotation: `⚠️ Retained official notice, recommend human review`

**Example**:
- ❌ Original: "Kimi.com malware warning...AI agent tool exposed containing crypto theft malware"
- ✅ Processing: **Direct deletion** (very likely fake news or competitor smear)

**Compliance Report**: `[R-02] Deleted: Domestic brand negative characterization (reputation defamation risk)`

---

### R-03: Political/Ideological Sensitivity

**Trigger Keywords**:
- National leader names
- Political system, ethnic/religious sensitive words
- Hong Kong/Macau/Taiwan political stance
- Historical sensitive events
- *Specific sensitive word database calls external API*

**Processing**:
- Direct deletion of entire news item

**Example**:
- ❌ Original: [Political sensitive content]
- ✅ Processing: **Direct deletion**

**Compliance Report**: `[R-03] Deleted: Political sensitive content`

---

### R-04: Illegal Stock Recommendation/Investment Advice

**Trigger Keywords**:
- `Bottom fishing`, `Add position`, `Reduce position`, `Clear position`, `Full position`
- `Target price`, `Stop loss`, `Take profit`, `Build position`
- `Surge`, `Plunge`, `Double`, `Ten-bagger`
- `Inside info`, `News`, `Rumor`
- `Code: [stock code]`, `Recommend buy`, `Strong recommend`

**Processing**:
- Delete specific investment advice statements
- If entire news is investment advice, delete entire item

**Example**:
- ❌ Original: "Various holders start bottom fishing, recommend attention to AI sector"
- ✅ Processing: **Delete or rewrite to objective description**

**Compliance Report**: `[R-04] Deleted/Rewritten: Illegal investment advice`

---

### R-05: Network Security/VPN Tools

**Trigger Keywords**:
- `Bypass GFW`, `Scientific internet`, `Ladder`, `VPN recommendation`
- `SS`, `SSR`, `V2Ray`, `Clash`, `Shadowsocks`
- `Airport recommendation`, `Proxy server`

**Processing**:
- Direct deletion of entire news item

**Compliance Report**: `[R-05] Deleted: Network security sensitive content`

---

### R-06: Hikvision Employee Special Compliance (Hikvision Insider Shield)

**Module Name**: Hikvision_Insider_Shield (Internal Firewall)

**Core Logic**: Based on user's sensitive identity as "Supply Chain Center · Finished Product Planner", must add enterprise trade secret and non-compete protection layer on top of general internet compliance. Any content involving supply chain data, capacity, supplier relationships, or geopolitical sensitive points, if linked to real identity, may trigger internal company audit or violate "Employee Confidentiality Agreement".

---

#### Layer 1: Core Data Desensitization (Data Loss Prevention - DLP)

**Rule**: Strictly prohibit any micro data that could infer company operational status.

##### 1. Material/SKU Information

**Trigger Keywords**:
- `SKU`, `Material number`, `BOM`, `Shortage`, `Kit rate`, `Inventory turnover`, `VMI`
- `DS-[model]`, `iDS-[model]`, `IPC-[model]`

**Risk Scenario**:
- Mentioning "certain high-end chip shortage" or "inventory backlog" may allow competitors to analyze Hikvision's capacity bottleneck

**Processing**:
- **[Block]** Block supply chain descriptions with specific numbers
- Delete all `DS-` prefix model strings

**Example**:
- ❌ Original: "Recently DS-7800 series severe shortage"
- ✅ Processing: **Direct deletion**

---

##### 2. Capacity/Production Information

**Trigger Keywords**:
- `Production line`, `Capacity ramp`, `Yield rate`, `Tonglu factory`, `Chongqing base`, `Wuhan base`
- `Production plan`, `Delivery cycle`, `Overtime`, `Rush`, `Shutdown`

**Risk Scenario**:
- Exposing specific factory operations (e.g., "recently production lines all working overtime")

**Processing**:
- **[Generalize]** Change to "industry overall supply chain tension"
- Delete specific factory names and capacity data

**Example**:
- ❌ Original: "Chongqing base capacity ramp, yield rate reaches 95%"
- ✅ Rewrite: "Industry overall capacity recovery, supply chain trending stable"

---

##### 3. Supplier Relationships

**Trigger Keywords**:
- `HiSilicon`, `Hisilicon`, `Nvidia`, `SOC`, `CMOS`, `Sensor`
- `OmniVision`, `Novatek`, `Ambarella`, `Sony`, `Intel`
- `Supply cut`, `Sanction`, `Cooperation`, `Price increase letter`

**Risk Scenario**:
- Evaluating specific suppliers (especially sanctioned entities or domestic alternatives)

**Processing**:
- **[Anonymize]** Change to "upstream core component manufacturers"
- Delete specific supplier names and cooperation details

**Example**:
- ❌ Original: "Hisilicon can't supply, considering switch to Ambarella solution"
- ✅ Rewrite: "Upstream core component supply tension, industry seeking alternative solutions"

---

##### 4. Internal Code/Project

**Trigger Keywords**:
- `EZVIZ` (Fluorite non-public project), `HIK`, `DS-`, `iVMS`, `HCNetSDK`
- Internal project codes, unreleased product models

**Risk Scenario**:
- Leaking unreleased product models or internal project codes

**Processing**:
- **[Block]** Strictly filter all internal codes and models

**Example**:
- ❌ Original: "New iVMS-5000 project about to launch"
- ✅ Processing: **Direct deletion**

---

#### Layer 2: Geopolitical & Sanction Isolation (Sanction Firewall)

**Rule**: As "Entity List" enterprise employee, strictly prohibit public comment on related sanction policies, which will be viewed as company position extension.

##### 1. Entity List/Sanctions

**Trigger Keywords**:
- `Entity List`, `Sanction`, `Entity List`, `Blacklist`, `Trade war`, `Ban`
- `US restriction`, `Export control`, `Technology blockade`

**Processing**:
- **[Context-Aware]** Macro news (e.g., "US hopes Russia-Ukraine ceasefire") safe
- **[High-Risk]** Security industry sanction news (e.g., "US restricts security exports") direct deletion

**Example**:
- ✅ Safe: "US hopes Russia-Ukraine ceasefire by June" (macro news)
- ❌ High-risk: "US expands sanction scope on Chinese security enterprises" (direct deletion)

---

##### 2. Xinjiang/Human Rights

**Trigger Keywords**:
- `Xinjiang`, `Human rights`, `Forced labor`, `Genocide`
- Any human rights accusations related to Hikvision

**Processing**:
- **[Kill Switch]** If appears, entire daily report prohibited from publishing
- This is Hikvision PR absolute red line

**Compliance Report**: `[R-06-CRITICAL] Violated company geopolitical red line, entire daily report blocked from publishing`

---

##### 3. Technology Decoupling/Domestic Substitution

**Trigger Keywords**:
- `Domestic substitution`, `De-Americanization`, `Independent controllable`, `Technology decoupling`

**Processing**:
- **[Neutralize]** Avoid aggressive nationalist narrative
- Maintain "technology neutral" observer perspective

**Example**:
- ❌ Original: "Hikvision successfully achieves chip de-Americanization, breaks technology blockade"
- ✅ Rewrite: "Industry advancing core component supply diversification"

---

##### 4. Cross-border Data Transmission Risk

**Trigger Keywords**:
- `Data outbound`, `Cross-border transmission`, `International supply chain data`, `Cross-border data`
- `Provide to overseas`, `Overseas server`, `Data localization`

**Risk Scenario**:
- Hikvision as Entity List enterprise, cross-border supply chain data transmission sensitivity extremely high
- Any expression involving "providing supply chain data to overseas entities" may trigger compliance risk

**Processing**:
- **[Block]** Delete specific cross-border data transmission details
- **[Generalize]** Change to "data security management" or "data compliance requirements"

**Example**:
- ❌ Original: "Hikvision provides supply chain traceability data to overseas partners"
- ✅ Rewrite: "Industry strengthens data security management and compliance requirements"

**Legal Basis**:
- "Data Security Law of the People's Republic of China"
- "Personal Information Outbound Standard Contract"

**Compliance Report**: `[R-06-HIGH] Deleted: Cross-border data transmission sensitive information`

---

#### Layer 3: Identity Isolation (Identity Gap)

**Rule**: Completely avoid Hikvision HR/internal control risk, execute physical isolation.

##### 1. Prohibit Identity Association

**Processing**:
- Never write "Hikvision employee", "Security industry", "Hikvision" in profile
- Only write "Supply chain practitioner" or "Big company planner"

**Compliance Report**: `[R-06-INFO] Recommend checking personal profile, ensure no employer information association`

---

##### 2. IP Location Risk

**Risk Scenario**:
- User in Chongqing. If Hikvision Chongqing base has sensitive actions (e.g., layoffs, expansion), and daily report IP in Chongqing discusses related topics, easy to be locked.

**Processing**:
- Keep daily report content globalized/generalized (AI, Web3, macro economy)
- Try to avoid "security", "surveillance", "camera" vertical topics

**Compliance Report**: `[R-06-WARNING] Detected security industry related content, recommend deletion or generalization`

---

##### 3. Timestamp Risk

**Risk Scenario**:
- Frequently publishing content during work hours (8:30 - 18:00) may be viewed as "work hour fraud" or "slacking"

**Processing**:
- Recommend scheduled publishing (after 20:00)

**Compliance Report**: `[R-06-INFO] Recommend publishing content during non-work hours`

---

#### Comprehensive Processing Logic

**Trigger Conditions**:
1. `Hikvision + [negative words]`
2. `Hikvision + [security breach|backdoor|spy]`
3. Supply chain micro data (materials, capacity, suppliers)
4. Geopolitical sensitive topics (Entity List, Xinjiang)
5. Internal code/project information
6. Security industry vertical topics

**Processing**:
- **[Block]** Direct deletion (protect employer reputation and trade secrets)
- **[Generalize]** Generalize to industry common expression
- **[Anonymize]** Anonymize suppliers and partners
- **[Kill Switch]** Xinjiang/human rights topics trigger entire article block

**Compliance Report**: `[R-06] Deleted/Rewritten: Hikvision employee special compliance (DLP + Sanction Isolation + Identity Protection)`

---

### R-07: Minor Protection Rules

**Legal Basis**: "Classification Measures for Network Information That May Affect Minors' Physical and Mental Health" (2025)

**Core Logic**: Although daily report mainly for adults, if content may be accessed by minors, need to add age restriction annotation.

---

#### Trigger Content Types

##### 1. Violence/Gore Content

**Trigger Keywords**:
- `Violence`, `Gore`, `Murder`, `Shooting`, `Terrorist attack`
- `War scene`, `Corpse`, `Casualties`

**Processing**:
- **[Label]** Add age restriction annotation: `⚠️ This content involves violent scenes, not suitable for minors`

---

##### 2. Horror/Thriller Content

**Trigger Keywords**:
- `Horror`, `Thriller`, `Supernatural`, `Ghost`

**Processing**:
- **[Label]** Add age restriction annotation

---

##### 3. Gambling/Drug Related

**Trigger Keywords**:
- `Gambling`, `Gaming`, `Casino`, `Drugs`, `Drug use`

**Processing**:
- **[Delete]** Direct deletion (overlaps with R-03 political sensitivity)

**Compliance Report**: `[R-07] Deleted: Gambling/drug content (minor protection)`

---

##### 4. Inducing Minor Consumption

**Trigger Keywords**:
- `Minor tipping`, `Child recharge`, `Youth consumption`

**Processing**:
- **[Delete]** Direct deletion

**Compliance Report**: `[R-07] Deleted: Inducing minor consumption`

---

## Layer 2: Soft Rewrite Rules (Orange Rules)

**Action**: **LLM rewrite**, preserve information increment, remove emotion and orientation.
**Executor**: Claude / Gemini

### O-01: De-Financialization

**Original Logic**: Describe asset price fluctuation, buy/sell advice
**New Logic**: Describe technology trends or industry observation

**Rewrite Rules**:
- `Bond market rebound` → `Bond market fluctuation`
- `Credit market pressure` → `Credit market adjustment`
- `Investors bottom fishing` → `Market participants attention`
- `Capital inflow` → `Capital allocation change`

**Example**:
- ❌ Original: "Tech AI investment triggers bond market rebound...credit market pressure"
- ✅ Rewrite: "Tech giants increase AI infrastructure capital expenditure (CapEx), market attention to cash flow impact"

**Compliance Report**: `[O-01] Rewritten: De-financialization`

---

### O-02: Source Isolation

**Original Logic**: Direct statement of facts
**New Logic**: Quote third party + skeptical attitude

**Rewrite Rules**:
- Add prefix: `According to overseas community feedback`, `According to foreign media reports`, `Some developers report`
- Add suffix: `Specific situation awaits official confirmation`, `Recommend obtaining from official channels`
- Blur brand: `Certain AI tool`, `Certain large model platform`, `Certain security device`

**Example**:
- ❌ Original: "AI agent tool exposed containing crypto theft malware"
- ✅ Rewrite: "According to overseas community feedback, some AI plugins downloaded from unofficial channels may have security risks, recommend developers only obtain tools from official website"

**Compliance Report**: `[O-02] Rewritten: Source isolation + brand blurring`

---

### O-03: Macro Neutrality

**Original Logic**: Use emotional vocabulary
**New Logic**: Use neutral expression

**Rewrite Rules**:
- `Collapse` → `Significant adjustment`
- `Crisis` → `Challenge`
- `Depression` → `Cyclical slowdown`
- `Plunge` → `Significant decline`
- `Shock` → `Impact`

**Example**:
- ❌ Original: "US employment + inflation data double shock"
- ✅ Rewrite: "US latest employment and inflation data about to be released, market expectations may fluctuate"

**Compliance Report**: `[O-03] Rewritten: Macro neutralization`

---

### O-04: Tech Content Preservation

**Original Logic**: Delete all Web3/Crypto
**New Logic**: Preserve pure tech content, delete trading/price content

**Preserve Content**:
- Zero-knowledge proof (ZK-Proof)
- Blockchain technology principles
- Distributed system architecture
- Smart contract security research

**Delete Content**:
- Coin price prediction
- Trading strategy
- Project tokenomics
- Exchange dynamics

**Rewrite Rules**:
- Section name: `Web3/Crypto` → `Distributed Technology`
- `Blockchain project` → `Distributed system project`
- `Encryption technology` → `Cryptography technology`

**Compliance Report**: `[O-04] Rewritten: Preserve tech content, delete financial attributes`

---

## Layer 3: Annotation (Yellow Rules)

### Y-01: AI Generated Content Identification (Complete Version)

**Legal Basis**:
- "Measures for Identification of AI Generated Synthetic Content" (effective September 1, 2025)
- Mandatory National Standard GB 45438—2025

**Processing**:

#### 1. Explicit Identification (User Visible)

Add at document end:
```markdown
---

> **AI Generation Statement**: This report is AI-assisted generated, content for reference only, does not constitute investment advice.
```

#### 2. Implicit Identification (File Metadata)

Add complete metadata in YAML Frontmatter:
```yaml
ai_generated: true
compliance_version: public
compliance_date: 2026-02-08
ai_metadata:
  provider: Cloud927
  provider_code: CLD927
  model: Claude-Sonnet-4.5 + Gemini-2.0-Flash
  content_id: YYYYMMDD-HHMMSS
  generation_timestamp: 2026-02-08T20:00:00+08:00
  content_type: text/markdown
  standard: GB45438-2025
```

#### 3. Platform Specific Identification

- **WeChat Official Account**: Check "AI Generated" tag when publishing
- **Douyin**: Check "AI Generated" badge when publishing
- **Xiaohongshu**: Add #AI生成 topic tag

**Compliance Report**: `[Y-01] Added: AI generation identification (explicit+implicit+platform)`

---

### Y-02: Disclaimer

**Processing**:
Add at document beginning:
```markdown
> **Disclaimer**: This report content sourced from public information, for learning and exchange only, does not constitute any investment advice. Investment has risks, decisions need caution.
```

**Compliance Report**: `[Y-02] Added: Disclaimer`

---

### Y-03: Information Source Attribution

**Processing**:
For retained sensitive content, add source attribution:
```markdown
> Information source: [Official notice/Foreign media report], specific situation subject to official release.
```

**Compliance Report**: `[Y-03] Added: Information source attribution`

---

### Y-04: News Source Attribution Rules

**Legal Basis**: Douyin 2026 "Safety and Trust Conference" requires "guide users to mark information sources"

**Processing**:
Each news must mark source, format:
```markdown
- **[Title]** (Source: Hacker News)
```

**Purpose**:
- Prevent platform misjudgment as rumor
- Improve content credibility
- Meet platform governance requirements

**Compliance Report**: `[Y-04] Added: News source attribution`

---

### Y-05: Employee Self-Media Revenue Reporting Reminder

**Legal Basis**: Reference ByteDance 2026 employee self-media regulations

**Trigger Conditions**:
- Self-media account generates revenue (ads, tips, paid subscriptions, etc.)
- Recent three months average monthly income exceeds 500 RMB

**Processing**:
Add reminder in compliance report:
```markdown
⚠️ **Revenue Risk Reminder**: If your self-media account generates revenue (monthly average exceeds 500 RMB), recommend reporting to company to avoid violating employee code of conduct.
```

**Compliance Report**: `[Y-05] Added: Revenue reporting reminder`

---

### Y-06: Electronic Evidence Preservation Recommendation

**Legal Basis**: 2026 trade secret litigation cases rise, electronic evidence technicalization

**Processing**:
Add recommendation in compliance report:
```markdown
📋 **Electronic Evidence Preservation Recommendation**:
- Save original daily report file (with timestamp)
- Recommend using blockchain notarization or timestamp service
- Retain compliance report as processing record
- Retention period: recommend at least 3 years
```

**Purpose**:
- Prevent trade secret disputes
- Prove compliance obligations fulfilled
- Protect personal and enterprise interests

**Compliance Report**: `[Y-06] Added: Electronic evidence preservation recommendation`

---

### Y-07: Local Regulation Reminder (Chongqing)

**Legal Basis**: Chongqing CAC has strong enforcement on illegal information reporting

**Processing**:
Add local reminder in compliance report:
```markdown
📍 **Chongqing Local Regulation Reminder**:
- Chongqing CAC has strong enforcement on illegal and harmful information reporting
- Recommend using platform's built-in "Content Safety Detection" function before publishing
- If receive report or warning, timely rectify and retain records
```

**Compliance Report**: `[Y-07] Added: Local regulation reminder`

---

## Execution Process

When user invokes this skill, execute in following order:

### Step 1: Read Content
- If user provides file path, read file
- If user directly provides content, use that content

### Step 2: Hard Block (Red Rules)
- Check in order R-01 to R-07
- Match any rule, directly delete entire item or section
- Record deletion items to compliance report

### Step 3: Soft Rewrite (Orange Rules)
- Apply O-01 to O-04 rewrite rules to remaining content
- Use LLM for intelligent rewrite
- Record rewrite items to compliance report

### Step 4: Annotation (Yellow Rules)
- Add AI generation identification (explicit+implicit)
- Add disclaimer
- Add news source attribution
- Add YAML Frontmatter
- Add revenue reporting reminder
- Add electronic evidence preservation recommendation
- Add local regulation reminder
- Record annotation items to compliance report

### Step 5: Generate Output
- Public version content (filtered)
- Compliance report (detailed record)

### Step 6: Save Files
- Public version: `YYYY-MM-DD_public.md`
- Compliance report: `YYYY-MM-DD_compliance_report.md`

---

## Notes

1. **Conservative Principle**: Rather over-filter than miss risks
2. **Human Review**: "Recommend human review" items in compliance report must be checked
3. **Timely Update**: When regulatory policies change, timely update filtering rules
4. **Personal Version Retention**: Personal version (Obsidian local) retains complete content, no filtering
5. **Whitelist Mechanism**: Official notice content retained, but still needs risk annotation

---

## References

For detailed keyword database and examples, see:
- `keywords.yaml` - Complete compliance keyword database
- `examples.md` - Filtering examples and test cases
- `CHANGELOG.md` - Version update history
