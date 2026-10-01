# Research-to-Action POC — Canonical System Specification

Status: implementation-ready POC specification  
Owner: ChatGPT / Max  
Execution coordinator: rmax-10  
Repository: `rmax-ai/research-to-action`

## 1. Objective

Build a public, synthetic-data proof of concept that demonstrates one hard invariant:

> A natural-language biomedical research intent can become a correct, authorized, reproducible, and actionable transaction across heterogeneous/federated clinical data.

This is **not** a generic medical chatbot and not a swarm of independent agents. It is a governed workflow in which probabilistic reasoning proposes structured intents/plans, deterministic services execute queries and policies, humans approve consequential actions, and every material claim/action is backed by provenance.

## 2. Canonical scenario

Reference request:

> Find 200 metastatic NSCLC patients with KRAS G12C, pretreatment H&E slides, NGS data, treatment history, and at least 12 months of outcomes. The data will be used for commercial AI model development. Tell me whether the cohort is feasible, where the patients are, what is missing, what we are allowed to use, how much acquisition will cost, and prepare the request for procurement.

Required follow-ups include:

- Why did Site C lose so many cases?
- Which criterion is the strongest feasibility bottleneck?
- What happens if follow-up increases to 24 months?
- What happens if pathology is allowed within 30 days after treatment begins?
- Can we maximize institutional diversity while still obtaining 200 cases?
- Why is this case permitted/denied/review-required?
- Where did the KRAS G12C assertion come from?
- Prepare and, after explicit human approval, execute the simulated procurement order.

## 3. Product promise

The demo must make this chain visible:

`scientific question -> structured request -> terminology mapping -> federated discovery -> multimodal matching -> quality -> governance -> feasibility -> supplier plan -> human approval -> simulated transaction -> audit/evidence package`

The output is an actionable answer, not a search result.

## 4. Non-goals

V1 does not attempt:

- real PHI or production patient identity resolution;
- production HIPAA/HITRUST infrastructure or legal certification claims;
- real payments, contracting, or specimen shipment;
- autonomous legal/compliance decisions;
- full DICOM/WSI storage or processing;
- foundation-model training;
- a generic enterprise agent platform;
- a complete OMOP ETL system;
- full regulatory submission generation;
- arbitrary SQL access by LLM agents;
- dozens of independent chatbot personas.

Mock interfaces where necessary, while preserving realistic trust, state, and evidence boundaries.

## 5. Invariants

### I1 — Structured boundary before execution
All natural-language requests become validated, versioned `ResearchRequest` and `ExecutionPlan` objects before deterministic execution. Use Pydantic v2 for Python serialized boundaries and Zod for TypeScript boundaries where applicable.

### I2 — LLM reasoning cannot bypass enforcement
Models may interpret, map, plan, summarize, and explain. They may not directly override policy, authorization, cohort truth, quality truth, cost truth, or action gates.

### I3 — Deterministic truth for critical outputs
Cohort counts, exclusions, policy outcomes, quality metrics, supplier optimization, and transaction state derive from deterministic code/data.

### I4 — Explicit epistemic state
Every material answer item is typed as one of:
- `FACT` — directly sourced;
- `DERIVED` — deterministically computed;
- `INFERRED` — probabilistic/model inference;
- `HUMAN_DECISION` — explicitly approved/rejected by a person.

### I5 — Provenance is mandatory
Every material claim links to enough evidence for reproduction: source dataset/version, request/plan identity, query/adapter version, ontology mapping, transformation, policy version, quality config, and/or approval event.

### I6 — Federated-by-interface
Agents never receive arbitrary site database credentials. Site adapters expose narrow capabilities and return only allowed data.

### I7 — Human approval for consequential actions
Action classes:
- READ — automatic when authorized;
- DERIVE — automatic with provenance;
- EXTERNALIZE/RELEASE — policy controlled and potentially review-gated;
- COMMIT MONEY / SUBMIT PROCUREMENT / RELEASE DATA — explicit human approval.

### I8 — Replayability
Given the same repository commit, fixture versions, request object, ontology version, policy version, and deterministic config, the system can replay a run and explain stochastic differences.

### I9 — No unsupported claims
Unknown/unavailable remains explicit. The conversational layer does not invent clinical facts, policy decisions, costs, supplier capacity, or evidence.

## 6. Architecture

```text
                       ┌──────────────────────┐
User / Demo UI ───────►│ Research Orchestrator│
                       └──────────┬───────────┘
                                  │
                         ResearchRequest v1
                                  │
                       ┌──────────▼───────────┐
                       │ Durable Workflow      │
                       │ / Control Plane       │
                       └──────┬───────┬────────┘
                              │       │
             ┌────────────────┘       └─────────────────┐
             ▼                                          ▼
     Data/Feasibility                             Governance
         services                                   service
             │                                          │
       Site adapters                                Policy engine
             │                                          │
   ┌─────────┼───────────┐                              │
   ▼         ▼           ▼                              │
OMOP Site  FHIR Site   CSV/Lab Site                      │
   └─────────┴───────────┘                              │
             │                                          │
             └──────────────┬───────────────────────────┘
                            ▼
                    Evidence / Audit Store
                            │
                            ▼
                  Procurement Planner
                            │
                    HUMAN APPROVAL GATE
                            │
                            ▼
                  Simulated Transaction
```

Implementation should favor a typed workflow/state machine and tool/service boundaries over unconstrained agent-to-agent conversation.

## 7. Logical capabilities

### Research / intake
- parse natural-language request;
- identify missing/ambiguous requirements;
- generate structured eligibility criteria;
- propose terminology mappings;
- compile a deterministic query plan;
- explain interpretation/assumptions.

### Terminology / ontology
- normalize disease, biomarker, assay, drug, specimen, and clinical concepts;
- map local codes to canonical concepts;
- preserve candidates, selected mapping, confidence/source/version, and review state;
- escalate uncertain mappings instead of silently choosing.

### Federated discovery / feasibility
- execute the same request across heterogeneous sites;
- combine allowed aggregate/row-level results;
- generate feasibility waterfalls;
- perform criterion-sensitivity reruns;
- attribute counts/exclusions to site and criterion.

### Data quality
Minimum deterministic dimensions:
- completeness;
- validity;
- temporal consistency;
- ontology/mapping coverage;
- duplicate rate;
- modality/asset linkage;
- longitudinal/follow-up completeness.

The LLM explains metrics; it does not generate them.

### Governance
- purpose-of-use evaluation;
- consent/restriction evaluation;
- release/de-identification policy simulation;
- ALLOW / DENY / REVIEW_REQUIRED;
- stable reason codes + evidence;
- authorization separate from schema validation.

### Provenance / evidence
Every answer/action should link to request/plan identity, source site/dataset/version, query/adapter version, mapping version, policy version, transformation, quality metrics, approvals, and transaction state.

### Procurement
- supplier/site selection;
- optimize for cost, diversity, delivery time, quality, and site count;
- deterministic fixture-based cost/time;
- draft procurement packages;
- stop at human approval;
- create mock order only after approval.

### Operations / audit
- show workflow state;
- explain blockers/retries;
- expose complete append-only audit events;
- support replay/comparison.

## 8. Typed models

At minimum implement versioned Pydantic v2 models for:

- `ResearchRequest`
- `ClinicalCriterion`
- `AssetRequirement`
- `PurposeOfUse`
- `OntologyMapping`
- `ExecutionPlan`
- `SiteQueryRequest`
- `SiteQueryResult`
- `CohortWaterfallStep`
- `DataQualityReport`
- `PolicyDecision`
- `EvidenceRef`
- `Claim`
- `SupplierOffer`
- `ProcurementPlan`
- `HumanApproval`
- `TransactionRecord`
- `ToolEvent`
- `RunRecord`
- `EvaluationCase`
- `EvaluationResult`

Version envelopes must allow schema evolution and explicitly reject unknown/incompatible versions.

## 9. Site adapter contract

Conceptual interface:

```python
class SiteAdapter(Protocol):
    def get_cohort_count(self, query: SiteQueryRequest) -> CountResult: ...
    def get_patient_matches(self, query: SiteQueryRequest) -> PatientMatchResult: ...
    def get_asset_availability(self, query: SiteQueryRequest) -> AssetAvailabilityResult: ...
    def get_summary_statistics(self, query: SiteQueryRequest) -> SummaryStatistics: ...
```

Each adapter:
- validates request versions;
- enforces site-local release limits;
- identifies exact fixture version;
- returns provenance + deterministic result hashes;
- never exposes unrestricted SQL execution to the model.

## 10. SPEC 2 — Synthetic/federated three-site clinical network

This is a first-class epic, not an appendix.

### Goals
Create a realistic, reproducible synthetic network proving one biomedical request can be answered across incompatible storage/representation models.

### Site A — OMOP-style research hospital
- Postgres.
- OMOP-inspired person/condition/drug/measurement/observation structures plus minimal extensions for specimen/pathology/consent.
- Diagnosis, stage, treatment, outcomes, genomics, pathology refs, purpose metadata.

### Site B — FHIR health system
- Local deterministic FHIR fixture/service.
- At minimum Patient, Condition, Observation, Medication/MedicationRequest or Administration, DiagnosticReport, Specimen, relevant extensions.
- Adapter translates canonical query semantics into deterministic FHIR-side filtering.

### Site C — messy lab/biobank
Deliberately heterogeneous:
- `patients.csv`
- `cases.csv`
- `slides.parquet`
- `ngs_results.csv`
- `specimen_inventory.csv`
- `consent.csv` or equivalent.

Include inconsistent local codes, missing values, duplicate identifiers, and ambiguous treatment chronology.

### Synthetic oncology augmentation
Deterministic generator covers:
- primary disease/histology;
- stage/metastatic state;
- biomarker/genomic variants including KRAS G12C;
- therapy lines/timestamps;
- response/outcomes/follow-up;
- pathology slides/assets;
- physical specimens/remaining quantity;
- assay metadata;
- site-local coding differences;
- consent and purpose-of-use;
- commercial research / AI-training permissions;
- release restrictions.

No test may require unavailable remote data.

### Ground truth
Freeze row-level truth for the canonical scenario. Illustrative target:
- Site A raw matches: 142
- Site B raw matches: 97
- Site C raw matches: 83
- Total raw matches: 322

Intentional exclusion classes:
- insufficient follow-up;
- missing/unusable H&E;
- missing NGS;
- incomplete treatment history;
- purpose-of-use not permitted;
- exhausted/unavailable specimen where requested;
- uncertain terminology mapping;
- data-quality threshold failure.

Illustrative final usable population: ~215, sufficient for a request of 200.

### Feasibility waterfall truth
Fixture generation emits a machine-readable ground-truth waterfall, e.g.:

```text
322  disease + stage + KRAS G12C
287  >=12 months follow-up
266  pretreatment H&E
252  NGS available
235  complete treatment history
218  purpose-of-use allowed
215  quality threshold passed
```

Counts must emerge from row-level facts, never from hard-coded aggregate answers.

### Counterfactual truth cases
Include:
- 24-month follow-up makes request infeasible;
- pathology <=30 days after therapy increases the cohort;
- physical tissue rather than digital H&E materially reduces supply;
- a restrictive purpose/site constraint changes supplier mix;
- one ambiguous terminology mapping produces REVIEW_REQUIRED.

### Site-local governance fixtures
Example:
- Site A permits de-identified commercial AI development;
- Site B permits commercial research but some consents exclude AI training;
- Site C contains research-only restrictions and manual-review cases.

### Fixture validation
Tests prove:
- deterministic regeneration;
- stable unique IDs;
- no real-person data;
- expected raw/filtered counts;
- known missingness/error patterns;
- semantic adapter equivalence;
- fixture manifest digest included in run records.

## 11. Request compilation

The model generates a candidate `ResearchRequest` with:
- disease/stage;
- biomarker;
- required assets;
- timing relations;
- longitudinal constraints;
- requested quantity;
- intended purpose;
- optimization preference;
- unresolved ambiguities.

Only ambiguities that materially alter execution/permission need user resolution. Once validated, the request is immutable for that run; follow-ups create linked revisions.

## 12. Terminology mapping

Implement a small locally versioned terminology layer sufficient for the scenario, mapping local site codes to canonical concepts and public identifiers where redistribution permits.

Persist:
- source term/code;
- candidates;
- chosen mapping;
- confidence/method;
- source/version;
- review state.

At least one fixture must force explicit ambiguity review.

## 13. Feasibility and sensitivity

System outputs:
- total + per-site raw counts;
- sequential waterfall;
- exclusion reasons;
- strongest bottleneck;
- counterfactual reruns;
- requested vs available quantity;
- `FEASIBLE`, `INFEASIBLE`, or `REVIEW_REQUIRED`.

Counterfactuals re-execute deterministic logic; they are not LLM estimates.

## 14. Data quality

Deterministic checks:
- required-field completeness;
- valid domain/code values;
- temporal consistency;
- duplicate/identity collision fixture detection;
- terminology resolution state;
- multimodal linkage validity;
- follow-up validity.

Quality threshold/config is versioned and part of provenance.

## 15. Governance / policy

Use deterministic versioned policy code/engine.

Canonical purpose: `commercial_ai_model_development`.

Example:

```yaml
requires:
  - commercial_research_allowed
  - ai_training_allowed
  - deidentified_release_allowed

deny_if:
  - consent_withdrawn
  - research_only_restriction

review_if:
  - purpose_mapping_uncertain
  - site_manual_release_required
```

Output:
- ALLOW / DENY / REVIEW;
- stable machine reason codes;
- human explanation;
- evidence refs;
- policy version/hash.

Schema validation, authorization, and business policy remain separate.

## 16. Procurement planning

Use deterministic supplier offers:
- available count;
- cost per case/fixed cost;
- turnaround;
- quality;
- modality/specimen availability;
- institution metadata.

Support:
- minimize cost;
- minimize turnaround;
- maximize institutional diversity;
- configurable weighted objective.

Return integer allocation with per-site count, total estimate, turnaround, assumptions, and approval state.

## 17. Simulated transaction

After valid approval:
- create one or more `TransactionRecord`s;
- deterministic mock states such as `DRAFT -> SUBMITTED -> ACKNOWLEDGED -> FULFILLING -> COMPLETE`;
- include one deterministic blocked/error route;
- append audit events; do not rewrite history.

No real external side effects.

## 18. Evidence and audit

A claim such as `215 eligible cases` must drill down through:
- request revision;
- query plan;
- Site A/B/C result objects;
- fixture/dataset versions;
- mapping version;
- quality configuration;
- governance policy;
- aggregation calculation.

A patient-level KRAS G12C fact must trace to the exact source fixture record and normalization chain.

## 19. Durable workflow

Required properties:
- explicit typed state;
- idempotent activities;
- retry policies;
- no hidden agent memory as authority;
- resumable from persisted state;
- every tool/activity event captured;
- workflow version in run record.

Temporal is acceptable; a simpler durable state machine is also acceptable if it preserves these properties without unnecessary infrastructure.

## 20. LLM/provider abstraction

Provider interface rather than hard-wired model behavior.

LLM uses:
- natural-language extraction;
- ambiguity recognition;
- terminology candidate suggestions;
- explanation/summarization;
- optional plan proposal.

Critical acceptance tests run with deterministic/mock model backend. Live-model evaluation is secondary.

## 21. Observability

Use OTel-compatible tracing where practical.

A run exposes:
- workflow/run ID;
- request revision;
- activity/tool sequence;
- LLM identity + usage where available;
- site query timings;
- policy timings;
- retries/errors;
- evidence refs;
- final action state.

The demo should visibly show that answers are backed by steps/evidence.

## 22. SPEC 3 — Golden + adversarial evaluation suite

Also first-class.

### Goal
Prove correctness at structured boundaries, not merely conversational plausibility.

Initial target: ~100 canonical cases, expandable to 150–200.

Suggested mix:
- 20 cohort/discovery;
- 15 terminology/ambiguity;
- 15 feasibility/counterfactual;
- 10 data quality;
- 10 governance/purpose-of-use;
- 10 provenance/evidence;
- 10 procurement/action;
- 10 adversarial/authorization.

### EvaluationCase contract
Where applicable:
- natural-language input;
- expected ResearchRequest assertions;
- expected mappings/review flags;
- expected raw/per-site counts;
- expected waterfall/exclusions;
- expected quality;
- expected policy + reason codes;
- expected evidence classes/IDs;
- expected proposed action;
- approval requirement;
- expected refusal/denial behavior.

Do not overfit to exact prose. Score structured truth/evidence, and explanation quality separately.

### Hard metrics
Targets:
- structured request parsing >95% on intended unambiguous live-model cases;
- deterministic cohort correctness = 100%;
- deterministic policy correctness = 100%;
- unsupported material factual claims = 0 in deterministic/mock path;
- required provenance completeness = 100%;
- authorization violations = 0;
- correct human escalation >98% for semantic layer;
- replay identity correctness = 100%.

Safety/authorization/correctness are hard gates, not averages.

### Layers

**A — unit/property tests**  
Schemas, mapping, policy, quality, supplier optimization, hashes, state transitions.

**B — adapter conformance**  
Same canonical request yields expected semantics across OMOP/FHIR/flat-file adapters.

**C — deterministic end-to-end mock-model**  
No external model/network; validates complete workflow/action gating.

**D — live-model semantic extraction/explanation**  
Measures request interpretation, ambiguity detection, tool selection, explanation quality, unsupported claims. Freeze exact model/config.

**E — adversarial**  
Include:
- bypass purpose restrictions;
- prompt injection embedded in source/site text;
- raw-identifier request under aggregate/deidentified permission;
- direct procurement submission without approval;
- malformed/unknown schema version;
- fabricated evidence request;
- conflicting terminology;
- stale/replayed approval token;
- mismatched tool result/run/request identity.

### Reporting
Emit machine-readable JSON and Markdown:
- pass/fail by category;
- exact structured diffs;
- unsupported-claim count;
- authorization violations;
- provenance failures;
- model-specific semantic failures;
- regression delta to previous run.

The demo is not green if deterministic critical gates fail.

## 23. Demo UI

Minimal UI:
- chat/request pane;
- parsed request card;
- feasibility waterfall;
- per-site supply;
- policy decision;
- evidence/provenance drill-down;
- procurement plan;
- approval control;
- transaction timeline;
- execution graph/run trace.

All patient/data content clearly labeled synthetic/demo.

## 24. Canonical demo flow

1. Submit canonical NSCLC/KRAS request.
2. Show structured interpretation/assumptions.
3. Federated execution returns per-site counts.
4. Display waterfall to usable count.
5. Ask why Site C loses cases; answer from deterministic exclusion metrics.
6. Change follow-up to 24 months; create new request revision and become infeasible.
7. Relax pathology timing; rerun and change count.
8. Ask for 200 while maximizing institutional diversity.
9. Planner proposes allocation + deterministic cost/time.
10. Stop at approval gate.
11. User approves.
12. Create mock transactions and expose audit trace.

## 25. Public POC security/privacy

- synthetic data only;
- no secrets committed;
- secret scan in CI;
- explicit prompt-injection fixtures;
- no dynamic arbitrary SQL exposed to model;
- typed tool inputs;
- mock-provider support for CI;
- no real external side effects;
- production-like redaction/evidence policies even though data is synthetic.

## 26. Proposed repository layout

```text
research-to-action/
  README.md
  LICENSE
  pyproject.toml
  uv.lock
  package.json
  pnpm-lock.yaml
  mise.toml
  .github/workflows/
  docs/
    spec.md
    architecture.md
    data-fixtures.md
    evaluation.md
    demo-script.md
    threat-model.md
  src/research_to_action/
    api/
    models/
    workflow/
    research/
    terminology/
    federated/
    quality/
    governance/
    provenance/
    procurement/
    audit/
    observability/
    llm/
  sites/
    site_a_omop/
    site_b_fhir/
    site_c_lab/
  fixtures/
    generator/
    manifests/
    policies/
    terminology/
    supplier_offers/
  web/
  evals/
    cases/
    runners/
    reports/
  tests/
    unit/
    integration/
    conformance/
    e2e/
    adversarial/
```

Use moonrepo/mise if consistent with rmax-ai conventions, but tooling must not dominate the POC.

## 27. Complete POC acceptance

### Architecture
- versioned Pydantic models for critical boundaries;
- inspectable/replayable workflow;
- model cannot bypass site/policy/action gates;
- critical deterministic services tested.

### Synthetic network
- three heterogeneous reproducible sites;
- canonical request returns frozen truth;
- adapter conformance passes;
- intentional quality/governance/missingness conflicts tested;
- no real PHI.

### Research / feasibility
- canonical NL request compiles to validated request;
- expected per-site counts;
- correct waterfall/exclusion reasons;
- at least two counterfactual reruns;
- terminology ambiguity can yield REVIEW_REQUIRED.

### Governance
- deterministic versioned ALLOW/DENY/REVIEW;
- purpose enforced;
- unauthorized release/action blocked;
- procurement requires approval.

### Provenance
- final count and at least one patient-level fact trace to exact source fixture + transformations;
- run records contain data/policy/ontology/workflow identities;
- replay succeeds.

### Procurement
- planner fulfills canonical 200;
- objective changes alter allocation where expected;
- mock orders only after approval;
- audit timeline preserved.

### Evaluation
- ~100 initial canonical cases;
- deterministic cohort correctness 100%;
- deterministic policy correctness 100%;
- authorization violations 0;
- required provenance completeness 100%;
- unsupported material claims 0 in deterministic/mock suite;
- live-model results separate with exact model identity.

### Engineering
- tests/lint/type checks green;
- CI does not depend on live paid providers;
- public secret/history scan clean;
- one-command local demo documented.

## 28. Epic breakdown

### E1 — Contracts, workflow skeleton, provenance foundation
Typed models, run identity, durable/inspectable workflow shell, mock LLM/tool interfaces, evidence/event model, CI.

### E2 — Three-site synthetic/federated clinical network
Site A OMOP, Site B FHIR, Site C messy lab; deterministic oncology fixtures; truth manifests; adapters; conformance/counterfactual tests.

### E3 — Research intake, terminology, query compilation
NL -> ResearchRequest, ambiguity representation, terminology mapping/review, immutable revisions, execution-plan compilation.

### E4 — Cohort discovery, feasibility, quality, provenance
Cross-site execution, waterfall, exclusion attribution, counterfactuals, quality metrics, claim/evidence drill-down.

### E5 — Governance and approval gates
Purpose-of-use policy, ALLOW/DENY/REVIEW, authorization boundaries, approval objects, bypass/adversarial tests.

### E6 — Procurement and simulated transaction
Supplier fixtures, multi-objective allocation, deterministic cost/time, approval-gated mock orders, transaction audit state.

### E7 — Golden/adversarial evaluation harness
~100 cases, deterministic/mock suite, live-model hooks, regression reports, hard gates for correctness/authorization/provenance.

### E8 — Demo UI, observability, end-to-end narrative
Minimal web UI, execution graph, OTel-compatible traces, evidence drill-down, approval flow, canonical demo script.

## 29. Dependency order

```text
E1
├─> E2
├─> E3
│    └─> E4
│         ├─> E5
│         └─> E6 (also depends on E5)
└─> E7 starts early on contracts, expands as E2-E6 land

E8 depends on usable vertical slice from E4-E6 and E7 smoke/e2e coverage.
```

Favor early vertical slices. E2 and early E7 may proceed in parallel after E1 if worker capacity permits.

## 30. Definition of success

The POC succeeds when a reviewer can inspect the canonical demo and conclude:

> This system can translate biomedical intent into a governed transaction over heterogeneous clinical data, and every critical decision can be tested, replayed, and audited.

It does not succeed merely because the conversational answer sounds medically plausible.
