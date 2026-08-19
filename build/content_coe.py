"""Page content for the COE documentation section."""

COE_SECTIONS = [
    ("Introduction", [("", "Overview"), ("concepts", "How it works")]),
    (
        "Reference",
        [
            ("mention-context", "Mention context"),
            ("matching", "Phrase matching"),
            ("outputs", "Outputs"),
        ],
    ),
    (
        "Operating COE",
        [
            ("quickstart", "Quickstart"),
            ("privacy", "Privacy controls"),
            ("curation", "Curation"),
            ("cli", "Command reference"),
        ],
    ),
]

COE_PAGES: dict[str, dict[str, str]] = {}

COE_PAGES[""] = {
    "nav": "Overview",
    "title": "COE — Corpus Ontology Enricher",
    "description": (
        "COE is an offline system that matches phrases in clinical text to pinned terminology "
        "releases and reports coding frequency, mention context, unmapped terms, and "
        "co-occurrence."
    ),
    "h1": "COE",
    "standfirst": (
        "An offline system that reads a fixed snapshot of clinical text, matches phrases "
        "against pinned terminology releases, and reports what was coded, in what context, "
        "and what could not be matched at all."
    ),
    "body": """
<dl class="facts">
  <div><dt>Version</dt><dd>0.4.0 alpha</dd></div>
  <div><dt>Runtime</dt><dd>Python 3.11+</dd></div>
  <div><dt>Dependencies</dt><dd>None at runtime</dd></div>
  <div><dt>Network</dt><dd>Never used</dd></div>
  <div><dt>License</dt><dd>Apache 2.0</dd></div>
</dl>

<h2>The question it answers</h2>

<p>Given a body of clinical notes and a set of terminology releases, which codes does that
text actually support, how often, and in what clinical sense? And — usually more useful —
which frequent clinical phrases match no code at all?</p>

<p>That last output is the point. A term appearing hundreds of times with no matching code is
either a gap in the terminology, a local abbreviation worth adding as a synonym, or a
documentation habit nobody has written down. All three are findings.</p>

<h2>What makes the counts trustworthy</h2>

<p>Three properties, each of which rules out a specific way this kind of analysis usually goes
wrong.</p>

<h3>A negated mention is never counted as a finding</h3>

<p>"No evidence of myocardial infarction" contains the phrase, and a naive counter records a
heart attack. COE assigns every mention exactly one context label, so affirmed, negated,
family-history, and historical mentions partition cleanly instead of collapsing into one
number. See <a href="/coe/mention-context/">mention context</a>.</p>

<h3>Every code returned exists in the release it claims</h3>

<p>Matching is exact-first with a small set of deterministic variants. A variant adds a
dictionary lookup; it never fabricates a code. If a code appears in the output, it is present
in the pinned release, and verification re-checks that afterwards. See
<a href="/coe/matching/">phrase matching</a>.</p>

<h3>The same inputs produce the same outputs</h3>

<p>No model, no embeddings, no network, no clock-dependent behaviour. A run is bound to an
immutable snapshot, pinned releases, a configuration version, and a curation snapshot. Re-running
reproduces the result, and <code>coe protected verify</code> checks an output against the same
releases independently.</p>

<h2>What it is not</h2>

<p>It is not a publication system and not a clinical decision system. Three limits are stated
in the software itself rather than buried in caveats:</p>

<ul>
  <li><strong>Candidate evidence is not acceptance.</strong> A discovered mapping stays pending
  until a human records a decision.</li>
  <li><strong>Coding counts are evidence about text, not clinical prevalence.</strong> They
  describe documentation behaviour, not disease frequency.</li>
  <li><strong>Association rows describe co-mention, not clinical relationship.</strong> Two
  codes appearing together may share a cause, a template, or nothing at all.</li>
</ul>

<p>Context qualification is a deliberately conservative screen over text, not a grammatical
parser. It cannot resolve nested or long-range scope, so an affirmed count remains lexical
evidence rather than a confirmed finding.</p>

<h2>Licensed terminologies</h2>

<div class="caution">
  <span class="label">Not in this repository</span>
  <p>No terminology release, publisher package, or derived index is distributed here. The public
  tree is code, schemas, and a synthetic demonstration set containing no patient data. Reference
  indexes are built locally on a machine that already holds the licensed files, under an
  explicit entitlement assertion.</p>
</div>

<div class="note">
  <span class="label">Start here</span>
  <p><a href="/coe/quickstart/">Quickstart</a> runs the synthetic slice end to end in four
  commands. <a href="/coe/concepts/">How it works</a> explains the execution profiles and the
  pipeline.</p>
</div>
""",
}

COE_PAGES["concepts"] = {
    "nav": "How it works",
    "title": "How it works — COE",
    "description": (
        "COE's three execution profiles, the pipeline from snapshot to output, and what binds "
        "a result to the inputs that produced it."
    ),
    "h1": "How it works",
    "standfirst": (
        "Three deliberately separate execution profiles, one pipeline, and a provenance chain "
        "that makes a result reproducible and checkable after the fact."
    ),
    "body": """
<h2>Three execution profiles</h2>

<p>They are separate because they carry different risk. Keeping them apart means the profile
that touches real records cannot be started casually, and the profile used for development
cannot touch anything sensitive.</p>

<div class="tw"><table>
  <thead><tr><th>Profile</th><th>Input</th><th>Purpose</th></tr></thead>
  <tbody>
    <tr>
      <td><strong>Synthetic slice</strong></td>
      <td>Generated fixtures, no patient data</td>
      <td>Deterministic regression testing and a complete worked example of the review
      workflow. This is what the public demo runs</td>
    </tr>
    <tr>
      <td><strong>Reference importer</strong></td>
      <td>Licensed terminology files on an entitled machine</td>
      <td>Builds immutable local indexes, pinned by checksum and row count. Never redistributed</td>
    </tr>
    <tr>
      <td><strong>Protected local runner</strong></td>
      <td>Approved plain-text corpus on an authorised host</td>
      <td>Produces the aggregate enrichment outputs under suppression and scrubbing</td>
    </tr>
  </tbody>
</table></div>

<h2>The pipeline</h2>

<ol>
  <li><strong>Snapshot.</strong> An immutable input set. Nothing downstream re-reads the
  original source, so a run cannot be affected by a file changing mid-analysis.</li>
  <li><strong>Mining.</strong> Sentences are split, then phrases are enumerated up to four
  tokens. A single newline is treated as soft, so hard-wrapped clinical text keeps its
  phrases; blank lines, terminal punctuation, and bullets split.</li>
  <li><strong>Context qualification.</strong> Each mention is labelled affirmed, negated,
  family, or historical — see <a href="/coe/mention-context/">mention context</a>.</li>
  <li><strong>Matching.</strong> Each phrase is resolved against the pinned releases,
  exact-first — see <a href="/coe/matching/">phrase matching</a>.</li>
  <li><strong>Aggregation.</strong> Document-level counts per code and context, plus
  co-occurrence pairs scored for association strength.</li>
  <li><strong>Privacy filtering.</strong> Small cells are suppressed and risky text is
  rejected before anything is written — see <a href="/coe/privacy/">privacy controls</a>.</li>
  <li><strong>Atomic write.</strong> Seven files, written together or not at all, with a run
  report carrying provenance and privacy counters.</li>
</ol>

<h2>What binds a result to its inputs</h2>

<p>A run is bound to four things, all recorded in the run report:</p>

<ul>
  <li>The snapshot identity — which text was analysed</li>
  <li>The terminology release identities — which code sets, at which versions</li>
  <li>The algorithm and configuration version — how it was analysed</li>
  <li>The curation snapshot — which human decisions were in force</li>
</ul>

<p>Verification re-derives the artefact and semantic digests, re-checks that every emitted code
is present in the supplied releases, confirms that no candidate term was actually groundable,
and confirms the suppression floor and scrub rules were honoured. It requires exactly the
releases the run was bound to, so verifying against a different vocabulary version fails rather
than passing quietly.</p>

<h2>Deliberate constraints</h2>

<div class="tw"><table class="tight">
  <thead><tr><th>Constraint</th><th>Reason</th></tr></thead>
  <tbody>
    <tr><td>No network, ever</td><td>Clinical text must not leave the host, and a run must not depend on a service being reachable</td></tr>
    <tr><td>No generative model</td><td>Every code must be traceable to a dictionary lookup in a pinned release</td></tr>
    <tr><td>No automatic acceptance</td><td>A discovered mapping is a candidate until a human records a decision</td></tr>
    <tr><td>No runtime dependencies</td><td>Fewer moving parts on a locked-down host, and a smaller supply-chain surface</td></tr>
    <tr><td>Exact matching runs on the processor</td><td>Dictionary lookup gains nothing from a graphics card; the release does not pretend otherwise</td></tr>
  </tbody>
</table></div>

<h2>Bounded, by design</h2>

<p>Current ceilings are 10,000 files and 100,000,000 input bytes. That makes this a qualification
slice rather than a full-corpus production engine. Larger approved corpora need a tested
partition and checkpoint design, not a raised limit — the limits exist so that resource
exhaustion fails early and visibly instead of midway through a long run.</p>
""",
}

COE_PAGES["mention-context"] = {
    "nav": "Mention context",
    "title": "Mention context — COE",
    "description": (
        "How COE separates affirmed, negated, family-history, and historical mentions, "
        "including precedence, scope rules, and stated limits."
    ),
    "h1": "Mention context",
    "standfirst": (
        "Every mention receives exactly one context label, so counts partition cleanly and a "
        "ruled-out diagnosis is never reported as a current finding."
    ),
    "body": """
<h2>The four labels</h2>

<div class="tw"><table>
  <thead><tr><th>Label</th><th>Meaning</th><th>Example</th></tr></thead>
  <tbody>
    <tr>
      <td><code>current_clinical</code></td>
      <td>Affirmed, about the patient, present — the clinical default</td>
      <td>"Patient reports fever"</td>
    </tr>
    <tr>
      <td><code>negated</code></td>
      <td>The text asserts the concept is absent</td>
      <td>"No evidence of fever", "denies chest pain", "ruled out"</td>
    </tr>
    <tr>
      <td><code>non_patient</code></td>
      <td>The mention belongs to a family member or other person</td>
      <td>"Family history of diabetes", "mother had breast cancer"</td>
    </tr>
    <tr>
      <td><code>historical</code></td>
      <td>The patient's past rather than the present</td>
      <td>"History of stroke", "status post appendectomy", "prior heart attack"</td>
    </tr>
  </tbody>
</table></div>

<p>Exactly one label per mention. Because they partition, affirmed, negated, family, and
historical counts for a code sum to its total mentions — so a suspiciously high count can be
decomposed instead of merely doubted.</p>

<h2>Precedence</h2>

<p>When more than one rule could apply, the order is:</p>

<pre><code>negated &gt; non_patient &gt; historical &gt; current_clinical</code></pre>

<p>The reasoning is that the strongest claim wins. "No family history of diabetes" is, first and
foremost, not an assertion about the patient — labelling it family-history would leave it
counted as evidence that someone had diabetes. Negation is therefore checked first.</p>

<h2>Scope</h2>

<p>Three mechanisms bound how far a trigger reaches:</p>

<h3>Sentence and distance</h3>

<p>A trigger applies within its sentence and within a bounded number of words. A negation early
in a long sentence does not silently negate a clause far away from it.</p>

<h3>Scope-breaking conjunctions</h3>

<p>Certain conjunctions end a trigger's reach:</p>

<pre><code>"no fever <strong>but</strong> reports cough"
<span class="c">   fever -> negated</span>
<span class="c">   cough -> current_clinical</span></code></pre>

<p>Without this rule the cough would inherit the negation and disappear from the affirmed
counts.</p>

<h3>Section headers</h3>

<p>Record headers scope the block beneath them until a header that resets the context appears.
A code mentioned under <em>Family History:</em> is treated as belonging to a relative until, say,
<em>Assessment:</em> resets the scope. This matters because within such a block the individual
sentences often carry no trigger word at all.</p>

<h2>Stated limits</h2>

<div class="caution">
  <span class="label">This is a screen, not a parser</span>
  <p>The rules are a conservative screen over text. They cannot resolve nested scope or
  long-range dependency, so <code>current_clinical</code> remains lexical evidence rather than a
  confirmed clinical finding. Treat an affirmed count as a well-filtered starting point for
  review, not as a diagnosis rate.</p>
</div>

<p>Concretely, the following are not handled reliably: negation spanning more than one sentence;
hypothetical and conditional framing ("if the fever returns"); uncertainty ("possible
pneumonia"), which is not currently a separate label; and attribution to a third party who is
not a family member.</p>

<h2>Why it changes the numbers</h2>

<p>Consider one sentence: <em>"Prior heart attack, no current chest pain, family history of
diabetes."</em></p>

<div class="tw"><table class="tight">
  <thead><tr><th>Concept</th><th>Naive count</th><th>With context</th></tr></thead>
  <tbody>
    <tr><td>Myocardial infarction</td><td>1 current</td><td>1 <code>historical</code></td></tr>
    <tr><td>Chest pain</td><td>1 current</td><td>1 <code>negated</code></td></tr>
    <tr><td>Diabetes</td><td>1 current</td><td>1 <code>non_patient</code></td></tr>
  </tbody>
</table></div>

<p>A naive counter reports three current findings. All three are wrong, and none of them looks
wrong in a summary table.</p>

<h2>Effect on published synonyms</h2>

<p>Only affirmed surface forms become published labels in a concept-scheme export. A term seen
solely in negated or family context is evidence about how the corpus is written, not a synonym
worth asserting about the concept — so it is retained in the context breakdown and excluded
from the exported labels.</p>
""",
}

COE_PAGES["matching"] = {
    "nav": "Phrase matching",
    "title": "Phrase matching — COE",
    "description": (
        "How COE resolves a phrase to a code: exact-first, deterministic variants only, and no "
        "fabricated codes."
    ),
    "h1": "Phrase matching",
    "standfirst": (
        "Exact matching first, then a small set of deterministic variants. A variant adds a "
        "dictionary lookup; it never invents a code that is absent from the pinned release."
    ),
    "body": """
<h2>The guarantee</h2>

<p>Every code in the output exists in the terminology release the output names. This is the
property the whole design protects, and verification re-checks it independently against the same
releases afterwards.</p>

<p>The distinction that matters: a variant changes <em>what is looked up</em>, never
<em>what may be returned</em>. Expanding an abbreviation produces another dictionary query; if
that query finds nothing, nothing is emitted.</p>

<h2>Resolution order</h2>

<ol>
  <li><strong>Exact.</strong> The phrase as written, case-folded, against preferred terms and
  aliases.</li>
  <li><strong>Punctuation-compacted.</strong> Handles differences in hyphenation and spacing
  between text and terminology.</li>
  <li><strong>Curated abbreviation.</strong> A closed, hand-checked map of unambiguous clinical
  abbreviations — for example an abbreviation for hypertension resolving to a release's
  hypertension designation.</li>
  <li><strong>Conservative singularisation.</strong> Plural to singular, only where the
  transformation is unambiguous.</li>
</ol>

<p>Each attempt records how the match was made, so an output row states not just which code was
matched but by what route:</p>

<div class="tw"><table class="tight">
  <thead><tr><th>match_method</th><th>Meaning</th></tr></thead>
  <tbody>
    <tr><td><code>exact</code></td><td>Matched a preferred term directly</td></tr>
    <tr><td><code>exact_alias</code></td><td>Matched a published alias or synonym</td></tr>
    <tr><td><code>variant_abbreviation</code></td><td>Matched after expanding a curated abbreviation</td></tr>
  </tbody>
</table></div>

<p>This makes the aggressiveness of matching auditable. If a reviewer distrusts abbreviation
expansion, those rows can be isolated and inspected rather than taken on trust.</p>

<h2>The abbreviation map is closed</h2>

<p>Abbreviations are only expanded where the expansion is unambiguous in clinical text, and the
map is curated by hand. This is intentionally restrictive: many clinical abbreviations are
genuinely ambiguous, and guessing between meanings would produce confident, wrong codes. An
ambiguous abbreviation is better left unmatched, where it surfaces as a candidate term for
review.</p>

<h2>Ambiguity is reported, not resolved</h2>

<p>When a phrase resolves to more than one code within a single system, COE does not choose. The
mention is recorded in the ambiguity counts for that system and excluded from the coding counts,
so an ambiguous phrase never inflates the count of one arbitrary winner.</p>

<p>Ambiguity counts are a useful signal in themselves: a phrase that is persistently ambiguous
is a candidate for a local curation decision.</p>

<h2>Sentence and phrase boundaries</h2>

<p>Clinical text is frequently hard-wrapped at a fixed column, which naive sentence splitting
mistakes for sentence ends and thereby destroys phrases spanning the break. COE treats a single
newline as soft. Blank lines, terminal punctuation, and bullet lines split.</p>

<p>Phrases are enumerated up to four tokens, which covers most multi-word clinical terms while
keeping the candidate set bounded.</p>

<h2>Unmapped terms</h2>

<p>Frequent phrases that resolve to nothing are ranked by salience — frequency weighted against
how distinctive the term is across documents — and reported as candidate terms with their
affirmed-mention count.</p>

<p>Verification asserts that no reported candidate term is in fact groundable in the supplied
releases. If a term could have been matched, its presence in the candidate list is a defect, and
verification fails rather than letting a false gap stand.</p>

<div class="note">
  <span class="label">No embedding stage</span>
  <p>There is no semantic or vector matching. A term that means the same thing in different
  words will not be matched, and will appear as a candidate. That is the intended behaviour: a
  human decides whether it is a synonym, and the decision is recorded.</p>
</div>
""",
}

COE_PAGES["outputs"] = {
    "nav": "Outputs",
    "title": "Outputs — COE",
    "description": (
        "The seven files a protected COE run writes, what each contains, and which two carry "
        "corpus text."
    ),
    "h1": "Outputs",
    "standfirst": (
        "The protected runner writes seven files atomically — together or not at all. Two of "
        "them can carry text from the corpus, and only when explicitly attested."
    ),
    "body": """
<div class="note">
  <span class="label">Two profiles, two output shapes</span>
  <p>This page documents the <strong>protected runner</strong>, which produces the aggregate
  enrichment results. The synthetic slice run by <code>coe run</code> writes a different set —
  <code>matches.jsonl</code>, <code>candidate_sets.jsonl</code>,
  <code>phrase_aggregates.jsonl</code>, <code>unmapped.jsonl</code>, plus a run manifest,
  artefact manifest, and run report — because it exists to exercise the pipeline
  deterministically rather than to produce a privacy-filtered deliverable.</p>
</div>

<h2>The seven files</h2>

<div class="tw"><table>
  <thead><tr><th>File</th><th>Contains</th><th>Corpus text</th></tr></thead>
  <tbody>
    <tr>
      <td><code>coding_counts.jsonl</code></td>
      <td>Uniquely grounded codings with document frequency, across every context</td>
      <td>No</td>
    </tr>
    <tr>
      <td><code>ambiguity_counts.jsonl</code></td>
      <td>Per-system counts where a phrase resolved to more than one code</td>
      <td>No</td>
    </tr>
    <tr>
      <td><code>context_counts.jsonl</code></td>
      <td>The context breakdown per code — affirmed, negated, family, historical</td>
      <td>No</td>
    </tr>
    <tr>
      <td><code>lexical_forms.jsonl</code></td>
      <td>Surface forms observed per code and context, with match method</td>
      <td><strong>Yes</strong></td>
    </tr>
    <tr>
      <td><code>candidate_terms.jsonl</code></td>
      <td>Ranked frequent unmapped terms with salience and affirmed count</td>
      <td><strong>Yes</strong></td>
    </tr>
    <tr>
      <td><code>associations.jsonl</code></td>
      <td>Code co-occurrence pairs, scored, from affirmed mentions only</td>
      <td>No</td>
    </tr>
    <tr>
      <td><code>run_report.json</code></td>
      <td>Provenance, software identity, privacy counters, digests</td>
      <td>No</td>
    </tr>
  </tbody>
</table></div>

<div class="caution">
  <span class="label">The two lexical files</span>
  <p><code>lexical_forms.jsonl</code> and <code>candidate_terms.jsonl</code> contain text drawn
  from the corpus. They are empty unless the attestation sets lexical output approved, and they
  are the two files to review before any transfer.</p>
</div>

<h2>Coding counts</h2>

<p>The primary result: for each code that a phrase resolved to unambiguously, how many documents
mention it. Counts are per document, not per mention, so a term repeated within one note does not
inflate the figure.</p>

<p>The count spans every context. To separate affirmed from negated, join against the context
counts — the two files are deliberately separate so that a total can never be silently mistaken
for an affirmed total.</p>

<h2>Context counts</h2>

<p>One row per code and context label. Because the labels partition, these sum to the code's
total mentions, which makes the coding count decomposable rather than opaque.</p>

<h2>Lexical forms</h2>

<p>Which words in the corpus actually produced each code, per context, with the match method
recorded. This is the synonym evidence, and the most direct answer to "what do clinicians here
actually write?"</p>

<p>Only affirmed forms become published labels in a concept-scheme export; a form seen solely in
negated or family context stays here as corpus evidence.</p>

<h2>Candidate terms</h2>

<p>Frequent phrases that matched nothing, ranked by salience and reported with their
affirmed-mention count. Verification asserts none of them was actually groundable.</p>

<h2>Associations</h2>

<p>Code pairs that co-occur more than chance would predict, computed from affirmed mentions only
so that negated and family mentions cannot manufacture an association.</p>

<div class="caution">
  <span class="label">Co-mention, not relationship</span>
  <p>Two codes appearing together may share a cause, or share a documentation template, or have
  nothing to do with each other. These rows are a starting point for a question, not an answer.</p>
</div>

<h2>Run report</h2>

<p>Restricted, path-free provenance: software identity, snapshot and release identities, the
privacy counters (how many rows were suppressed, how many scrubbed), resource totals, and the
digests verification re-derives. Deliberately free of file paths, hostnames, and usernames so
that the report itself can be reviewed without disclosing anything about the host.</p>

<h2>Export formats</h2>

<pre><code>coe export csv  --run /restricted/run/output --output /restricted/run/csv
coe export skos --run /restricted/run/output --output /restricted/run/scheme.ttl</code></pre>

<p>The concept-scheme export emits one concept per coding row, the code as its notation,
affirmed surface forms as preferred and alternative labels, associations as related concepts, and
each concept's affirmed document count as an annotation.</p>

<div class="note">
  <span class="label">Classification is inherited</span>
  <p>An export of a protected run carries the same restriction as the run it came from.
  Converting the format does not change what the data is.</p>
</div>
""",
}

COE_PAGES["quickstart"] = {
    "nav": "Quickstart",
    "title": "Quickstart — COE",
    "description": (
        "Install COE and run the synthetic slice end to end, with no patient data and no "
        "licensed terminology files."
    ),
    "h1": "Quickstart",
    "standfirst": (
        "The synthetic profile runs end to end with no patient data and no licensed "
        "terminology files. It is the intended way to evaluate COE."
    ),
    "body": """
<h2>Requirements</h2>

<ul>
  <li>Python 3.11 or newer</li>
  <li><a href="https://docs.astral.sh/uv/">uv</a> for development commands</li>
  <li>No network access needed after install, and none used at runtime</li>
</ul>

<h2>Install and test</h2>

<pre><code>git clone https://github.com/gegesay89/coe-corpus-ontology-enricher.git
cd coe-corpus-ontology-enricher
uv sync --extra dev
uv run ruff format --check .
uv run ruff check .
uv run pytest</code></pre>

<p>The suite covers context qualification, matching variants, curation chaining, the privacy
floor, export shapes, and an end-to-end grounding smoke test. One Windows-specific test skips
where no PowerShell parser is available.</p>

<h2>Run the synthetic slice</h2>

<pre><code>uv run coe demo create demo
uv run coe preflight snapshot demo/snapshot
uv run coe preflight reference demo/reference --environment synthetic
uv run coe run \\
  --snapshot demo/snapshot \\
  --reference demo/reference \\
  --config demo/coe_config.json \\
  --curation-snapshot genesis-v0 \\
  --output out</code></pre>

<div class="tw"><table class="tight">
  <thead><tr><th>Command</th><th>Does</th></tr></thead>
  <tbody>
    <tr><td><code>demo create</code></td><td>Writes a synthetic snapshot, reference set, and configuration</td></tr>
    <tr><td><code>preflight snapshot</code></td><td>Validates the input contract without analysing anything</td></tr>
    <tr><td><code>preflight reference</code></td><td>Validates the reference set for the synthetic environment</td></tr>
    <tr><td><code>run</code></td><td>Executes the deterministic slice into <code>out/</code></td></tr>
  </tbody>
</table></div>

<p>Preflight exists so a contract problem is reported before any analysis begins, rather than
surfacing halfway through a long run.</p>

<h2>Check the capability report</h2>

<pre><code>uv run coe hardware probe</code></pre>

<p>Emits a sanitised runtime capability report — deliberately free of hostnames, usernames, and
paths, so it can be attached to a support request. Exact phrase mining and dictionary lookup run
on the processor by design; passing <code>--require-nvidia</code> fails closed if a graphics card
cannot be confirmed, rather than silently continuing.</p>

<p>The synthetic profile demonstrates the full pipeline without patient data. Its outputs are
described on the <a href="/coe/outputs/">outputs</a> page.</p>

<h2>Reproducibility</h2>

<p>Run the slice twice into different directories and the analytical outputs match, because
there is no model, no network, and no clock-dependent behaviour. This is the property the
synthetic profile exists to protect: a change in output means a change in code or inputs, never
noise.</p>

<h2>What comes next</h2>

<p>Two things separate the demo from real use, and both are deliberate gates:</p>

<ul>
  <li><strong>A reference set</strong> built from licensed terminology files on an entitled
  machine, under a recorded entitlement assertion.</li>
  <li><strong>An attestation</strong> naming the approval, retention policy, and output
  classification for the corpus — see <a href="/coe/privacy/">privacy controls</a>.</li>
</ul>

<div class="note">
  <span class="label">Not included</span>
  <p>This repository contains no terminology release and no patient data. The demo is entirely
  synthetic, which is why it can be public.</p>
</div>
""",
}

COE_PAGES["privacy"] = {
    "nav": "Privacy controls",
    "title": "Privacy controls — COE",
    "description": (
        "COE's suppression floor, scrub filter, association bounds, attestation gate, and the "
        "limits each control does not cover."
    ),
    "h1": "Privacy controls",
    "standfirst": (
        "Four controls applied before anything is written, each recorded in the run report and "
        "re-checked by the verifier. Each is stated with what it does not cover."
    ),
    "body": """
<h2>Small-cell suppression</h2>

<p>Rows whose document count falls below a floor — three by default — are suppressed and
reported only as a count of suppressed rows. The reasoning is that near-unique evidence can
single out an individual: a code appearing in exactly one document, together with a rare surface
form, may identify the patient it came from.</p>

<p>The floor is configurable upward. The count of what was suppressed is always reported, so a
reader can see that filtering occurred and how much.</p>

<h2>Scrub filter</h2>

<p>Any text that would leave the process is rejected if it carries long digit runs, contact
markers, or excessive length. Scrubbed rows are counted, never emitted.</p>

<p>This targets the realistic failure mode for text extracted from clinical notes: a phrase that
has swept up an identifier, a phone number, or a pasted block. The filter is deterministic —
the same text is always rejected — and the counter makes rejection visible.</p>

<h2>Association bounds</h2>

<p>Documents containing more codes than a per-document limit are excluded from association
counting, and the pair table is hard-capped. A single document dense with codes would otherwise
generate a combinatorial number of pairs, both distorting the statistics and creating a
fingerprint of that one document.</p>

<h2>The attestation gate</h2>

<p>A protected run requires a machine-readable data-use attestation naming the approval, the
retention policy, and the output classification. The software validates that the approval is
affirmative and that the classification remains restricted.</p>

<p>Lexical outputs — the two files that can carry corpus text — are emitted only when the
attestation explicitly approves lexical output. Coding counts, ambiguity counts, and association
rows are always aggregate-only.</p>

<div class="caution">
  <span class="label">What the attestation is not</span>
  <p>The file is unsigned and reusable, so it is a procedural fail-closed gate, not proof of
  authorisation. An authorised person must confirm before each run that its references still bind
  to the exact corpus, purpose, host, and validity window. The example attestation shipped with
  the repository is a template and is intentionally not approved.</p>
</div>

<h2>Input handling</h2>

<p>The protected adapter accepts recursively discovered plain-text files only, and rejects links,
junctions, reparse points, hard links, and non-regular files. Inputs are read in place, mounted
read-only, with a separate restricted writable directory for output. Resource limits are bounded
so exhaustion fails early rather than midway.</p>

<p>Documents in other formats need a separately reviewed extraction step that writes plain text
into an approved directory first. COE performs no document conversion and no optical character
recognition, and does not pretend to.</p>

<h2>Limits worth stating plainly</h2>

<ul>
  <li><strong>Suppression and scrubbing are not a de-identification method.</strong> They are
  defence in depth. The data owner must document the approved method and the residual-risk
  decision separately.</li>
  <li><strong>Aggregate output is still treated as restricted.</strong> Even a table of counts
  inherits the classification of the corpus it came from.</li>
  <li><strong>Text exists transiently in process memory,</strong> and the runtime cannot
  guarantee secure erasure. Host access controls, swap and crash-dump policy, disk encryption,
  and retention rules remain mandatory.</li>
  <li><strong>An export inherits its source classification.</strong> Converting to another format
  does not change what the data is.</li>
</ul>

<h2>Verifying afterwards</h2>

<pre><code>coe protected verify \\
  --output /restricted/run/output \\
  --index /path/to/reference/one.sqlite3 \\
  --index /path/to/reference/two.sqlite3</code></pre>

<p>Verification independently re-checks the exact file inventory, canonical encoding, artefact
and semantic digests, run fingerprint, release identities, code grounding — including that no
candidate term was actually groundable — and compliance with both the suppression floor and the
scrub rules.</p>

<p>It requires exactly the releases the run was bound to. Verifying against a different
vocabulary version fails rather than passing quietly, which is the behaviour that makes the check
worth running.</p>
""",
}

COE_PAGES["curation"] = {
    "nav": "Curation",
    "title": "Curation — COE",
    "description": (
        "How COE records human accept and reject decisions as an append-only, hash-chained log "
        "pinned by an immutable snapshot."
    ),
    "h1": "Curation",
    "standfirst": (
        "Discovered mappings are candidates until a person decides. Decisions are recorded as "
        "an append-only, hash-chained log and pinned by an immutable snapshot."
    ),
    "body": """
<h2>Why nothing is auto-accepted</h2>

<p>COE discovers that a phrase in the corpus resolves to a code. That is evidence about the text,
not a ruling that the mapping is clinically correct. Two things are deliberately kept apart:</p>

<div class="tw"><table class="tight">
  <thead><tr><th>Question</th><th>Who answers it</th></tr></thead>
  <tbody>
    <tr><td>Does this code exist in the pinned release?</td><td>The software, and it must always be yes</td></tr>
    <tr><td>Does this phrase genuinely mean this code?</td><td>A human reviewer, recorded by name</td></tr>
  </tbody>
</table></div>

<p>Conflating the two is how a plausible mapping becomes an asserted fact without anyone
deciding. Code validity is mechanical; semantic correctness is a judgement.</p>

<h2>Acceptance states</h2>

<div class="tw"><table class="tight">
  <thead><tr><th>State</th><th>Meaning</th></tr></thead>
  <tbody>
    <tr><td><code>pending</code></td><td>Discovered, no decision recorded — the default</td></tr>
    <tr><td><code>curator_accepted</code></td><td>A named reviewer accepted the mapping</td></tr>
    <tr><td><code>curator_rejected</code></td><td>A named reviewer rejected it</td></tr>
  </tbody>
</table></div>

<p>Anything without a recorded decision stays pending. There is no path by which a candidate
becomes accepted through frequency, score, or repetition.</p>

<h2>Recording a decision</h2>

<pre><code>coe curation decide \\
  --decisions decisions.jsonl \\
  --form "alpha finding" \\
  --system urn:example:system \\
  --release 00000000-0000-4000-8000-000000000001 \\
  --code U1 \\
  --decision accepted \\
  --curator reviewer-1</code></pre>

<p>Each decision names the surface form, the terminology system, the exact release, the code, the
verdict, and the curator. Naming the release matters: accepting a mapping against one version is
not the same as accepting it against a later one.</p>

<h2>The chain</h2>

<p>Decisions are appended to a log where each entry incorporates a hash of the previous one. The
consequence is that history cannot be quietly rewritten — altering or removing an earlier
decision breaks the chain, and the break is detectable.</p>

<p>This matters because curation decisions accumulate authority over time. If a mapping was
accepted two years ago and a result depends on it, the record of who decided, when, and against
which release must be tamper-evident rather than merely present.</p>

<h2>Pinning a snapshot</h2>

<pre><code>coe curation snapshot \\
  --decisions decisions.jsonl \\
  --id review-1 \\
  --scope demo \\
  --output curation_snapshot.json</code></pre>

<p>A snapshot pins the chain at a point in time. Runs reference a snapshot rather than a live
log, so a result cannot shift because someone appended a decision while it was executing.</p>

<h2>Applying decisions to a run</h2>

<pre><code>coe run \\
  --snapshot demo/snapshot \\
  --reference demo/reference \\
  --config demo/coe_config.json \\
  --curation-snapshot curation_snapshot.json \\
  --curation-decisions decisions.jsonl \\
  --output out --overwrite</code></pre>

<p>Decisions in the pinned snapshot are applied on the next run: accepted and rejected mappings
take their recorded state, everything else stays pending. The run report records which curation
snapshot was in force, so a result can always be traced to the decisions behind it.</p>

<div class="note">
  <span class="label">Completable by design</span>
  <p>The workflow has an end state. A reviewer can work through a candidate set, record a
  decision for each, pin a snapshot, and re-run — and the second run reflects exactly those
  decisions. The synthetic profile demonstrates the full cycle without any patient data.</p>
</div>

<h2>What curation does not do</h2>

<p>It does not publish. There is no path from an accepted mapping to an external system, and
acceptance does not create a code — it records a judgement about a code that already exists in a
pinned release.</p>
""",
}

COE_PAGES["cli"] = {
    "nav": "Command reference",
    "title": "Command reference — COE",
    "description": "Every COE command group and subcommand, with the arguments each takes.",
    "h1": "Command reference",
    "standfirst": (
        "Nine command groups. Every command is offline, and every command that writes does so "
        "atomically."
    ),
    "body": """
<pre><code>coe [-h] [--version]
    {demo,preflight,run,curation,export,benchmark,reference,protected,hardware}</code></pre>

<div class="tw"><table class="tight">
  <thead><tr><th>Group</th><th>Purpose</th></tr></thead>
  <tbody>
    <tr><td><code>demo</code></td><td>Manage deterministic synthetic inputs</td></tr>
    <tr><td><code>preflight</code></td><td>Validate input contracts without analysis</td></tr>
    <tr><td><code>run</code></td><td>Run the synthetic deterministic slice</td></tr>
    <tr><td><code>curation</code></td><td>Record and snapshot hash-chained decisions</td></tr>
    <tr><td><code>export</code></td><td>Project run output into interchange formats</td></tr>
    <tr><td><code>benchmark</code></td><td>Bounded, non-semantic performance checks</td></tr>
    <tr><td><code>reference</code></td><td>Manage private licensed reference indexes</td></tr>
    <tr><td><code>protected</code></td><td>Aggregate-only analysis on approved local text</td></tr>
    <tr><td><code>hardware</code></td><td>Emit a sanitised runtime capability report</td></tr>
  </tbody>
</table></div>

<h2>demo</h2>

<pre><code>coe demo create &lt;path&gt;</code></pre>

<p>Creates a synthetic snapshot, reference set, and configuration. No patient data.</p>

<h2>preflight</h2>

<pre><code>coe preflight {snapshot,reference,config,all} &lt;path&gt; [--environment ENV]</code></pre>

<p>Validates an input contract and stops. Use it before a long run so a contract error surfaces
immediately.</p>

<h2>run</h2>

<pre><code>coe run --snapshot SNAPSHOT --reference REFERENCE --config CONFIG
        --curation-snapshot CURATION_SNAPSHOT
        [--curation-decisions DECISIONS]
        --output OUTPUT [--overwrite]</code></pre>

<p>A curation snapshot is required, not optional — a run must always state which decisions were
in force, even if that is the genesis snapshot with none.</p>

<h2>curation</h2>

<pre><code>coe curation decide   --decisions FILE --form FORM --system SYSTEM
                      --release RELEASE --code CODE
                      --decision {accepted,rejected} --curator NAME

coe curation snapshot --decisions FILE --id ID --scope SCOPE --output FILE</code></pre>

<p>See <a href="/coe/curation/">curation</a> for the chaining model.</p>

<h2>reference</h2>

<pre><code>coe reference build-index   <span class="c">-- build one pinned terminology index</span>
coe reference verify-index  <span class="c">-- verify one immutable index</span>
coe reference build-set     <span class="c">-- atomically build every pinned terminology</span>
coe reference verify-set    <span class="c">-- verify a complete index set</span></code></pre>

<p>Building a set is atomic and does not copy raw publisher packages, normalised source files,
access logs, or credentials into the result:</p>

<pre><code>coe reference build-set \\
  --source-dir /approved/path/to/normalized \\
  --spec specs/licensed_terminologies.json \\
  --entitlement governance/terminology_entitlement_assertion.json \\
  --output private_build/references

coe reference verify-set private_build/references</code></pre>

<p>The committed specification pins each release by file name, byte count, row count, checksum,
canonical system identifier, version, effective date, code format, alias policy, and active-status
rule.</p>

<h2>protected</h2>

<pre><code>coe protected run    --corpus DIR --attestation FILE
                     --index INDEX [--index INDEX ...]
                     --output DIR
                     [--min-cell-document-count N]
                     [--max-association-codes-per-document N]

coe protected verify --output DIR --index INDEX [--index INDEX ...]</code></pre>

<p>Between one and seven releases are accepted. Verification requires exactly the releases the run
was bound to. See <a href="/coe/privacy/">privacy controls</a>.</p>

<h2>export</h2>

<pre><code>coe export csv  --run RUN --output DIR
coe export skos --run RUN --output FILE.ttl</code></pre>

<p>Neither adds a runtime dependency. An export inherits the classification of its source run.</p>

<h2>hardware</h2>

<pre><code>coe hardware probe [--require-nvidia]</code></pre>

<p>Sanitised capability report. With the flag, fails closed when a graphics card cannot be
confirmed rather than silently falling back.</p>

<h2>Default limits</h2>

<p>Applied by the protected runner unless overridden:</p>

<div class="tw"><table class="tight">
  <thead><tr><th>Limit</th><th>Default</th></tr></thead>
  <tbody>
    <tr><td>Files</td><td>10,000</td></tr>
    <tr><td>Total input bytes</td><td>100,000,000</td></tr>
    <tr><td>Bytes per file</td><td>10,000,000</td></tr>
    <tr><td>Tokens per file</td><td>250,000</td></tr>
    <tr><td>Phrase length</td><td>4 tokens</td></tr>
    <tr><td>Suppression floor</td><td>3 documents</td></tr>
    <tr><td>Candidate terms reported</td><td>5,000</td></tr>
    <tr><td>Codes per document for associations</td><td>150</td></tr>
  </tbody>
</table></div>

<p>These make the tool a bounded qualification slice rather than a full-corpus engine. Raising
them is not the way to process a larger corpus; a tested partition and checkpoint design is.</p>
""",
}
