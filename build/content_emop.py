"""Page content for the EMOP documentation section."""

EMOP_SECTIONS = [
    ("Introduction", [("", "Overview"), ("data-model", "Design principles")]),
    (
        "Reference",
        [
            ("extension", "Egyptian tables"),
            ("tables", "Core tables"),
            ("vocabularies", "Reference data"),
        ],
    ),
    (
        "Using EMOP",
        [
            ("install", "Installation"),
            ("crosswalk", "International research"),
            ("interoperability", "Interoperability"),
        ],
    ),
]

EMOP_PAGES: dict[str, dict[str, str]] = {}

EMOP_PAGES[""] = {
    "nav": "Overview",
    "title": "EMOP — Egyptian Medical Observational Profile",
    "description": (
        "EMOP is a PostgreSQL data model for observational health records collected in Egypt: "
        "national identifiers, governorates, insurance schemes, referrals, and national code lists."
    ),
    "h1": "EMOP",
    "standfirst": (
        "A data model for observational health records collected in Egypt. It keeps an "
        "established international core intact and adds the facts Egyptian care actually "
        "records, so that neither has to be distorted to accommodate the other."
    ),
    "body": """
<dl class="facts">
  <div><dt>Version</dt><dd>0.1.0</dd></div>
  <div><dt>Database</dt><dd>PostgreSQL 14+</dd></div>
  <div><dt>Tables</dt><dd>39 core, 13 Egyptian</dd></div>
  <div><dt>Foreign keys</dt><dd>194</dd></div>
  <div><dt>License</dt><dd>Apache 2.0</dd></div>
</dl>

<h2>The problem this solves</h2>

<p>Research data models for health records are written around the systems that produced
them. Applied to Egyptian records, several facts have nowhere to go. A patient is identified
by a national identity number, not by a payer member number. Care is delivered across
parallel systems — civil, military, police, and university hospitals — that are funded and
governed differently. Insurance is being restructured around a universal scheme running
alongside the older organisation it replaces. Names are recorded in Arabic, in English, or
in both, and the legal spelling matters. Referral between facilities is a recorded event
with its own priority, not an inference drawn from two consecutive visits.</p>

<p>The usual workaround is to force these into generic observation rows or free-text source
fields. That is lossy in a way that is hard to detect later: the data is present, but its
meaning depends on a convention that lives in someone's head rather than in the schema.</p>

<h2>The approach</h2>

<p>EMOP keeps the international core exactly as published — same table names, same columns,
same grain — and places the Egyptian facts in thirteen dedicated tables beside it. Anyone
who already knows the core can read an EMOP database without learning new names for old
concepts. Anyone who needs the Egyptian detail finds it in a table whose name says what it
holds.</p>

<p>The trade-off is explicit: because the extension tables are additions rather than
reinterpretations, international tooling built for the unmodified core will not see them.
The <a href="/emop/crosswalk/">international research</a> page gives a rule for every
extension table, so a database can be reduced to a standard instance deliberately rather
than by accident.</p>

<h2>What version 0.1 contains</h2>

<ul>
  <li>Complete schema definitions for PostgreSQL — tables, primary keys, foreign keys, indexes</li>
  <li>Thirteen <a href="/emop/extension/">Egyptian extension tables</a> with documented columns</li>
  <li><a href="/emop/vocabularies/">Reference data</a> for the twenty-seven governorates,
      the payer organisations, and the care sectors</li>
  <li>Small illustrative code lists, labelled as such in the data itself</li>
  <li>A fictional patient journey for verifying an installation</li>
  <li>A translation rule for every extension table, and an
      <a href="/emop/interoperability/">interoperability mapping</a></li>
</ul>

<h2>What it is not</h2>

<p>It is not an official publication of any Egyptian authority, and it does not carry
official Ministry of Health, universal insurance, or health insurance organisation code
lists. The illustrative codes shipped with it exist so the model can be read and installed,
and every one of them is flagged in the data. It is not a clinical system, and it holds no
patient data.</p>

<div class="note">
  <span class="label">Start here</span>
  <p><a href="/emop/install/">Installation</a> takes an empty database to a populated schema
  in four commands. <a href="/emop/data-model/">Design principles</a> explains the rules the
  schema follows and why.</p>
</div>
""",
}

EMOP_PAGES["data-model"] = {
    "nav": "Design principles",
    "title": "Design principles — EMOP",
    "description": (
        "The four rules EMOP follows: keep core table names, add rather than overload, "
        "reserve the local concept range, and never invent an official code."
    ),
    "h1": "Design principles",
    "standfirst": (
        "Four rules govern every decision in the schema. They exist so that a reader can "
        "predict where a fact lives, and so that a claim about the data can be checked "
        "against the database rather than against documentation."
    ),
    "body": """
<h2>1. Core table names do not change</h2>

<p><code>person</code> is <code>person</code>. <code>visit_occurrence</code> is
<code>visit_occurrence</code>. Every core table keeps its published name, columns, and grain,
because renaming would impose a translation cost on every reader and every existing extract
script while adding no information.</p>

<p>A practical consequence: extract logic written against the standard core runs against an
EMOP database unmodified, provided it does not require the extension tables.</p>

<h2>2. Add tables rather than overload existing ones</h2>

<p>National identity numbers do not go into a source-value column that also holds something
else. Insurance scheme membership does not become an untyped observation row. Each Egyptian
fact gets a table whose name and columns state its meaning.</p>

<p>The cost is more tables. The benefit is that meaning is enforced by structure: a foreign
key either exists or it does not, and a column either has a value or it does not. Neither
depends on a convention that has to be remembered.</p>

<div class="note">
  <span class="label">Why this matters</span>
  <p>Overloaded columns fail quietly. If national identity numbers and hospital numbers share
  one field, a query counting patients by identifier type cannot distinguish them, and the
  error surfaces as a plausible-looking number rather than as an exception.</p>
</div>

<h2>3. Local concepts live at 2,000,000,000 and above</h2>

<p>The convention in the international model reserves concept identifiers at and above two
billion for concepts defined by a local site. EMOP follows it. Illustrative concepts shipped
with this release occupy that range, so they can never collide with a standard vocabulary
loaded later.</p>

<p>Identifier <code>0</code> is also populated, with the conventional
<em>No matching concept</em> row, because the published foreign-key constraints reference
it.</p>

<h2>4. An official code is never invented</h2>

<p>This is the rule with the most consequence for how the release is shipped. Publishing
plausible-looking Ministry of Health or insurance authority codes would make the model
unusable for the exact audience it targets, because a reader could not tell which codes were
real. So the schema for national code lists is complete, and the codes populating it are
labelled.</p>

<p>Three states are distinguished, and all three are visible in the data:</p>

<div class="tw"><table>
  <thead><tr><th>State</th><th>Flag</th><th>Example</th></tr></thead>
  <tbody>
    <tr>
      <td>Invented for illustration</td>
      <td><code>example_not_official = true</code>, code prefixed <code>EX-</code></td>
      <td><code>EX-MOH-PROC-001</code></td>
    </tr>
    <tr>
      <td>Published code, illustrative label</td>
      <td><code>example_not_official = false</code>, <code>official_status</code> records the nuance</td>
      <td><code>E11.9</code> with an Arabic translation</td>
    </tr>
    <tr>
      <td>Published reference data</td>
      <td><code>example_not_official = false</code></td>
      <td>Governorate code <code>EG-C</code></td>
    </tr>
  </tbody>
</table></div>

<p><a href="/emop/vocabularies/">Reference data</a> lists what ships in each state.</p>

<h2>Naming conventions</h2>

<ul>
  <li>Extension tables use singular nouns matching core style: <code>governorate</code>,
      <code>referral</code>.</li>
  <li>A table extending exactly one core table one-to-one is named
      <code>&lt;core&gt;_extension</code> and takes the core primary key as its own — see
      <code>facility_extension</code>.</li>
  <li>Bilingual columns are suffixed <code>_en</code> and <code>_ar</code>.</li>
  <li>Every table that can carry illustrative rows has an
      <code>example_not_official</code> boolean.</li>
</ul>

<h2>Versioning</h2>

<p>The deployed model records its own version in <code>emop_cdm_source</code>, alongside the
version of the international core it was built against. A database can therefore state what
it is without reference to external documentation, which matters when an extract outlives the
person who produced it.</p>
""",
}

EMOP_PAGES["extension"] = {
    "nav": "Egyptian tables",
    "title": "Egyptian extension tables — EMOP",
    "description": (
        "Column-level reference for the thirteen Egyptian tables: identity, geography, "
        "facilities, insurance, care sector, referral, bilingual names, and national codes."
    ),
    "h1": "Egyptian extension tables",
    "standfirst": (
        "Thirteen tables, grouped by the question each one answers. Every column is listed "
        "with its type and its meaning; every foreign key names the table it points at."
    ),
    "body": """
<p>All thirteen live in schema <code>emop</code> beside the core tables and are created by
<code>ddl/emop_extension.sql</code>. Apply that file after the core schema and its primary
keys, since several of these tables reference core tables.</p>

<div class="tw"><table class="tight">
  <thead><tr><th>Group</th><th>Tables</th></tr></thead>
  <tbody>
    <tr><td>Identity</td><td><code>national_identifier</code>, <code>person_name_bilingual</code></td></tr>
    <tr><td>Geography and facilities</td><td><code>governorate</code>, <code>facility_extension</code></td></tr>
    <tr><td>Payment</td><td><code>insurance_scheme</code>, <code>person_insurance</code></td></tr>
    <tr><td>Care delivery</td><td><code>care_sector</code>, <code>referral</code>, <code>visit_care_context</code></td></tr>
    <tr><td>Terminology</td><td><code>source_vocabulary</code>, <code>source_code</code>, <code>source_code_omop_map</code></td></tr>
    <tr><td>Metadata</td><td><code>emop_cdm_source</code></td></tr>
  </tbody>
</table></div>

<h2>Identity</h2>

<h3>national_identifier</h3>

<p>One row per identifier held by a person, so a patient with a national identity number and
a passport has two rows rather than one overloaded field.</p>

<div class="tw"><table>
  <thead><tr><th>Column</th><th>Type</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td><code>national_identifier_id</code></td><td>integer</td><td>Primary key</td></tr>
    <tr><td><code>person_id</code></td><td>integer</td><td>References <code>person</code>, required</td></tr>
    <tr><td><code>identifier_type</code></td><td>varchar(64)</td><td><code>national_id</code>, <code>passport</code>, <code>military_id</code>, <code>refugee</code></td></tr>
    <tr><td><code>identifier_type_concept_id</code></td><td>integer</td><td>Optional concept for the type</td></tr>
    <tr><td><code>identifier_source_value</code></td><td>varchar(128)</td><td>The identifier as recorded</td></tr>
    <tr><td><code>valid_start_date</code></td><td>date</td><td>Required</td></tr>
    <tr><td><code>valid_end_date</code></td><td>date</td><td>Null while current</td></tr>
    <tr><td><code>example_not_official</code></td><td>boolean</td><td>Defaults true; public rows are fictional</td></tr>
  </tbody>
</table></div>

<div class="caution">
  <span class="label">Handling</span>
  <p>This table is the most sensitive in the schema. A national identity number identifies a
  person directly and outlives any episode of care. Exclude it from research extracts and
  from anything leaving the source institution — the
  <a href="/emop/crosswalk/">translation rules</a> drop it by default.</p>
</div>

<h3>person_name_bilingual</h3>

<p>One optional row per person. The international core has no name columns by design; this
table exists for operational systems that must reproduce a legal name.</p>

<div class="tw"><table>
  <thead><tr><th>Column</th><th>Type</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td><code>person_id</code></td><td>integer</td><td>Primary key, references <code>person</code></td></tr>
    <tr><td><code>given_name_en</code>, <code>family_name_en</code></td><td>varchar(255)</td><td>Latin script</td></tr>
    <tr><td><code>given_name_ar</code>, <code>family_name_ar</code></td><td>varchar(255)</td><td>Arabic script</td></tr>
    <tr><td><code>preferred_language</code></td><td>varchar(8)</td><td><code>ar</code> or <code>en</code>; defaults <code>ar</code></td></tr>
  </tbody>
</table></div>

<h2>Geography and facilities</h2>

<h3>governorate</h3>

<p>All twenty-seven governorates, each with both name forms, an international subdivision
code, and a regional grouping for aggregate reporting.</p>

<div class="tw"><table>
  <thead><tr><th>Column</th><th>Type</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td><code>governorate_id</code></td><td>integer</td><td>Primary key</td></tr>
    <tr><td><code>governorate_code</code></td><td>varchar(16)</td><td>Short code, unique</td></tr>
    <tr><td><code>governorate_name_en</code>, <code>governorate_name_ar</code></td><td>varchar(255)</td><td>Required</td></tr>
    <tr><td><code>region_name_en</code>, <code>region_name_ar</code></td><td>varchar(255)</td><td>Greater Cairo, Delta, Canal, Sinai, Upper Egypt, Frontier</td></tr>
    <tr><td><code>location_id</code></td><td>integer</td><td>Optional link to core <code>location</code></td></tr>
    <tr><td><code>iso_3166_2</code></td><td>varchar(16)</td><td>For example <code>EG-C</code></td></tr>
    <tr><td><code>example_not_official</code></td><td>boolean</td><td>False — these codes are published</td></tr>
  </tbody>
</table></div>

<h3>facility_extension</h3>

<p>One optional row per <code>care_site</code>, sharing its primary key. Sector is the column
that matters most analytically, because funding and referral behaviour differ sharply between
sectors.</p>

<div class="tw"><table>
  <thead><tr><th>Column</th><th>Type</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td><code>care_site_id</code></td><td>integer</td><td>Primary key and foreign key to <code>care_site</code></td></tr>
    <tr><td><code>moh_facility_code</code></td><td>varchar(64)</td><td>Ministry facility code; illustrative in this release</td></tr>
    <tr><td><code>facility_sector</code></td><td>varchar(32)</td><td><code>public</code>, <code>private</code>, <code>university</code>, <code>military</code>, <code>ngo</code>, <code>police</code></td></tr>
    <tr><td><code>governorate_id</code></td><td>integer</td><td>References <code>governorate</code></td></tr>
    <tr><td><code>urban_rural</code></td><td>varchar(16)</td><td>Catchment character</td></tr>
    <tr><td><code>teaching_facility_flag</code></td><td>integer</td><td>0 or 1</td></tr>
    <tr><td><code>example_not_official</code></td><td>boolean</td><td>Defaults true</td></tr>
  </tbody>
</table></div>

<h2>Payment</h2>

<h3>insurance_scheme</h3>

<p>The payer organisations, named rather than numbered. Organisation names are public, so
these rows are not flagged illustrative; what is <em>not</em> included is any benefit
schedule or tariff.</p>

<div class="tw"><table class="tight">
  <thead><tr><th>Code</th><th>Organisation</th><th>Type</th></tr></thead>
  <tbody>
    <tr><td><code>UHIA</code></td><td>Universal Health Insurance Authority</td><td>social</td></tr>
    <tr><td><code>HIO</code></td><td>Health Insurance Organization</td><td>social</td></tr>
    <tr><td><code>AFMS</code></td><td>Armed Forces Medical Services</td><td>military</td></tr>
    <tr><td><code>POLICE</code></td><td>Police medical services</td><td>military</td></tr>
    <tr><td><code>PRIVATE</code></td><td>Private insurance</td><td>private</td></tr>
    <tr><td><code>OOP</code></td><td>Out of pocket</td><td>out_of_pocket</td></tr>
  </tbody>
</table></div>

<p>Columns are <code>insurance_scheme_id</code>, <code>scheme_code</code> (unique),
<code>scheme_name_en</code>, <code>scheme_name_ar</code>, <code>scheme_type</code>, and
<code>example_not_official</code>.</p>

<h3>person_insurance</h3>

<p>Coverage intervals. Two schemes overlapping in time is a legitimate state, not an error —
supplementary private cover alongside a public scheme is common.</p>

<div class="tw"><table>
  <thead><tr><th>Column</th><th>Type</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td><code>person_insurance_id</code></td><td>integer</td><td>Primary key</td></tr>
    <tr><td><code>person_id</code></td><td>integer</td><td>References <code>person</code></td></tr>
    <tr><td><code>insurance_scheme_id</code></td><td>integer</td><td>References <code>insurance_scheme</code></td></tr>
    <tr><td><code>coverage_start_date</code></td><td>date</td><td>Required</td></tr>
    <tr><td><code>coverage_end_date</code></td><td>date</td><td>Null while active</td></tr>
    <tr><td><code>subscriber_source_value</code></td><td>varchar(128)</td><td>Membership reference as recorded</td></tr>
    <tr><td><code>example_not_official</code></td><td>boolean</td><td>Defaults true</td></tr>
  </tbody>
</table></div>

<h2>Care delivery</h2>

<h3>care_sector</h3>

<p>Four values — <code>CIVIL</code>, <code>MILITARY</code>, <code>POLICE</code>,
<code>UNIVERSITY</code> — with both name forms. Kept as a table rather than a text column so
that a visit can reference it by key.</p>

<h3>referral</h3>

<p>A referral is recorded as an event in its own right, which makes an incomplete referral
visible: a row with no subsequent visit at the destination is a patient who did not arrive.</p>

<div class="tw"><table>
  <thead><tr><th>Column</th><th>Type</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td><code>referral_id</code></td><td>integer</td><td>Primary key</td></tr>
    <tr><td><code>person_id</code></td><td>integer</td><td>References <code>person</code></td></tr>
    <tr><td><code>from_care_site_id</code></td><td>integer</td><td>Referring facility</td></tr>
    <tr><td><code>to_care_site_id</code></td><td>integer</td><td>Destination facility</td></tr>
    <tr><td><code>referring_visit_occurrence_id</code></td><td>integer</td><td>Visit the referral was issued at</td></tr>
    <tr><td><code>referral_date</code></td><td>date</td><td>Required</td></tr>
    <tr><td><code>referral_priority</code></td><td>varchar(32)</td><td><code>routine</code>, <code>urgent</code>, <code>emergency</code></td></tr>
    <tr><td><code>referral_reason_source_value</code></td><td>varchar(255)</td><td>Reason as recorded</td></tr>
    <tr><td><code>referral_reason_concept_id</code></td><td>integer</td><td>Optional mapped reason</td></tr>
    <tr><td><code>example_not_official</code></td><td>boolean</td><td>Defaults true</td></tr>
  </tbody>
</table></div>

<h3>visit_care_context</h3>

<p>One optional row per visit, attaching sector, payer, and referral to the encounter. This is
what makes questions like <em>which sector treated publicly insured patients referred
urgently</em> a join rather than an inference.</p>

<div class="tw"><table>
  <thead><tr><th>Column</th><th>Type</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td><code>visit_occurrence_id</code></td><td>integer</td><td>Primary key and foreign key to <code>visit_occurrence</code></td></tr>
    <tr><td><code>care_sector_id</code></td><td>integer</td><td>References <code>care_sector</code></td></tr>
    <tr><td><code>insurance_scheme_id</code></td><td>integer</td><td>Scheme that covered this visit</td></tr>
    <tr><td><code>referral_id</code></td><td>integer</td><td>Referral that produced this visit</td></tr>
    <tr><td><code>emergency_flag</code></td><td>integer</td><td>0 or 1</td></tr>
    <tr><td><code>example_not_official</code></td><td>boolean</td><td>Defaults true</td></tr>
  </tbody>
</table></div>

<h2>Terminology</h2>

<p>Three tables hold national code systems and their mapping into standard concepts. They are
the working area used before — or instead of — loading a licensed vocabulary release.</p>

<h3>source_vocabulary</h3>

<p><code>source_vocabulary_id</code>, <code>vocabulary_code</code> (unique),
<code>vocabulary_name_en</code>, <code>vocabulary_name_ar</code>, and
<code>official_status</code>, which defaults to <code>example_not_official</code> and records
whether a system is a real published release, an illustrative one, or a real code set carrying
illustrative labels.</p>

<h3>source_code</h3>

<div class="tw"><table>
  <thead><tr><th>Column</th><th>Type</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td><code>source_code_id</code></td><td>integer</td><td>Primary key</td></tr>
    <tr><td><code>source_vocabulary_id</code></td><td>integer</td><td>References <code>source_vocabulary</code></td></tr>
    <tr><td><code>source_code</code></td><td>varchar(64)</td><td>The code as published</td></tr>
    <tr><td><code>code_name_en</code>, <code>code_name_ar</code></td><td>varchar(512)</td><td>Both labels required</td></tr>
    <tr><td><code>domain_id</code></td><td>varchar(32)</td><td>Clinical domain the code belongs to</td></tr>
    <tr><td><code>valid_start_date</code>, <code>valid_end_date</code></td><td>date</td><td>Validity window</td></tr>
    <tr><td><code>example_not_official</code></td><td>boolean</td><td>Per-code status</td></tr>
  </tbody>
</table></div>

<h3>source_code_omop_map</h3>

<p>Composite primary key over <code>source_code_id</code>, <code>concept_id</code>, and
<code>relationship_id</code>, so one source code can carry more than one relationship.
<code>relationship_id</code> defaults to <code>Maps to</code>, matching the standard
convention.</p>

<h2>Metadata</h2>

<h3>emop_cdm_source</h3>

<p><code>emop_cdm_source_name</code>, <code>emop_cdm_version</code>,
<code>omop_cdm_version</code>, <code>emop_release_date</code>, and a free-text
<code>comment</code>. Populated once per deployment so a database can report which version of
the model produced it.</p>

<h2>Indexes</h2>

<p>Six indexes cover the joins these tables are built for: person lookups on
<code>national_identifier</code> and <code>person_insurance</code>, governorate lookup on
<code>facility_extension</code>, person lookup on <code>referral</code>, a composite on
<code>source_code</code> over vocabulary and code, and concept lookup on
<code>source_code_omop_map</code>.</p>
""",
}

EMOP_PAGES["tables"] = {
    "nav": "Core tables",
    "title": "Core tables — EMOP",
    "description": "The 39 international core tables carried unchanged in EMOP, grouped by role.",
    "h1": "Core tables",
    "standfirst": (
        "Thirty-nine tables carried without modification from the international model, "
        "grouped by the role each group plays. Names, columns, and grain are unchanged."
    ),
    "body": """
<p>These are vendored from the published PostgreSQL definitions, version 5.4, under the Apache
License 2.0. The only edit is mechanical: the schema placeholder is replaced with
<code>emop</code> so the files run without a templating step. Provenance is recorded in
<code>ddl/omop_cdm_5.4/SOURCE.txt</code>.</p>

<div class="note">
  <span class="label">Column definitions</span>
  <p>Authoritative column-level documentation for these tables is maintained upstream by the
  OHDSI community. This page states which tables EMOP carries and what each is for; it does
  not restate the upstream specification.</p>
</div>

<h2>Clinical events</h2>

<p>The record of what happened to a patient.</p>

<div class="tw"><table class="tight">
  <thead><tr><th>Table</th><th>Holds</th></tr></thead>
  <tbody>
    <tr><td><code>person</code></td><td>One row per patient: birth date parts, gender, race, ethnicity, home location</td></tr>
    <tr><td><code>observation_period</code></td><td>Spans during which the patient's data is expected to be complete</td></tr>
    <tr><td><code>visit_occurrence</code></td><td>Encounters — outpatient, inpatient, emergency</td></tr>
    <tr><td><code>visit_detail</code></td><td>Sub-encounters, such as a ward transfer within an admission</td></tr>
    <tr><td><code>condition_occurrence</code></td><td>Diagnoses and clinical findings</td></tr>
    <tr><td><code>drug_exposure</code></td><td>Prescriptions, dispensations, administrations</td></tr>
    <tr><td><code>procedure_occurrence</code></td><td>Procedures performed</td></tr>
    <tr><td><code>device_exposure</code></td><td>Devices used or implanted</td></tr>
    <tr><td><code>measurement</code></td><td>Laboratory results and vital signs, with values and units</td></tr>
    <tr><td><code>observation</code></td><td>Clinical facts that are not measurements</td></tr>
    <tr><td><code>death</code></td><td>Date and cause where recorded</td></tr>
    <tr><td><code>note</code></td><td>Clinical documents as text</td></tr>
    <tr><td><code>note_nlp</code></td><td>Structured output extracted from those notes</td></tr>
    <tr><td><code>specimen</code></td><td>Samples collected</td></tr>
    <tr><td><code>fact_relationship</code></td><td>Typed relationships between two records in any domain</td></tr>
    <tr><td><code>episode</code></td><td>Higher-level clinical episodes spanning several events</td></tr>
    <tr><td><code>episode_event</code></td><td>Links individual events to an episode</td></tr>
  </tbody>
</table></div>

<h2>Health system</h2>

<div class="tw"><table class="tight">
  <thead><tr><th>Table</th><th>Holds</th></tr></thead>
  <tbody>
    <tr><td><code>location</code></td><td>Geographic addresses</td></tr>
    <tr><td><code>care_site</code></td><td>Facilities delivering care — extended by <code>facility_extension</code></td></tr>
    <tr><td><code>provider</code></td><td>Individual clinicians and their specialties</td></tr>
  </tbody>
</table></div>

<h2>Economics</h2>

<div class="tw"><table class="tight">
  <thead><tr><th>Table</th><th>Holds</th></tr></thead>
  <tbody>
    <tr><td><code>payer_plan_period</code></td><td>Coverage intervals in the standard shape — see also <code>person_insurance</code></td></tr>
    <tr><td><code>cost</code></td><td>Amounts attached to a clinical event</td></tr>
  </tbody>
</table></div>

<h2>Derived eras</h2>

<p>Computed rather than loaded: contiguous spans inferred from the event tables.</p>

<p><code>drug_era</code>, <code>dose_era</code>, <code>condition_era</code></p>

<h2>Cohorts</h2>

<p><code>cohort</code> holds subject entry and exit dates for a defined population;
<code>cohort_definition</code> holds the definition itself. Populated by analytical tooling
rather than by an extract process.</p>

<h2>Vocabulary</h2>

<p>The terminology backbone. In a research deployment these are loaded from a standard
vocabulary release; this repository ships only a small illustrative set.</p>

<div class="tw"><table class="tight">
  <thead><tr><th>Table</th><th>Holds</th></tr></thead>
  <tbody>
    <tr><td><code>concept</code></td><td>Every concept, standard or not, with its domain and vocabulary</td></tr>
    <tr><td><code>vocabulary</code></td><td>The code systems present, and their versions</td></tr>
    <tr><td><code>domain</code></td><td>Which clinical domain a concept belongs to</td></tr>
    <tr><td><code>concept_class</code></td><td>Classification within a vocabulary</td></tr>
    <tr><td><code>concept_relationship</code></td><td>Typed relationships between concepts, including <code>Maps to</code></td></tr>
    <tr><td><code>relationship</code></td><td>The relationship types themselves</td></tr>
    <tr><td><code>concept_synonym</code></td><td>Alternative names, including other languages</td></tr>
    <tr><td><code>concept_ancestor</code></td><td>Pre-computed hierarchy for descendant queries</td></tr>
    <tr><td><code>source_to_concept_map</code></td><td>Legacy source-code mapping table</td></tr>
    <tr><td><code>drug_strength</code></td><td>Ingredient strengths for drug concepts</td></tr>
  </tbody>
</table></div>

<h2>Metadata</h2>

<p><code>cdm_source</code> describes the deployed instance and the model version;
<code>metadata</code> holds arbitrary key-value annotations. EMOP adds
<code>emop_cdm_source</code> alongside these rather than modifying either.</p>

<h2>Counting</h2>

<p>Thirty-nine core tables plus thirteen Egyptian tables give fifty-two, which is what a
verified installation reports:</p>

<pre><code>select count(*) from information_schema.tables where table_schema = 'emop';
<span class="c">-- 52</span></code></pre>
""",
}

EMOP_PAGES["vocabularies"] = {
    "nav": "Reference data",
    "title": "Reference data — EMOP",
    "description": (
        "What reference data ships with EMOP, and precisely which rows are published codes "
        "versus illustrative examples."
    ),
    "h1": "Reference data",
    "standfirst": (
        "Some rows shipped with EMOP are real published reference data; others are invented so "
        "the model can be read and installed. This page states which is which, row by row."
    ),
    "body": """
<div class="caution">
  <span class="label">Read before citing</span>
  <p>No clinical or tariff code in this repository comes from the Ministry of Health, the
  Universal Health Insurance Authority, or the Health Insurance Organization. Invented codes
  carry an <code>EX-</code> prefix and <code>example_not_official = true</code>. Do not quote
  any code from this repository as an official Egyptian code.</p>
</div>

<h2>What ships, and its status</h2>

<div class="tw"><table>
  <thead><tr><th>File</th><th>Rows</th><th>Status</th></tr></thead>
  <tbody>
    <tr>
      <td><code>governorate.csv</code></td><td>27</td>
      <td><strong>Published.</strong> International subdivision codes — geographic, not clinical</td>
    </tr>
    <tr>
      <td><code>insurance_scheme.csv</code></td><td>6</td>
      <td><strong>Published.</strong> Organisation names only; no benefit schedule or tariff</td>
    </tr>
    <tr>
      <td><code>care_sector.csv</code></td><td>4</td>
      <td><strong>Published.</strong> Civil, military, police, university</td>
    </tr>
    <tr>
      <td><code>icd10_eg.example.csv</code></td><td>2</td>
      <td><strong>Published codes, illustrative labels.</strong> Real international diagnosis
      codes and titles; the Arabic labels are translations, not an official Egyptian release</td>
    </tr>
    <tr>
      <td><code>moh_procedure.example.csv</code></td><td>2</td>
      <td><strong>Invented.</strong> <code>EX-MOH-PROC-*</code></td>
    </tr>
    <tr>
      <td><code>egyptian_drug.example.csv</code></td><td>2</td>
      <td><strong>Invented.</strong> <code>EX-EDRUG-*</code></td>
    </tr>
    <tr>
      <td><code>uhia_service.example.csv</code></td><td>1</td>
      <td><strong>Invented.</strong> <code>EX-UHIA-*</code></td>
    </tr>
  </tbody>
</table></div>

<h2>Why the distinction is in the data</h2>

<p>A reader should not have to consult documentation to learn whether a code is real. Both the
per-code <code>example_not_official</code> flag and the per-system
<code>official_status</code> value are queryable:</p>

<pre><code>select sv.vocabulary_code, sv.official_status,
       sc.source_code, sc.example_not_official
  from emop.source_code sc
  join emop.source_vocabulary sv using (source_vocabulary_id)
 order by sc.source_code_id;</code></pre>

<div class="tw"><table class="tight">
  <thead><tr><th>vocabulary_code</th><th>official_status</th><th>source_code</th><th>example_not_official</th></tr></thead>
  <tbody>
    <tr><td>MOH_PROCEDURE</td><td>example_not_official</td><td>EX-MOH-PROC-001</td><td>t</td></tr>
    <tr><td>MOH_PROCEDURE</td><td>example_not_official</td><td>EX-MOH-PROC-002</td><td>t</td></tr>
    <tr><td>EG_DRUG</td><td>example_not_official</td><td>EX-EDRUG-001</td><td>t</td></tr>
    <tr><td>EG_DRUG</td><td>example_not_official</td><td>EX-EDRUG-002</td><td>t</td></tr>
    <tr><td>ICD10_EG</td><td>official_code_illustrative_label</td><td>E11.9</td><td>f</td></tr>
    <tr><td>ICD10_EG</td><td>official_code_illustrative_label</td><td>I10</td><td>f</td></tr>
    <tr><td>UHIA_SERVICE</td><td>example_not_official</td><td>EX-UHIA-OPD-001</td><td>t</td></tr>
  </tbody>
</table></div>

<h2>Governorates</h2>

<p>All twenty-seven, grouped into six regions for aggregate reporting: Greater Cairo, Delta,
Canal, Sinai, Upper Egypt, and Frontier. Each row carries both name forms and its
international subdivision code — Cairo is <code>EG-C</code>, Alexandria <code>EG-ALX</code>,
Luxor <code>EG-LX</code>.</p>

<p>These are geographic identifiers. They say nothing clinical, which is why they are the one
part of the reference data that can be used as-is.</p>

<h2>Illustrative concepts</h2>

<p><code>vocabulary/load_examples.sql</code> also populates the vocabulary tables so that a
fresh database is referentially complete: concept <code>0</code>, one metadata concept,
language concepts, the gender, race, ethnicity, visit and type concepts the toy data
references, and the <code>domain</code> and <code>concept_class</code> rows those concepts
depend on.</p>

<p>Without those reference rows the published foreign-key constraints cannot be applied. With
them, all 194 apply cleanly — which is what makes the example set worth shipping.</p>

<div class="caution">
  <span class="label">Do not mix</span>
  <p>If you are loading a real standard vocabulary release, skip
  <code>load_examples.sql</code> entirely. Its concepts occupy the reserved local range and
  will not collide, but having illustrative rows beside a production vocabulary is confusing
  for no benefit. See <a href="/emop/install/">Installation</a>.</p>
</div>
""",
}

EMOP_PAGES["install"] = {
    "nav": "Installation",
    "title": "Installation — EMOP",
    "description": (
        "Install the EMOP schema on PostgreSQL, load the example data, apply foreign keys and "
        "indexes, and verify the result."
    ),
    "h1": "Installation",
    "standfirst": (
        "Four commands take an empty database to a populated, referentially complete schema. "
        "Every figure on this page was measured on a clean PostgreSQL 17 database."
    ),
    "body": """
<h2>Requirements</h2>

<ul>
  <li>PostgreSQL 14 or newer, with <code>psql</code> and <code>createdb</code> on the path</li>
  <li>A database role permitted to create schemas</li>
  <li>No extensions and no other dependencies</li>
</ul>

<h2>Install</h2>

<pre><code>git clone https://github.com/gegesay89/emop.git
cd emop
createdb emop
./ddl/install.sh postgres://localhost/emop</code></pre>

<p>The script applies four files in a fixed order, stopping on the first error:</p>

<div class="tw"><table class="tight">
  <thead><tr><th>#</th><th>File</th><th>Effect</th></tr></thead>
  <tbody>
    <tr><td>1</td><td><code>ddl/00_create_schema.sql</code></td><td>Creates schema <code>emop</code></td></tr>
    <tr><td>2</td><td><code>ddl/omop_cdm_5.4/…_ddl.sql</code></td><td>39 core tables</td></tr>
    <tr><td>3</td><td><code>ddl/omop_cdm_5.4/…_primary_keys.sql</code></td><td>Core primary keys</td></tr>
    <tr><td>4</td><td><code>ddl/emop_extension.sql</code></td><td>13 Egyptian tables, their keys and indexes</td></tr>
  </tbody>
</table></div>

<h2>Load the example data</h2>

<p>Optional, and only for an empty database you intend to explore.</p>

<pre><code>psql postgres://localhost/emop -v ON_ERROR_STOP=1 \\
  -f vocabulary/load_examples.sql
psql postgres://localhost/emop -v ON_ERROR_STOP=1 \\
  -f examples/toy_egypt.sql</code></pre>

<p>The first file loads reference data and the illustrative concepts. The second loads one
fictional patient: a primary care visit, an urgent referral, a hospital visit, a diagnosis,
and a prescription — enough to exercise every extension table join.</p>

<div class="note">
  <span class="label">Always pass ON_ERROR_STOP</span>
  <p>Without <code>-v ON_ERROR_STOP=1</code>, <code>psql</code> reports an error and continues,
  leaving a partly loaded database that looks installed. The install script sets it for you;
  set it yourself for these two files.</p>
</div>

<h2>Apply foreign keys and indexes</h2>

<p>The published constraint file requires the vocabulary reference rows to exist. If you loaded
the example set, they do:</p>

<pre><code>psql postgres://localhost/emop -v ON_ERROR_STOP=1 \\
  -f ddl/omop_cdm_5.4/OMOPCDM_postgresql_5.4_constraints.sql
psql postgres://localhost/emop -v ON_ERROR_STOP=1 \\
  -f ddl/omop_cdm_5.4/OMOPCDM_postgresql_5.4_indices.sql</code></pre>

<h2>Verify</h2>

<pre><code>select count(*) from information_schema.tables
 where table_schema = 'emop';
<span class="c">-- 52</span>

select count(*) from information_schema.table_constraints
 where constraint_schema = 'emop' and constraint_type = 'FOREIGN KEY';
<span class="c">-- 194</span>

select count(*) from emop.governorate;
<span class="c">-- 27</span>

select count(*) from emop.visit_occurrence;
<span class="c">-- 2</span></code></pre>

<p>A join across the extension tables confirms the Egyptian layer is wired correctly:</p>

<pre><code>select p.person_id,
       g.governorate_name_en as governorate,
       s.scheme_code         as payer,
       cs.sector_name_en     as sector,
       c.concept_name        as condition
  from emop.person p
  join emop.person_insurance   pi  on pi.person_id = p.person_id
  join emop.insurance_scheme   s   on s.insurance_scheme_id = pi.insurance_scheme_id
  join emop.visit_occurrence   v   on v.person_id = p.person_id
  join emop.visit_care_context vcc on vcc.visit_occurrence_id = v.visit_occurrence_id
  join emop.care_sector        cs  on cs.care_sector_id = vcc.care_sector_id
  join emop.facility_extension fe  on fe.care_site_id = v.care_site_id
  join emop.governorate        g   on g.governorate_id = fe.governorate_id
  left join emop.condition_occurrence co on co.visit_occurrence_id = v.visit_occurrence_id
  left join emop.concept c on c.concept_id = co.condition_concept_id
 order by v.visit_occurrence_id;</code></pre>

<p>Two rows: a primary care visit in the civil sector, then the university hospital visit it
was referred to, carrying the diagnosis.</p>

<h2>Loading a real vocabulary instead</h2>

<p>For a research deployment, skip the example loader:</p>

<ol>
  <li>Run <code>./ddl/install.sh</code></li>
  <li>Load your standard vocabulary release into the vocabulary tables</li>
  <li>Apply the constraint and index files</li>
  <li>Load clinical data, then populate the extension tables</li>
</ol>

<p>Illustrative concepts occupy the reserved local range and so cannot collide with a standard
release, but mixing them adds confusion without adding value.</p>

<h2>Uninstall</h2>

<pre><code>psql postgres://localhost/emop -c 'drop schema emop cascade;'</code></pre>
""",
}

EMOP_PAGES["crosswalk"] = {
    "nav": "International research",
    "title": "International research — EMOP",
    "description": (
        "How to reduce an EMOP database to a standard research instance: a rule for each of "
        "the thirteen Egyptian tables."
    ),
    "h1": "Taking EMOP to international research",
    "standfirst": (
        "The core is already standard. This page gives a rule for each Egyptian table, so a "
        "network extract drops or maps each one deliberately rather than by omission."
    ),
    "body": """
<p>Every core table in EMOP is the standard table of the same name, so an extract process that
already targets the international model needs no column renaming. The decisions concern the
thirteen extension tables, which have no standard equivalent.</p>

<div class="note">
  <span class="label">The short version</span>
  <p>Drop every Egyptian table, remap the illustrative concepts onto real standard concepts,
  and what remains is a valid standard instance. Everything below is about what you lose and
  how to keep the parts that matter.</p>
</div>

<h2>Rules by table</h2>

<div class="tw"><table>
  <thead><tr><th>Egyptian table</th><th>Destination</th><th>Rule</th></tr></thead>
  <tbody>
    <tr>
      <td><code>governorate</code></td><td><code>location</code></td>
      <td>Create one <code>location</code> row per governorate if geographic filtering is
      needed. Keep <code>governorate</code> as the local source of truth</td>
    </tr>
    <tr>
      <td><code>national_identifier</code></td><td>none</td>
      <td><strong>Drop.</strong> Directly identifying. Do not relocate it into
      <code>person_source_value</code></td>
    </tr>
    <tr>
      <td><code>person_name_bilingual</code></td><td>none</td>
      <td><strong>Drop.</strong> The standard <code>person</code> table has no name columns by
      design</td>
    </tr>
    <tr>
      <td><code>facility_extension</code></td><td><code>care_site</code></td>
      <td><code>moh_facility_code</code> may go to <code>care_site_source_value</code>. Sector
      and teaching flag have no destination — drop or emit as observations</td>
    </tr>
    <tr>
      <td><code>insurance_scheme</code></td><td><code>payer_plan_period</code></td>
      <td>Use <code>scheme_code</code> as the payer source value</td>
    </tr>
    <tr>
      <td><code>person_insurance</code></td><td><code>payer_plan_period</code></td>
      <td>One period row per coverage interval — a direct translation</td>
    </tr>
    <tr>
      <td><code>care_sector</code></td><td><code>observation</code>, or drop</td>
      <td>If a study needs civil versus military, emit a mapped observation. Do not invent a
      column on <code>visit_occurrence</code></td>
    </tr>
    <tr>
      <td><code>referral</code></td><td><code>fact_relationship</code>, or drop</td>
      <td>Expressible as a typed relationship between two visits, which loses priority and
      reason. Prefer keeping it local</td>
    </tr>
    <tr>
      <td><code>visit_care_context</code></td><td><code>visit_occurrence</code></td>
      <td>Emergency can inform the visit concept; payer belongs in
      <code>payer_plan_period</code></td>
    </tr>
    <tr>
      <td><code>source_vocabulary</code>, <code>source_code</code></td>
      <td><code>vocabulary</code>, <code>concept</code></td>
      <td>Load official lists into the standard vocabulary tables when you hold redistribution
      rights. The Egyptian tables are the staging area before that</td>
    </tr>
    <tr>
      <td><code>source_code_omop_map</code></td><td><code>source_to_concept_map</code></td>
      <td>Same grain: source code to standard concept</td>
    </tr>
    <tr>
      <td><code>emop_cdm_source</code></td><td><code>cdm_source</code></td>
      <td>Keep both locally; drop the EMOP row from the extract</td>
    </tr>
  </tbody>
</table></div>

<h2>Remapping the illustrative concepts</h2>

<p>A database loaded from the example set references concepts in the reserved local range for
gender, race, ethnicity, visit and type concepts. Those are placeholders. Before an extract can
be called a valid standard instance, each must be remapped onto a real standard concept from a
vocabulary release. This is the step most easily forgotten, because the database is internally
consistent without it.</p>

<h2>What is genuinely lost</h2>

<p>Stated plainly, so the decision is informed:</p>

<ul>
  <li><strong>Sector.</strong> Whether care was civil, military, police, or university has no
  standard home. As an observation it survives; as an analytic dimension it does not.</li>
  <li><strong>Referral detail.</strong> Priority and reason do not survive translation into a
  relationship between two visits.</li>
  <li><strong>Identity and names.</strong> Deliberately dropped.</li>
  <li><strong>Facility character.</strong> Teaching status and urban or rural catchment have no
  standard column.</li>
</ul>

<p>This is the cost of the design choice described in
<a href="/emop/data-model/">design principles</a>: the extension tables carry facts the
international model does not model, so translation is lossy in exactly those places, and
visibly so.</p>
""",
}

EMOP_PAGES["interoperability"] = {
    "nav": "Interoperability",
    "title": "Interoperability mapping — EMOP",
    "description": (
        "How EMOP tables correspond to interoperability resources for exchanging records "
        "between systems."
    ),
    "h1": "Interoperability mapping",
    "standfirst": (
        "A resource-by-resource correspondence for exchanging EMOP records between systems. "
        "This is a mapping note, not a published implementation guide."
    ),
    "body": """
<p>EMOP is a model for storing and analysing records. Exchange standards address a different
problem: moving one patient's data between systems. The two are complementary, and the mapping
below is the practical bridge. Resource names follow the widely used release 4.</p>

<div class="note">
  <span class="label">Scope</span>
  <p>This is a table-level correspondence, deliberately stopping short of publishing executable
  structure maps or profiles. Version 0.1 does not claim to be an implementation guide, because
  a guide implies conformance rules and a test suite that do not yet exist.</p>
</div>

<h2>Resource correspondence</h2>

<div class="tw"><table>
  <thead><tr><th>Resource</th><th>EMOP source</th><th>Notes</th></tr></thead>
  <tbody>
    <tr><td><code>Patient</code></td><td><code>person</code> + <code>person_name_bilingual</code></td>
        <td>Demographics from the core; names from the extension</td></tr>
    <tr><td><code>Patient.identifier</code></td><td><code>national_identifier</code></td>
        <td>One entry per row. Identifier type maps to the identifier system</td></tr>
    <tr><td><code>Patient.address</code></td><td><code>location</code>, <code>governorate</code></td>
        <td>Governorate is the meaningful administrative level</td></tr>
    <tr><td><code>Encounter</code></td><td><code>visit_occurrence</code> + <code>visit_care_context</code></td>
        <td>Class from the visit concept; sector and payer from the context row</td></tr>
    <tr><td><code>Encounter</code> referral fields</td><td><code>referral</code></td>
        <td>Priority maps to the encounter priority</td></tr>
    <tr><td><code>Condition</code></td><td><code>condition_occurrence</code></td><td>Direct</td></tr>
    <tr><td><code>MedicationRequest</code>, <code>MedicationStatement</code></td>
        <td><code>drug_exposure</code></td>
        <td>Which resource applies depends on whether the row records an order or an
        administration</td></tr>
    <tr><td><code>Procedure</code></td><td><code>procedure_occurrence</code></td><td>Direct</td></tr>
    <tr><td><code>Observation</code></td><td><code>measurement</code>, <code>observation</code></td>
        <td>Measurements carry value and unit; observations may not</td></tr>
    <tr><td><code>Organization</code></td><td><code>care_site</code> + <code>facility_extension</code></td>
        <td>Ministry facility code becomes an organisation identifier</td></tr>
    <tr><td><code>Practitioner</code></td><td><code>provider</code></td><td>Direct</td></tr>
    <tr><td><code>Coverage</code></td><td><code>person_insurance</code> + <code>insurance_scheme</code></td>
        <td>Period from the coverage row; payer from the scheme</td></tr>
    <tr><td><code>Coverage.payor</code></td><td><code>insurance_scheme.scheme_code</code></td>
        <td><code>UHIA</code>, <code>HIO</code>, <code>AFMS</code>, and so on</td></tr>
    <tr><td>Coded values</td><td><code>source_code</code> → <code>source_code_omop_map</code> → <code>concept</code></td>
        <td>Emit both the national code and the standard concept it maps to</td></tr>
  </tbody>
</table></div>

<h2>Two traps worth stating</h2>

<h3>Identity is not the primary key</h3>

<p>A national identity number belongs in the identifier list, never in the resource id. The
resource id is a system key, meaningless outside the server that issued it; the national
identifier is a real-world identifier that must survive being moved between systems. Conflating
them makes the record impossible to re-link correctly and leaks an identifier into every URL
that references the patient.</p>

<h3>Language is a property of the name, not the record</h3>

<p><code>person_name_bilingual.preferred_language</code> states which form to display, but a
name resource can carry both. When the Arabic form is the legal name, mark it as the official
use rather than dropping the Latin form — both are needed, for different purposes.</p>

<h2>Coded values in both directions</h2>

<p>When exporting a diagnosis, emit two codings on the same element: the national source code
from <code>source_code</code>, and the standard concept reached through
<code>source_code_omop_map</code>. The receiving system can then use whichever it understands
without a lossy guess, and the mapping stays auditable.</p>
""",
}
