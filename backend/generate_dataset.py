import random
import pandas as pd
from pathlib import Path


# =========================================================
# CONFIGURATION
# =========================================================

random.seed(42)

BASE_DIR = Path(__file__).resolve().parents[1]

OUTPUT_PATH = BASE_DIR / "data" / "train.csv"


# =========================================================
# DATA BUILDING BLOCKS
# =========================================================

DATA = {

    "healthcare": {

        "interventions": [
            "mobile healthcare clinics",
            "medical camps",
            "telemedicine services",
            "primary healthcare centres",
            "preventive healthcare programs",
            "maternal healthcare services",
            "child healthcare services",
            "diagnostic facilities",
            "health screening programs",
            "community health centres",
        ],

        "beneficiaries": [
            "rural families",
            "low income households",
            "underserved communities",
            "remote villages",
            "children and families",
            "elderly residents",
            "women and children",
            "marginalized communities",
        ],

        "locations": [
            "remote villages",
            "rural districts",
            "underserved regions",
            "aspirational districts",
            "low access communities",
            "remote tribal areas",
        ],

        "outcomes": [
            "improve access to healthcare",
            "reduce barriers to medical treatment",
            "increase preventive healthcare coverage",
            "improve health outcomes",
            "provide timely medical assistance",
            "expand healthcare access",
        ],
    },


    "education": {

        "interventions": [
            "digital classrooms",
            "scholarship programs",
            "teacher training",
            "school infrastructure improvement",
            "learning resource centres",
            "remedial education programs",
            "computer education programs",
            "after school learning programs",
            "education technology programs",
            "library development programs",
        ],

        "beneficiaries": [
            "government school students",
            "children from disadvantaged communities",
            "rural students",
            "low income students",
            "school children",
            "students in underserved areas",
            "young learners",
        ],

        "locations": [
            "rural schools",
            "government schools",
            "remote districts",
            "underserved communities",
            "aspirational districts",
            "low income neighbourhoods",
        ],

        "outcomes": [
            "improve access to quality education",
            "increase learning opportunities",
            "improve student outcomes",
            "reduce educational inequality",
            "increase digital literacy",
            "support school participation",
        ],
    },


    "livelihood": {

        "interventions": [
            "vocational training",
            "skill development programs",
            "employment training",
            "entrepreneurship training",
            "job readiness programs",
            "self help group training",
            "technical skills training",
            "livelihood development programs",
            "small business training",
            "workforce development programs",
        ],

        "beneficiaries": [
            "unemployed youth",
            "rural workers",
            "low income households",
            "young adults",
            "women entrepreneurs",
            "job seekers",
            "economically disadvantaged communities",
        ],

        "locations": [
            "rural districts",
            "underserved communities",
            "small towns",
            "aspirational districts",
            "low income areas",
            "remote villages",
        ],

        "outcomes": [
            "increase employment opportunities",
            "improve income generation",
            "develop job ready skills",
            "support sustainable livelihoods",
            "increase economic independence",
            "improve employability",
        ],
    },


    "women_empowerment": {

        "interventions": [
            "women entrepreneurship programs",
            "women leadership training",
            "financial literacy programs for women",
            "self help group development",
            "women skill development programs",
            "women employment initiatives",
            "female entrepreneurship support",
            "gender equality programs",
            "women business development programs",
        ],

        "beneficiaries": [
            "rural women",
            "women from low income households",
            "women entrepreneurs",
            "young women",
            "women in underserved communities",
            "female workers",
        ],

        "locations": [
            "rural communities",
            "underserved districts",
            "remote villages",
            "aspirational districts",
            "low income communities",
        ],

        "outcomes": [
            "increase women's economic independence",
            "improve employment opportunities for women",
            "support women entrepreneurs",
            "increase financial independence",
            "improve women's participation in the workforce",
            "promote gender equality",
        ],
    },


    "environment": {

        "interventions": [
            "tree plantation programs",
            "waste management systems",
            "recycling facilities",
            "renewable energy projects",
            "watershed conservation",
            "forest restoration",
            "environmental awareness programs",
            "solar energy installations",
            "biodiversity conservation",
            "land restoration programs",
        ],

        "beneficiaries": [
            "rural communities",
            "local residents",
            "vulnerable communities",
            "farmers",
            "future generations",
            "communities near degraded ecosystems",
        ],

        "locations": [
            "rural districts",
            "degraded land areas",
            "villages",
            "environmentally vulnerable regions",
            "water stressed areas",
        ],

        "outcomes": [
            "reduce environmental pollution",
            "restore degraded ecosystems",
            "improve environmental sustainability",
            "increase renewable energy access",
            "improve local biodiversity",
            "reduce waste generation",
        ],
    },


    "water_sanitation": {

        "interventions": [
            "clean drinking water systems",
            "community water facilities",
            "rural sanitation programs",
            "toilet construction",
            "water purification systems",
            "rainwater harvesting",
            "wastewater management",
            "sanitation infrastructure",
            "water treatment facilities",
        ],

        "beneficiaries": [
            "rural households",
            "underserved villages",
            "low income families",
            "school children",
            "remote communities",
            "water stressed communities",
        ],

        "locations": [
            "rural villages",
            "water stressed districts",
            "remote communities",
            "underserved regions",
            "aspirational districts",
        ],

        "outcomes": [
            "increase access to safe drinking water",
            "improve sanitation",
            "reduce waterborne disease risks",
            "improve hygiene",
            "increase reliable water access",
            "improve community health",
        ],
    },


    "rural_development": {

        "interventions": [
            "village infrastructure development",
            "rural road improvement",
            "community infrastructure projects",
            "rural livelihood infrastructure",
            "village development programs",
            "community centre construction",
            "rural connectivity projects",
            "integrated rural development",
        ],

        "beneficiaries": [
            "rural communities",
            "village households",
            "farmers",
            "remote communities",
            "low income rural families",
        ],

        "locations": [
            "rural villages",
            "aspirational districts",
            "remote districts",
            "underserved rural regions",
            "backward rural areas",
        ],

        "outcomes": [
            "improve rural infrastructure",
            "increase access to basic services",
            "improve rural connectivity",
            "support community development",
            "improve quality of life",
        ],
    },


    "sports": {

        "interventions": [
            "sports training programs",
            "community sports centres",
            "sports infrastructure development",
            "athlete development programs",
            "youth sports programs",
            "sports coaching",
            "sports equipment programs",
            "grassroots sports development",
        ],

        "beneficiaries": [
            "rural youth",
            "children from disadvantaged communities",
            "young athletes",
            "school students",
            "underprivileged youth",
        ],

        "locations": [
            "rural communities",
            "government schools",
            "underserved districts",
            "small towns",
            "remote villages",
        ],

        "outcomes": [
            "increase youth participation in sports",
            "develop sporting talent",
            "improve access to sports facilities",
            "promote physical activity",
            "support young athletes",
        ],
    },


    "disaster_management": {

        "interventions": [
            "disaster relief programs",
            "flood rehabilitation",
            "emergency response programs",
            "disaster preparedness training",
            "community resilience programs",
            "emergency shelter development",
            "post disaster rehabilitation",
            "disaster recovery programs",
        ],

        "beneficiaries": [
            "disaster affected families",
            "flood affected communities",
            "vulnerable households",
            "disaster prone communities",
            "affected rural populations",
        ],

        "locations": [
            "flood affected districts",
            "disaster prone regions",
            "rural districts",
            "coastal communities",
            "vulnerable villages",
        ],

        "outcomes": [
            "improve disaster preparedness",
            "support disaster recovery",
            "restore community infrastructure",
            "increase community resilience",
            "provide emergency assistance",
        ],
    },


    "social_inequality": {

        "interventions": [
            "social inclusion programs",
            "support programs for disadvantaged groups",
            "disability inclusion initiatives",
            "assistive support programs",
            "equal opportunity programs",
            "community inclusion programs",
            "support for marginalized communities",
            "accessibility programs",
        ],

        "beneficiaries": [
            "persons with disabilities",
            "marginalized communities",
            "socially disadvantaged groups",
            "low income households",
            "vulnerable populations",
            "underserved communities",
        ],

        "locations": [
            "urban communities",
            "rural districts",
            "underserved regions",
            "low income communities",
            "remote villages",
        ],

        "outcomes": [
            "reduce social inequalities",
            "increase social inclusion",
            "improve accessibility",
            "increase equal opportunities",
            "support disadvantaged populations",
        ],
    },
}


# =========================================================
# SENTENCE TEMPLATES
# =========================================================

TEMPLATES = [

    "The project will provide {intervention} for {beneficiaries} in {location}.",

    "The initiative will establish {intervention} to support {beneficiaries} in {location}.",

    "The program focuses on {intervention} for {beneficiaries} living in {location}.",

    "The project aims to {outcome} through {intervention}.",

    "A new {intervention} program will be implemented for {beneficiaries}.",

    "The initiative will use {intervention} to {outcome} in {location}.",

    "{beneficiaries} in {location} will receive support through {intervention}.",

    "The CSR project will implement {intervention} to help {beneficiaries}.",

    "The program will expand {intervention} across {location} to {outcome}.",

    "The proposed project addresses community needs by providing {intervention}.",

    "The intervention will focus on {beneficiaries} and aim to {outcome}.",

    "The organization plans to develop {intervention} for communities in {location}.",

]


# =========================================================
# GENERATE DATASET
# =========================================================

rows = []

EXAMPLES_PER_CATEGORY = 100


for category, values in DATA.items():

    generated = set()

    while len(generated) < EXAMPLES_PER_CATEGORY:

        template = random.choice(TEMPLATES)

        sentence = template.format(
            intervention=random.choice(values["interventions"]),
            beneficiaries=random.choice(values["beneficiaries"]),
            location=random.choice(values["locations"]),
            outcome=random.choice(values["outcomes"]),
        )

        sentence = sentence.strip()

        generated.add(sentence)

    for sentence in generated:

        rows.append(
            {
                "text": sentence,
                "label": category,
            }
        )


# =========================================================
# SHUFFLE
# =========================================================

random.shuffle(rows)

df = pd.DataFrame(rows)


# =========================================================
# SAVE
# =========================================================

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_PATH,
    index=False
)


# =========================================================
# REPORT
# =========================================================

print()
print("=" * 60)
print("IMPACT SPHERE DATASET GENERATED")
print("=" * 60)

print()
print(f"Total examples: {len(df)}")
print(f"Categories: {df['label'].nunique()}")

print()
print("Examples per category:")

print(
    df["label"].value_counts()
)

print()
print(f"Saved to:")
print(OUTPUT_PATH)